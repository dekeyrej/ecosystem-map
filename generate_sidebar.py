import os

DOCS_DIR = "docs"
EXCLUDE = {"index.md", "_config.yml", "style.css"}
HEADER = "        <h2>Docs</h2>\n        <ul>\n"
FOOTER = "        </ul>"

def title_from_filename(filename):
    name = os.path.splitext(filename)[0]
    return name.replace("-", " ").title()

def generate_sidebar():
    items = []
    for fname in sorted(os.listdir(DOCS_DIR)):
        if not fname.endswith(".md") or fname in EXCLUDE or fname.startswith("_"):
            continue
        title = title_from_filename(fname)
        link = fname.replace(".md", ".html")
        items.append(f'          <li><a href="{link}">{title}</a></li>')
    return HEADER + "\n".join(items) + "\n" + FOOTER

if __name__ == "__main__":
    sidebar_html = generate_sidebar()
    print(sidebar_html)