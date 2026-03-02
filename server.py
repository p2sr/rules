# simple dev server: serves out/, runs generate.py on file changes, and notifies clients to reload
import http.server
import socketserver
import threading
import time
import os
import sys
import subprocess
import urllib.parse

PORT = 80
OUT_DIR = os.path.join(os.getcwd(), 'out')


class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


clients = []
clients_lock = threading.Lock()

def inject(html):
    # inject live-reload script into html
    inject = "<script>" \
    "let __liveserver = new EventSource('/__reload');" \
    "__liveserver.onmessage=function(){location.reload();};" \
    "window.addEventListener('beforeunload', function() { __liveserver.close(); });" \
    "</script>"
    if '</body>' in html.lower():
        idx = html.lower().rfind('</body>')
        return html[:idx] + inject + html[idx:]
    else:
        return html + inject


class DevHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Serve files from the out/ directory
        path = path.split('?', 1)[0].split('#', 1)[0]
        path = urllib.parse.unquote(path)
        requested = path.lstrip('/')
        full_path = os.path.join(OUT_DIR, requested)
        return full_path

    def do_GET(self):
        if self.path.startswith('/__reload'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.end_headers()
            # register client
            with clients_lock:
                clients.append(self)
                print('Client connected, total clients:', len(clients))
            try:
                # keep connection open
                while True:
                    time.sleep(1)
            except Exception:
                print('Client connection error')
                pass
            finally:
                with clients_lock:
                    if self in clients:
                        clients.remove(self)
                        print('Client disconnected, total clients:', len(clients))
            return
        # serve from out/, but inject reload script into html responses
        # resolve filesystem path for requested resource
        req_path = self.path.split('?', 1)[0].split('#', 1)[0]
        fs_path = self.translate_path(req_path)

        # if path is a directory, try index.html
        if fs_path.endswith(os.path.sep) or os.path.isdir(fs_path):
            # If the request URL omitted the trailing slash (e.g. GET /bpe2text),
            # browsers resolve relative URLs incorrectly (they request /bpe2text.js).
            # GitHub Pages redirects to the slash. Mirror that behavior here.
            if os.path.isdir(fs_path):
                if not req_path.endswith('/'):
                    # preserve query string if present
                    qs = ''
                    if '?' in self.path:
                        qs = self.path.split('?', 1)[1]
                        qs = '?' + qs
                    self.send_response(301)
                    self.send_header('Location', req_path + '/' + qs)
                    self.end_headers()
                    return
            index_path = os.path.join(fs_path, 'index.html') if os.path.isdir(fs_path) else fs_path
            if os.path.exists(index_path):
                fs_path = index_path

        # if requested path has no extension, try adding .html
        if not os.path.exists(fs_path):
            base, ext = os.path.splitext(fs_path)
            if ext == '':
                html_candidate = fs_path + '.html'
                if os.path.exists(html_candidate) and os.path.isfile(html_candidate):
                    fs_path = html_candidate

        if os.path.exists(fs_path) and os.path.isfile(fs_path):
            # serve the file
            try:
                ctype = self.guess_type(fs_path)
                if ctype == 'text/html':
                    with open(fs_path, 'rb') as f:
                        data = f.read()
                    try:
                        text = data.decode('utf-8', errors='ignore')
                        text = inject(text)
                        encoded = text.encode('utf-8')
                        self.send_response(200)
                        self.send_header('Content-Type', 'text/html; charset=utf-8')
                        self.send_header('Content-Length', str(len(encoded)))
                        self.end_headers()
                        self.wfile.write(encoded)
                    except Exception:
                        # fallback to binary stream
                        with open(fs_path, 'rb') as f:
                            self.send_response(200)
                            self.send_header('Content-Type', ctype)
                            fs = os.fstat(f.fileno())
                            self.send_header('Content-Length', str(fs.st_size))
                            self.end_headers()
                            self.copyfile(f, self.wfile)
                else:
                    with open(fs_path, 'rb') as f:
                        self.send_response(200)
                        self.send_header('Content-Type', ctype)
                        fs = os.fstat(f.fileno())
                        self.send_header('Content-Length', str(fs.st_size))
                        self.end_headers()
                        self.copyfile(f, self.wfile)
            except BrokenPipeError:
                return
            return

        # file not found: try to serve out/404.html (like GitHub Pages)
        notfound_path = os.path.join(OUT_DIR, '404.html')
        if os.path.exists(notfound_path):
            try:
                with open(notfound_path, 'rb') as f:
                    data = f.read()
                text = data.decode('utf-8', errors='ignore')
                text = inject(text)
                encoded = text.encode('utf-8')
                self.send_response(404)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(encoded)))
                self.end_headers()
                self.wfile.write(encoded)
                return
            except BrokenPipeError:
                return

        # fallback to default 404
        self.send_error(404, 'File not found')


def notify_clients():
    dead = []
    with clients_lock:
        for h in list(clients):
            try:
                msg = 'data: reload\n\n'
                h.wfile.write(msg.encode('utf-8'))
                h.wfile.flush()
            except Exception:
                dead.append(h)
        for d in dead:
            if d in clients:
                clients.remove(d)


def snapshot_tree(root):
    state = {}
    for dirpath, dirnames, filenames in os.walk(root):
        for name in filenames:
            if dirpath.startswith(OUT_DIR):
                continue
            if dirpath.startswith(os.path.join(os.getcwd(), '.git')):
                continue
            path = os.path.join(dirpath, name)
            try:
                state[path] = os.path.getmtime(path)
            except OSError:
                state[path] = None
    return state


def watch_and_build(root, interval=1.0):
    prev = snapshot_tree(root)
    while True:
        time.sleep(interval)
        curr = snapshot_tree(root)
        if curr != prev:
            try:
                subprocess.run([sys.executable, os.path.join(os.getcwd(), 'generate.py')], check=False)
            except Exception as e:
                print('Error running generate.py:', e)
            notify_clients()
            prev = curr


if __name__ == '__main__':
    subprocess.run([sys.executable, os.path.join(os.getcwd(), 'generate.py')], check=False)
    print('Serving', OUT_DIR, 'on port', PORT)
    server = ThreadingHTTPServer(('', PORT), DevHandler)
    watcher = threading.Thread(target=watch_and_build, args=(os.getcwd(),), daemon=True)
    watcher.start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nShutting down')
        server.shutdown()
