"""4강 학습용 도식: IP 주소, IPv4 주소 길이, 8bit 표기, Network ID·Host ID, Net-mask AND 연산."""
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


# ---------- 보드 1: IP 주소와 Net-mask ----------
def ip_host(s):
    s.text(40, 28, "IP 주소와 Net-mask", 38, W)
    s.text(40, 84, "IP = Internet Protocol", 22, B)
    s.text(40, 120, "IP 주소 = Host에 대한 식별자", 24, W)
    hline(s, 40, 152, 330, R)
    # 비유 표: 행정체계 ↔ 네트워크
    CA, CB, CW = 40, 400, 280
    s.ctext(CA + CW / 2, 200, "비유: 대한민국 행정체계", 20, G)
    s.ctext(CB + CW / 2, 200, "네트워크", 20, G)
    rows = [("대한민국의 행정체계", "Network (인프라)", 230),
            ("개인 (국민)", "Host", 330),
            ("주민등록번호", "IP 주소", 430)]
    for a, b, y in rows:
        box(s, CA, y, CW, 60, a, 21, W, W)
        last = b == "IP 주소"
        box(s, CB, y, CW, 60, b, 22, R if last else B, R if last else B)
        s.arrow(CA + CW + 6, y + 30, [[0, 0], [CB - CA - CW - 12, 0]], G,
                strokeStyle="dashed", strokeWidth=1, head=None)
    for cx in (CA + CW / 2, CB + CW / 2):
        s.arrow(cx, 428, [[0, 0], [0, -36]], G)
        s.text(cx + 10, 398, "유일하게 식별", 15, G)


def ip_version(s):
    X = 760
    box(s, X, 260, 130, 64, "IP 주소", 22, B, B)
    s.arrow(X + 134, 280, [[0, 0], [50, -60]], B)
    s.arrow(X + 134, 304, [[0, 0], [50, 60]], B)
    box(s, X + 190, 190, 120, 54, "IPv4", 24, B, B)
    box(s, X + 190, 340, 120, 54, "IPv6", 24, B, B)
    s.text(X + 330, 201, "주소 길이 32bit", 26, R)
    s.text(X + 330, 351, "주소 길이 128bit", 26, R)
    hline(s, X + 330, 240, 200, R)
    hline(s, X + 330, 390, 216, R)
    s.text(X + 190, 90, "IPv4 주소의 경우의 수", 20, W)
    s.text(X + 190, 122, "2^32 = 4,294,967,296 ≈ 43억 개", 24, R)
    s.arrow(X + 250, 186, [[0, 0], [0, -26]], G)
    s.text(X, 440, "인터넷(전 세계)에 참여할 수 있는 Host 수", 20, W)
    s.text(X, 470, "→ IPv4로는 약 43억 개를 넘을 수 없음", 20, W)
    s.text(X, 512, "2022년 기준 인터넷은 IPv4가 주류", 20, B)
    s.text(X, 540, "(IPv6는 학술용 등 일부 구간에서 사용)", 16, G)


# ---------- ipconfig 확인 화면 ----------
def ipconfig(s):
    s.text(40, 28, "IP 주소 확인: 명령 프롬프트에서 ipconfig (Windows)", 30, W)
    TX, TY, TW_, TH = 40, 90, 860, 330
    s.rect(TX, TY, TW_, TH, W)
    hline(s, TX, TY + 34, TW_, W)
    s.text(TX + 14, TY + 6, "명령 프롬프트", 16, G)
    lines = [("C:\\> ipconfig", W),
             ("무선 LAN 어댑터 Wi-Fi 2:", W),
             ("   링크-로컬 IPv6 주소 . . : fe80::e446:abcd:19be:2bda%28", G),
             ("   IPv4 주소 . . . . . . . : 192.168.60.14", R),
             ("   서브넷 마스크 . . . . . : 255.255.255.0", B),
             ("   기본 게이트웨이 . . . . : 192.168.60.1", G)]
    for i, (t, c) in enumerate(lines):
        s.text(TX + 20, TY + 56 + i * 42, t, 20, c)
    NX = 950
    s.text(NX, 150, "IPv4 주소", 22, R)
    s.text(NX, 180, "192.168.60.14", 24, R)
    s.text(NX, 250, "서브넷 마스크", 22, B)
    s.text(NX, 280, "= 넷마스크(Net-mask)", 20, B)
    s.text(NX, 310, "255.255.255.0", 24, B)
    s.text(NX, 380, "IPv6 주소도 함께 표시됨", 18, G)


# ---------- 보드 2: 8bit 표기, Network ID / Host ID ----------
OX, OW, OY, OH, STEP = 100, 150, 220, 70, 200


