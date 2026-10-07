/* Daily Korean medicine learning cards. No network, storage, or third-party dependencies. */
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
    const dayIndex = ((dayNumber(date) % cards.length) + cards.length) % cards.length;
    const card = cards[dayIndex];
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
    if (countNode) countNode.textContent = "오늘의 카드 " + (dayIndex + 1) + " / " + cards.length;
  };

  const init = function () {
    document.querySelectorAll("[data-daily-km]").forEach(function (widget) {
      let offset = 0;
      render(widget, offset);
      widget.querySelectorAll("[data-km-shift]").forEach(function (button) {
        button.addEventListener("click", function () {
          offset += Number(button.getAttribute("data-km-shift"));
          render(widget, offset);
          window.dispatchEvent(new CustomEvent("daily-km-offset", {detail: {offset: offset}}));
        });
      });
    });
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
