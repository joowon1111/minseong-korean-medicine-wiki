# DE440 solar-term calculator assets

`docs/assets/solar-terms/calculator.js` solves 15-degree crossings of the geocentric apparent solar longitude of date. Each lazy-loaded decade file contains Chebyshev longitude coefficients, not a solar-term event lookup table. The model covers KST calendar years 1900–2100. The large NASA binary kernel is intentionally external.

To regenerate with the same numerical dependencies:

```sh
python -m pip install -r tools/solar_terms_requirements.txt
curl --fail --location https://ssd.jpl.nasa.gov/ftp/eph/planets/bsp/de440.bsp --output /tmp/de440.bsp
python tools/build_solar_term_model.py --kernel /tmp/de440.bsp --as-of 2026-11-01
node --test tools/test_solar_terms.cjs
```

The metadata records the kernel URL and SHA-256, coordinate frame, timescale, dependency versions and independent direct-search reference events. Generation splits known UTC leap boundaries and checks interpolation probes in every segment. Future UTC conversion depends on unknown future leap seconds; pre-1972 results are retroactive UTC+9, not historical Korean civil time.

The automated tests check all 201 years, 192 directly searched reference events, all 48 public KASI minute values for 2026/2027, rounding and malformed inputs. The separately checked KASI 1920–2100 public dataset had all 4,344 events within one minute of this model (data as of 2026-09-01).

- NASA ephemerides: https://ssd.jpl.nasa.gov/planets/eph_export.html
- Skyfield solar terms: https://rhodesmill.org/skyfield/almanac.html#solar-terms
- KASI public data: https://astro.kasi.re.kr/kor/almanac/solarTerms/download

For browser acceptance after a MkDocs build, serve `site/` locally and run `BASE_URL=http://127.0.0.1:8767 node tools/check_solar_terms.cjs`. `PLAYWRIGHT_EXECUTABLE_PATH` and `SOLAR_SCREENSHOT_DIR` optionally select the browser and screenshot directory.