def dotted(s):
    s.text(60, 30, "IPv4 주소: 32bit = 2^32", 32, W)
    hline(s, 60, 76, 380, R)
    for i, v in enumerate(["192", "168", "60", "14"]):
        x = OX + i * STEP
        box(s, x, OY, OW, OH, v, 34, W, W)
        s.ctext(x + OW / 2, OY + OH + 22, "8bit", 18, B)
        if i < 3:
            s.ctext(x + OW + 25, OY + OH - 14, ".", 34, B)
    s.text(OX + 3 * STEP + OW + 30, OY + 20, "점(.) 3개로 4칸 구분", 18, B)
    s.text(OX, OY + OH + 50, "한 칸의 범위: 0 ~ 255  (2^8 = 256가지 = 8bit)", 20, R)
    s.text(OX, OY + OH + 80, "8bit × 4칸 = 32bit", 20, W)
    # 오른쪽 핵심 문장
    box(s, 1010, 40, 340, 90, None, stroke=R)
    s.ctext(1180, 70, "IP 주소는 8bit씩", 24, W)
    s.ctext(1180, 102, "끊어서 표시", 24, W)
    # 192의 2진수·16진수 변환
    Y = 450
    s.text(OX, Y, "192", 30, W)
    s.arrow(OX + 64, Y + 18, [[0, 0], [60, 0]], G)
    s.text(OX + 140, Y - 26, "8 4 2 1   8 4 2 1", 18, B)
    s.text(OX + 140, Y, "1 1 0 0   0 0 0 0 (2)", 30, W)
    s.arrow(OX + 470, Y + 18, [[0, 0], [60, 0]], G)
    s.text(OX + 545, Y, "C0 (16)", 30, B)
    s.text(OX + 140, Y + 48, "1100 → 8 + 4 = 12 = C,   0000 → 0", 18, G)


def net_host(s):
    y = OY - 40
    x0, x3 = OX, OX + 2 * STEP + OW
    x4a, x4b = OX + 3 * STEP, OX + 3 * STEP + OW
    s.arrow(x0, y, [[0, 0], [x3 - x0, 0]], B, startArrowhead="arrow")
    s.arrow(x4a, y, [[0, 0], [x4b - x4a, 0]], B, startArrowhead="arrow")
    s.ctext((x0 + x3) / 2, y - 22, "Network ID (24bit)", 22, B)
    s.ctext((x4a + x4b) / 2, y - 22, "Host ID (8bit)", 22, B)
    # 길이 관계식
    Y = 580
    s.text(60, Y, "IP 주소", 28, W)
    s.text(190, Y, "=", 28, W)
    box(s, 230, Y - 10, 210, 56, "Network ID", 26, B, B)
    s.text(460, Y, "+", 28, W)
    box(s, 500, Y - 10, 180, 56, "Host ID", 26, B, B)
    s.text(60, Y + 64, "32bit", 24, W)
    s.ctext(335, Y + 76, "24bit", 24, R)
    s.ctext(590, Y + 76, "32 − 24 = 8bit", 22, W)
    s.text(230, Y + 104, "Network ID의 길이를 나타내는 것 = Net-mask", 20, R)


# ---------- 보드 3: Net-mask와 AND 연산 ----------
def netmask(s):
    LX, CX0, CW, STEP3 = 60, 300, 130, 170
    rows = [("IP 주소", ["192", "168", "60", "14"], W, 50),
            ("Net-mask", ["255", "255", "255", "0"], W, 120),
            ("Network ID", ["192", "168", "60", "0"], B, 240)]
    for label, vals, c, y in rows:
        s.text(LX, y + 10, label, 24, c)
        for i, v in enumerate(vals):
            x = CX0 + i * STEP3
            box(s, x, y, CW, 56, v, 28, c, c)
            if i < 3:
                s.ctext(x + CW + 20, y + 42, ".", 28, c)
    s.text(LX, 196, "bit AND", 20, B)
    hline(s, CX0, 214, 3 * STEP3 + CW, W)
    s.text(CX0 + 4 * STEP3 + 10, 132, "255 = 0xFF = 1111 1111", 20, G)
    s.text(CX0 + 4 * STEP3 + 10, 252, "Net-mask의 1이 24개 → 24bit", 20, B)
    # AND 계산 예시 두 개
    def calc(x, y, title, a, b, r, ad, bd, rd):
        s.text(x, y, title, 20, G)
        for i, (op, bits, dec, c) in enumerate([("", a, ad, W), ("&", b, bd, W)]):
            s.text(x, y + 34 + i * 36, op, 24, c)
            s.text(x + 34, y + 34 + i * 36, bits, 24, c)
            s.text(x + 230, y + 34 + i * 36, dec, 24, G)
        hline(s, x, y + 106, 330, W)
        s.text(x + 34, y + 116, r, 24, B)
        s.text(x + 230, y + 116, rd, 24, B)
    calc(LX, 340, "192 AND 255", "1100 0000", "1111 1111", "1100 0000", "(192)", "(255)", "→ 192")
    calc(560, 340, "14 AND 0", "0000 1110", "0000 0000", "0000 0000", "(14)", "(0)", "→ 0")
    s.text(LX, 520, "AND: 두 bit가 모두 1일 때만 1, 하나라도 0이면 0", 20, R)
    # 슬래시 표기
    box(s, LX, 580, 420, 70, "192.168.60.14/24", 34, B, B)
    s.text(LX + 450, 584, "/24 = Network ID 24bit", 22, W)
    s.text(LX + 450, 618, "→ Host ID는 32 − 24 = 8bit", 22, W)
    s.text(LX + 450, 652, "Net-mask 255.255.255.0을 줄여 쓴 표기", 18, G)


specs = [
    ("01_IP_주소와_호스트", 540, [ip_host]),
    ("02_IPv4와_IPv6", 590, [ip_host, ip_version]),
    ("03_ipconfig로_주소_확인", 460, [ipconfig]),
    ("04_8bit_단위_표기", 560, [dotted]),
    ("05_Network_ID와_Host_ID", 740, [dotted, net_host]),
    ("06_Net-mask와_AND_연산", 710, [netmask]),
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
