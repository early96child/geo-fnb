#!/usr/bin/env python3
"""store-info.json -> 매장별 원페이지(HTML + JSON-LD + FAQ).

그룹 폴더를 따로 처리한다. 그룹끼리 데이터를 섞지 않는다.
verified:false 값은 본문에 "(추정)"을 붙이고 JSON-LD에는 넣지 않는다.
"""
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TBD = "[확인 필요]"

# 필드 키 -> (표 라벨, FAQ 질문 or None)
FIELDS = {
    "address": ("주소", "주소가 어디인가요?"),
    "hours": ("영업시간", "영업시간은 어떻게 되나요?"),
    "break_time": ("브레이크타임", "브레이크타임이 있나요?"),
    "pet_friendly": ("반려견", "반려견과 같이 갈 수 있나요?"),
    "takeout_delivery": ("포장·배달", "포장이나 배달이 되나요?"),
    "parking": ("주차", "주차할 수 있나요?"),
    "reservation": ("예약", "예약할 수 있나요?"),
    "menu_highlights": ("대표 메뉴", "대표 메뉴가 뭔가요?"),
    "price_range": ("가격대", "가격대는 어느 정도인가요?"),
    "phone": ("전화", "전화번호가 어떻게 되나요?"),
    "instagram": ("인스타그램", None),
    "branch": ("지점", None),
}


def known(item):
    return item["value"] != TBD


def mark(item):
    """본문용 표기. 미확인은 (추정), 값 없음은 [확인 필요]."""
    if not known(item):
        return TBD
    return item["value"] if item["verified"] else f'{item["value"]} (추정)'


def jsonld_restaurant(store):
    d = {"@context": "https://schema.org", "@type": "Restaurant", "name": store["name"]}
    ok = lambda k: k in store and store[k]["verified"] and known(store[k])
    if ok("one_liner"):
        d["description"] = store["one_liner"]["value"]
    if ok("category"):
        d["servesCuisine"] = store["category"]["value"]
    if ok("address"):
        d["address"] = {"@type": "PostalAddress", "streetAddress": store["address"]["value"], "addressCountry": "KR"}
    if ok("phone"):
        d["telephone"] = store["phone"]["value"]
    if ok("instagram"):
        d["sameAs"] = ["https://www.instagram.com/" + store["instagram"]["value"].lstrip("@")]
    if ok("reservation"):
        d["acceptsReservations"] = "True"
    return d


def faq_items(store):
    """(질문, 화면용 답, JSON-LD용 답 or None)."""
    items = []
    if "one_liner" in store:
        a = store["one_liner"]["value"]
        items.append((f'{store["name"]}은 어떤 곳인가요?', mark(store["one_liner"]),
                      a if store["one_liner"]["verified"] else None))
    if "tone" in store:
        a = f'분위기는 "{store["tone"]["value"]}"입니다.'
        items.append(("분위기가 어떤가요?", a if store["tone"]["verified"] else a + " (추정)",
                      a if store["tone"]["verified"] else None))
    for key, (label, q) in FIELDS.items():
        if q and key in store:
            it = store[key]
            items.append((q, mark(it), it["value"] if it["verified"] and known(it) else None))
    return items


def render(store, popup):
    e = html.escape
    faqs = faq_items(store)
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": ja}}
            for q, _, ja in faqs if ja
        ],
    }
    rows = []
    for key in ("category", "tone"):
        if key in store:
            rows.append(("업종" if key == "category" else "분위기", mark(store[key])))
    for key, (label, _) in FIELDS.items():
        if key in store:
            rows.append((label, mark(store[key])))
    table = "\n".join(f"<dt>{e(l)}</dt><dd>{e(v)}</dd>" for l, v in rows)
    faq_html = "\n".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a, _ in faqs)
    popup_html = ""
    if popup:
        popup_html = (
            f'<section><h2>팝업</h2><p>\'{e(popup["name"])}\' 팝업 콜라보 ({e(popup["participants"])}).</p>'
            f'<p>날짜: {e(popup["date"]["value"])}. 후속 일정: {TBD}</p></section>'
        )
    desc = store["one_liner"]["value"]
    ld = lambda o: json.dumps(o, ensure_ascii=False, indent=2)
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(store["name"])}</title>
<meta name="description" content="{e(desc)}">
<style>
body{{font-family:system-ui,-apple-system,"Noto Sans KR",sans-serif;max-width:640px;margin:0 auto;padding:24px 16px;line-height:1.7;color:#222}}
h1{{margin-bottom:4px}} .lead{{font-size:1.1rem;color:#444}}
dl{{display:grid;grid-template-columns:7em 1fr;gap:6px 12px}} dt{{font-weight:700}} dd{{margin:0}}
details{{border-top:1px solid #ddd;padding:8px 0}} summary{{cursor:pointer;font-weight:600}}
.note{{font-size:.85rem;color:#777;margin-top:32px}}
</style>
<script type="application/ld+json">
{ld(jsonld_restaurant(store))}
</script>
<script type="application/ld+json">
{ld(faq_ld)}
</script>
</head>
<body>
<main>
<h1>{e(store["name"])}</h1>
<p class="lead">{e(desc)}</p>
<section><h2>정보</h2>
<dl>
{table}
</dl></section>
<section><h2>자주 묻는 질문</h2>
{faq_html}
</section>
{popup_html}
<p class="note">(추정)·[확인 필요] 표시는 사장님 확인 전 정보입니다.</p>
</main>
</body>
</html>
"""


def build_group(group_dir):
    info = json.loads((group_dir / "store-info.json").read_text(encoding="utf-8"))
    popup = info.get("popup")
    for store in info["stores"]:
        out = group_dir / "output" / "site" / store["id"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        mine = popup if popup and store["name"] in popup["participants"] else None
        out.write_text(render(store, mine), encoding="utf-8")
        print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    for g in sorted((ROOT / "stores").iterdir()):
        if (g / "store-info.json").exists():
            build_group(g)
