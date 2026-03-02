#!/usr/bin/env python3

import os
import csv
import re
import markdown

# Markdown to HTML conversion functions
def mdspan(md, classname=None):
    html = markdown.markdown(md)
    if not html.startswith("<p>") and not html.endswith("</p>"):
        html = f"<p>{html}</p>"
    if classname is not None:
        html = html.replace("<p>", f'<span class="{classname}">')
    else:
        html = html.replace("<p>", "<span>")
    html = html.replace("</p>", "</span>")
    return html

def read_section(path):
    out = ""
    if os.path.isfile(f"{path}.html"):
        with open(f"{path}.html", "r") as f:
            out += f.read()
    if os.path.isfile(f"{path}.md"):
        with open(f"{path}.md", "r") as f:
            out += f.read()

    if os.path.isdir(path):
        for ent in sorted(os.listdir(path)):
            ent_path = os.path.join(path, ent)
            if not os.path.isfile(ent_path): continue
            if not ent_path.endswith(".md") and not ent_path.endswith(".html"): continue
            out += "\n"
            basename = os.path.splitext(ent_path)[0]
            out += read_section(basename)

    if os.path.isfile(f"{path}.cats"):
        out += '<div class="categories">'
        with open(f"{path}.cats", "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                out += '<div class="category">'
                out += mdspan(f"##### {row['Name']}")
                out += mdspan(row["Objective"], "objective")
                out += "<hr />"
                out += mdspan(f"**OOB:** {row['OOB']}")
                out += mdspan(f"**SLA:** {row['SLA']}")
                out += mdspan(f"**Pause Abuse:** {row['Pause Abuse']}")
                out += mdspan(f"**Demo Requirement:** {row['Demo Requirement']}")
                out += mdspan(f"**Video Requirement:** {row['Video Requirement']}")
                out += mdspan(f"[Leaderboard]({row['Leaderboard']})")
                out += mdspan(f"**Moderators:** {row['Moderators']}")
                if row["Notes"] != "":
                    out += "<hr />"
                    out += mdspan(row["Notes"], "notes")
                out += '</div>'
        out += '</div>'

    return out

# Nav section generation
def generate_nav(page, sections):
    out = ""
    for sect in sections:
        sect_id = sect["id"]
        name = sect["name"]
        children = sect["children"]

        out += f"<a href='#{sect_id}'>{name}</a>"
        if len(children) > 0:
            out += "<div class='navindent'>"
            out += generate_nav("__INDENT__" + page, children)
            out += "</div>"
    
    if (not page.startswith("__INDENT__")):
        out += "<div id='nav-links'>\n"
        if (page != "index"):
            out += '<a href="/" class="fa-solid fa-house"></a>\n'
        out += """
                <a href="https://github.com/p2sr/rules" target="_blank" class="fa-brands fa-github"></a>
                <a href="https://discord.com/invite/hRwE4Zr" target="_blank" class="fa-brands fa-discord"></a>
            </div>
            """

    return out

# Console commands
def sort_command_func(cmd):
    command = cmd["Command"]
    if command.startswith('-'):
        return '0' + command[1:] + '1'
    elif command.startswith('+'):
        return '0' + command[1:] + '0'
    return '1' + command + '2'

def generate_command_table():
    out = """
    <input type="text" id="command-search" onkeyup="searchCommands()" placeholder="Search commands...">
    <table class="commands">
        <tr>
            <th>Command</th>
            <th>Type</th>
            <th>Allowed Values</th>
        </tr>
    """

    commands = []
    with open("commands.csv", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            commands.append(row)

    last = ''
    for cmd in sorted(commands, key=sort_command_func):
        if cmd['Command'] == last:
            print(f"Duplicate command: {cmd['Command']}")
        out += "<tr>"
        out += f"<td>{cmd['Command']}</td>"
        out += f"<td>{cmd['Type']}</td>"
        out += f"<td>{cmd['Allowed Values']}</td>"
        out += "</tr>"
        last = cmd['Command']

    out += "</table>"
    return out
commands = generate_command_table()

# Replace Discord-style UNIX epoch markdown like <t:1609459200:R>
# with HTML <time> elements that client-side JS will render.
def _replace_timestamp_tokens(s):
    def _repl(m):
        epoch = m.group(1)
        fmt = m.group(2)
        return f'<time class="discord-timestamp" data-epoch="{epoch}" data-format="{fmt}">{epoch}</time>'
    return re.sub(r'<t:(\d+):([tTdDfFR])>', _repl, s)

with open("template.html", "r") as f:
    template = f.read()

for page in os.listdir("content"):
    md_str = ""
    md = markdown.Markdown(extensions=['toc'])
    # Combine sections of the page into one markdown string
    for ent in sorted(os.listdir(os.path.join("content", page))):
        ent_path = os.path.join("content", page, ent)
        if not os.path.isfile(ent_path): continue
        if not ent_path.endswith(".md") and not ent_path.endswith(".html"): continue
        basename = os.path.splitext(ent_path)[0]
        md_str += read_section(basename)

    md_str = _replace_timestamp_tokens(md_str)

    content = md.convert(md_str)

    out = (template
        .replace("{{CONTENT}}", content)
        .replace("{{NAV_MENU}}", generate_nav(page, md.toc_tokens))
        .replace("{{COMMAND_LIST}}", commands)
    )

    page_path = os.path.join("out", page, "index.html")
    if page == "index":
        page_path = os.path.join("out", "index.html")
    os.makedirs(os.path.dirname(page_path), exist_ok=True)
    with open(page_path, "w") as f:
        f.write(out)
