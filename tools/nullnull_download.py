"""널널한 개발자 공식 사이트(HLS) 강의의 영상과 자막을 받습니다.

사용법:
    python3 tools/nullnull_download.py '<m3u8 URL>' [--name 이름] [--lang ko] [--model 경로] [--out data]

결과: <out>/<번호>_<이름>/lecture.mp4, lecture.srt
서명 URL(Policy·Signature)은 로그에 출력하지 않습니다.
"""
import argparse, base64, json, pathlib, re, shutil, subprocess, sys, tempfile, time
import urllib.error, urllib.parse, urllib.request

DEFAULT_MODEL = pathlib.Path.home() / ".cache/whisper-cpp/ggml-large-v3-turbo-q5_0.bin"
UA = {"User-Agent": "Mozilla/5.0"}


def die(msg):
    print(f"오류: {msg}", file=sys.stderr)
    sys.exit(1)


def log(msg):
    print(f"==> {msg}", flush=True)


def policy_expiry(query):
    """CloudFront Policy의 만료 시각(epoch)을 읽습니다. 없으면 None."""
    pol = urllib.parse.parse_qs(query).get("Policy", [None])[0]
    if not pol:
        return None
    raw = pol.replace("-", "+").replace("_", "=").replace("~", "/")
    try:
        doc = json.loads(base64.b64decode(raw))
        return doc["Statement"][0]["Condition"]["DateLessThan"]["AWS:EpochTime"]
    except Exception:
        return None


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        die(f"재생목록 요청 실패 (HTTP {e.code}). URL이 만료됐거나 잘못 복사됐을 수 있습니다.")
    except urllib.error.URLError as e:
        die(f"네트워크 오류: {e.reason}")


def sign(url, query):
    return url if "?" in url else f"{url}?{query}"


def load_playlist(url, query):
    """미디어 재생목록을 받아 (텍스트, 기준 URL)을 돌려줍니다. 마스터 목록이면 최고 화질을 고릅니다."""
    text = fetch(sign(url, query))
    if not text.startswith("#EXTM3U"):
        head = text.strip().splitlines()[0][:120] if text.strip() else "(빈 응답)"
        die(f"재생목록이 아닌 응답을 받았습니다: {head}")
    if "#EXT-X-STREAM-INF" in text:
        lines = text.splitlines()
        best, bw = None, -1
        for i, l in enumerate(lines):
            m = re.search(r"BANDWIDTH=(\d+)", l)
            if l.startswith("#EXT-X-STREAM-INF") and m and int(m.group(1)) > bw:
                bw, best = int(m.group(1)), lines[i + 1].strip()
        if not best:
            die("마스터 재생목록에서 화질 목록을 찾지 못했습니다.")
        url = urllib.parse.urljoin(url, best)
        return load_playlist(url.split("?")[0], query)
    return text, url


def signed_playlist(text, base_url, query):
    if "#EXT-X-KEY" in text:
        die("암호화된 영상(#EXT-X-KEY)이라 받을 수 없습니다.")
    out = []
    for l in text.splitlines():
        s = l.strip()
        if s and not s.startswith("#"):
            s = sign(urllib.parse.urljoin(base_url, s), query)
            out.append(s)
        else:
            out.append(l)
    n = sum(1 for l in out if l and not l.startswith("#"))
    if n == 0:
        die("재생목록에 영상 조각이 없습니다.")
    return "\n".join(out) + "\n", n


def run(cmd, what):
    r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if r.returncode != 0:
        # ffmpeg 오류에는 서명 URL이 들어 있으므로 쿼리를 가립니다.
        err = re.sub(r"\?Policy=[^\s'\"]+", "?<서명 생략>", r.stderr.strip())
        die(f"{what} 실패:\n" + "\n".join(err.splitlines()[-8:]))


def next_dir(out_root, name):
    out_root.mkdir(parents=True, exist_ok=True)
    nums = [int(m.group(1)) for p in out_root.iterdir()
            if p.is_dir() and (m := re.match(r"(\d+)_", p.name))]
    return out_root / f"{max(nums, default=0) + 1}_{name}"


def main():
    ap = argparse.ArgumentParser(description="널널한 개발자 강의 영상·자막 받기")
    ap.add_argument("url", help="개발자도구에서 복사한 m3u8 URL 전체")
    ap.add_argument("--name", help="폴더 이름 (기본: URL의 영상 번호)")
    ap.add_argument("--lang", default="ko", help="자막 언어 (기본: ko)")
    ap.add_argument("--model", default=str(DEFAULT_MODEL), help="whisper.cpp 모델 파일")
    ap.add_argument("--out", default="data", help="결과를 저장할 상위 폴더 (기본: data)")
    a = ap.parse_args()

    u = urllib.parse.urlsplit(a.url.strip())
    if u.scheme != "https" or not u.path.endswith(".m3u8"):
        die("https로 시작하는 .m3u8 URL을 넣어 주세요.")
    if not u.query:
        die("URL에 서명(?Policy=...&Signature=...)이 없습니다. URL 전체를 복사해 주세요.")
    exp = policy_expiry(u.query)
    if exp and exp < time.time():
        die(f"URL이 만료됐습니다 ({time.strftime('%Y-%m-%d %H:%M', time.localtime(exp))}). 다시 복사해 주세요.")

    for tool in ("ffmpeg", "whisper-cli"):
        if not shutil.which(tool):
            die(f"{tool}가 없습니다. 먼저 설치해 주세요.")
    model = pathlib.Path(a.model).expanduser()
    if not model.is_file():
        die(f"모델 파일이 없습니다: {model}\nREADME의 사전 준비를 확인해 주세요.")

    m = re.search(r"/videos/([^/]+)/", u.path)
    name = a.name or (m.group(1) if m else "lecture")
    name = re.sub(r"[\\/:*?\"<>|\s]+", "_", name).strip("_") or "lecture"

    page_url = urllib.parse.urlunsplit((u.scheme, u.netloc, u.path, "", ""))
    with tempfile.TemporaryDirectory(prefix="nullnull_") as tmp:
        tmp = pathlib.Path(tmp)
        log("재생목록 받는 중")
        text, base = load_playlist(page_url, u.query)
        signed, n = signed_playlist(text, base, u.query)
        (tmp / "signed.m3u8").write_text(signed)

        log(f"영상 받는 중 (조각 {n}개)")
        run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error",
             "-protocol_whitelist", "file,https,tcp,tls,crypto",
             "-allowed_extensions", "ALL", "-extension_picky", "0",
             "-i", str(tmp / "signed.m3u8"), "-c", "copy", str(tmp / "lecture.mp4")], "영상 병합")

        log("음성 변환 중")
        run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", str(tmp / "lecture.mp4"),
             "-ar", "16000", "-ac", "1", str(tmp / "a.wav")], "음성 변환")

        log("자막 만드는 중 (whisper)")
        run(["whisper-cli", "-m", str(model), "-l", a.lang, "-f", str(tmp / "a.wav"),
             "-osrt", "-of", str(tmp / "lecture")], "자막 생성")
        if not (tmp / "lecture.srt").is_file():
            die("자막 파일이 만들어지지 않았습니다.")

        dest = next_dir(pathlib.Path(a.out), name)
        dest.mkdir()
        for f in ("lecture.mp4", "lecture.srt"):
            shutil.move(str(tmp / f), dest / f)

    log(f"완료: {dest}/lecture.mp4, {dest}/lecture.srt")


if __name__ == "__main__":
    main()
