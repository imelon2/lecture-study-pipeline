"""6강 학습용 도식: Layer와 Layered 구조 (요소·관계 → 의존 → 전제 조건)."""
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1]))
from excalidraw_scene import Scene, save, frame_origin, W, B, R

G = "#9ca3af"  # 보조 설명(회색)
ROUND = {"type": 3}

# ---------- 공통 격자 ----------
ST_X, ST_W, ROW_H, ROW_GAP, TOP = 110, 260, 60, 10, 110     # 계층(스택) 그림
ZX = (440, 590)                                              # 직렬 그림 열
ZY = (110, 260)                                              # 직렬 그림 행
ZW, ZH = 110, 120
NOTE_X = 760                                                 # 오른쪽 설명 열
PANEL_X, PANEL_W, HALF_W = 70, 1040, 500


def row_y(n):
    """n층(1~4) 칸의 위쪽 y좌표."""
    return TOP + (4 - n) * (ROW_H + ROW_GAP)


def stage_figures(s):
    s.text(40, 30, "Layer와 Layered 구조", 28, W)
    # 계층 표현: 4 / 3 / 2 / 1
    for n in (4, 3, 2, 1):
        s.rect(ST_X, row_y(n), ST_W, ROW_H, W, roundness=ROUND)
        s.ctext(ST_X + 70, row_y(n) + ROW_H / 2, str(n), 24, W)
    s.ctext(ST_X + ST_W / 2, 404, "계층(Layered) 표현", 17, G)
    # 직렬 표현: 4 → 3 → 2 → 1
    pos = {4: (ZX[0], ZY[0]), 3: (ZX[1], ZY[0]), 2: (ZX[0], ZY[1]), 1: (ZX[1], ZY[1])}
    for n, (x, y) in pos.items():
        s.rect(x, y, ZW, ZH, W, roundness=ROUND)
        s.ctext(x + ZW / 2, y + ZH / 2, str(n), 24, W)
    gap = ZX[1] - ZX[0] - ZW
    for y in ZY:
        s.arrow(ZX[0] + ZW + 4, y + ZH / 2, [[0, 0], [gap - 8, 0]], W,
                strokeStyle="dashed", strokeWidth=1)
    mid_y = (ZY[0] + ZH + ZY[1]) / 2
    s.arrow(ZX[1] + ZW / 2, ZY[0] + ZH + 4,
            [[0, 0], [0, mid_y - ZY[0] - ZH - 4], [-(ZX[1] - ZX[0]), mid_y - ZY[0] - ZH - 4],
             [-(ZX[1] - ZX[0]), ZY[1] - ZY[0] - ZH - 8]], W,
            strokeStyle="dashed", strokeWidth=1)["roundness"] = None   # 꺾은선은 직각으로
    s.ctext((ZX[0] + ZX[1] + ZW) / 2, 404, "직렬(한 줄) 표현", 17, G)


def stage_design(s):
    notes = [("요소 (Element)", "시스템을 이루는 구성 단위", B, 106),
             ("관계 (Relation)", "요소와 요소 사이의 연결", R, 216),
             ("도식 (Diagram)", "요소 간의 관계를 표현한 그림", B, 326)]
    for title, sub, color, y in notes:
        s.text(NOTE_X, y, title, 24, color)
        s.text(NOTE_X, y + 36, sub, 17, G)
    for y in (176, 286):
        s.arrow(NOTE_X + 24, y, [[0, 0], [0, 30]], G, strokeWidth=1)
    s.rect(PANEL_X, 450, PANEL_W, 66, B, roundness=ROUND)
    s.ctext(PANEL_X + PANEL_W / 2, 483, "설계 = 목표 시스템을 이루는 요소 정의 + 요소 간 관계 규정", 22, B)


def stage_dependency(s):
    for n, name in ((4, "학사"), (3, "고등"), (2, "중등"), (1, "초등")):
        s.ctext(ST_X + 180, row_y(n) + ROW_H / 2, name, 19, B)
    # 4층 → 3층 의존
    y4, y3 = row_y(4) + ROW_H / 2, row_y(3) + ROW_H / 2
    s.arrow(ST_X - 10, y4, [[0, 0], [-24, (y3 - y4) / 2], [0, y3 - y4]], R)
    s.text(28, (y4 + y3) / 2 - 12, "의존", 19, R)
    # 위층에서 아래층으로 이어지는 의존 방향
    s.arrow(ST_X + ST_W + 22, TOP, [[0, 0], [0, row_y(1) + ROW_H - TOP]], B)
    # 의존의 범위
    s.text(PANEL_X, 546, "의존의 범위", 24, W)
    s.rect(PANEL_X, 590, HALF_W, 120, W, roundness=ROUND)
    s.text(PANEL_X + 24, 606, "행위·기능에 한정된 의존", 21, W)
    s.text(PANEL_X + 24, 644, "특정 행위나 기능에 대해서만 기댐", 16, G)
    s.text(PANEL_X + 24, 670, "예: 출근(행위) → 지하철", 16, G)
    bx = PANEL_X + PANEL_W - HALF_W
    s.rect(bx, 590, HALF_W, 120, R, roundness=ROUND, strokeWidth=3)
    s.text(bx + 24, 606, "존립에 대한 의존", 21, R)
    s.text(bx + 24, 644, "아래층이 없으면 위층이 성립하지 않음", 16, W)
    s.text(bx + 24, 670, "예: 학사 → 고등 → 중등 → 초등 교육", 16, G)


def stage_precondition(s):
    # 직렬 그림에서 4와 3의 관계 강조
    s.rect(ZX[0] - 6, ZY[0] - 6, ZW + 12, ZH + 12, B, roundness=ROUND, strokeWidth=1)
    s.rect(ZX[1] - 6, ZY[0] - 6, ZW + 12, ZH + 12, R, roundness=ROUND, strokeWidth=1)
    s.ctext(ZX[1] + ZW / 2, 86, "4의 전제 조건", 16, R)
    s.text(PANEL_X, 740, "전제 조건", 24, W)
    s.rect(PANEL_X, 784, HALF_W, 100, W, roundness=ROUND)
    s.text(PANEL_X + 24, 800, "4는 3을 전제한다", 21, W)
    s.text(PANEL_X + 24, 838, "= 3은 4의 전제 조건", 21, R)
    bx = PANEL_X + PANEL_W - HALF_W
    s.arrow(PANEL_X + HALF_W + 6, 834, [[0, 0], [bx - PANEL_X - HALF_W - 12, 0]], G)
    s.rect(bx, 784, HALF_W, 100, B, roundness=ROUND)
    s.text(bx + 24, 800, "전제 관계의 직렬화 = Layered 구조", 21, B)
    s.text(bx + 24, 838, "대표 사례: OSI 7 Layer", 21, R)


specs = [
    ("01_요소와_관계", 560, [stage_figures, stage_design]),
    ("02_계층과_의존", 750, [stage_figures, stage_design, stage_dependency]),
    ("03_전제_조건과_OSI", 920, [stage_figures, stage_design, stage_dependency, stage_precondition]),
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
