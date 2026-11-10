"""1강 학습용 도식 v2: 칠판 구도 유지 + 오와 열 정돈 + 생략 내용 보완."""
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1]))
from excalidraw_scene import Scene, save, frame_origin, W, B, R

G = "#9ca3af"  # 보조 설명(회색)
ROUND = {"type": 3}

# ---------- 공통 격자 ----------
TOP, U_K, K_H, BOT = 140, 320, 460, 560      # User | Kernel | H/W 경계
X_L, X_R = 40, 1160
OSI_X, DOD_X, IMP_X, ANN_X = 290, 540, 800, 1010
COL_W, IMP_W = 220, 170


def box(s, x, y, w, h, label=None, size=20, color=B, stroke=W, **kw):
    s.rect(x, y, w, h, stroke, **kw)
    if label:
        s.ctext(x + w / 2, y + h / 2, label, size, color)


def stage_layers(s, describe=False):
    for y in (U_K, K_H):
        s.line(X_L, y, [[0, 0], [X_R - X_L, 0]])
    rows = [("User 모드", "응용 S/W", TOP, U_K), ("Kernel 모드", "시스템 S/W", U_K, K_H),
            ("H/W", "하드웨어", K_H, BOT)]
    for name, sub, a, b in rows:
        mid = (a + b) / 2
        s.text(X_L, mid - 26, name, 24)
        s.text(X_L, mid + 6, sub, 16, G)
    # S/W 영역 화살표
    s.arrow(232, TOP, [[0, 0], [0, K_H - TOP]], G, head="arrow", startArrowhead="arrow")
    s.text(242, (TOP + K_H) / 2 - 12, "S/W", 18, G)
    if describe:
        s.text(320, (TOP + U_K) / 2 - 14, "응용 프로그램(Process)이 동작하는 영역", 22, G)
        s.text(320, (U_K + K_H) / 2 - 14, "운영체제의 핵심(Kernel)이 동작하는 영역", 22, G)
        s.text(320, (K_H + BOT) / 2 - 14, "물리 장치가 있는 영역", 22, G)


def stage_osi_dod(s):
    s.ctext(OSI_X + COL_W / 2, 100, "OSI 7 Layer", 28, B)
    osi = [("L7  Application", TOP, 200), ("L6  Presentation", 200, 260),
           ("L5  Session", 260, U_K), ("L4  Transport", U_K, 380),
           ("L3  Network", 380, K_H), ("L2  Data Link", K_H, 510), ("L1  Physical", 510, BOT)]
    for name, a, b in osi:
        s.rect(OSI_X, a, COL_W, b - a, W)
        cy = 165 if a == TOP else (a + b) / 2
        s.ctext(OSI_X + COL_W / 2, cy, name, 20, B)
    s.ctext(DOD_X + COL_W / 2, 100, "DoD 4계층", 28, B)
    dod = [("Application", TOP, U_K), ("Transport", U_K, 380),
           ("Internet", 380, K_H), ("Network Access", K_H, BOT)]
    for name, a, b in dod:
        box(s, DOD_X, a, COL_W, b - a, name, 22)


def stage_impl(s):
    s.ctext(IMP_X + IMP_W / 2, 100, "실제 구현", 28, W)
    # Process 창
    s.rect(IMP_X, 160, IMP_W, 122, W, roundness=ROUND)
    s.line(IMP_X, 184, [[0, 0], [IMP_W, 0]], strokeWidth=1)
    s.text(IMP_X + IMP_W - 22, 160, "x", 16)
    s.ctext(IMP_X + IMP_W / 2, 225, "Process", 24, W)
    # Kernel: TCP / IP / Driver
    box(s, IMP_X, U_K, IMP_W, 60, "TCP", 24, W)
    box(s, IMP_X, 380, IMP_W, 40, "IP", 22, W)
    box(s, IMP_X, 420, IMP_W, 40, "Driver", 18, G)
    # H/W: NIC
    box(s, IMP_X, 475, IMP_W, 70, "NIC", 24, W)
    s.ctext(IMP_X + IMP_W / 2, 532, "LAN 카드", 14, G)
    # DoD 계층 → 구현 대응
    for y in ((TOP + U_K) / 2, 350, 400, (K_H + BOT) / 2 + 2):
        s.arrow(DOD_X + COL_W + 6, y, [[0, 0], [IMP_X - DOD_X - COL_W - 12, 0]], G,
                strokeStyle="dashed", strokeWidth=1)


