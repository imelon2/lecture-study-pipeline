"""7강 학습용 도식: User mode와 Kernel mode (구현 요소 → Socket → OSI 대응)."""
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1]))
from excalidraw_scene import Scene, save, frame_origin, W, B, R

G = "#9ca3af"  # 보조 설명(회색)
ROUND = {"type": 3}

# ---------- 공통 격자 ----------
TOP, U_K, K_H, BOT = 110, 330, 570, 700      # User | Kernel | H/W 경계
X_L, X_R = 40, 840
IMP_X, IMP_W = 250, 190                      # 구현 요소 열
OSI_X, OSI_W = 560, 230                      # OSI 7 Layer 열
LV_X, NOTE_X, DESC_X = 800, 870, 500
L4_L3 = 410                                  # Transport | Network 경계
L3_END = 490                                 # Network 칸 아래쪽
L2_L1 = 635                                  # Data Link | Physical 경계


def box(s, x, y, w, h, label=None, size=22, color=W, stroke=W, **kw):
    s.rect(x, y, w, h, stroke, **kw)
    if label:
        s.ctext(x + w / 2, y + h / 2, label, size, color)


def stage_base(s):
    s.text(40, 30, "User mode와 Kernel mode", 28, W)
    for y in (U_K, K_H):
        s.line(X_L, y, [[0, 0], [X_R - X_L, 0]])
    s.text(X_L, U_K - 34, "User mode", 20)
    s.text(X_L, U_K + 8, "Kernel mode", 20)
    s.text(X_L, U_K + 38, "OS", 18, B)
    s.text(X_L, K_H - 32, "S/W", 20)
    s.text(X_L, K_H + 8, "H/W", 20)
    # User: 응용 프로그램 창
    s.rect(IMP_X, 120, IMP_W, 90, W, roundness=ROUND)
    s.line(IMP_X, 144, [[0, 0], [IMP_W, 0]], strokeWidth=1)
    s.text(IMP_X + IMP_W - 22, 120, "x", 16)
    s.ctext(IMP_X + IMP_W / 2, 177, "Chrome", 24, W)
    # Kernel: TCP / IP, Driver
    s.rect(IMP_X, 340, IMP_W, 140, W)
    s.line(IMP_X, L4_L3, [[0, 0], [IMP_W, 0]], strokeStyle="dashed", strokeWidth=1)
    s.ctext(IMP_X + IMP_W / 2, 375, "TCP", 24, W)
    s.ctext(IMP_X + IMP_W / 2, 445, "IP", 24, W)
    box(s, IMP_X, 505, IMP_W, 50, "Driver", 20)
    # H/W: NIC
    s.rect(IMP_X, 595, IMP_W, 85, W)
    s.ctext(IMP_X + IMP_W / 2, 650, "NIC", 24, W)
    s.arrow(IMP_X + IMP_W / 2, 557, [[0, 0], [0, 36]], W, strokeWidth=1)


def stage_describe(s):
    rows = [(150, "응용 프로그램(Process)이 실행되는 영역", "예: Chrome으로 영상 시청, 웹 서핑"),
            (385, "운영체제(OS) 영역: 프로토콜을 구현한 소프트웨어", "TCP, IP가 Kernel의 구성 요소로 들어 있음"),
            (505, "Driver: 하드웨어를 제어하는 소프트웨어", "설치되어야 NIC가 작동함"),
            (612, "NIC (Network Interface Card)", "흔히 LAN 카드라고 부르는 하드웨어")]
    for y, title, sub in rows:
        s.text(DESC_X, y, title, 19, W)
        s.text(DESC_X, y + 30, sub, 16, G)


def stage_socket(s, describe=False):
    s.ellipse(IMP_X + 50, 250, 90, 66, B)
    s.ctext(IMP_X + IMP_W / 2, 283, "File", 20, B)
    s.text(IMP_X + 150, 268, "Socket", 20, R)
    if describe:
        s.text(DESC_X, 240, "인터페이스 = File: Process가 Kernel에 접근하는 통로", 19, B)
        s.text(DESC_X, 270, "Socket: TCP/IP를 추상화한 인터페이스 파일", 19, R)


