"""3강 학습용 도식: Host·Switch·Network의 관계, 인터넷 구성요소, 계층별 스위치."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import excalidraw_scene as xs
from excalidraw_scene import Scene, save, frame_origin, W, B, R

xs.FW = 1400
G = "#9ca3af"
ROUND = {"type": 3}


def box(s, x, y, w, h, label=None, size=20, color=W, stroke=W, **kw):
    s.rect(x, y, w, h, stroke, roundness=ROUND, **kw)
    if label:
        s.ctext(x + w / 2, y + h / 2, label, size, color)


def hline(s, x, y, w, color=W, **kw):
    s.line(x, y, [[0, 0], [w, 0]], color, **kw)


# 제목 위치: Host / Switch / Network
HX, SX, NX, TY = 100, 450, 790, 24


def host(s):
    s.text(HX, TY, "Host", 42, W)
    s.text(SX, TY, "Switch", 42, W)
    s.text(NX, TY, "Network", 42, W)
    hline(s, HX, TY + 58, 96, B)
    s.arrow(HX + 40, TY + 64, [[0, 0], [0, 40]], W)
    box(s, 40, 130, 340, 56, "Computer + Network", 24, B, B)
    s.text(40, 200, "호스트 = 네트워크에 연결된 컴퓨터", 22, W)
    s.text(40, 230, "(연결 없이 단독으로 보면 워크스테이션 등으로 부름)", 16, G)


BOX_Y, BOX_H = 280, 400
LX, RX, CW = 60, 390, 300


def endpoint_switch(s):
    box(s, 40, BOX_Y, 670, BOX_H, None, stroke=W)
    s.text(56, BOX_Y + 8, "Host", 20, G)
    # 왼쪽: 네트워크 이용 주체
    box(s, LX, BOX_Y + 40, CW, BOX_H - 60, None, stroke=B)
    s.ctext(LX + CW / 2, BOX_Y + 70, "네트워크 이용 주체", 22, B)
    s.ctext(LX + CW / 2, BOX_Y + 120, "End-point (단말)", 28, R)
    hline(s, LX + 40, BOX_Y + 146, CW - 80, R)
    for i, t in enumerate(["Client", "Server", "Peer"]):
        box(s, LX + 60, BOX_Y + 180 + i * 56, CW - 120, 44, t, 22, W, W)
    s.ctext(LX + CW / 2, BOX_Y + BOX_H - 34, "역할(기능)에 따라 구분", 16, G)
    # 오른쪽: 네트워크 자체를 이룸
    box(s, RX, BOX_Y + 40, CW, BOX_H - 60, None, stroke=B)
    s.ctext(RX + CW / 2, BOX_Y + 70, "네트워크 자체를 이룸", 22, B)
    s.ctext(RX + CW / 2, BOX_Y + 120, "Switch", 28, R)
    hline(s, RX + 90, BOX_Y + 146, CW - 180, R)
    box(s, RX + 30, BOX_Y + 180, CW - 60, 44, "Router", 22, W, W)
    # Switch 제목과 연결
    hline(s, SX, TY + 58, 136, B)
    s.arrow(SX + 68, BOX_Y + 40, [[0, 0], [0, -(BOX_Y + 40 - TY - 64)]], B)


def internet(s):
    s.arrow(NX + 60, TY + 62, [[0, 0], [0, 18]], G, strokeStyle="dashed")
    s.text(NX, 112, "Internet ≒ Router + DNS", 30, B)
    hline(s, NX, 152, 360, B)
    s.text(NX, 166, "인터넷을 이루는 가장 중대한 구성요소 두 가지", 18, G)
    s.text(NX, 192, "① Router (라우터)   ② DNS", 18, G)


def purpose(s):
    s.ctext(RX + CW / 2, BOX_Y + 238, "목적: 경로 선정 (길 찾기)", 17, R)
    box(s, RX + 30, BOX_Y + 268, CW - 60, 44, "F/W, IPS", 22, W, W)
    s.ctext(RX + CW / 2, BOX_Y + 326, "목적: 보안 → 보안 스위치", 17, R)
    s.ctext(RX + CW / 2, BOX_Y + BOX_H - 34, "하는 일은 모두 스위칭", 16, G)


# 계층 스택
MX, LNX, LNW, IDX, IDW, SWX, SWW = 760, 840, 170, 1010, 130, 1150, 120
Y0, RH = 268, 64
LAYERS = [("L7 Application", "HTTP", "L7 스위치"),
          ("L4 Transport", "Port 번호", "L4 스위치"),
          ("L3 Network", "IP 주소", "L3 스위치"),
          ("L2 Data Link", "MAC 주소", "L2 스위치")]


def layer_switch(s):
    s.ctext(LNX + LNW / 2, Y0 - 24, "계층", 18, G)
    s.ctext(IDX + IDW / 2, Y0 - 24, "스위칭 기준", 18, G)
    s.ctext(SWX + SWW / 2, Y0 - 24, "스위치 종류", 18, G)
    for i, (ln, ident, sw) in enumerate(LAYERS):
        y = Y0 + i * RH
        s.rect(LNX, y, LNW, RH, W)
        s.ctext(LNX + LNW / 2, y + RH / 2, ln, 18, B)
        s.rect(IDX, y, IDW, RH, W)
        s.ctext(IDX + IDW / 2, y + RH / 2, ident, 20, W)
        box(s, SWX, y + 10, SWW, RH - 20, sw, 19, R, R)
    for y in (Y0 + RH, Y0 + 3 * RH):
        hline(s, MX, y, SWX - MX - 10, G, strokeStyle="dashed", strokeWidth=1)
    for name, a, b in [("User", Y0, Y0 + RH), ("Kernel", Y0 + RH, Y0 + 3 * RH),
                       ("H/W", Y0 + 3 * RH, Y0 + 4 * RH)]:
        s.text(MX, (a + b) / 2 - 12, name, 18, G)
    s.text(SWX - 40, Y0 + 4 * RH + 12, "L3 스위치의 대표 = Router", 18, B)
    # 가격·연산 복잡도
    ax = 1300
    s.arrow(ax, Y0 + 4 * RH, [[0, 0], [0, -4 * RH]], W, startArrowhead="arrow")
    s.text(ax + 10, Y0 - 4, "비쌈", 16, R)
    s.text(ax + 10, Y0 + 18, "연산", 14, G)
    s.text(ax + 10, Y0 + 36, "복잡", 14, G)
    s.text(ax + 10, Y0 + 4 * RH - 50, "단순", 14, G)
    s.text(ax + 10, Y0 + 4 * RH - 22, "저렴", 16, R)


def tcpip(s):
    Y = 610
    s.text(MX, Y - 34, "계층별 대표 프로토콜", 20, W)
    rows = [("L4", "TCP"), ("L3", "IP"), ("L2", "Ethernet (유선) · IEEE 802.11 (무선)")]
    for i, (l, p) in enumerate(rows):
        s.text(MX, Y + i * 32, l, 18, B)
        s.text(MX + 50, Y + i * 32, p, 18, W)
    box(s, 1150, Y - 30, 90, 80, None, stroke=W)
    s.ctext(1195, Y - 6, "TCP", 20, W)
    hline(s, 1162, Y + 10, 66, W)
    s.ctext(1195, Y + 28, "IP", 20, W)
    s.arrow(1246, Y + 10, [[0, 0], [30, 0]], G)
    s.text(1284, Y - 2, "TCP/IP", 22, B)
    # 생각해 볼 문제
    s.text(40, 720, "생각해 볼 문제: 인터넷 공유기도 스위치라고 할 수 있을까? 그렇다면 몇 계층(L?) 스위치일까?",
           18, G)


specs = [
    ("01_호스트", 280, [host]),
    ("02_엔드포인트와_스위치", 720, [host, endpoint_switch]),
    ("03_인터넷_라우터와_DNS", 720, [host, endpoint_switch, internet]),
    ("04_스위치의_목적", 720, [host, endpoint_switch, internet, purpose]),
    ("05_계층별_스위치", 720, [host, endpoint_switch, internet, purpose, layer_switch]),
    ("06_TCP_IP", 770, [host, endpoint_switch, internet, purpose, layer_switch, tcpip]),
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
