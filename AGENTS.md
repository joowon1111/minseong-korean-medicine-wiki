# Repository security rules

This repository is public. Treat every committed file, pull request, issue, and workflow log as public information.

## Secrets

- Never add API keys, tokens, passwords, private keys, service-account files, or `.env` files to Git.
- Keep runtime secrets only in GitHub repository or environment secrets. Reference them in Actions as `${{ secrets.NAME }}`; do not place their values in workflow files, command lines, logs, documentation, or examples.
- Use placeholder values such as `YOUR_API_KEY` in examples.
- If a credential is found, stop before committing or pushing. Remove it from the proposed change, rotate it in its issuing service, and review Git history if it may already have been committed.

## Required check before a commit or push

Run `python tools/check_secrets.py` after staging and before every commit or push.
It checks the actual Git index; `--staged` checks only staged changes. The check
must finish without findings. Never bypass a finding with inline allow markers
or weaker patterns. Any false positive must be reviewed without exposing values.
A failed or incomplete security check blocks publication; do not silently pass it.

## Content integration

- Read the whole target document before expanding it. Integrate new material into the relevant existing paragraphs, tables, and sections; merge or replace overlapping explanations.
- Do not accumulate unrelated update blocks, repeated warnings, link lists, or duplicate summaries at the end of a page. Add a section only when it serves a distinct question in the document's reading order.
- Place related links where readers need the next explanation. Keep the established taxonomy and URLs; verify existing heading anchors when restructuring.
- Prefer strengthening existing documents to creating overlapping pages. Preserve the policy against blanket public review dates and do not invent clinical experience, authorship, or credentials.

## Classical and modern clinical knowledge expansion

- Select knowledge with present clinical or scholarly value. Connect the existing archive instead of accumulating standalone classical ebooks or duplicate pages.
- Prefer: original passage and edition → Korean interpretation → pattern/pathogenesis → treatment principle → relevant herbs/formulas/acupuncture → modern clinical context → research. These are context links, not claims that a classical passage proves efficacy.
- Strengthen both directions between existing classic, condition, symptom, pattern, herb, formula, acupuncture and Evidence Hub pages. Keep specific source anchors and label original formulas, later adaptations and trial products accurately.
- Use the WHO Global Traditional Medicine Strategy 2025–2034 direction: stronger scientific evidence, safety, effectiveness, research and appropriate health-system integration. Verify official sources. Explain WHO and ICD-11 meaningfully in selected upper hubs only; do not duplicate them in child-page introductions or imply WHO endorsement of the archive or a treatment.
- Introduce ICD-11 Traditional Medicine as standardized recording and research infrastructure. Do not fabricate official code mappings. Classification, clinical recommendations and treatment-efficacy evidence have distinct roles.
- Do not create public sections, pages, grades or tags cataloguing negative historical evaluations. Omit content without current inclusion value rather than reproducing it and appending repeated caveats. Retain clinically material safety information where it affects a decision; report research outcomes accurately, including uncertainty.
- Do not newly include deterministic season/time treatment claims, five-movement/six-qi cosmology, one-to-one organ–emotion claims, or pulse-only claims of specific anatomical lesions. Avoid importing historical anatomy as modern anatomy.
- Work in order: Shanghan Lun connections → Jingui Yaolue connections → Donguibogam clinical index across its five divisions → Wenbing Tiaobian → Piwei Lun → Jingyue Quanshu → selected clinical Huangdi Neijing chapters → Zhenjiu Jiayi Jing and Zhenjiu Dacheng → Dongyi Suse Bowon. Preserve Sasang medicine's own ordinary-symptom, pattern and treatment system.
- In parallel, maintain the existing evidence layer: CPG, SR/meta-analysis, RCT, observational/safety and relevant mechanistic research. These are different study roles, not an automatic chain proving an intervention. Link verified evidence cards instead of pasting papers under every classic page; match population, formulation, comparator, outcomes and safety.
- Report the concrete completed tranche and remaining scope. Do not call a reading summary a complete translation or a connected index a completed critical edition.
