# Daily calendar display

The daily reader shows the selected KST civil date, Korean lunar date (including leap months), approximate moon illumination at KST noon, and solar-term-based year/month/day ganji. The lunar conversion display supports 1900–2050; moon/solar-term ganji support 1900–2100. Outside these ranges the UI states the applicable range and retains the solar date.

Year ganji changes at Ipchun; month ganji changes at the twelve jie boundaries, using the existing DE440 solver and model assets. Day ganji changes at KST midnight. Today uses the current instant, other selected dates use KST noon; a jie date also shows its transition time and the before/after month labels. A 30-second refresh updates open date labels without rebuilding reading cards. Failed/stale asynchronous results never overwrite the currently selected date.

`calendar-core.js` bundles the following locally with their complete licenses; it makes no external requests:

- Korean lunar conversion: [usingsky/korean_lunar_calendar_js](https://github.com/usingsky/korean_lunar_calendar_js), MIT, Jinil Lee. TypeScript type annotations removed with Node's built-in stripper; runtime logic/data retained. Calendar source blob `001400996c5995cf49b1ea4c89d2e6795e4ee751`, data blob `389d9d9685399f815057cb98bc03988f33f7a289`.
- Moon illumination: [mourner/suncalc](https://github.com/mourner/suncalc), BSD-2-Clause, Volodymyr Agafonkin. Only the time, Sun/Moon coordinates, nutation and illumination subset is bundled. Moon shape names are approximate phase bins; the percentage is illuminated disk fraction, not weather-dependent observed brightness.

Reference tests use [KASI 2026 month starts](https://astro.kasi.re.kr/kor/life/post/calendarData?search_year=2026), [KASI 2025 leap sixth month](https://astro.kasi.re.kr/kor/life/post/calendarData?search_year=2025), the KASI November 2026 monthly table, and [USNO primary moon phases](https://aa.usno.navy.mil/calculated/moon/phases?year=2026). Important regression: Korean lunar 2026-09-01 is solar 2026-10-11, not the Chinese-calendar date one day earlier. The solar-term ganji is intentionally distinct from the lunar-month ganji in KASI's lunar monthly table.

Tests: `node --test tools/test_daily_calendar.cjs tools/test_daily_reader.cjs`; `python -m unittest discover -s tools -p test_page_assets.py`. `tools/check_daily_reader.cjs` checks the rendered UI, date navigation, leap-month display and term-boundary notice on both mobile and desktop.