def stage_socket(s):
    s.rect(IMP_X, U_K, IMP_W, 100, R, strokeWidth=3)          # TCP/IP 강조
    s.rect(IMP_X + 30, 288, IMP_W - 60, 26, R, roundness=ROUND)
    s.ctext(IMP_X + IMP_W / 2, 301, "File = Socket", 15, R)
    s.text(ANN_X, 190, "Socket", 32, R)
    s.text(ANN_X, 236, "Transport 계층(TCP)", 16, W)
    s.text(ANN_X, 258, "인터페이스를 파일", 16, W)
    s.text(ANN_X, 280, "형태로 추상화한 것", 16, W)
    s.arrow(ANN_X - 6, 292, [[0, 0], [-(ANN_X - 6 - (IMP_X + IMP_W - 28)), 8]], R, strokeWidth=1)


def stage_ids(s):
    s.ctext(IMP_X + IMP_W / 2, 255, "예: HTTP", 15, R)
    ids = [("Port 번호", "예: 80, 443", 350), ("IP 주소", "예: 192.168.0.10", 400),
           ("MAC 주소", "예: 00:1A:2B:3C:4D:5E", (K_H + BOT) / 2 + 2)]
    for name, ex, y in ids:
        s.line(IMP_X + IMP_W + 8, y, [[0, 0], [24, 0]], R, strokeWidth=1)
        s.text(ANN_X - 2, y - 24, name, 20, R)
        s.text(ANN_X - 2, y + 2, ex, 13, G)
    s.ctext(OSI_X + COL_W / 2, 189, "예: HTTP", 13, R)


def concept_frame(s):
    s.ctext(330, 70, "개념 (추상화)", 30, B)
    s.ctext(830, 70, "실체 (구현)", 30, R)
    s.text(565, 52, "vs", 30, G)
    rows = [("사람", "최호성, 김영희", "사람의 한 사례"),
            ("Java 추상 클래스", "구현 클래스", "추상화 → 구현"),
            ("OSI 7 Layer", "TCP/IP, HTTP", "모델 → 프로토콜")]
    y = 130
    for a, b, note in rows:
        box(s, 170, y, 320, 70, a, 24, W)
        box(s, 670, y, 320, 70, b, 24, W)
        s.arrow(500, y + 35, [[0, 0], [160, 0]], G)
        s.ctext(580, y + 15, note, 14, G)
        y += 110
    s.rect(170, 470, 820, 60, R, roundness=ROUND)
    s.ctext(580, 500, "학습 순서: 실체(TCP/IP · HTTP)를 먼저 → 개념(OSI 7 Layer)은 그다음", 22, R)


specs = [
    ("01_개념과_실체", 580, [concept_frame]),
    ("02_컴퓨터_3계층", 600, [lambda s: stage_layers(s, describe=True)]),
    ("03_OSI_DoD_대응", 600, [stage_layers, stage_osi_dod]),
    ("04_실제_구현", 600, [stage_layers, stage_osi_dod, stage_impl]),
    ("05_소켓", 600, [stage_layers, stage_osi_dod, stage_impl, stage_socket]),
    ("06_계층별_식별자", 680, [stage_layers, stage_osi_dod, stage_impl, stage_socket, stage_ids]),
]
frames = []
for i, (name, h, stages) in enumerate(specs):
    s = Scene(*frame_origin(i))
    for st in stages:
        st(s)
    if name.startswith("06"):
        s.ctext(600, 625, "생각해 볼 질문: Port 번호, IP 주소, MAC 주소는 각각 무엇을 식별하는가?", 22, W)
    for e in s.items:
        e["roughness"] = 0
    frames.append((name, h, s))
save(frames, sys.argv[1])
print("saved")
