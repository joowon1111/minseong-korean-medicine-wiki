/* Daily Korean medicine learning cards. No network or storage. */
(function () {
  "use strict";

  const cards = [
    {
      line: "같은 통증이라도, 먼저 살필 맥락은 다를 수 있어요.",
      note: "언제 시작됐는지, 어떤 움직임에서 달라지는지, 감각·근력과 일상 기능은 어떤지 함께 살피면 치료 목표가 또렷해집니다.",
      source: "통증·근골격 통합 안내",
      href: "/conditions/low-back-pain/"
    },
    {
      line: "좋아짐은 통증 점수 밖에서도 보입니다.",
      note: "걷는 거리, 잠을 깨는 횟수, 업무나 집안일처럼 실제로 회복하고 싶은 기능도 치료 전후에 비교해 보세요.",
      source: "침구치료 경과·재평가",
      href: "/acupuncture-integrated/followup/"
    },
    {
      line: "평소의 나를 알면, 오늘의 변화를 더 잘 읽을 수 있어요.",
      note: "사상의학의 소증은 평소 상태를 살피는 개념입니다. 현재 증상과 함께 식욕·소화·대변·수면 등 기준선을 비교합니다.",
      source: "사상체질과 소증",
      href: "/sasang-pattern-differential/"
    },
    {
      line: "체질을 살피는 일과, 지금 병증을 살피는 일은 함께 갑니다.",
      note: "체형이나 성격 하나만으로 체질을 단정하지 않고, 평소 반응과 현재 병증을 구분해 종합적으로 이해합니다.",
      source: "사상체질 진단·병증 감별",
      href: "/sasang-pattern-differential/"
    },
    {
      line: "같은 증상에도 처방 선택이 달라지는 이유가 있어요.",
      note: "동반 증상, 한열·허실, 식욕·소화, 대소변과 복용약을 함께 살펴 치료 목표와 처방 구성을 정합니다.",
      source: "맞춤 처방 선택 원리",
      href: "/herbal-integrated/formula-selection-guide/"
    },
    {
      line: "약재는 처방 안에서 서로 역할을 나눕니다.",
      note: "한 본초의 효능만 떼어 보기보다 배합, 용량, 제형, 처방 안에서 맡는 역할을 함께 읽어 보세요.",
      source: "본초·방제 한눈에 보기",
      href: "/herbal-integrated/"
    },
    {
      line: "한약 상담 때 복용 중인 약 목록은 좋은 출발점입니다.",
      note: "처방약·일반약·건강기능식품과 최근 검사 결과를 함께 알리면 병용과 안전성을 더 구체적으로 검토할 수 있습니다.",
      source: "한약 상담 전 준비",
      href: "/conditions/herbal-consultation-prep/"
    },
    {
      line: "침 치료는 ‘어디가 아픈가’와 ‘무엇을 회복할까’를 함께 봅니다.",
      note: "통증 부위뿐 아니라 움직임, 감각, 근력, 경맥과 해부학적 위치를 살펴 치료를 구성하고 변화를 재평가합니다.",
      source: "통합 침구치료 탐색",
      href: "/acupuncture-integrated/"
    },
    {
      line: "치료 방법은 목표에 맞춰 조합할 수 있어요.",
      note: "침·전침·약침·뜸·부항은 자극 방식과 적용 상황이 다릅니다. 현재 기능 목표와 반응을 확인해 알맞게 구성합니다.",
      source: "침구치료 방법 비교",
      href: "/acupuncture-integrated/methods/"
    },
    {
      line: "어지럼은 ‘빙빙 도는 느낌’만으로 설명되지 않아요.",
      note: "회전감인지, 중심을 잡기 어려운지, 청력 변화나 신경학적 증상이 동반되는지 살펴 원인 평가와 치료를 연결합니다.",
      source: "어지럼 안내",
      href: "/conditions/dizziness/"
    },
    {
      line: "복통은 위치와 함께 ‘언제, 어떻게’ 시작됐는지도 기록해요.",
      note: "식사와의 관계, 대변·구토·발열, 지속시간을 적어두면 원인 감별과 필요한 진료를 결정하는 데 도움이 됩니다.",
      source: "복통 안내",
      href: "/conditions/abdominal-pain/"
    },
    {
      line: "잠을 몇 시간 잤는지와 낮에 어떻게 느끼는지를 함께 봅니다.",
      note: "잠든 시각, 깬 횟수, 낮잠과 카페인, 아침 회복감을 1~2주 적으면 수면 문제의 패턴을 이해하는 데 도움이 됩니다.",
      source: "불면증·수면장애",
      href: "/conditions/insomnia/"
    },
    {
      line: "이명은 소리의 크기뿐 아니라 청력과 생활 영향을 살펴요.",
      note: "언제 시작됐는지, 한쪽인지, 청력 변화·어지럼이 함께 있는지 확인하고 필요한 평가와 증상 관리를 연결합니다.",
      source: "이명 안내",
      href: "/conditions/tinnitus/"
    },
    {
      line: "얼굴 통증은 통증 양상과 감각 변화를 차근히 구분합니다.",
      note: "짧고 전기 오는 듯한 통증인지, 지속되는 통증인지, 감각저하나 다른 신경 증상이 동반되는지 평가가 중요합니다.",
      source: "삼차신경통 안내",
      href: "/conditions/trigeminal-neuralgia/"
    },
    {
      line: "몸이 불편할 때는 증상 이름부터 몰라도 괜찮아요.",
      note: "언제 심해지는지, 무엇이 나아지게 하는지, 일상에서 무엇이 달라졌는지부터 정리하면 알맞은 안내를 찾기 쉽습니다.",
      source: "증상으로 찾기",
      href: "/symptom-integrated/"
    },
    {
      line: "복용 후 변화도 기록하면 다음 진료가 더 구체적입니다.",
      note: "좋아진 증상과 남은 불편, 식욕·소화·수면의 변화, 새로 생긴 반응을 날짜와 함께 적어 보세요.",
      source: "한약 복용 후 변화 기록",
      href: "/conditions/herbal-followup/"
    },
    {
      line: "침을 놓는 위치는 전통 이론과 실제 해부를 함께 살핍니다.",
      note: "경혈·경맥의 임상 논리에 근육·신경·혈관·장기의 위치를 더해 시술 위치와 깊이, 방향을 계획합니다.",
      source: "침구치료와 임상해부학",
      href: "/acupuncture-integrated/"
    },
    {
      line: "사상체질은 체형이나 성격 한 가지로 정하지 않아요.",
      note: "체형기상·용모·평소 소증과 현재 병증을 함께 살피며, 설문 하나의 결과보다 전체 흐름과 일관성을 봅니다.",
      source: "사상의학 한눈에 보기",
      href: "/sasang/"
    },
    {
      line: "한약은 이름보다 어떤 병증과 목표에 쓰는지 읽어 보세요.",
      note: "같은 처방명도 구성과 적용 맥락이 다를 수 있어 출전, 구성 약재, 대상 증후와 근거를 함께 확인합니다.",
      source: "임상 핵심 처방·방제 안내",
      href: "/herbal-integrated/"
    },
    {
      line: "안전 확인은 치료를 잘 이어가기 위한 첫 단계입니다.",
      note: "복용약, 알레르기, 임신·수유, 기저질환과 최근 치료 정보를 공유하면 침구·한약 치료를 더 알맞게 계획할 수 있습니다.",
      source: "침구치료 안전·위험신호",
      href: "/acupuncture-integrated/safety/"
    },
    {
      line: "몸의 신호가 갑자기 달라지면 평가의 우선순위도 달라집니다.",
      note: "갑작스러운 마비·언어장애, 심한 호흡곤란, 지속되는 심한 복통처럼 급격하거나 중대한 변화는 신속한 의료 평가를 먼저 연결합니다.",
      source: "질환별 건강정보와 위험신호",
      href: "/conditions/"
    },
    {
      "line": "눈피로를 말할 때는 흐림과 건조를 나누어 보세요.",
      "note": "작은 글씨가 흐린지, 따갑고 뻑뻑한지, 목·이마가 당기는지 구분하면 시력·눈물막·근육의 평가가 더 구체적입니다.",
      "introducedOn": "2026-10-12",
      "source": "눈피로·안구피로",
      "href": "/conditions/eye-fatigue/"
    },
    {
      "line": "눈과 입이 함께 마르면 두 곳의 기능을 함께 살펴요.",
      "note": "눈물막과 눈꺼풀, 침샘과 구강 상태를 각각 확인하고 복용약·전신 증상과 연결해 원인을 평가합니다.",
      "introducedOn": "2026-10-12",
      "source": "안구건조와 전신 상태",
      "href": "/conditions/dry-eye/"
    },
    {
      "line": "침은 입안의 편안함과 치아를 함께 지킵니다.",
      "note": "입마름이 지속되면 말하기·식사뿐 아니라 충치·점막 상태를 함께 살펴 구강 보호와 원인 평가를 이어갑니다.",
      "introducedOn": "2026-10-12",
      "source": "구강건조증·입마름",
      "href": "/conditions/dry-mouth/"
    },
    {
      "line": "두통이 잦다면 아픈 날과 약을 먹은 날을 따로 세어 보세요.",
      "note": "월 두통일수·지속시간·급성기 약 복용일수와 업무 중단 정도를 나누면 치료 전후의 변화를 이해하기 쉽습니다.",
      "introducedOn": "2026-10-12",
      "source": "긴장형두통의 경과 평가",
      "href": "/conditions/tension-headache/"
    },
    {
      "line": "경혈의 여러 분류는 한 자리에서 함께 만날 수 있어요.",
      "note": "원혈·오수혈·팔맥교회혈은 다른 분류 체계입니다. 한 경혈에 여러 속성이 있어도 소속·위치·배혈 역할을 나누어 읽습니다.",
      "introducedOn": "2026-10-12",
      "source": "특정혈 통합 아틀라스",
      "href": "/acupuncture-specific/special-points-atlas/"
    },
    {
      "line": "경혈의 이름과 실제 위치를 함께 기억해 보세요.",
      "note": "같은 팔이나 발에 있는 경혈도 근육·힘줄·뼈의 표지가 다릅니다. 표준 위치와 주변 해부를 연결하면 이름만 외울 때보다 잘 구분됩니다.",
      "introducedOn": "2026-10-12",
      "source": "표준 경혈 아틀라스",
      "href": "/acupoint-network/standard-atlas/"
    },
    {
      "line": "본초의 첫 질문은 무엇을 쓰는가입니다.",
      "note": "뿌리·뿌리줄기·껍질·꽃봉오리·열매처럼 약용 부위를 먼저 확인하고, 같은 식물 계열의 다른 본초와 구분합니다.",
      "introducedOn": "2026-10-12",
      "source": "본초의 약용 부위와 배합",
      "href": "/herbal-integrated/herbs/"
    },
    {
      "line": "계지와 육계는 이름의 한 글자보다 약용 부위로 구분합니다.",
      "note": "계지의 가지와 육계의 줄기껍질, 전통 배합의 역할을 나누어 봅니다. 원전 약명과 실제 원료가 무엇인지 함께 확인합니다.",
      "introducedOn": "2026-10-12",
      "source": "계지와 온성 배합",
      "href": "/herbs/cinnamon-twig/"
    },
    {
      "line": "고전 조문은 결론 앞의 조건까지 함께 읽습니다.",
      "note": "若·但·反·不得 같은 표현은 적용·분기·예외를 보여줍니다. 처방명만 기억하기보다 조건과 경과를 자신의 말로 풀어 보세요.",
      "introducedOn": "2026-10-12",
      "source": "상한론 조문 독해",
      "href": "/shanghan-network/"
    },
    {
      "line": "치료 뒤 달라진 몸은 다시 살펴야 합니다.",
      "note": "상한론의 수증치지는 처음의 진단명보다 현재 맥증을 다시 보라는 독해 원칙입니다. 처방을 반복하기 전에 경과를 읽는 중요성을 보여줍니다.",
      "introducedOn": "2026-10-12",
      "source": "상한론 16조 · 수증치지",
      "href": "/classics/shanghanlun/clauses/taiyang-upper/#clause-016"
    },
    {
      "line": "태음병이라는 말은 문헌에 따라 체계가 달라집니다.",
      "note": "상한론의 태음병과 사상의학의 소음인 리한병 안의 태음병을 구분합니다. 같은 글자를 보더라도 책과 병론을 먼저 확인합니다.",
      "introducedOn": "2026-10-12",
      "source": "소음인 태음병·소음병 비교",
      "href": "/sasang-pattern-differential/soeumin-taeeum-vs-soeum/"
    },
    {
      "line": "판본을 적으면 처방의 차이가 더 잘 보입니다.",
      "note": "원방과 후대 가감방, 약미 수와 제형의 차이를 기록합니다. 같은 처방명이라도 모든 원료·용량·연구제품이 같다고 가정하지 않습니다.",
      "introducedOn": "2026-10-12",
      "source": "처방 출전·약미·배합",
      "href": "/herbal-integrated/general-formulary/"
    }
  ];

  const dateParts = function (date) {
    const parts = new Intl.DateTimeFormat("en-CA", {
      timeZone: "Asia/Seoul",
      year: "numeric",
      month: "2-digit",
      day: "2-digit"
    }).formatToParts(date);
    const values = {};
    parts.forEach(function (part) {
      if (part.type !== "literal") values[part.type] = part.value;
    });
    return values;
  };

  const kstDate = function (offset) {
    const parts = dateParts(new Date());
    return new Date(Date.UTC(
      Number(parts.year),
      Number(parts.month) - 1,
      Number(parts.day) + offset
    ));
  };

  const dayNumber = function (date) {
    return Math.floor(Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate()) / 86400000);
  };

  const formatKoreanDate = function (date) {
    return new Intl.DateTimeFormat("ko-KR", {
      timeZone: "UTC",
      year: "numeric",
      month: "long",
      day: "numeric"
    }).format(date);
  };

  const render = function (widget, offset) {
    const date = kstDate(offset);
    const dateKey = date.toISOString().slice(0, 10);
    const available = cards.filter(function (card) { return !card.introducedOn || card.introducedOn <= dateKey; });
    const dayIndex = ((dayNumber(date) % available.length) + available.length) % available.length;
    const card = available[dayIndex];
    const dateNode = widget.querySelector("[data-km-date]");
    const lineNode = widget.querySelector("[data-km-line]");
    const noteNode = widget.querySelector("[data-km-note]");
    const sourceNode = widget.querySelector("[data-km-source]");
    const countNode = widget.querySelector("[data-km-count]");

    if (dateNode) {
      dateNode.textContent = formatKoreanDate(date);
      dateNode.setAttribute("datetime", date.toISOString().slice(0, 10));
    }
    if (lineNode) lineNode.textContent = card.line;
    if (noteNode) noteNode.textContent = card.note;
    if (sourceNode) {
      sourceNode.textContent = card.source + "에서 이어 읽기 →";
      sourceNode.setAttribute("href", card.href);
    }
    if (countNode) countNode.textContent = "오늘의 카드 " + (dayIndex + 1) + " / " + available.length;
  };

  const reader = window.MinseongDailyReader;
  const initialized = new WeakSet();
  let offset = reader.offsetFor(new URL(window.location.href).searchParams.get("date")) || 0;

  const update = function (widget) {
    render(widget, offset);
    const date = kstDate(offset).toISOString().slice(0, 10);
    const picker = widget.querySelector("[data-km-day-picker]");
    if (picker) picker.value = date;
    const todayButton = widget.querySelector("[data-km-today]");
    if (todayButton) todayButton.disabled = offset === 0;
    const fallback = widget.querySelector("[data-km-copy-fallback]");
    if (fallback) fallback.hidden = true;
  };

  const changeDay = function (next) {
    const date = reader.dateFor(next);
    if (!date || !reader.parseDate(date.toISOString().slice(0, 10))) return;
    offset = next;
    const url = new URL(window.location.href);
    if (offset === 0) url.searchParams.delete("date");
    else url.searchParams.set("date", date.toISOString().slice(0, 10));
    window.history.replaceState(null, "", url);
    window.dispatchEvent(new CustomEvent("daily-km-offset", {detail: {offset: offset}}));
  };

  window.addEventListener("daily-km-offset", function (event) {
    const next = event.detail && Number(event.detail.offset);
    if (!Number.isInteger(next) || !reader.dateFor(next)) return;
    offset = next;
    document.querySelectorAll("[data-daily-km]").forEach(update);
  });

  const init = function () {
    document.querySelectorAll("[data-daily-km]").forEach(function (widget) {
      update(widget);
      if (initialized.has(widget)) return;
      initialized.add(widget);
      widget.querySelectorAll("[data-km-shift]").forEach(function (button) {
        button.addEventListener("click", function () { changeDay(offset + Number(button.getAttribute("data-km-shift"))); });
      });
      const picker = widget.querySelector("[data-km-day-picker]");
      if (picker) picker.addEventListener("change", function () {
        const next = reader.offsetFor(picker.value);
        if (next !== null) changeDay(next);
        else update(widget);
      });
      const todayButton = widget.querySelector("[data-km-today]");
      if (todayButton) todayButton.addEventListener("click", function () { changeDay(0); });
      const share = widget.querySelector("[data-km-share-date]");
      if (share) share.addEventListener("click", function () {
        const url = new URL("/daily-korean-medicine/", window.location.origin);
        url.searchParams.set("date", kstDate(offset).toISOString().slice(0, 10));
        reader.copyLink(url.href, widget.querySelector("[data-km-copy-fallback]"), widget.querySelector("[data-km-share-status]"));
      });
    });
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
  if (typeof document$ !== "undefined") document$.subscribe(init);
})();
