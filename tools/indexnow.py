#!/usr/bin/env python3
"""IndexNow 일괄 색인 통보 — 빙(Bing) & 네이버(Naver)

사용법:
    python tools/indexnow.py          # 전체 URL 통보
    python tools/indexnow.py --dry    # URL 목록만 출력 (실제 전송 안 함)

IndexNow 참여 엔진: Bing, Naver, Yandex (Google은 미참여 — 별도 Indexing API 필요)
"""
import json
import sys
import urllib.request
import urllib.error

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.dirname(__file__)))
from content.site import BASE_URL
from build import INDEXNOW_KEY, PAGES, MIN_INDEX_CHARS
from build import text_length

BASE = BASE_URL.rstrip("/")
KEY_LOCATION = f"{BASE}/{INDEXNOW_KEY}.txt"

ENDPOINTS = [
    "https://www.bing.com/indexnow",
    "https://searchadvisor.naver.com/indexnow",
]

def get_urls():
    urls = []
    for page in PAGES:
        if page.get("noindex"):
            continue
        if text_length(page["body"]) < MIN_INDEX_CHARS:
            continue
        urls.append(BASE + "/" + page["path"])
    # 루트 URL 추가
    if BASE + "/gyeonggi/uiwang/" in urls:
        urls.insert(0, BASE + "/")
    return urls


def submit(urls: list, dry: bool = False):
    payload = {
        "host": BASE.replace("https://", "").replace("http://", ""),
        "key": INDEXNOW_KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }
    print(f"총 {len(urls)}개 URL 통보 준비")
    for u in urls:
        print(f"  {u}")

    if dry:
        print("\n[DRY RUN] 실제 전송하지 않음.")
        return

    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    for endpoint in ENDPOINTS:
        req = urllib.request.Request(
            endpoint,
            data=body,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                print(f"✓ {endpoint} → HTTP {resp.status}")
        except urllib.error.HTTPError as e:
            print(f"✗ {endpoint} → HTTP {e.code}: {e.read().decode()}")
        except Exception as e:
            print(f"✗ {endpoint} → {e}")


if __name__ == "__main__":
    dry = "--dry" in sys.argv
    submit(get_urls(), dry=dry)
