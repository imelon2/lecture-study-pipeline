"""2강 학습용 도식: 계층별 식별자와 각 식별자가 식별하는 대상."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import excalidraw_scene as xs
from excalidraw_scene import Scene, save, frame_origin, W, B, R

xs.FW = 1400
G = "#9ca3af"
ROUND = {"type": 3}

TOP, U_K, L43, K_H, L21, BOT = 150, 310, 390, 470, 550, 630
X_L, X_R = 40, 1360
OSI_X, OSI_W = 290, 200
ID_X, ID_W = 540, 170
TG_X, TG_W = 770, 170          # 식별 대상 칸
NOTE_X = 975                   # 보조 설명 영역


def box(s, x, y, w, h, label=None, size=20, color=W, stroke=W, **kw):
    s.rect(x, y, w, h, stroke, **kw)
    if label:
        s.ctext(x + w / 2, y + h / 2, label, size, color)


def base_layers(s):
    for y in (U_K, K_H):
        s.line(X_L, y, [[0, 0], [X_R - X_L, 0]])
    for name, sub, a, b in [("User 모드", "응용 S/W", TOP, U_K),
                            ("Kernel 모드", "시스템 S/W", U_K, K_H),
                            ("H/W", "하드웨어", K_H, BOT)]:
        mid = (a + b) / 2
        s.text(X_L, mid - 26, name, 24)
        s.text(X_L, mid + 6, sub, 16, G)
    s.arrow(232, TOP, [[0, 0], [0, K_H - TOP]], G, startArrowhead="arrow")
    s.text(242, (TOP + U_K) / 2 - 12, "S/W", 18, G)
    # OSI 7 Layer
    s.ctext(OSI_X + OSI_W / 2, 105, "OSI 7 Layer", 28, B)
    rows = [("L7  Application", TOP, 203), ("L6  Presentation", 203, 256),
            ("L5  Session", 256, U_K), ("L4  Transport", U_K, L43),
            ("L3  Network", L43, K_H), ("L2  Data Link", K_H, L21), ("L1  Physical", L21, BOT)]
    for name, a, b in rows:
        s.rect(OSI_X, a, OSI_W, b - a)
        s.ctext(OSI_X + OSI_W / 2, (a + b) / 2, name, 19, B)
    # 계층별 식별자
    s.ctext(ID_X + ID_W / 2, 105, "식별자", 28, W)
    ids = [("Port 번호", None, U_K, L43), ("IP 주소", "IPv4 · IPv6", L43, K_H),
           ("MAC 주소", "하드웨어 주소", K_H, BOT)]
    for name, sub, a, b in ids:
        mid = (a + b) / 2
        s.rect(ID_X, mid - 30, ID_W, 60, B, roundness=ROUND)
        s.ctext(ID_X + ID_W / 2, mid - (9 if sub else 0), name, 22, B)
        if sub:
            s.ctext(ID_X + ID_W / 2, mid + 16, sub, 14, G)
        s.arrow(OSI_X + OSI_W + 4, mid, [[0, 0], [ID_X - OSI_X - OSI_W - 8, 0]], G,
                strokeStyle="dashed", strokeWidth=1, head=None)


def target(s, mid, label, sub=None):
    s.ctext(TG_X + TG_W / 2, 105, "식별 대상", 28, R) if not getattr(s, "_tg", False) else None
    s._tg = True
    s.arrow(ID_X + ID_W + 6, mid, [[0, 0], [TG_X - ID_X - ID_W - 12, 0]], R)
    s.rect(TG_X, mid - 30, TG_W, 60, R, roundness=ROUND)
    s.ctext(TG_X + TG_W / 2, mid - (9 if sub else 0), label, 22, R)
    if sub:
        s.ctext(TG_X + TG_W / 2, mid + 16, sub, 14, G)


def mac(s):
    mid = (K_H + BOT) / 2
    target(s, mid, "NIC", "LAN 카드")
    s.text(TG_X + 14, BOT - 22, "유선 / 무선", 15, G)
    # 노트북 예시
    s.rect(NOTE_X, K_H + 14, 400, 132, W, roundness=ROUND)
    s.text(NOTE_X + 14, K_H + 22, "노트북(호스트) 1대", 17, W)
    for i, (nic, m) in enumerate([("유선 NIC", "MAC 주소 ①"), ("무선 NIC", "MAC 주소 ②")]):
        y = K_H + 54 + i * 44
        box(s, NOTE_X + 20, y, 140, 34, nic, 16, R, R)
        s.arrow(NOTE_X + 166, y + 17, [[0, 0], [40, 0]], G, head="arrow")
        s.text(NOTE_X + 214, y + 6, m, 17, B)
    s.text(NOTE_X, BOT + 10, "NIC마다 MAC 주소 1개 → 노트북의 MAC 주소는 2개", 16, W)
    s.text(NOTE_X, BOT + 34, "MAC 주소는 하드웨어 주소지만 변경할 수 있음", 16, R)


def ip(s):
    mid = (L43 + K_H) / 2
    target(s, mid, "Host")
    s.text(NOTE_X, mid - 28, "Host = 인터넷(네트워크)에", 17, W)
    s.text(NOTE_X, mid - 4, "연결된 컴퓨터", 17, W)
    # NIC 하나에 IP 여러 개 바인딩
    s.text(NOTE_X, TOP + 6, "NIC 1개에 IP 주소 여러 개 바인딩", 17, W)
    box(s, NOTE_X, TOP + 50, 110, 70, "NIC", 22, R, R)
    for i, name in enumerate(["IP 주소 1", "IP 주소 2", "IP 주소 n"]):
        y = TOP + 40 + i * 32
        s.text(NOTE_X + 210, y, name, 17, B)
        s.arrow(NOTE_X + 204, y + 11, [[0, 0], [-88, TOP + 85 - (y + 11)]], B, strokeWidth=1)
    s.text(NOTE_X, U_K - 30, "→ 한 호스트의 IP 주소는 n개", 16, R)


def port(s):
    y4 = (U_K + L43) / 2
    # 네트워크 관리 관점: Service
    target(s, y4, "Service", "예: HTTP")
    s.text(NOTE_X, y4 - 22, "네트워크 관리 관점", 17, W)
    s.text(NOTE_X, y4 + 2, "HTTP → TCP 80 (또는 8080)", 15, G)
    # SW 개발·관리 관점: Process
    box(s, ID_X, TOP + 30, ID_W, 60, None, stroke=R, roundness=ROUND)
    s.ctext(ID_X + ID_W / 2, TOP + 60, "Process", 22, R)
    s.arrow(ID_X + ID_W / 2, y4 - 32, [[0, 0], [0, -(y4 - 32 - TOP - 94)]], R)
    s.text(ID_X, TOP + 4, "SW 개발·관리 관점", 15, W)
    # 물리 설치 관점: 인터페이스 번호
    s.arrow(ID_X - 4, y4 + 12, [[0, 0], [-20, 30], [-24, BOT + 40 - y4 - 12]], R)
    box(s, OSI_X, BOT + 52, 420, 56, None, stroke=R, roundness=ROUND)
    s.ctext(OSI_X + 210, BOT + 72, "인터페이스 번호", 22, R)
    s.ctext(OSI_X + 210, BOT + 96, "공유기 LAN 단자 번호 · 물리 설치 관점", 14, G)


specs = [
    ("01_계층별_식별자", 680, [base_layers]),
    ("02_MAC_주소", 700, [base_layers, mac]),
    ("03_IP_주소와_호스트", 700, [base_layers, mac, ip]),
    ("04_Port_번호", 760, [base_layers, mac, ip, port]),
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
