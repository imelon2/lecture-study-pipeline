"""Excalidraw 파일의 Frame마다 PNG를 내보냅니다.
사용법: python3 export_frames.py <file.excalidraw> <out_dir>
"""
import base64, json, sys, pathlib
from playwright.sync_api import sync_playwright

VER = "0.18.0"
src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
scene = json.loads(src.read_text())

HTML = f"""<!doctype html><html><body><script>
window.EXCALIDRAW_ASSET_PATH = "https://esm.sh/@excalidraw/excalidraw@{VER}/dist/prod/";
</script><script type="module">
import {{ exportToBlob }} from "https://esm.sh/@excalidraw/excalidraw@{VER}?bundle-deps";
window.exportFrame = async (scene, frameId) => {{
  const frame = scene.elements.find(e => e.id === frameId);
  const blob = await exportToBlob({{
    elements: scene.elements,
    appState: {{ ...scene.appState, exportBackground: true, exportScale: 2, exportWithDarkMode: false }},
    files: scene.files || {{}},
    exportingFrame: frame,
    exportPadding: 0,
    mimeType: "image/png",
  }});
  const buf = new Uint8Array(await blob.arrayBuffer());
  let s = ""; for (const b of buf) s += String.fromCharCode(b);
  return btoa(s);
}};
window.ready = true;
</script></body></html>"""

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page()
    page.on("console", lambda m: m.type == "error" and print("console:", m.text, file=sys.stderr))
    page.set_content(HTML)
    page.wait_for_function("window.ready === true", timeout=120000)
    for f in [e for e in scene["elements"] if e["type"] == "frame" and not e.get("isDeleted")]:
        data = page.evaluate("([s, id]) => window.exportFrame(s, id)", [scene, f["id"]])
        path = out / f"{f['name']}.png"
        path.write_bytes(base64.b64decode(data))
        print(path)
    b.close()
