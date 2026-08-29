# Experience Census

This census is the pressure test for the composition model. It is not a commitment to build fifteen bespoke sites.

## Maturity scale

- `E0` — declared: exact intended authorities and renderer/profile are known.
- `E1` — compiled: a reproducible `CollectionRelease` exists from real source material.
- `E2` — rendered: a human can open/use the generated experience.
- `E3` — proven: important cross-repo seam has executable evidence.
- `E4` — operational: deployed or repeatedly used by a real consumer.

## Census

| # | Experience | Primary source authority | Likely experience | Pressure tested |
|---|---|---|---|---|
| 1 | Thesis bibliography | Paper KB | static navigator | paper collection baseline |
| 2 | Thesis rapid paper review | Paper KB | Abstract Scroller | external renderer handoff |
| 3 | Author works | Paper KB | chronology/faceted navigator | contributors/authors |
| 4 | Working-paper series | Paper KB | year/author/topic navigator | venue/series selection |
| 5 | Economic-complexity reading path | Paper KB + curation | curated navigator | human judgment/order/trails |
| 6 | FCV literature corpus | Paper KB | private research profile | visibility + richer workbench demand |
| 7 | Literature-review snapshot | Paper KB | Abstract Scroller | immutable release/review |
| 8 | LCD institutional corpus | LCD knowledgebase | static navigator | non-paper producer |
| 9 | LCD thesis/resources subset | LCD knowledgebase | static navigator | same corpus, cheap new collection |
| 10 | Course readings | paper/doc producers | grouped simple navigator | pedagogical grouping |
| 11 | Economics of Aggregation programme | Thesis | existing Docusaurus vertical | adopt mature bespoke experience |
| 12 | Working-memory journal | Journal | existing Quartz vertical | publication policy / semantic garden |
| 13 | Knowledge-ecosystem technical docs | ecosystem docs/doc producer | technical navigator | documentation corpus |
| 14 | Personal publications | mixed publication/paper refs | curated portfolio navigator | multi-source pressure |
| 15 | Policy/research dossier | mixed governed evidence | dossier/workbench | multi-source + curation + possible intelligence |

## Required per-case ledger

As implementation proceeds, add a row or record containing:

```text
experience_id
maturity
source authorities
exact source release/hash
collection release
renderer/profile
new code?
new producer projection?
new adapter?
capabilities reused
observed friction
V2 candidate lesson
```

## Interpretation rules

- A manifest with invented/demo items does not raise a case above `E0`.
- A real source compiled reproducibly can reach `E1` without a polished UI.
- A rendered fixture is useful for renderer development but does not establish the real source seam.
- `E3` should test the producer/consumer boundary that matters, not only schema validation in isolation.
- `E4` requires actual deployment/use evidence; do not infer it from CI.

## Marginal-cost test

The key outcome is the slope of new engineering effort:

```text
first experience: core + adapter + renderer baseline
next experience: mostly configuration + selection
later similar experience: configuration/curation only
```

For each case, explicitly note whether it required:

- configuration only;
- bounded source adapter;
- producer projection change;
- reusable renderer capability;
- bespoke vertical implementation.

If too many cases require the last category, investigate the composition model before building more verticals.
