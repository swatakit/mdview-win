"""mdview - double-click a .md file and read it rendered in your browser.

Usage: python mdview.py path\\to\\file.md
Converts the Markdown to a temporary HTML page and opens it in the default browser.
No installation needed. Uses the 'markdown' package if present; otherwise the
browser renders it with marked.js (needs internet), and if that is blocked too,
the plain text is shown.
"""
import hashlib
import html
import pathlib
import sys
import tempfile
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


def main():
    if len(sys.argv) < 2:
        return
    src = pathlib.Path(sys.argv[1]).resolve()
    text = src.read_text(encoding="utf-8-sig", errors="replace")

    try:
        import markdown
        body = markdown.markdown(
            text, extensions=["tables", "fenced_code", "sane_lists", "toc"])
        scripts = MERMAID
    except Exception:
        body = '<pre id="raw">' + html.escape(text) + "</pre>"
        scripts = MARKED + MERMAID

    page = (
        "<!doctype html><html><head><meta charset='utf-8'>"
        f"<title>{html.escape(src.name)}</title>"
        f"<base href='{src.parent.as_uri()}/'>"
        f"<style>{CSS}</style></head><body>{body}{scripts}</body></html>"
    )

    out_dir = pathlib.Path(tempfile.gettempdir()) / "mdview"
    out_dir.mkdir(exist_ok=True)
    tag = hashlib.md5(str(src).encode("utf-8")).hexdigest()[:8]
    out = out_dir / f"{src.stem}-{tag}.html"
    out.write_text(page, encoding="utf-8")
    webbrowser.open(out.as_uri())


if __name__ == "__main__":
    main()
