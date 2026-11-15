#!/usr/bin/env python3
"""앱 안 설명서(Markdown)를 정적 HTML 로 바꿔 `guide/` 에 쓴다.

    python build_guide.py <설명서 폴더> [--pandoc <pandoc 경로>]

- 설명서 폴더: lumiStudio 저장소의 `apps/md-studio/resources/help/ko`
- 변환은 Pandoc(gfm → html5)이 한다. 결과 HTML 을 커밋하므로 Pandoc 은 이 스크립트를 돌릴 때만 필요하다.
- 쪽 사이 링크(`03-layout.md`)는 `03-layout.html` 로 고친다. 앱이 실행 중에 만드는 「부록: 단축키」 쪽은 파일이 없어 여기에 없다.
"""
import argparse, html, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "guide"


def title_of(md: str, fallback: str) -> str:
    for line in md.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def pandoc(exe: str, md: str) -> str:
    r = subprocess.run(
        [exe, "-f", "gfm", "-t", "html5", "--no-highlight", "--wrap=none"],
        input=md.encode("utf-8"), capture_output=True, check=True,
    )
    return r.stdout.decode("utf-8")


def fix_links(body: str) -> str:
    # 쪽 사이 링크 .md → .html (바깥 주소·코드 안 글자는 건드리지 않는다: href 속성만)
    return re.sub(r'href="(\d\d-[A-Za-z0-9_-]+)\.md((?:#[^"]*)?)"', r'href="\1.html\2"', body)


def page(title: str, nav: str, body: str, prev_next: str) -> str:
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} — MDStudio 사용 설명서</title>
<meta name="description" content="MDStudio 사용 설명서: {html.escape(title)}">
<link rel="stylesheet" href="../style.css">
</head>
<body>
<header class="site"><div class="wrap">
<a class="brand" href="../">MDStudio</a>
<a href="../#features">기능</a>
<a href="01-start.html" aria-current="page">사용 설명서</a>
<a href="../privacy.html">처리방침</a>
<a href="../terms.html">이용약관</a>
</div></header>
<main><div class="wrap guide">
<nav class="toc" aria-label="설명서 목차">
{nav}
</nav>
<article>
{body}
{prev_next}
</article>
</div></main>
<footer class="site"><div class="wrap">앱 안 설명서(F1)와 같은 내용입니다. 앱 버전에 따라 화면이 조금 다를 수 있습니다. 「부록: 단축키」 쪽은 앱 안에서만 볼 수 있습니다(현재 키맵 그대로 나옵니다). · <a href="../privacy.html">개인정보 처리방침</a> · <a href="../terms.html">이용약관</a></div></footer>
</body>
</html>
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("src", type=Path)
    ap.add_argument("--pandoc", default=shutil.which("pandoc") or "pandoc")
    a = ap.parse_args()
    files = sorted(p for p in a.src.glob("*.md") if re.match(r"\d\d-", p.name))
    if not files:
        print("설명서 파일이 없다:", a.src, file=sys.stderr)
        return 1
    pages = []
    for p in files:
        md = p.read_text(encoding="utf-8")
        pages.append((p.stem, title_of(md, p.stem), md))
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.html"):
        old.unlink()
    for i, (stem, title, md) in enumerate(pages):
        nav = "<ul>\n" + "\n".join(
            f'<li><a href="{s}.html"{" aria-current=\"page\"" if s == stem else ""}>{html.escape(t)}</a></li>'
            for s, t, _ in pages
        ) + "\n</ul>"
        body = fix_links(pandoc(a.pandoc, md))
        pn = []
        if i > 0:
            pn.append(f'<a href="{pages[i-1][0]}.html">← {html.escape(pages[i-1][1])}</a>')
        if i + 1 < len(pages):
            pn.append(f'<a href="{pages[i+1][0]}.html">{html.escape(pages[i+1][1])} →</a>')
        prev_next = '<p class="pn">' + " &nbsp;·&nbsp; ".join(pn) + "</p>" if pn else ""
        (OUT / f"{stem}.html").write_text(page(title, nav, body, prev_next), encoding="utf-8", newline="\n")
    print(f"{len(pages)}쪽을 guide/ 에 썼다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
