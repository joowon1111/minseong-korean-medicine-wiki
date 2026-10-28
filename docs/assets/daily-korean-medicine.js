/* Daily Korean medicine learning cards. No network or storage. */
(function () {
  "use strict";

  const cards = [
    {
      line: "같은 통증이라도, 먼저 살필 맥락은 다를 수 있어요.",
      note: "통증이 시작된 때와 더 아픈 동작을 한 가지씩 적어 보세요. 허리는 앉기·걷기, 무릎은 계단·일어나기처럼 실제 동작을 기준으로 삼으면 침·약침·한약과 운동의 목표를 구체적으로 정하기 좋습니다. 새 근력저하나 감각 변화도 함께 전합니다.",
      source: "통증·근골격 통합 안내",
      href: "/conditions/low-back-pain/"
    },
    {
      line: "좋아짐은 통증 점수 밖에서도 보입니다.",
      note: "치료 전에 가장 불편한 일 하나를 정해 두세요. 쉬지 않고 걷는 시간, 통증 때문에 깨는 횟수, 물건을 들어 올릴 때의 불편을 같은 조건에서 비교합니다. 덜 움직여 점수만 낮아진 경우와 가능한 활동이 늘어난 회복은 구분합니다.",
      source: "침구치료 경과·재평가",
      href: "/acupuncture-integrated/followup/"
    },
    {
      line: "평소의 나를 알면, 오늘의 변화를 더 잘 읽을 수 있어요.",
      note: "편안했던 날의 식사량·식후 느낌·대변·수면을 짧게 남겨 보세요. 불편이 생겼을 때 평소에도 그랬는지 새로 바뀐 것인지 비교하는 자료가 됩니다. 한 항목만으로 체질이나 병증을 정하지 않고 소증과 현증을 함께 봅니다.",
      source: "사상체질과 소증",
      href: "/sasang-pattern-differential/"
    },
    {
      line: "체질을 살피는 일과, 지금 병증을 살피는 일은 함께 갑니다.",
      note: "평소 추위를 타는 것과 이번에 발열 뒤 오한이 생긴 것은 다른 정보입니다. 언제부터 달라졌는지, 식사·배변·잠도 함께 바뀌었는지를 정리해 보세요. 체형·성격이나 설문 하나보다 여러 관찰이 일관되는지를 확인합니다.",
      source: "사상체질 진단·병증 감별",
      href: "/sasang-pattern-differential/"
    },
    {
      line: "같은 증상에도 처방 선택이 달라지는 이유가 있어요.",
      note: "피로가 같아도 식욕저하가 중심인지, 불면·두근거림이 중심인지에 따라 확인할 내용이 달라집니다. 가장 불편한 증상과 함께 생긴 변화, 복용 중인 약을 적어 오세요. 처방은 이런 조합과 치료 목표를 바탕으로 개별화합니다.",
      source: "맞춤 처방 선택 원리",
      href: "/herbal-integrated/formula-selection-guide/"
    },
    {
      line: "약재는 처방 안에서 서로 역할을 나눕니다.",
      note: "같은 약재가 들어 있다고 같은 처방은 아닙니다. 연결 문서에서 어떤 약용 부위를 쓰는지와 함께 배합되는 약재·제형을 확인해 보세요. 음식·차와 처방의 약재를 같은 효과로 바꾸어 읽거나 재료를 임의로 더하지 않습니다.",
      source: "본초·방제 한눈에 보기",
      href: "/herbal-integrated/"
    },
    {
      line: "한약 상담 때 복용 중인 약 목록은 좋은 출발점입니다.",
      note: "약 이름이 기억나지 않으면 포장이나 처방전 사진을 준비해도 좋습니다. 처방약·일반약·건강기능식품의 제품명과 복용량을 한곳에 모으고 알레르기·임신·수유·기저질환도 전해 주세요. 기존 약을 임의로 중단하지 않고 병용을 검토합니다.",
      source: "한약 상담 전 준비",
      href: "/conditions/herbal-consultation-prep/"
    },
    {
      line: "침 치료는 ‘어디가 아픈가’와 ‘무엇을 회복할까’를 함께 봅니다.",
      note: "아픈 곳을 가리키는 것에 더해 어떤 동작을 되찾고 싶은지 전해 보세요. 고개 돌리기·팔 올리기·앉았다 일어나기처럼 구체적인 목표가 도움이 됩니다. 진찰에서 움직임·감각·근력과 해부학적 위치를 살펴 배혈하고 치료 전후를 비교합니다.",
      source: "통합 침구치료 탐색",
      href: "/acupuncture-integrated/"
    },
    {
      line: "치료 방법은 목표에 맞춰 조합할 수 있어요.",
      note: "침·전침·약침·뜸·부항은 방식과 적용 부위가 다릅니다. 모든 방법을 한꺼번에 받는 횟수보다 현재의 목표와 치료 뒤 반응을 함께 확인해 보세요. 이전 시술의 불편, 알레르기와 복용약을 알리면 구성을 조절하는 데 도움이 됩니다.",
      source: "침구치료 방법 비교",
      href: "/acupuncture-integrated/methods/"
    },
    {
      line: "어지럼은 ‘빙빙 도는 느낌’만으로 설명되지 않아요.",
      note: "고개를 돌릴 때 잠깐 도는지, 일어설 때 아찔한지, 가만히 있어도 오래 지속되는지 적어 보세요. 청력 변화·두통·구역과의 시간 관계도 중요합니다. 갑작스러운 마비·말 어눌함·심한 보행 장애가 함께 있으면 신속한 평가가 우선입니다.",
      source: "어지럼 안내",
      href: "/conditions/dizziness/"
    },
    {
      line: "복통은 위치와 함께 ‘언제, 어떻게’ 시작됐는지도 기록해요.",
      note: "배가 아픈 위치와 시작 시각을 적고 식사·대변·구토·발열과의 순서를 남겨 보세요. 음식을 먹고 바로인지 몇 시간 뒤인지, 계속 아픈지 반복되는지도 유용합니다. 심한 통증이 지속되거나 피를 토하고 검은 변이 나오면 기록만 하며 기다리지 않습니다.",
      source: "복통 안내",
      href: "/conditions/abdominal-pain/"
    },
    {
      line: "잠을 몇 시간 잤는지와 낮에 어떻게 느끼는지를 함께 봅니다.",
      note: "잠든 시각·깬 시각·밤중 각성·낮잠과 카페인을 같은 메모에 1~2주 남겨 보세요. 침대에 있던 시간과 실제 잔 시간, 다음 날 졸림은 따로 살핍니다. 주말까지 비교하면 바꿀 일과와 진료에서 물어볼 점이 구체적으로 보입니다.",
      source: "불면증·수면장애",
      href: "/conditions/insomnia/"
    },
    {
      line: "이명은 소리의 크기뿐 아니라 청력과 생활 영향을 살펴요.",
      note: "한쪽인지 양쪽인지, 박동에 맞는 소리인지, 청력이 달라졌는지 함께 기록해 보세요. 수면·업무 방해 정도도 치료 목표가 됩니다. 갑자기 잘 안 들리는 변화가 동반되면 이명 관리만 미루지 말고 청력 평가를 서두릅니다.",
      source: "이명 안내",
      href: "/conditions/tinnitus/"
    },
    {
      line: "얼굴 통증은 통증 양상과 감각 변화를 차근히 구분합니다.",
      note: "얼굴의 어디가 얼마나 오래 아픈지, 씹기·말하기·세수에 유발되는지 남겨 보세요. 짧은 전기 느낌과 지속되는 통증, 감각저하는 서로 다른 단서입니다. 통증을 확인하려고 같은 곳을 반복 자극하기보다 진료에서 그 양상을 설명합니다.",
      source: "삼차신경통 안내",
      href: "/conditions/trigeminal-neuralgia/"
    },
    {
      line: "몸이 불편할 때는 증상 이름부터 몰라도 괜찮아요.",
      note: "증상 이름을 몰라도 시작된 때와 생활에서 달라진 일을 말할 수 있습니다. 무엇을 할 때 더 불편하고 무엇을 못 하게 됐는지 한 가지씩 적어 보세요. 증상별 안내에서 관련 문서를 찾고 진료 때 가장 해결하고 싶은 문제부터 전합니다.",
      source: "증상으로 찾기",
      href: "/symptom-integrated/"
    },
    {
      line: "복용 후 변화도 기록하면 다음 진료가 더 구체적입니다.",
      note: "복용 뒤 좋아진 증상과 새 불편을 따로 적어 보세요. 날짜·복용량·식사와 함께 소화·수면·배변 변화를 남기면 다음 상담에 도움이 됩니다. 이상반응이 의심되면 억지로 계속 복용하거나 임의로 양을 늘리지 말고 처방한 의료진에게 알립니다.",
      source: "한약 복용 후 변화 기록",
      href: "/conditions/herbal-followup/"
    },
    {
      line: "침을 놓는 위치는 전통 이론과 실제 해부를 함께 살핍니다.",
      note: "경혈 이름을 익힐 때는 연결된 표준 위치와 주변 근육·힘줄·신경을 함께 살펴보세요. 같은 부위도 체형과 자세에 따라 실제 구조를 확인해야 합니다. 위치를 공부하는 것과 침의 깊이·방향을 정해 직접 시술하는 일은 구분합니다.",
      source: "침구치료와 임상해부학",
      href: "/acupuncture-integrated/"
    },
    {
      line: "사상체질은 체형이나 성격 한 가지로 정하지 않아요.",
      note: "체질 설문 결과 하나를 음식 금지표로 바꾸기보다 평소 소화·땀·배변·수면과 병이 들었을 때 변화를 나란히 봅니다. 체형기상·용모와 여러 소견을 종합하고 치료 뒤의 경과도 확인합니다. 맞지 않는 음식을 찾는 일과 체질 판정도 같은 일은 아닙니다.",
      source: "사상의학 한눈에 보기",
      href: "/sasang/"
    },
    {
      line: "한약은 이름보다 어떤 병증과 목표에 쓰는지 읽어 보세요.",
      note: "관심 있는 처방 문서에서는 적용 증후와 구성·출전을 먼저 확인해 보세요. 같은 이름이라도 원방·후대 가감방·연구제품은 성분과 용량이 다를 수 있습니다. 논문의 결과를 읽을 때도 어떤 환자가 어떤 제형을 썼는지 함께 살핍니다.",
      source: "임상 핵심 처방·방제 안내",
      href: "/herbal-integrated/"
    },
    {
      line: "안전 확인은 치료를 잘 이어가기 위한 첫 단계입니다.",
      note: "새 치료 전에는 복용약과 알레르기, 임신·수유, 기저질환과 최근 시술을 알려 주세요. 항응고제나 이식형 전자기기처럼 치료 구성에 영향을 줄 수 있는 정보도 포함합니다. 이름이 어렵다면 약 봉투나 의료기기 정보를 준비해 함께 확인합니다.",
      source: "침구치료 안전·위험신호",
      href: "/acupuncture-integrated/safety/"
    },
    {
      line: "몸의 신호가 갑자기 달라지면 평가의 우선순위도 달라집니다.",
      note: "평소와 갑자기 달라진 신호는 치료 계획을 다시 정할 정보입니다. 마비·언어장애, 심한 호흡곤란, 갑자기 시작한 매우 심한 두통이나 지속되는 심한 복통은 신속한 의료 평가가 우선입니다. 평소 받던 치료가 있다는 이유로 새 변화를 기다려 보지는 않습니다.",
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
