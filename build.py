#!/usr/bin/env python3
"""의왕 출장마사지 88마사지 — 정적 사이트 빌드 스크립트.

content/ 패키지의 페이지 정의를 읽어 정적 HTML을 생성한다.

규칙(자동 적용):
  - 본문 텍스트 2,000자 미만 페이지는 robots noindex 처리
  - sitemap.xml 에는 index 허용 페이지만 포함
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content import PAGES
from content.site import BASE_URL, BRAND, NAV, PHONE, PHONE_DISPLAY, TELEGRAM

ROOT = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = ROOT
MIN_INDEX_CHARS = 2000


def text_length(body_html: str) -> int:
    text = re.sub(r'<section class="pricing">.*?</section>', " ", body_html, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text)


def render_nav(current_path: str) -> str:
    items = []
    for label, href, children in NAV:
        active = " is-active" if href == "/" + current_path else ""
        if children:
            sub = "".join(
                f'<li><a href="{c_href}">{c_label}</a></li>'
                for c_label, c_href in children
            )
            items.append(
                f'<li class="nav-item has-sub{active}">'
                f'<a href="{href}">{label}</a>'
                f'<ul class="sub-menu">{sub}</ul></li>'
            )
        else:
            items.append(
                f'<li class="nav-item{active}"><a href="{href}">{label}</a></li>'
            )
    return "".join(items)


def render_breadcrumb(crumbs) -> str:
    if not crumbs:
        return ""
    parts = ['<nav class="breadcrumb" aria-label="현재 위치"><ol>']
    parts.append('<li><a href="/gyeonggi/uiwang/">의왕 홈</a></li>')
    for label, href in crumbs:
        if href:
            parts.append(f'<li><a href="{href}">{label}</a></li>')
        else:
            parts.append(f"<li><span>{label}</span></li>")
    parts.append("</ol></nav>")
    return "".join(parts)


def inject_toc(body: str):
    items = []
    counter = [0]

    def repl(m):
        attrs, title = m.group(1), m.group(2)
        idm = re.search(r'id="([^"]+)"', attrs)
        if idm:
            sid = idm.group(1)
            opening = f"<section{attrs}>"
        else:
            counter[0] += 1
            sid = f"sec-{counter[0]}"
            opening = f'<section id="{sid}"{attrs}>'
        label = re.sub(r"<[^>]+>", "", title).strip()
        items.append((sid, label))
        return f"{opening}<h2>{title}</h2>"

    body = re.sub(r"<section([^>]*)>\s*<h2>(.*?)</h2>", repl, body, flags=re.S)
    return body, items


def render_toc(items) -> str:
    if len(items) < 3:
        return ""
    links = "".join(
        f'<li><a href="#{sid}">{label}</a></li>' for sid, label in items
    )
    return (
        '<aside class="page-toc"><nav aria-label="페이지 목차">'
        '<p class="toc-title">목차</p>'
        f"<ul>{links}</ul></nav></aside>"
    )


def _ld(obj: dict) -> str:
    return (
        '<script type="application/ld+json">\n'
        + json.dumps(obj, ensure_ascii=False, indent=2)
        + "\n</script>\n"
    )


def make_org_schema() -> dict:
    base = BASE_URL.rstrip("/")
    return {
        "@context": "https://schema.org",
        "@type": ["LocalBusiness", "HealthAndBeautyBusiness"],
        "@id": base + "/#organization",
        "name": BRAND,
        "url": base + "/gyeonggi/uiwang/",
        "logo": base + "/assets/apple-touch-icon.png",
        "image": base + "/assets/og-image.png",
        "telephone": PHONE,
        "priceRange": "₩₩",
        "areaServed": {"@type": "AdministrativeArea", "name": "경기도 의왕시"},
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.9",
            "reviewCount": "187",
            "bestRating": "5",
            "worstRating": "1",
        },
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": PHONE,
            "contactType": "reservations",
            "availableLanguage": ["ko"],
            "areaServed": "KR",
        },
    }


# ── 롱테일 내부링크 ────────────────────────────────────────────────────────────

_LONGTAIL = {
    "/gyeonggi/uiwang/":                                       "의왕 전지역 출장마사지·홈타이 예약 및 생활권별 방문 기준",
    "/gyeonggi/uiwang/gocheon-dong/":                          "고천동 출장마사지·홈타이 예약 방법과 이동 가능 지역",
    "/gyeonggi/uiwang/wanggok-dong/":                          "왕곡동 출장마사지·홈타이 당일 예약 및 방문 기준 안내",
    "/gyeonggi/uiwang/ojeon-dong/":                            "오전동 출장마사지·홈타이 예약 시 확인해야 할 이동 기준",
    "/gyeonggi/uiwang/bugok-dong/":                            "부곡동 출장마사지·홈타이 아파트 단지 방문 및 예약 안내",
    "/gyeonggi/uiwang/sam-dong/":                              "삼동 출장마사지·홈타이 의왕역 인근 예약 가능 지역",
    "/gyeonggi/uiwang/i-dong/":                                "이동 출장마사지·홈타이 방문 기준 및 추가 이동비 안내",
    "/gyeonggi/uiwang/woram-dong/":                            "월암동 출장마사지·홈타이 예약 전 방문 가능 주소 확인",
    "/gyeonggi/uiwang/chopyeong-dong/":                        "초평동 출장마사지·홈타이 수원 인접 지역 방문 기준",
    "/gyeonggi/uiwang/naeson-dong/":                           "내손동 출장마사지·홈타이 평촌 인접 예약 및 방문 안내",
    "/gyeonggi/uiwang/poil-dong/":                             "포일동 출장마사지·홈타이 인덕원역 인근 예약 방법",
    "/gyeonggi/uiwang/cheonggye-dong/":                        "청계동 출장마사지·홈타이 백운밸리 인근 방문 기준",
    "/gyeonggi/uiwang/hagui-dong/":                            "학의동 출장마사지·홈타이 청계·백운밸리 생활권 예약",
    "/gyeonggi/uiwang/baegun-valley/":                         "백운밸리 출장마사지·홈타이 청계동 인접 방문 안내",
    "/gyeonggi/uiwang/station/uiwang-station/":                "의왕역 인근 출장마사지·홈타이 당일 예약 가능 여부",
    "/gyeonggi/uiwang/station/indeogwon-nearby-area/":         "인덕원역 인접 출장마사지·홈타이 이동 기준 및 예약",
    "/gyeonggi/uiwang/station/pyeongchon-nearby-area/":        "평촌역 인접 의왕 출장마사지·홈타이 예약 방법",
    "/gyeonggi/uiwang/station/beomgye-nearby-area/":           "범계역 인접 의왕 출장마사지·홈타이 방문 기준",
    "/gyeonggi/uiwang/station/gunpo-nearby-area/":             "군포역 인접 의왕 출장마사지·홈타이 이동 가능 지역",
    "/gyeonggi/uiwang/station/dangjeong-nearby-area/":         "당정역 인접 의왕 출장마사지·홈타이 예약 및 방문",
    "/gyeonggi/uiwang/station/sungkyunkwan-univ-nearby-area/": "성균관대역 인접 의왕 출장마사지·홈타이 이동 기준",
    "/gyeonggi/uiwang/area/uiwang-station-bugok/":             "의왕역·부곡 생활권 출장마사지·홈타이 방문 조건",
    "/gyeonggi/uiwang/area/gocheon-wanggok/":                  "고천·왕곡 생활권 출장마사지·홈타이 예약 가능 지역",
    "/gyeonggi/uiwang/area/ojeon-dong/":                       "오전동 생활권 출장마사지·홈타이 이동 기준 상세 안내",
    "/gyeonggi/uiwang/area/naeson-poil/":                      "내손·포일 생활권 출장마사지·홈타이 평촌 인접 예약",
    "/gyeonggi/uiwang/area/cheonggye-hagui/":                  "청계·학의 생활권 출장마사지·홈타이 방문 조건 확인",
    "/gyeonggi/uiwang/area/baegun-valley/":                    "백운밸리 생활권 출장마사지·홈타이 청계 인접 예약",
    "/gyeonggi/uiwang/area/bugok-sam-dong/":                   "부곡·삼동 생활권 출장마사지·홈타이 의왕역 근처 예약",
    "/gyeonggi/uiwang/area/woram-chopyeong/":                  "월암·초평 생활권 출장마사지·홈타이 방문 가능 기준",
    "/gyeonggi/uiwang/area/i-dong-obong/":                     "이동·오봉 인접 생활권 출장마사지·홈타이 이동비 안내",
    "/gyeonggi/uiwang/area/indeogwon-cheonggye-nearby/":       "인덕원·청계 인접 출장마사지·홈타이 예약 조건",
    "/gyeonggi/uiwang/area/pyeongchon-naeson-nearby/":         "평촌·내손 인접 출장마사지·홈타이 방문 기준 안내",
    "/gyeonggi/uiwang/area/gunpo-bugok-nearby/":               "군포·부곡 인접 출장마사지·홈타이 이동비 및 예약",
    "/gyeonggi/uiwang/reservation/":                           "의왕 출장마사지·홈타이 24시간 예약 방법 및 절차",
    "/gyeonggi/uiwang/check/":                                 "의왕 출장마사지·홈타이 예약 전 필수 확인사항",
    "/gyeonggi/uiwang/guide/":                                 "의왕 홈타이 서비스 이용 가이드 및 준비사항",
    "/gyeonggi/uiwang/support/":                               "의왕 출장마사지 88마사지 고객센터 문의",
    "/gyeonggi/uiwang/support/privacy/":                       "88마사지 개인정보처리방침 확인",
}

_RELATED = {
    "gyeonggi/uiwang/": [
        "/gyeonggi/uiwang/station/uiwang-station/",
        "/gyeonggi/uiwang/area/uiwang-station-bugok/",
        "/gyeonggi/uiwang/area/gocheon-wanggok/",
        "/gyeonggi/uiwang/naeson-dong/",
        "/gyeonggi/uiwang/reservation/",
    ],
    "gyeonggi/uiwang/gocheon-dong/": [
        "/gyeonggi/uiwang/wanggok-dong/",
        "/gyeonggi/uiwang/ojeon-dong/",
        "/gyeonggi/uiwang/area/gocheon-wanggok/",
        "/gyeonggi/uiwang/station/uiwang-station/",
        "/gyeonggi/uiwang/reservation/",
    ],
    "gyeonggi/uiwang/wanggok-dong/": [
        "/gyeonggi/uiwang/gocheon-dong/",
        "/gyeonggi/uiwang/ojeon-dong/",
        "/gyeonggi/uiwang/area/gocheon-wanggok/",
        "/gyeonggi/uiwang/station/dangjeong-nearby-area/",
        "/gyeonggi/uiwang/reservation/",
    ],
    "gyeonggi/uiwang/ojeon-dong/": [
        "/gyeonggi/uiwang/gocheon-dong/",
        "/gyeonggi/uiwang/naeson-dong/",
        "/gyeonggi/uiwang/area/ojeon-dong/",
        "/gyeonggi/uiwang/station/beomgye-nearby-area/",
        "/gyeonggi/uiwang/check/",
    ],
    "gyeonggi/uiwang/bugok-dong/": [
        "/gyeonggi/uiwang/sam-dong/",
        "/gyeonggi/uiwang/gocheon-dong/",
        "/gyeonggi/uiwang/area/uiwang-station-bugok/",
        "/gyeonggi/uiwang/station/uiwang-station/",
        "/gyeonggi/uiwang/reservation/",
    ],
    "gyeonggi/uiwang/sam-dong/": [
        "/gyeonggi/uiwang/bugok-dong/",
        "/gyeonggi/uiwang/i-dong/",
        "/gyeonggi/uiwang/area/bugok-sam-dong/",
        "/gyeonggi/uiwang/station/uiwang-station/",
        "/gyeonggi/uiwang/reservation/",
    ],
    "gyeonggi/uiwang/i-dong/": [
        "/gyeonggi/uiwang/sam-dong/",
        "/gyeonggi/uiwang/woram-dong/",
        "/gyeonggi/uiwang/area/i-dong-obong/",
        "/gyeonggi/uiwang/station/uiwang-station/",
        "/gyeonggi/uiwang/check/",
    ],
    "gyeonggi/uiwang/woram-dong/": [
        "/gyeonggi/uiwang/chopyeong-dong/",
        "/gyeonggi/uiwang/i-dong/",
        "/gyeonggi/uiwang/area/woram-chopyeong/",
        "/gyeonggi/uiwang/station/sungkyunkwan-univ-nearby-area/",
        "/gyeonggi/uiwang/check/",
    ],
    "gyeonggi/uiwang/chopyeong-dong/": [
        "/gyeonggi/uiwang/woram-dong/",
        "/gyeonggi/uiwang/area/woram-chopyeong/",
        "/gyeonggi/uiwang/station/sungkyunkwan-univ-nearby-area/",
        "/gyeonggi/uiwang/check/",
        "/gyeonggi/uiwang/reservation/",
    ],
    "gyeonggi/uiwang/naeson-dong/": [
        "/gyeonggi/uiwang/poil-dong/",
        "/gyeonggi/uiwang/ojeon-dong/",
        "/gyeonggi/uiwang/area/naeson-poil/",
        "/gyeonggi/uiwang/station/pyeongchon-nearby-area/",
        "/gyeonggi/uiwang/reservation/",
    ],
    "gyeonggi/uiwang/poil-dong/": [
        "/gyeonggi/uiwang/naeson-dong/",
        "/gyeonggi/uiwang/cheonggye-dong/",
        "/gyeonggi/uiwang/area/naeson-poil/",
        "/gyeonggi/uiwang/station/indeogwon-nearby-area/",
        "/gyeonggi/uiwang/reservation/",
    ],
    "gyeonggi/uiwang/cheonggye-dong/": [
        "/gyeonggi/uiwang/hagui-dong/",
        "/gyeonggi/uiwang/baegun-valley/",
        "/gyeonggi/uiwang/area/cheonggye-hagui/",
        "/gyeonggi/uiwang/station/indeogwon-nearby-area/",
        "/gyeonggi/uiwang/check/",
    ],
    "gyeonggi/uiwang/hagui-dong/": [
        "/gyeonggi/uiwang/cheonggye-dong/",
        "/gyeonggi/uiwang/baegun-valley/",
        "/gyeonggi/uiwang/area/cheonggye-hagui/",
        "/gyeonggi/uiwang/station/indeogwon-nearby-area/",
        "/gyeonggi/uiwang/check/",
    ],
    "gyeonggi/uiwang/baegun-valley/": [
        "/gyeonggi/uiwang/cheonggye-dong/",
        "/gyeonggi/uiwang/hagui-dong/",
        "/gyeonggi/uiwang/area/baegun-valley/",
        "/gyeonggi/uiwang/check/",
        "/gyeonggi/uiwang/reservation/",
    ],
    "gyeonggi/uiwang/station/uiwang-station/": [
        "/gyeonggi/uiwang/bugok-dong/",
        "/gyeonggi/uiwang/sam-dong/",
        "/gyeonggi/uiwang/area/uiwang-station-bugok/",
        "/gyeonggi/uiwang/area/bugok-sam-dong/",
        "/gyeonggi/uiwang/reservation/",
    ],
    "gyeonggi/uiwang/station/indeogwon-nearby-area/": [
        "/gyeonggi/uiwang/poil-dong/",
        "/gyeonggi/uiwang/cheonggye-dong/",
        "/gyeonggi/uiwang/area/indeogwon-cheonggye-nearby/",
        "/gyeonggi/uiwang/area/naeson-poil/",
        "/gyeonggi/uiwang/reservation/",
    ],
    "gyeonggi/uiwang/station/pyeongchon-nearby-area/": [
        "/gyeonggi/uiwang/naeson-dong/",
        "/gyeonggi/uiwang/ojeon-dong/",
        "/gyeonggi/uiwang/area/pyeongchon-naeson-nearby/",
        "/gyeonggi/uiwang/area/ojeon-dong/",
        "/gyeonggi/uiwang/reservation/",
    ],
    "gyeonggi/uiwang/station/beomgye-nearby-area/": [
        "/gyeonggi/uiwang/ojeon-dong/",
        "/gyeonggi/uiwang/naeson-dong/",
        "/gyeonggi/uiwang/area/ojeon-dong/",
        "/gyeonggi/uiwang/station/pyeongchon-nearby-area/",
        "/gyeonggi/uiwang/reservation/",
    ],
    "gyeonggi/uiwang/station/gunpo-nearby-area/": [
        "/gyeonggi/uiwang/bugok-dong/",
        "/gyeonggi/uiwang/gocheon-dong/",
        "/gyeonggi/uiwang/area/gunpo-bugok-nearby/",
        "/gyeonggi/uiwang/station/uiwang-station/",
        "/gyeonggi/uiwang/reservation/",
    ],
    "gyeonggi/uiwang/station/dangjeong-nearby-area/": [
        "/gyeonggi/uiwang/bugok-dong/",
        "/gyeonggi/uiwang/wanggok-dong/",
        "/gyeonggi/uiwang/area/uiwang-station-bugok/",
        "/gyeonggi/uiwang/station/uiwang-station/",
        "/gyeonggi/uiwang/reservation/",
    ],
    "gyeonggi/uiwang/station/sungkyunkwan-univ-nearby-area/": [
        "/gyeonggi/uiwang/woram-dong/",
        "/gyeonggi/uiwang/chopyeong-dong/",
        "/gyeonggi/uiwang/area/woram-chopyeong/",
        "/gyeonggi/uiwang/check/",
        "/gyeonggi/uiwang/reservation/",
    ],
    "gyeonggi/uiwang/area/uiwang-station-bugok/": [
        "/gyeonggi/uiwang/bugok-dong/",
        "/gyeonggi/uiwang/sam-dong/",
        "/gyeonggi/uiwang/station/uiwang-station/",
        "/gyeonggi/uiwang/area/bugok-sam-dong/",
        "/gyeonggi/uiwang/reservation/",
    ],
    "gyeonggi/uiwang/area/gocheon-wanggok/": [
        "/gyeonggi/uiwang/gocheon-dong/",
        "/gyeonggi/uiwang/wanggok-dong/",
        "/gyeonggi/uiwang/station/uiwang-station/",
        "/gyeonggi/uiwang/area/ojeon-dong/",
        "/gyeonggi/uiwang/reservation/",
    ],
    "gyeonggi/uiwang/area/ojeon-dong/": [
        "/gyeonggi/uiwang/ojeon-dong/",
        "/gyeonggi/uiwang/area/gocheon-wanggok/",
        "/gyeonggi/uiwang/station/beomgye-nearby-area/",
        "/gyeonggi/uiwang/station/pyeongchon-nearby-area/",
        "/gyeonggi/uiwang/check/",
    ],
    "gyeonggi/uiwang/area/naeson-poil/": [
        "/gyeonggi/uiwang/naeson-dong/",
        "/gyeonggi/uiwang/poil-dong/",
        "/gyeonggi/uiwang/station/indeogwon-nearby-area/",
        "/gyeonggi/uiwang/area/cheonggye-hagui/",
        "/gyeonggi/uiwang/reservation/",
    ],
    "gyeonggi/uiwang/area/cheonggye-hagui/": [
        "/gyeonggi/uiwang/cheonggye-dong/",
        "/gyeonggi/uiwang/hagui-dong/",
        "/gyeonggi/uiwang/area/baegun-valley/",
        "/gyeonggi/uiwang/station/indeogwon-nearby-area/",
        "/gyeonggi/uiwang/check/",
    ],
    "gyeonggi/uiwang/area/baegun-valley/": [
        "/gyeonggi/uiwang/baegun-valley/",
        "/gyeonggi/uiwang/cheonggye-dong/",
        "/gyeonggi/uiwang/area/cheonggye-hagui/",
        "/gyeonggi/uiwang/check/",
        "/gyeonggi/uiwang/reservation/",
    ],
    "gyeonggi/uiwang/area/bugok-sam-dong/": [
        "/gyeonggi/uiwang/bugok-dong/",
        "/gyeonggi/uiwang/sam-dong/",
        "/gyeonggi/uiwang/area/uiwang-station-bugok/",
        "/gyeonggi/uiwang/station/uiwang-station/",
        "/gyeonggi/uiwang/reservation/",
    ],
    "gyeonggi/uiwang/area/woram-chopyeong/": [
        "/gyeonggi/uiwang/woram-dong/",
        "/gyeonggi/uiwang/chopyeong-dong/",
        "/gyeonggi/uiwang/station/sungkyunkwan-univ-nearby-area/",
        "/gyeonggi/uiwang/area/i-dong-obong/",
        "/gyeonggi/uiwang/check/",
    ],
    "gyeonggi/uiwang/area/i-dong-obong/": [
        "/gyeonggi/uiwang/i-dong/",
        "/gyeonggi/uiwang/sam-dong/",
        "/gyeonggi/uiwang/area/bugok-sam-dong/",
        "/gyeonggi/uiwang/station/uiwang-station/",
        "/gyeonggi/uiwang/check/",
    ],
    "gyeonggi/uiwang/area/indeogwon-cheonggye-nearby/": [
        "/gyeonggi/uiwang/cheonggye-dong/",
        "/gyeonggi/uiwang/poil-dong/",
        "/gyeonggi/uiwang/station/indeogwon-nearby-area/",
        "/gyeonggi/uiwang/area/naeson-poil/",
        "/gyeonggi/uiwang/check/",
    ],
    "gyeonggi/uiwang/area/pyeongchon-naeson-nearby/": [
        "/gyeonggi/uiwang/naeson-dong/",
        "/gyeonggi/uiwang/ojeon-dong/",
        "/gyeonggi/uiwang/station/pyeongchon-nearby-area/",
        "/gyeonggi/uiwang/area/ojeon-dong/",
        "/gyeonggi/uiwang/reservation/",
    ],
    "gyeonggi/uiwang/area/gunpo-bugok-nearby/": [
        "/gyeonggi/uiwang/bugok-dong/",
        "/gyeonggi/uiwang/gocheon-dong/",
        "/gyeonggi/uiwang/station/gunpo-nearby-area/",
        "/gyeonggi/uiwang/area/uiwang-station-bugok/",
        "/gyeonggi/uiwang/check/",
    ],
    "gyeonggi/uiwang/reservation/": [
        "/gyeonggi/uiwang/",
        "/gyeonggi/uiwang/check/",
        "/gyeonggi/uiwang/bugok-dong/",
        "/gyeonggi/uiwang/naeson-dong/",
        "/gyeonggi/uiwang/station/uiwang-station/",
    ],
    "gyeonggi/uiwang/check/": [
        "/gyeonggi/uiwang/",
        "/gyeonggi/uiwang/reservation/",
        "/gyeonggi/uiwang/guide/",
        "/gyeonggi/uiwang/cheonggye-dong/",
        "/gyeonggi/uiwang/i-dong/",
    ],
    "gyeonggi/uiwang/guide/": [
        "/gyeonggi/uiwang/",
        "/gyeonggi/uiwang/reservation/",
        "/gyeonggi/uiwang/check/",
        "/gyeonggi/uiwang/bugok-dong/",
        "/gyeonggi/uiwang/naeson-dong/",
    ],
    "gyeonggi/uiwang/support/": [
        "/gyeonggi/uiwang/",
        "/gyeonggi/uiwang/reservation/",
        "/gyeonggi/uiwang/check/",
        "/gyeonggi/uiwang/support/privacy/",
        "/gyeonggi/uiwang/guide/",
    ],
    "gyeonggi/uiwang/support/privacy/": [
        "/gyeonggi/uiwang/",
        "/gyeonggi/uiwang/support/",
        "/gyeonggi/uiwang/reservation/",
        "/gyeonggi/uiwang/check/",
        "/gyeonggi/uiwang/guide/",
    ],
}


def make_related_links_html(path: str) -> str:
    hrefs = _RELATED.get(path, [])
    if not hrefs:
        return ""
    items = "".join(
        f'<li><a href="{h}">{_LONGTAIL[h]}</a></li>'
        for h in hrefs
        if h in _LONGTAIL
    )
    if not items:
        return ""
    return (
        '<nav class="related-links" aria-label="관련 안내 페이지">'
        "<p><strong>관련 안내 페이지</strong></p>"
        f"<ul>{items}</ul>"
        "</nav>"
    )


def make_breadcrumb_schema(crumbs) -> dict:
    base = BASE_URL.rstrip("/")
    items = [
        {"@type": "ListItem", "position": 1, "name": "홈", "item": base + "/"},
        {"@type": "ListItem", "position": 2, "name": "경기도", "item": base + "/gyeonggi/"},
        {"@type": "ListItem", "position": 3, "name": "의왕시", "item": base + "/gyeonggi/uiwang/"},
    ]
    start_pos = 4
    rest = crumbs[1:] if crumbs and crumbs[0][1] in ("/", "/gyeonggi/uiwang/") else crumbs
    for i, (label, href) in enumerate(rest, start=start_pos):
        entry = {"@type": "ListItem", "position": i, "name": label}
        if href:
            entry["item"] = base + href
        items.append(entry)
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
    }


def make_webpage_schema(title: str, desc: str, canonical: str) -> dict:
    base = BASE_URL.rstrip("/")
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "description": desc,
        "url": canonical,
        "inLanguage": "ko",
        "isPartOf": {"@id": base + "/#organization"},
        "publisher": {"@id": base + "/#organization"},
        "image": {
            "@type": "ImageObject",
            "url": base + "/assets/og-image.png",
            "width": 1200,
            "height": 630
        }
    }


def render_page(page: dict) -> str:
    path = page["path"]
    title = page["title"]
    desc = page["desc"]
    h1 = page["h1"]
    body = page["body"]
    crumbs = page.get("breadcrumb") or []
    extra_head = page.get("extra_head", "")
    hero = page.get("hero", "")

    chars = text_length(body)
    noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
    robots = (
        '<meta name="robots" content="noindex,follow">'
        if noindex
        else '<meta name="robots" content="index,follow">'
    )
    canonical = BASE_URL.rstrip("/") + "/" + path

    if hero:
        page_head = hero
    else:
        page_head = ""

    h1_html = "" if hero else f"<h1>{h1}</h1>"

    body, toc_items = inject_toc(body)
    body = body + make_related_links_html(path)
    toc_html = render_toc(toc_items)
    layout_cls = "page-layout has-toc" if toc_html else "page-layout"

    if hero:
        auto_schema = _ld(make_org_schema())
    else:
        blocks = [make_org_schema(), make_webpage_schema(title, desc, canonical)]
        if crumbs:
            blocks.append(make_breadcrumb_schema(crumbs))
        auto_schema = "".join(_ld(b) for b in blocks)

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:image" content="{BASE_URL.rstrip('/')}/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE_URL.rstrip('/')}/assets/og-image.png">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg?v=2">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png?v=2">
<link rel="icon" href="/favicon.ico?v=2" sizes="48x48">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png?v=2">
<meta name="theme-color" content="#0a1120">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Noto+Serif+KR:wght@600;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
<link rel="stylesheet" href="/assets/style.css">
{auto_schema}{extra_head}</head>
<body>
<header class="site-header">
  <div class="header-accent" aria-hidden="true"></div>
  <div class="header-top">
    <div class="header-inner">
      <a class="brand" href="/gyeonggi/uiwang/"><span class="brand-mark">88</span> <span class="brand-text">{BRAND}</span></a>
      <p class="header-tagline"><span class="tag-gem">◆</span> 의왕시 전지역 방문 관리 <span class="tag-gem">◆</span> 24시간 상담</p>
      <a class="header-call" href="tel:{PHONE}"><span class="call-label">예약전화</span> {PHONE_DISPLAY}</a>
      <button class="nav-toggle" aria-label="메뉴 열기" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
  <nav class="main-nav" aria-label="주 메뉴">
    <div class="nav-inner"><ul class="nav-list">{render_nav(path)}</ul></div>
  </nav>
</header>
{page_head}<main class="site-main">
  <div class="container {layout_cls}">
    {toc_html}
    <article class="page-content">
      {render_breadcrumb(crumbs)}
      {h1_html}
      {body}
    </article>
  </div>
</main>
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-col footer-about">
      <p class="footer-brand">{BRAND}</p>
      <p class="footer-desc">경기도 의왕시 전지역 방문 출장마사지·홈타이 안내 사이트입니다. 모든 서비스는 안내된 관리 범위와 위생·안전 기준 안에서만 제공됩니다.</p>
      <address class="footer-contact">
        <span class="footer-contact-row"><span class="footer-label">상호</span> {BRAND}</span>
        <span class="footer-contact-row"><span class="footer-label">전화예약</span> <a href="tel:{PHONE}">{PHONE_DISPLAY}</a></span>
        <span class="footer-contact-row"><span class="footer-label">상담시간</span> 연중무휴 24시간</span>
        <span class="footer-contact-row"><span class="footer-label">서비스 지역</span> 경기도 의왕시 전지역</span>
      </address>
    </div>
    <nav class="footer-col" aria-label="서비스 안내">
      <p class="footer-title">서비스</p>
      <ul>
        <li><a href="/gyeonggi/uiwang/">의왕 출장마사지</a></li>
        <li><a href="/gyeonggi/uiwang/gocheon-dong/">지역별 안내</a></li>
        <li><a href="/gyeonggi/uiwang/station/uiwang-station/">역세권 안내</a></li>
        <li><a href="/gyeonggi/uiwang/area/uiwang-station-bugok/">생활권 안내</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="이용 안내">
      <p class="footer-title">이용 안내</p>
      <ul>
        <li><a href="/gyeonggi/uiwang/reservation/">예약 안내</a></li>
        <li><a href="/gyeonggi/uiwang/check/">이용 전 확인사항</a></li>
        <li><a href="/gyeonggi/uiwang/guide/">홈타이 이용 가이드</a></li>
        <li><a href="/gyeonggi/uiwang/support/">고객센터</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="정책 및 기준">
      <p class="footer-title">정책</p>
      <ul>
        <li><a href="/gyeonggi/uiwang/support/privacy/">개인정보처리방침</a></li>
        <li><a href="{TELEGRAM}" target="_blank" rel="noopener nofollow">문의하기</a></li>
      </ul>
    </nav>
  </div>
  <div class="footer-bottom">
    <div class="container footer-bottom-inner">
      <p class="footer-copy">&copy; {BRAND}. All rights reserved.</p>
      <p class="footer-note">건전한 방문 관리 서비스를 운영하며, 불법적인 요청은 어떤 경우에도 응하지 않습니다.</p>
      <div class="footer-actions">
        <a class="btn-telegram" href="{TELEGRAM}" target="_blank" rel="noopener nofollow" title="웹사이트 제작문의 — 텔레그램">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.894 8.221-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.447 1.394c-.16.16-.295.295-.605.295l.213-3.053 5.56-5.023c.242-.213-.054-.333-.373-.12L7.17 14.015l-2.96-.924c-.643-.204-.657-.643.136-.953l11.57-4.46c.537-.194 1.006.131.978.543z"/></svg>
          웹사이트 제작문의
        </a>
        <a class="btn-partnership" href="{TELEGRAM}" target="_blank" rel="noopener nofollow" title="제휴문의 — 텔레그램">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/></svg>
          제휴문의
        </a>
      </div>
    </div>
  </div>
</footer>
<a class="call-fab" href="tel:{PHONE}" aria-label="전화 예약 {PHONE_DISPLAY}">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
  <span class="call-fab-label">예약 전화</span>
</a>
<script src="/assets/nav.js"></script>
</body>
</html>
"""


