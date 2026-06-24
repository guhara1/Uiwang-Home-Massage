import json
from .site import BRAND, BASE_URL, PHONE

_BASE = BASE_URL.rstrip("/")

DESC = "의왕 출장마사지·홈타이 예약 전 의왕역, 내손동, 청계동, 고천동, 부곡동 생활권을 확인하세요."

_FAQ = [
    ("의왕은 구별 페이지를 만들어야 하나요?",
     "의왕은 행정구가 없으므로 구별 페이지를 만들지 않습니다. 의왕 메인, 대표 지역, 역세권, 생활권 구조로 안내합니다."),
    ("의왕역 페이지는 꼭 확인해야 하나요?",
     "의왕역은 부곡동, 삼동, 월암동 인접 생활권을 연결하는 핵심 역세권입니다. 예약 전 방문 주소와 건물 출입 가능 여부를 확인하세요."),
    ("인덕원역 인접 생활권은 어떻게 다른가요?",
     "인덕원역은 안양시 성격이 강하므로 의왕에서는 청계동, 포일동, 내손동 인접 생활권으로 안내합니다. 실제 방문 주소 기준으로 확인하세요."),
    ("내손1동과 내손2동을 따로 확인해야 하나요?",
     "내손동 대표 페이지로 통합 안내합니다. 내손1·2 생활권은 내손동 페이지 본문에서 자연스럽게 설명합니다."),
    ("백운밸리는 별도로 확인해야 하나요?",
     "백운밸리는 청계동·학의동과 연결되는 신도시형 생활권입니다. 인접 지역과 함께 방문 주소 기준을 확인하세요."),
    ("추가 이동비는 어떻게 확인하나요?",
     "월암동, 초평동, 이동처럼 차량 이동 기준 지역은 예약 시 추가 이동비 여부를 반드시 먼저 확인하세요."),
]

_faq_schema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {
            "@type": "Question",
            "@id": f"#faq-{i+1}",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a}
        }
        for i, (q, a) in enumerate(_FAQ)
    ]
}

_org_schema = {
    "@context": "https://schema.org",
    "@type": "HealthAndBeautyBusiness",
    "@id": _BASE + "/#organization",
    "name": BRAND,
    "telephone": PHONE,
    "url": _BASE + "/gyeonggi/uiwang/",
    "image": _BASE + "/assets/og-image.png",
    "description": "경기도 의왕시 출장마사지·홈타이 안내 사이트",
    "areaServed": {
        "@type": "AdministrativeArea",
        "name": "경기도 의왕시"
    },
    "openingHoursSpecification": {
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
        "opens": "00:00",
        "closes": "23:59"
    }
}

_breadcrumb_schema = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "홈", "item": _BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": "경기도", "item": _BASE + "/gyeonggi/"},
        {"@type": "ListItem", "position": 3, "name": "의왕시", "item": _BASE + "/gyeonggi/uiwang/"},
    ]
}

_webpage_schema = {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "의왕 출장마사지｜의왕역·내손·청계·고천 홈타이 지역 안내",
    "description": DESC,
    "url": _BASE + "/gyeonggi/uiwang/",
    "inLanguage": "ko",
    "isPartOf": {"@id": _BASE + "/#organization"},
    "publisher": {"@id": _BASE + "/#organization"},
    "image": {
        "@type": "ImageObject",
        "url": _BASE + "/assets/og-image.png",
        "width": 1200,
        "height": 630
    }
}

_EXTRA_HEAD = f"""<script type="application/ld+json">
{json.dumps(_org_schema, ensure_ascii=False, indent=2)}
</script>
<script type="application/ld+json">
{json.dumps(_breadcrumb_schema, ensure_ascii=False, indent=2)}
</script>
<script type="application/ld+json">
{json.dumps(_webpage_schema, ensure_ascii=False, indent=2)}
</script>
<script type="application/ld+json">
{json.dumps(_faq_schema, ensure_ascii=False, indent=2)}
</script>"""

_HERO = """<div class="hero">
  <div class="hero-content">
    <div class="hero-badge">의왕시 전지역 방문 관리</div>
    <h1 class="hero-title">의왕 출장마사지<br><span class="hero-accent">홈타이</span><br>지역별 예약 안내</h1>
    <p class="hero-lead">의왕역, 내손동, 청계동, 고천동, 오전동, 부곡동, 백운밸리 생활권별 방문 가능 지역과 예약 전 확인사항을 안내합니다.</p>
    <div class="hero-cta">
      <a href="#areas" class="btn btn-primary">지역별 안내 보기</a>
      <a href="#stations" class="btn btn-secondary">가까운 역 찾기</a>
      <a href="/gyeonggi/uiwang/reservation/" class="btn btn-secondary">예약 안내 보기</a>
      <a href="/gyeonggi/uiwang/check/" class="btn btn-secondary">이용 전 확인사항</a>
    </div>
  </div>
  <div class="hero-stats">
    <div class="stat">
      <div class="stat-number">13</div>
      <div class="stat-label">지역 페이지</div>
    </div>
    <div class="stat">
      <div class="stat-number">7</div>
      <div class="stat-label">역세권 안내</div>
    </div>
    <div class="stat">
      <div class="stat-number">12</div>
      <div class="stat-label">생활권 안내</div>
    </div>
    <div class="stat">
      <div class="stat-number">24H</div>
      <div class="stat-label">상담 가능</div>
    </div>
  </div>
</div>"""

