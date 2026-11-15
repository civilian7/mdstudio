# MDStudio 소개 페이지

MDStudio(Markdown 편집기)의 소개·개인정보 처리방침·이용약관을 담은 **정적 페이지**입니다. 빌드 도구가 없고 파일 그대로 올립니다.

| 파일 | 내용 |
|---|---|
| `index.html` | 소개 |
| `privacy.html` | 개인정보 처리방침 (Microsoft Store 제출 시 이 주소를 입력) |
| `terms.html` | 이용약관 (앱의 `resources/legal/terms-ko.html` 과 같은 본문) |
| `guide/` | 사용 설명서 16쪽(앱 안 설명서 F1 과 같은 내용). `build_guide.py` 가 만든 결과이므로 직접 고치지 않는다 |
| `build_guide.py` | 설명서 Markdown → `guide/*.html` 변환 스크립트 |
| `style.css` | 공통 스타일(밝게·어둡게 자동) |
| `.nojekyll` | GitHub Pages 가 파일을 그대로 서비스하게 함 |

## 사용 설명서 다시 만들기

설명서 원본은 lumiStudio 저장소의 `apps/md-studio/resources/help/ko/*.md` 입니다. 원본이 바뀌면 다시 만들어 `guide/` 를 같이 커밋합니다.
Pandoc(3.x)이 필요합니다(스크립트를 돌릴 때만 — 올린 페이지에는 필요 없습니다).

    python build_guide.py E:\works\PROJECTS\lumiStudiopps\md-studioesources\help\ko --pandoc <pandoc.exe 경로>

쪽 사이 링크(`02-layout.md`)는 `.html` 로 고쳐 씁니다. 「부록: 단축키」 쪽은 앱이 실행 중에 만들어 파일이 없으므로 웹에는 없습니다.

## 올리기 전에 채울 자리

노란 배경 `[대괄호]` 자리가 남아 있으면 안 됩니다.

- `[시행일]` — `privacy.html`, `terms.html`
- `[게시자 이름]` — 세 페이지 모두(아래 footer 포함), `privacy.html` 머리
- `[연락처 이메일]` — `index.html`, `privacy.html`, `terms.html`

남은 자리 찾기(아무것도 안 나와야 합니다):

    grep -n "class=\"todo\"" *.html

## GitHub Pages 로 올리기

1. GitHub 에서 **공개** 저장소 `mdstudio` 를 만듭니다(비공개 저장소는 무료 Pages 가 안 됩니다).
2. 이 폴더의 파일을 `main` 브랜치 맨 위에 올립니다.
3. 저장소 **Settings > Pages > Build and deployment** 에서 Source 를 *Deploy from a branch*, Branch 를 `main` / `/ (root)` 로 저장합니다.
4. 몇 분 뒤 `https://<GitHub 사용자>.github.io/mdstudio/` 로 열립니다. 처리방침 주소는 `.../mdstudio/privacy.html`.

## 올린 뒤 앱 쪽

- 앱 `src/ext/help.rs` 의 `HOMEPAGE_URL` 을 실제 주소로 바꿉니다.
- 앱 `resources/legal/terms-ko.html`·`terms-en.html` 제14조(문의)와 이 폴더의 `terms.html` 을 맞춥니다(앱 쪽은 아직 `fullbit.co.kr` 을 문의처로 적고 있습니다).
- 처리방침이 바뀌면 `docs/95-mdstudio-privacy-draft.md`(lumiStudio 저장소)와 `privacy.html` 을 같이 고칩니다.