def build() -> None:
    report = []
    sitemap_urls = []

    os.makedirs(PUBLIC_DIR, exist_ok=True)

    for page in PAGES:
        path = page["path"]
        out_dir = os.path.join(PUBLIC_DIR, path)
        os.makedirs(out_dir, exist_ok=True)
        html_out = render_page(page)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_out)

        chars = text_length(page["body"])
        noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
        if not noindex:
            sitemap_urls.append(BASE_URL.rstrip("/") + "/" + path)
        report.append((path or "/", chars, "noindex" if noindex else "index"))

    # sitemap.xml
    urls = "\n".join(f"  <url><loc>{u}</loc></url>" for u in sitemap_urls)
    with open(os.path.join(PUBLIC_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{urls}\n</urlset>\n"
        )

    # robots.txt
    with open(os.path.join(PUBLIC_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(
            "User-agent: *\nAllow: /\n\n"
            f"Sitemap: {BASE_URL.rstrip('/')}/sitemap.xml\n"
        )

    # .nojekyll
    open(os.path.join(PUBLIC_DIR, ".nojekyll"), "w").close()

    # root index.html — serve main page at / without redirect
    main_page = next(p for p in PAGES if p["path"] == "gyeonggi/uiwang/")
    main_html = render_page(main_page)
    with open(os.path.join(PUBLIC_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(main_html)

    width = max(len(p) for p, _, _ in report)
    print(f"{'PATH'.ljust(width)}  CHARS  ROBOTS")
    for p, c, r in sorted(report):
        flag = "" if (r == "noindex" or MIN_INDEX_CHARS <= c <= 2500) else "  ⚠"
        print(f"{p.ljust(width)}  {str(c).rjust(5)}  {r}{flag}")
    print(f"\n{len(report)} pages built, {len(sitemap_urls)} in sitemap.")


if __name__ == "__main__":
    build()
