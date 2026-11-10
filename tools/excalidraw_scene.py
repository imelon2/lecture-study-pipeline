"""칠판 장면을 Excalidraw Frame으로 그리는 도우미.

사용 예:
    from excalidraw_scene import Scene, save
    frames = []
    s = Scene(0, 0); s.text(60, 30, "User"); s.line(80, 70, [[0, 0], [1000, 0]])
    frames.append(("01_주제", 600, s))
    save(frames, "out.excalidraw")
Frame은 가로로 나란히 놓이며, Scene(ox, 0)의 ox는 i * (FW + GAP)로 맞춥니다.
"""
import json, random, unicodedata

W, B, R, OLIVE = "#e5e5e5", "#4a9eed", "#ef4444", "#808000"
FONT = 5  # Excalifont (CJK는 Excalidraw가 Xiaolai로 대체)
_n = 0


def tw(s, size):
    """Excalifont 기준 글자 폭 추정(한글 0.92, 공백 0.32, 그 외 0.58)."""
    w = 0
    for ch in s:
        if unicodedata.east_asian_width(ch) in "WF":
            w += size * 0.92
        elif ch == " ":
            w += size * 0.32
        else:
            w += size * 0.58
    return w


def base(t, x, y, w, h, color=W, **kw):
    global _n
    _n += 1
    e = dict(id=f"e{_n}", type=t, x=x, y=y, width=w, height=h, angle=0,
             strokeColor=color, backgroundColor="transparent", fillStyle="solid",
             strokeWidth=2, strokeStyle="solid", roughness=1, opacity=100,
             groupIds=[], frameId=None, roundness=None,
             seed=random.randint(1, 2**31), version=1,
             versionNonce=random.randint(1, 2**31), isDeleted=False,
             boundElements=None, updated=1, link=None, locked=False)
    e.update(kw)
    return e


class Scene:
    def __init__(self, ox, oy):
        self.ox, self.oy, self.items = ox, oy, []

    def add(self, e):
        e["x"] += self.ox
        e["y"] += self.oy
        self.items.append(e)
        return e

    def text(self, x, y, s, size=26, color=W):
        return self.add(base("text", x, y, tw(s, size), size * 1.25, color,
                             text=s, originalText=s, fontSize=size, fontFamily=FONT,
                             textAlign="left", verticalAlign="top", containerId=None,
                             autoResize=True, lineHeight=1.25))

    def ctext(self, cx, cy, s, size=22, color=B):
        w = tw(s, size)
        return self.text(cx - w / 2, cy - size * 0.625, s, size, color)

    def rect(self, x, y, w, h, color=W, **kw):
        return self.add(base("rectangle", x, y, w, h, color, **kw))

    def ellipse(self, x, y, w, h, color=W):
        return self.add(base("ellipse", x, y, w, h, color))

    def _poly(self, t, x, y, pts, color, **kw):
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        return self.add(base(t, x, y, max(xs) - min(xs), max(ys) - min(ys), color,
                             points=pts, lastCommittedPoint=None, startBinding=None,
                             endBinding=None, startArrowhead=kw.pop("startArrowhead", None),
                             endArrowhead=kw.pop("head", None),
                             roundness={"type": 2} if len(pts) > 2 else None, **kw))

    def line(self, x, y, pts, color=W, **kw):
        return self._poly("line", x, y, pts, color, **kw)

    def arrow(self, x, y, pts, color=W, head="arrow", **kw):
        return self._poly("arrow", x, y, pts, color, head=head, **kw)


FW, GAP = 1180, 120


def frame_origin(i):
    return i * (FW + GAP), 0


def save(frames, path):
    """frames: [(이름, 높이, Scene)] 목록을 Frame으로 묶어 저장합니다."""
    out = []
    for i, (name, fh, s) in enumerate(frames):
        ox, oy = frame_origin(i)
        fr = base("frame", ox, oy, FW, fh, "#bbb", name=name, roughness=0)
        for e in s.items:
            e["frameId"] = fr["id"]
        out.extend(s.items)
        out.append(fr)
    doc = {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
           "elements": out,
           "appState": {"viewBackgroundColor": "#1e1e1e", "gridSize": None},
           "files": {}}
    with open(path, "w") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
