"""5강 학습용 도식: 고속도로 비유, Switching(경로 선택), 이정표, 경로, Router, Routing Table."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import excalidraw_scene as xs
from excalidraw_scene import Scene, save, frame_origin, W, B, R

xs.FW = 1400
G = "#9ca3af"
ROUND = {"type": 3}

# 도로 격자: 세로선 2개(A·B·C / D·E·F), 가로선 3개
XA, XD = 330, 620
Y1, Y2, Y3 = 230, 370, 510
X0, X1 = 170, 860
NODES = {"A": (XA, Y1), "B": (XA, Y2), "C": (XA, Y3),
         "D": (XD, Y1), "E": (XD, Y2), "F": (XD, Y3)}
PX = 1000  # 오른쪽 설명 영역


def box(s, x, y, w, h, label=None, size=20, color=W, stroke=W, **kw):
    s.rect(x, y, w, h, stroke, roundness=ROUND, **kw)
    if label:
        s.ctext(x + w / 2, y + h / 2, label, size, color)


def hline(s, x, y, w, color=W, **kw):
    s.line(x, y, [[0, 0], [w, 0]], color, **kw)


# ---------- 1. 고속도로 비유와 도로 격자 ----------
def road(s):
    s.text(40, 28, "Switch와 Switching", 38, W)
    s.arrow(X0, Y1, [[0, 0], [X1 - X0, 0]], W)
    hline(s, X0, Y2, X1 - X0)
    hline(s, X0, Y3, X1 - X0)
    s.line(X1, Y2, [[0, 0], [0, Y3 - Y2]], W)
    for x in (XA, XD):
        s.line(x, 150, [[0, 0], [0, 396]], W)
    for name, (x, y) in NODES.items():
        s.ellipse(x - 5, y - 5, 10, 10, W)
        s.text(x + 22, y + 20, name, 22, W)
    s.text(40, Y1 - 16, "출발지", 24, W)
    s.text(X1 + 24, Y1 - 44, "(최종)", 18, G)
    s.text(X1 + 24, Y1 - 16, "목적지", 24, W)
    box(s, 180, 184, 76, 30, "자동차", 16, W, W)
    s.text(40, 566, "Network → 고속도로", 26, B)
    s.text(330, 573, "(네트워크를 고속도로에 비유)", 18, G)


# ---------- 2. Switching = 경로 선택 ----------
def switching(s):
    s.ellipse(XA - 14, Y1 - 14, 28, 28, R)
    s.text(236, Y1 + 26, "교차로", 20, B)
    s.arrow(XA - 18, Y1 - 16, [[0, 0], [0, -46]], B)
    s.text(XA - 44, Y1 - 62, "①", 20, B)
    s.arrow(XA + 18, Y1 - 24, [[0, 0], [46, 0]], B)
    s.text(XA + 70, Y1 - 38, "②", 20, B)
    s.arrow(XA - 18, Y1 + 62, [[0, 0], [0, 46]], B)
    s.text(XA - 44, Y1 + 84, "③", 20, B)
    s.text(PX, 96, "Switching", 28, B)
    s.text(PX, 136, "= 경로 선택 (인터페이스 선택)", 22, W)
    s.text(PX, 174, "선택: 여러 개 중 하나를 고르는 것", 20, R)
    s.text(PX, 208, "교차로 A의 선택지: ① 위 ② 직진 ③ 아래", 17, G)


# ---------- 3. 이정표 = 경로 선택의 근거 ----------
def signpost(s):
    s.text(PX, 256, "이정표", 22, B)
    box(s, PX, 290, 180, 70, None)
    box(s, PX + 190, 290, 180, 70, None)
    s.ctext(PX + 90, 312, "← 판교 · 김포", 18, W)
    s.ctext(PX + 90, 340, "인천공항", 18, W)
    s.ctext(PX + 280, 312, "의정부 ↗", 18, W)
    s.ctext(PX + 280, 340, "일산", 18, W)
    for x in (PX + 90, PX + 280):
        s.line(x, 360, [[0, 0], [0, 26]], W)
    s.text(PX, 400, "이정표 = 경로 선택의 근거", 24, R)
    hline(s, PX, 434, 290, R)


# ---------- 4. 경로와 최적 경로 ----------
def path(s):
    e = s.arrow(XA + 14, Y1 + 28, [[0, 0], [0, Y2 - Y1 - 14], [XD - XA, Y2 - Y1 - 14],
                                   [XD - XA, -42], [XD - XA + 216, -42]], B)
    e["roundness"] = None
    s.arrow(190, Y1 + 14, [[0, 0], [X1 - 200, 0]], R)
    s.text(PX, 462, "교차로 = Switch", 20, B)
    s.text(PX, 494, "길 = 경로 · 인터페이스", 20, B)
    s.text(PX, 526, "길을 선택하는 것 = Switching", 20, B)
    Y = 640
    s.text(40, Y, "돌아가는 경로", 20, B)
    s.text(220, Y - 4, "출발지 → A → B → E → D → 목적지", 26, B)
    s.text(40, Y + 50, "최적 경로", 20, R)
    s.text(220, Y + 46, "출발지 → A → D → 목적지", 26, R)
    s.text(760, Y, "교차로마다의 선택이 이어진 것 = 경로", 20, W)
    s.text(760, Y + 50, "어떻게 하면 최적화된 경로로 갈 수 있을까?", 20, W)
    hline(s, 760, Y + 82, 400, R)


# ---------- 5. Internet = Router의 집합체 ----------
def router(s):
    for n in "ABDE":
        x, y = NODES[n]
        s.ellipse(x - 22, y - 22, 44, 44, B)
    dash = dict(strokeStyle="dashed", strokeWidth=1, startArrowhead="arrow")
    s.arrow(XA + 90, Y1 - 50, [[0, 0], [XD - XA - 120, 0]], G, **dash)
    s.arrow(XA + 40, Y2 - 30, [[0, 0], [XD - XA - 80, 0]], G, **dash)
    s.arrow(XA + 64, Y1 + 40, [[0, 0], [0, Y2 - Y1 - 80]], G, **dash)
    s.arrow(XD - 34, Y1 + 40, [[0, 0], [0, Y2 - Y1 - 80]], G, **dash)
    s.text(XA + 110, Y1 - 82, "Router끼리 통신", 16, G)
    s.text(180, Y2 + 16, "인터페이스 4개", 17, B)
    Y = 800
    hline(s, 40, Y - 20, 1320, G, strokeWidth=1)
    s.text(40, Y, "Internet = Router의 집합체", 30, W)
    hline(s, 40, Y + 44, 390, R)
    s.text(40, Y + 66, "Router = L3 Switching을 하는 장비 (도로의 교차로)", 22, B)
    s.text(40, Y + 104, "교차로마다 선 4개 = 네트워크 인터페이스 4개", 20, W)
    s.text(40, Y + 136, "→ 정보가 도착한 선을 뺀 3개 중 하나를 선택", 20, W)
    s.text(720, Y + 6, "Router끼리 프로토콜로 통신해", 20, W)
    s.text(720, Y + 36, "최적화된 경로를 결정", 20, W)
    s.text(720, Y + 104, "Router 몇 개가 손상돼도", 20, W)
    s.text(720, Y + 134, "네트워크 전체는 유지되도록 설계", 20, W)


# ---------- 6. Packet과 Routing Table ----------
def packet(s):
    s.text(180, 150, "= Packet", 20, R)
    s.text(PX + 80, 254, "= Routing Table", 24, R)
    Y = 1010
    hline(s, 40, Y - 26, 1320, G, strokeWidth=1)
    cols = [("고속도로", "Internet", B), ("교차로", "Router (L3 Switch)", B),
            ("자동차", "Packet", B), ("길 선택", "Switching", B),
            ("이정표", "Routing Table", R)]
    CW, X = 244, 150
    s.text(40, Y + 16, "도로", 20, G)
    s.text(40, Y + 96, "네트워크", 20, G)
    for i, (a, b, c) in enumerate(cols):
        x = X + i * CW
        box(s, x, Y, CW - 16, 56, a, 21, W, W)
        box(s, x, Y + 80, CW - 16, 56, b, 20, c, c)
    s.text(X, Y + 156, "Packet이 Router에 도착하면 Routing Table을 근거로 경로를 선택(Switching)", 20, W)


specs = [
    ("01_네트워크와_고속도로", 620, [road]),
    ("02_Switching과_경로_선택", 620, [road, switching]),
    ("03_이정표와_선택의_근거", 620, [road, switching, signpost]),
    ("04_경로와_최적_경로", 760, [road, switching, signpost, path]),
    ("05_인터넷과_라우터", 970, [road, switching, signpost, path, router]),
    ("06_패킷과_라우팅_테이블", 1220, [road, switching, signpost, path, router, packet]),
]
frames = []
for i, (name, h, stages) in enumerate(specs):
    s = Scene(*frame_origin(i))
    for st in stages:
        st(s)
    for e in s.items:
        e["roughness"] = 0
    frames.append((name, h, s))
save(frames, sys.argv[1])
print("saved")
