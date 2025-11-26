#!/usr/bin/env python3

import os
import csv
import markdown

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
    with open(f"{path}.md", "r") as f:
        out += f.read()

    if os.path.isdir(path):
        for ent in sorted(os.listdir(path)):
            ent_path = os.path.join(path, ent)
            if not os.path.isfile(ent_path): continue
            if not ent_path.endswith(".md"): continue
            out += "\n"
            out += read_section(ent_path[:-3])

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
                out += '</div>\n'
        out += '</div>'
    else:
        out = f"""<div class="content" markdown="block">{out}</div>"""

    return out

def generate_nav(sections):
    out = ""
    for sect in sections:
        sect_id = sect["id"]
        name = sect["name"]
        children = sect["children"]

        out += f"<a href='#{sect_id}'>{name}</a>"
        if len(children) > 0:
            out += "<div class='navindent'>"
            out += generate_nav(children)
            out += "</div>"

    return out

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


md_str = ""
for ent in sorted(os.listdir("content")):
    ent_path = os.path.join("content", ent)
    if not os.path.isfile(ent_path): continue
    if not ent_path.endswith(".md"): continue
    md_str += read_section(ent_path[:-3])

md = markdown.Markdown(extensions=['toc', 'md_in_html'])
content = md.convert(md_str)

with open("template.html", "r") as f:
    template = f.read()

out = (template
    .replace("{{CONTENT}}", content)
    .replace("{{NAV_MENU}}", generate_nav(md.toc_tokens) + """
        <div id='nav-links'>
            <a href="https://github.com/p2sr/rules" target="_blank" class="fa-brands fa-github"></a>
            <a href="https://discord.com/invite/hRwE4Zr" target="_blank" class="fa-brands fa-discord"></a>
        </div>
        """)
    .replace("{{COMMAND_LIST}}", generate_command_table())
)

with open("out/index.html", "w") as f:
    f.write(out)
