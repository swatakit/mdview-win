"""mdview - double-click a .md file and read it rendered in your browser.

Usage: python mdview.py path\\to\\file.md
Converts the Markdown to a temporary HTML page and opens it in the default browser.
No installation needed. Uses the 'markdown' package if present; otherwise the
browser renders it with marked.js (needs internet), and if that is blocked too,
the plain text is shown.
"""
import hashlib
import html
import json
import pathlib
import re
import sys
import tempfile
import urllib.parse
import webbrowser

CSS = """
body{font-family:Segoe UI,Arial,sans-serif;line-height:1.6;color:#1f2328;
     max-width:900px;margin:40px auto;padding:0 24px;}
h1,h2{border-bottom:1px solid #d0d7de;padding-bottom:.3em;}
code{background:#f0f2f4;padding:.15em .35em;border-radius:4px;font-family:Consolas,monospace;font-size:90%;}
pre{background:#f6f8fa;padding:14px;border-radius:6px;overflow:auto;}
pre code{background:none;padding:0;}
table{border-collapse:collapse;margin:1em 0;}
th,td{border:1px solid #d0d7de;padding:6px 12px;}
th{background:#f6f8fa;}
blockquote{border-left:4px solid #d0d7de;margin:0;padding:0 1em;color:#59636e;}
img{max-width:100%;}
a{color:#0969da;}
@media (prefers-color-scheme: dark){
 body{background:#0d1117;color:#e6edf3;}
 h1,h2{border-color:#30363d;}
 code,pre,th{background:#161b22;}
 th,td{border-color:#30363d;}
 blockquote{border-color:#30363d;color:#9198a1;}
 a{color:#4493f8;}
}
"""

MARKED = """
<script src="https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js"></script>
<script>
if (window.marked) {
  var raw = document.getElementById('raw');
  var div = document.createElement('div');
  div.innerHTML = marked.parse(raw.textContent);
  raw.replaceWith(div);
}
</script>
"""

MERMAID = """
<script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"></script>
<script>
if (window.mermaid) {
  document.querySelectorAll('code.language-mermaid').forEach(function (c) {
    var d = document.createElement('div');
    d.className = 'mermaid';
    d.textContent = c.textContent;
    c.parentElement.replaceWith(d);
  });
  mermaid.initialize({startOnLoad: false});
  mermaid.run();
}
</script>
"""


LINKS = """
<script>
(function () {
  var map = __MAP__;
  document.querySelectorAll('a[href]').forEach(function (a) {
    var u;
    try { u = new URL(a.href); } catch (e) { return; }
    var hash = u.hash;
    u.hash = '';
    var key;
    try { key = decodeURIComponent(u.href).toLowerCase(); } catch (e) { return; }
    if (map[key]) a.href = map[key] + hash;
  });
})();
</script>
"""

MAX_FILES = 200
LINK_RE = re.compile(
    r"""(?:\]\(\s*<?|href\s*=\s*["']|^\s*\[[^\]]+\]:\s*<?)([^)\s>"'#]+\.(?:md|markdown))""",
    re.I | re.M)
OUT_DIR = pathlib.Path(tempfile.gettempdir()) / "mdview"


def out_path(src):
    tag = hashlib.md5(str(src).encode("utf-8")).hexdigest()[:8]
    return OUT_DIR / f"{src.stem}-{tag}.html"


def linked_files(src, text):
    """Local .md files that this file links to (existing ones only)."""
    found = []
    for target in LINK_RE.findall(text):
        if re.match(r"[a-z][a-z0-9+.-]+:", target, re.I):
            continue  # http:, mailto:, file: ... (a one-letter prefix is a drive)
        try:
            path = (src.parent / urllib.parse.unquote(target)).resolve()
            if path.is_file() and path not in found:
                found.append(path)
        except OSError:
            pass
    return found


def render(src, text, links):
    try:
        import markdown
        body = markdown.markdown(
            text, extensions=["tables", "fenced_code", "sane_lists", "toc"])
        scripts = MERMAID
    except Exception:
        body = '<pre id="raw">' + html.escape(text) + "</pre>"
        scripts = MARKED + MERMAID

    link_map = {urllib.parse.unquote(p.as_uri()).lower(): out_path(p).as_uri()
                for p in links}
    scripts += LINKS.replace(
        "__MAP__", json.dumps(link_map).replace("</", "<\\/"))

    return (
        "<!doctype html><html><head><meta charset='utf-8'>"
        f"<title>{html.escape(src.name)}</title>"
        f"<base href='{src.parent.as_uri()}/'>"
        f"<style>{CSS}</style></head><body>{body}{scripts}</body></html>"
    )


def main():
    if len(sys.argv) < 2:
        return
    first = pathlib.Path(sys.argv[1]).resolve()
    OUT_DIR.mkdir(exist_ok=True)

    # Render the opened file plus every local .md it links to (each once),
    # so links between pages open rendered copies instead of raw text.
    queue, seen = [first], {first}
    while queue:
        src = queue.pop(0)
        try:
            text = src.read_text(encoding="utf-8-sig", errors="replace")
        except OSError:
            if src == first:
                raise
            continue
        links = linked_files(src, text)
        for path in links:
            if path not in seen and len(seen) < MAX_FILES:
                seen.add(path)
                queue.append(path)
        out_path(src).write_text(render(src, text, links), encoding="utf-8")

    webbrowser.open(out_path(first).as_uri())


if __name__ == "__main__":
    main()
