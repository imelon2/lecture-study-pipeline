"""스터디 자료(.md)를 Notion용 Markdown으로 바꾸고 이미지를 업로드합니다.

사용법:
  python3 md_to_notion.py images  <자료.md>
      본문 이미지 목록(로컬 PNG 경로)을 출력합니다. 각 파일마다 Notion MCP의
      create-file-upload를 호출해 업로드 정보를 받습니다.
  python3 md_to_notion.py upload  <자료.md> <uploads.json>
      uploads.json의 정보로 각 PNG를 Notion에 업로드합니다.
      uploads.json 형식: {"01_주제.png": {"id": "...", "url": "...", "token": "..."}}
      (token은 create-file-upload 응답의 authorization 헤더에서 "Bearer " 뒤 값)
  python3 md_to_notion.py convert <자료.md> <uploads.json>
      Notion용 Markdown을 출력합니다.
      - 맨 위 # 제목 제거(페이지 제목과 중복)
      - ![...](assets/...png) → <image source="file-upload://ID">캡션</image>
      - 복습 질문 섹션의 "질문 / 들여쓴 답변" 목록 → <toggle>
"""
import json, pathlib, re, subprocess, sys

IMG = re.compile(r"^!\[(.*)\]\((.+\.png)\)\s*$")
REVIEW = "## 복습 질문"


def images(md):
    base = md.parent
    return [(m.group(1), base / m.group(2)) for l in md.read_text().splitlines()
            if (m := IMG.match(l))]


def upload(md, uploads):
    for _, path in images(md):
        u = uploads[path.name]
        out = subprocess.run(
            ["curl", "-s", "-X", "POST", u["url"], "-H", f"authorization: Bearer {u['token']}",
             "-F", f"file=@{path};type=image/png"], capture_output=True, text=True).stdout
        status = json.loads(out).get("status")
        print(path.name, status)
        if status != "uploaded":
            sys.exit(f"업로드 실패: {path.name}: {out[:300]}")


def convert(md, uploads):
    lines = md.read_text().splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    while lines and not lines[0].strip():
        lines = lines[1:]
    out, k, in_review = [], 0, False
    while k < len(lines):
        l = lines[k]
        m = IMG.match(l)
        if m:
            fid = uploads[pathlib.Path(m.group(2)).name]["id"]
            out.append(f'<image source="file-upload://{fid}">{m.group(1)}</image>')
        elif l.startswith("## "):
            in_review = l.startswith(REVIEW)
            out.append(l)
        elif in_review and l.startswith("- "):
            q, ans = l[2:], []
            while k + 1 < len(lines) and lines[k + 1].startswith("  - "):
                k += 1
                ans.append(lines[k].strip()[2:])
            out.append("<toggle>\n" + q + "\n\n" + "\n\n".join(ans) + "\n</toggle>\n")
        else:
            out.append(l)
        k += 1
    print("\n".join(out).rstrip())


if __name__ == "__main__":
    cmd, md = sys.argv[1], pathlib.Path(sys.argv[2])
    if cmd == "images":
        for cap, p in images(md):
            print(p.name, p, sep="\t")
    else:
        uploads = json.loads(pathlib.Path(sys.argv[3]).read_text())
        {"upload": upload, "convert": convert}[cmd](md, uploads)
