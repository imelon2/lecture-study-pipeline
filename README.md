# Lecture Study Pipeline

YouTube 강의 **복습용 스터디 자료(Markdown)** 제작 파이프라인 프로젝트


## 구성

| 경로 | 역할 |
|---|---|
| `AGENTS.md` | 스터디 자료·도식·Notion 작성 규칙. 에이전트가 자동으로 읽는 기준 문서 |
| `CLAUDE.md` | Claude Code가 `AGENTS.md`를 읽도록 연결(`@AGENTS.md`) |
| `.agents/skills/summarize` | `/summarize` 스킬(`.claude/skills/summarize`는 이 폴더의 심볼릭 링크) |
| `tools/excalidraw_scene.py` | 칠판 장면을 Excalidraw Frame으로 그리는 도우미 |
| `tools/lectures/*.py` | 강의별 도식 스크립트 |
| `tools/export_excalidraw_frames.py` | Frame마다 PNG로 내보내기 |
| `tools/md_to_notion.py` | 스터디 자료를 Notion용으로 변환하고 이미지 업로드 |
| `study/` | 결과물(스터디 자료와 첨부 도식) |

## 사전 준비

**1. 필수 도구 설치**

| 도구 | 용도 | 설치 예시 |
|---|---|---|
| Node.js + `summarize` CLI | YouTube 자막 추출 | `npm i -g @steipete/summarize` |
| `yt-dlp` | 영상 다운로드(칠판 장면 확인용) | `pip install yt-dlp` |
| `ffmpeg` | 영상에서 장면 캡처 | `sudo apt install ffmpeg` |
| Python 3 + Playwright | Excalidraw PNG 내보내기 | `pip install playwright && playwright install chromium` |

설치 후 확인합니다.

```bash
summarize --version && yt-dlp --version && ffmpeg -version | head -1
python3 -c "import playwright"
```

PNG 내보내기는 Excalidraw 라이브러리를 CDN(esm.sh)에서 불러오므로 **인터넷 연결**이 필요합니다.

**2. Notion 연결 (Notion에 작성할 때만)**

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

Claude Code에서 `/mcp` → `notion`을 선택해 로그인하고, 작성할 페이지에 접근 권한을 허용합니다.

## 사용법

Claude Code에서 요청합니다.

```
/summarize '<YouTube URL>' 스터디 자료를 만들어줘
```

결과물은 `study/<번호>_<영상 제목>.md`와 `study/assets/<번호>_<영상 제목>/`에 저장됩니다. Notion에 옮길 때는 작성할 **페이지 링크를 함께** 알려 줍니다. 링크가 없으면 작성 위치를 먼저 묻습니다.

```
<자료 이름>을 '<Notion 페이지 링크>'에 작성해줘
```