PAGE = {
    "path": "gyeonggi/uiwang/",
    "title": "의왕 출장마사지｜의왕역·내손·청계·고천 홈타이 지역 안내",
    "desc": DESC,
    "h1": "의왕 출장마사지 · 의왕 홈타이 지역별 예약 안내",
    "hero": _HERO,
    "breadcrumb": [],
    "extra_head": _EXTRA_HEAD,
    "body": """
<section id="criteria">
  <h2>의왕에서 출장마사지를 찾을 때 먼저 확인할 기준</h2>
  <p>의왕시는 경기도 중부에 위치한 도시로, 행정구가 따로 없는 단일 시 구조입니다. 다만 생활권 차이가 뚜렷하여 지역별로 이동 기준과 예약 조건이 다르게 적용됩니다. 출장마사지를 예약하기 전에 자신의 위치가 어느 생활권에 해당하는지 파악하는 것이 예약 과정의 첫 번째 단계입니다.</p>
  <p>의왕역과 부곡동은 경부선 1호선 중심 생활권으로, 삼동·이동·월암동과 연결됩니다. 고천동과 왕곡동은 의왕시청·경수대로 중심 생활권이며, 오전동은 고천동과 내손동 사이의 중간 생활권입니다. 내손동과 포일동은 평촌·인덕원 인접 생활권과 연결되고, 청계동과 학의동은 백운밸리·인덕원 인접권을 함께 확인해야 합니다. 월암동과 초평동은 차량 이동 기준과 추가 이동비 확인이 중요한 외곽 생활권입니다.</p>
  <p>의왕 전역으로 방문이 가능하며, 자택·숙소·오피스텔 등 다양한 방문 장소에 대응합니다. 예약 전에 정확한 주소와 가장 가까운 지하철역을 확인하면 예약 과정이 원활해집니다.</p>
</section>

<section id="areas">
  <h2>의왕 대표 지역별 방문 가능 지역 안내</h2>
  <div class="card-grid">
    <a href="/gyeonggi/uiwang/gocheon-dong/" class="card">
      <h3>고천동</h3>
      <p>의왕시청, 왕곡동, 오전동 인접 생활권</p>
      <span class="card-arrow">→</span>
    </a>
    <a href="/gyeonggi/uiwang/wanggok-dong/" class="card">
      <h3>왕곡동</h3>
      <p>고천동, 오전동, 경수대로 인접 생활권</p>
      <span class="card-arrow">→</span>
    </a>
    <a href="/gyeonggi/uiwang/ojeon-dong/" class="card">
      <h3>오전동</h3>
      <p>고천동, 내손동, 평촌 인접 생활권</p>
      <span class="card-arrow">→</span>
    </a>
    <a href="/gyeonggi/uiwang/bugok-dong/" class="card">
      <h3>부곡동</h3>
      <p>의왕역, 삼동, 이동, 월암동 인접 생활권</p>
      <span class="card-arrow">→</span>
    </a>
    <a href="/gyeonggi/uiwang/sam-dong/" class="card">
      <h3>삼동</h3>
      <p>의왕역, 부곡동, 철도 생활권 인접 지역</p>
      <span class="card-arrow">→</span>
    </a>
    <a href="/gyeonggi/uiwang/i-dong/" class="card">
      <h3>이동</h3>
      <p>부곡동, 오봉, 월암동 인접 차량 이동권</p>
      <span class="card-arrow">→</span>
    </a>
    <a href="/gyeonggi/uiwang/woram-dong/" class="card">
      <h3>월암동</h3>
      <p>부곡동, 초평동, 성균관대역 인접권</p>
      <span class="card-arrow">→</span>
    </a>
    <a href="/gyeonggi/uiwang/chopyeong-dong/" class="card">
      <h3>초평동</h3>
      <p>월암동, 수원 인접권, 차량 이동 기준 중심</p>
      <span class="card-arrow">→</span>
    </a>
    <a href="/gyeonggi/uiwang/naeson-dong/" class="card">
      <h3>내손동</h3>
      <p>내손1·2 생활권, 포일동, 평촌 인접권</p>
      <span class="card-arrow">→</span>
    </a>
    <a href="/gyeonggi/uiwang/poil-dong/" class="card">
      <h3>포일동</h3>
      <p>내손동, 청계동, 인덕원 인접 생활권</p>
      <span class="card-arrow">→</span>
    </a>
    <a href="/gyeonggi/uiwang/cheonggye-dong/" class="card">
      <h3>청계동</h3>
      <p>학의동, 백운밸리, 인덕원 인접 생활권</p>
      <span class="card-arrow">→</span>
    </a>
    <a href="/gyeonggi/uiwang/hagui-dong/" class="card">
      <h3>학의동</h3>
      <p>백운밸리, 청계동, 포일동 인접 생활권</p>
      <span class="card-arrow">→</span>
    </a>
    <a href="/gyeonggi/uiwang/baegun-valley/" class="card">
      <h3>백운밸리</h3>
      <p>청계·학의 생활권과 연결되는 신도시형 주거지</p>
      <span class="card-arrow">→</span>
    </a>
  </div>
</section>

<section id="stations">
  <h2>의왕 주요 역세권별 홈타이 안내</h2>
  <p>의왕시 대표 역세권과 인접 생활권별로 방문 기준을 안내합니다. 실제 방문 주소를 기준으로 가장 가까운 역을 선택하세요.</p>
  <div class="card-grid">
    <a href="/gyeonggi/uiwang/station/uiwang-station/" class="card">
      <h3>의왕역</h3>
      <p>부곡동, 삼동, 월암동 인접 생활권입니다.</p>
      <small style="color:var(--text-dim);display:block;margin-top:8px">방문 주소와 건물 출입 가능 여부를 먼저 확인하세요.</small>
      <span class="card-arrow">→</span>
    </a>
    <a href="/gyeonggi/uiwang/station/indeogwon-nearby-area/" class="card">
      <h3>인덕원역 인접 생활권</h3>
      <p>청계동, 포일동, 내손동 인접 생활권입니다.</p>
      <small style="color:var(--text-dim);display:block;margin-top:8px">의왕 내부 핵심역이 아니므로 실제 주소 기준으로 확인하세요.</small>
      <span class="card-arrow">→</span>
    </a>
    <a href="/gyeonggi/uiwang/station/pyeongchon-nearby-area/" class="card">
      <h3>평촌역 인접 생활권</h3>
      <p>내손동, 오전동 인접 생활권입니다.</p>
      <span class="card-arrow">→</span>
    </a>
    <a href="/gyeonggi/uiwang/station/beomgye-nearby-area/" class="card">
      <h3>범계역 인접 생활권</h3>
      <p>오전동, 내손동 이동 기준 생활권입니다.</p>
      <span class="card-arrow">→</span>
    </a>
    <a href="/gyeonggi/uiwang/station/gunpo-nearby-area/" class="card">
      <h3>군포역 인접 생활권</h3>
      <p>부곡동, 오전동 이동 기준 생활권입니다.</p>
      <span class="card-arrow">→</span>
    </a>
    <a href="/gyeonggi/uiwang/station/dangjeong-nearby-area/" class="card">
      <h3>당정역 인접 생활권</h3>
      <p>부곡동, 군포 인접 생활권입니다.</p>
      <span class="card-arrow">→</span>
    </a>
    <a href="/gyeonggi/uiwang/station/sungkyunkwan-univ-nearby-area/" class="card">
      <h3>성균관대역 인접 생활권</h3>
      <p>월암동, 초평동 이동 기준 생활권입니다.</p>
      <span class="card-arrow">→</span>
    </a>
  </div>
</section>

<section id="lifestyle">
  <h2>의왕 생활권별 예약 기준</h2>
  <p>지역과 역을 연결한 생활권 기준으로 예약하면 더 정확한 방문 주소와 이동 시간을 확인할 수 있습니다.</p>
  <div class="card-grid">
    <a href="/gyeonggi/uiwang/area/uiwang-station-bugok/" class="card">
      <h3>의왕역·부곡</h3>
      <span class="card-arrow">→</span>
    </a>
    <a href="/gyeonggi/uiwang/area/gocheon-wanggok/" class="card">
      <h3>고천·왕곡</h3>
      <span class="card-arrow">→</span>
    </a>
    <a href="/gyeonggi/uiwang/area/ojeon-dong/" class="card">
      <h3>오전동 생활권</h3>
      <span class="card-arrow">→</span>
    </a>
    <a href="/gyeonggi/uiwang/area/naeson-poil/" class="card">
      <h3>내손·포일</h3>
      <span class="card-arrow">→</span>
    </a>
    <a href="/gyeonggi/uiwang/area/cheonggye-hagui/" class="card">
      <h3>청계·학의</h3>
      <span class="card-arrow">→</span>
    </a>
    <a href="/gyeonggi/uiwang/area/baegun-valley/" class="card">
      <h3>백운밸리</h3>
      <span class="card-arrow">→</span>
    </a>
    <a href="/gyeonggi/uiwang/area/bugok-sam-dong/" class="card">
      <h3>부곡·삼동</h3>
      <span class="card-arrow">→</span>
    </a>
    <a href="/gyeonggi/uiwang/area/woram-chopyeong/" class="card">
      <h3>월암·초평</h3>
      <span class="card-arrow">→</span>
    </a>
    <a href="/gyeonggi/uiwang/area/i-dong-obong/" class="card">
      <h3>이동·오봉 인접</h3>
      <span class="card-arrow">→</span>
    </a>
    <a href="/gyeonggi/uiwang/area/indeogwon-cheonggye-nearby/" class="card">
      <h3>인덕원·청계 인접</h3>
      <span class="card-arrow">→</span>
    </a>
    <a href="/gyeonggi/uiwang/area/pyeongchon-naeson-nearby/" class="card">
      <h3>평촌·내손 인접</h3>
      <span class="card-arrow">→</span>
    </a>
    <a href="/gyeonggi/uiwang/area/gunpo-bugok-nearby/" class="card">
      <h3>군포·부곡 인접</h3>
      <span class="card-arrow">→</span>
    </a>
  </div>
</section>

<section id="check">
  <h2>의왕 홈타이 예약 전 확인사항</h2>
  <p>예약을 진행하기 전에 다음 항목들을 먼저 확인하면 예약 과정이 훨씬 수월합니다.</p>
  <ul>
    <li><strong>방문 가능 주소 확인</strong> — 자택, 숙소, 오피스텔 등 정확한 방문 주소와 건물 유형 확인</li>
    <li><strong>예약 가능 시간 확인</strong> — 희망 예약 시간이 가능한지 미리 확인</li>
    <li><strong>추가 이동비 여부 확인</strong> — 월암동·초평동·이동 등 외곽 지역은 추가 이동비 발생 여부 사전 확인</li>
    <li><strong>건물 출입 방식 확인</strong> — 공동현관, 자동문, 경비 확인 등</li>
    <li><strong>자택·숙소·오피스텔 이용 기준 확인</strong> — 서비스 제공 장소 기준</li>
    <li><strong>결제 방식 확인</strong> — 현금, 계좌이체 등 가능한 결제 수단</li>
    <li><strong>예약 변경·취소 기준 확인</strong> — 변경·취소 수수료 및 절차</li>
    <li><strong>개인정보 처리 기준 확인</strong> — 개인정보 수집·이용·보관 방식</li>
    <li><strong>불법·선정적 서비스 불가 안내</strong> — 건전한 관리 서비스만 제공</li>
  </ul>
</section>

<section id="faq">
  <h2>의왕 출장마사지 자주 묻는 질문</h2>
  <dl class="faq-list">
    <dt id="faq-1">의왕은 구별 페이지를 만들어야 하나요?</dt>
    <dd>의왕은 행정구가 없으므로 구별 페이지를 만들지 않습니다. 의왕 메인, 대표 지역, 역세권, 생활권 구조로 안내합니다.</dd>

    <dt id="faq-2">의왕역 페이지는 꼭 확인해야 하나요?</dt>
    <dd>의왕역은 부곡동, 삼동, 월암동 인접 생활권을 연결하는 핵심 역세권입니다. 예약 전 방문 주소와 건물 출입 가능 여부를 확인하세요.</dd>

    <dt id="faq-3">인덕원역 인접 생활권은 어떻게 다른가요?</dt>
    <dd>인덕원역은 안양시 성격이 강하므로 의왕에서는 청계동, 포일동, 내손동 인접 생활권으로 안내합니다. 실제 방문 주소 기준으로 확인하세요.</dd>

    <dt id="faq-4">내손1동과 내손2동을 따로 확인해야 하나요?</dt>
    <dd>내손동 대표 페이지로 통합 안내합니다. 내손1·2 생활권은 내손동 페이지 본문에서 자연스럽게 설명합니다.</dd>

    <dt id="faq-5">백운밸리는 별도로 확인해야 하나요?</dt>
    <dd>백운밸리는 청계동·학의동과 연결되는 신도시형 생활권입니다. 인접 지역과 함께 방문 주소 기준을 확인하세요.</dd>

    <dt id="faq-6">추가 이동비는 어떻게 확인하나요?</dt>
    <dd>월암동, 초평동, 이동처럼 차량 이동 기준 지역은 예약 시 추가 이동비 여부를 반드시 먼저 확인하세요.</dd>
  </dl>
</section>
"""
}