def stage_osi(s):
    s.ctext(OSI_X + OSI_W / 2, 84, "OSI 7 Layer", 26, B)
    u = (U_K - TOP) / 3
    layers = [("L7", "Application", TOP, TOP + u), ("L6", "Presentation", TOP + u, TOP + 2 * u),
              ("L5", "Session", TOP + 2 * u, U_K), ("L4", "Transport", U_K, L4_L3),
              ("L3", "Network", L4_L3, L3_END), ("L2", "Data Link", K_H, L2_L1),
              ("L1", "Physical", L2_L1, BOT)]
    s.rect(OSI_X, TOP, OSI_W, BOT - TOP, W)
    for lv, name, a, b in layers:
        s.rect(OSI_X, a, OSI_W, b - a, W, strokeWidth=1)
        s.ctext(OSI_X + OSI_W / 2, (a + b) / 2, name, 20, W)
        s.text(LV_X, (a + b) / 2 - 12, lv, 19, B)
    # L5 이상 = User mode Application
    s.text(IMP_X + IMP_W + 10, 126, "Process", 18, B)
    s.line(NOTE_X - 16, TOP + 6, [[0, 0], [0, U_K - TOP - 12]], B)
    s.text(NOTE_X, 170, "L5 ~ L7", 22, B)
    s.text(NOTE_X, 204, "User mode Application", 16, W)
    s.text(NOTE_X, 228, "Process 수준에서 구현", 16, G)
    # TCP = L4, IP = L3
    for y in (375, 445):
        s.line(IMP_X + IMP_W + 6, y, [[0, 0], [OSI_X - IMP_X - IMP_W - 12, 0]], B,
               strokeStyle="dashed", strokeWidth=1)


def stage_notation(s):
    s.text(NOTE_X + 30, 346, "TCP", 24, W)
    s.text(NOTE_X + 95, 351, "L4 전송", 16, B)
    s.line(NOTE_X + 24, 386, [[0, 0], [170, 0]], W, strokeWidth=1)
    s.text(NOTE_X + 30, 394, "IP", 24, W)
    s.text(NOTE_X + 95, 399, "L3 네트워크", 16, B)
    s.arrow(NOTE_X + 46, 434, [[0, 0], [0, 22]], G, strokeWidth=1)
    s.text(NOTE_X, 462, "TCP/IP", 26, R)
    s.text(NOTE_X, 502, "'/' = 서로 다른 계층", 16, G)
    s.text(NOTE_X, 526, "위·아래 표기와 같은 뜻", 16, G)


def stage_lower(s):
    # Data Link = Driver + NIC 펌웨어 일부
    s.rect(IMP_X - 7, 498, IMP_W + 14, 130, R, strokeStyle="dashed")
    s.ctext(IMP_X + IMP_W / 2, 610, "Firmware", 15, G)
    s.line(IMP_X + IMP_W + 9, 602, [[0, 0], [OSI_X - IMP_X - IMP_W - 15, 0]], R,
           strokeStyle="dashed", strokeWidth=1)
    s.line(IMP_X + IMP_W + 6, 667, [[0, 0], [OSI_X - IMP_X - IMP_W - 12, 0]], B,
           strokeStyle="dashed", strokeWidth=1)
    s.text(NOTE_X, 583, "L2 Data Link", 18, R)
    s.text(NOTE_X, 609, "Driver + NIC 펌웨어 일부", 15, G)
    s.text(NOTE_X, 645, "L1 Physical", 18, B)
    s.text(NOTE_X, 671, "NIC 하드웨어", 15, G)


def stage_open(s):
    s.arrow(IMP_X + IMP_W / 2, 213, [[0, 0], [0, 34]], R)
    s.text(IMP_X + IMP_W / 2 + 10, 218, "open", 15, R)
    s.rect(X_L, 730, 1100, 84, R, roundness=ROUND)
    s.ctext(590, 757, "Socket을 여는 주체 = Process", 22, R)
    s.ctext(590, 790, "Process가 네트워크를 추상화한 파일(Socket)을 연다", 17, W)


sock_desc = lambda s: stage_socket(s, describe=True)
specs = [
    ("01_구현_요소", 740, [stage_base, stage_describe]),
    ("02_파일과_소켓", 740, [stage_base, stage_describe, sock_desc]),
    ("03_OSI_대응", 740, [stage_base, stage_socket, stage_osi]),
    ("04_TCP_IP_표기", 740, [stage_base, stage_socket, stage_osi, stage_notation]),
    ("05_DataLink_Physical", 740, [stage_base, stage_socket, stage_osi, stage_notation, stage_lower]),
    ("06_소켓과_프로세스", 850, [stage_base, stage_socket, stage_osi, stage_notation, stage_lower, stage_open]),
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
