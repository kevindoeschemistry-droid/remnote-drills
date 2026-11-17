"""Render the <img src="TEX:..."> placeholders written by scripts/gdoc.ts into PNG files.

    python3 scripts/gdoc_math.py tests/out/gdoc/heat-transfer-unit-01.html <img-dir> <base-url>

Each formula is saved as <img-dir>/<sha1 of its LaTeX>.png and the placeholder becomes
<base-url>/<that name>. Google fetches images by URL when it converts HTML into a Doc, so the
base URL has to be public (the raw.githubusercontent.com path of a pushed commit works).

Uses the repo's own KaTeX (node_modules/katex) in headless Chrome through Playwright, so the
images match the RemNote cards. The LaTeX stays in each image's alt text.
"""
import base64
import hashlib
import html
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
KATEX = ROOT / "node_modules/katex/dist"
SCALE = 3  # device pixels per CSS pixel, so the images stay sharp in print


def main(path: str, img_dir: str, base_url: str) -> None:
    src = Path(path).read_text(encoding="utf8")
    found = list(dict.fromkeys(re.findall(r'src="TEX:([A-Za-z0-9+/=]+)"', src)))
    if not found:
        print("no formulas to render")
        return
    texs = [base64.b64decode(b).decode("utf8") for b in found]
    page_html = f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="file://{KATEX}/katex.min.css">
<script src="file://{KATEX}/katex.min.js"></script>
<style>body{{margin:8px;background:#fff}} .f{{display:inline-block;padding:2px 1px;margin:6px;font-size:9.5pt}}</style></head><body>
{"".join(f'<div><span class="f" id="f{i}" data-tex="{html.escape(t, quote=True)}"></span></div>' for i, t in enumerate(texs))}
<script>for (const el of document.querySelectorAll('.f')) katex.render(el.dataset.tex, el, {{throwOnError: false}});</script>
</body></html>"""
    tmp = Path(path).with_suffix(".math.html")
    tmp.write_text(page_html, encoding="utf8")
    out = src
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        page = browser.new_page(device_scale_factor=SCALE)
        page.goto(f"file://{tmp.resolve()}")
        page.wait_for_function("document.fonts.status === 'loaded'")
        for i, b in enumerate(found):
            el = page.locator(f"#f{i}")
            box = el.bounding_box()
            name = hashlib.sha1(texs[i].encode("utf8")).hexdigest()[:12] + ".png"
            Path(img_dir).mkdir(parents=True, exist_ok=True)
            el.screenshot(type="png", path=str(Path(img_dir) / name))
            out = out.replace(
                f'src="TEX:{b}"',
                f'src="{base_url.rstrip("/")}/{name}" width="{round(box["width"])}" height="{round(box["height"])}" style="vertical-align:middle;"',
            )
        browser.close()
    tmp.unlink()
    Path(path).write_text(out, encoding="utf8")
    print(f"rendered {len(found)} formulas into {img_dir}; {path} is {len(out) // 1024} KB")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
