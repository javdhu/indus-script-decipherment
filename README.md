# Indus decipherment laboratory

This is an evidence-first attempt to recover **testable functional and phonetic
readings** from Indus inscriptions. It deliberately distinguishes:

1. archaeological and corpus facts;
2. structural inferences that can be tested without knowing the language;
3. semantic hypotheses;
4. proposed phonetic readings.

The project does not treat either scholarly pessimism or confident internet
"decipherments" as a verdict. Candidate readings have to predict held-out
inscriptions, context, or independent archaeological evidence better than
alternatives. The result so far is a narrow functional reading of recurring
formulas, not a recovered language.

## Layout

- `research/`: the write-ups. Start with
  [`research/decipherment_attempt.md`](research/decipherment_attempt.md).
- `hypotheses/preregistered.md`: the tests a candidate reading must pass,
  fixed before the assignments were made.
- `src/`: the analysis scripts (Python 3, standard library only, except
  `render_signs.py`, which needs Pillow).
- `vendor/plos-wells-s2-data/`: the Wells-numbered sequence corpus released
  with Ashraf & Sinha (2018), CC BY 4.0 (see its README).
- `SOURCE_MANIFEST.md`: every input, with the commit or checksum used.

## Reproduce the first-pass analysis

From a fresh clone, with Python 3.9 or later and git:

```bash
scripts/fetch_inputs.sh          # clones the three upstream corpora at their pinned commits into vendor/

python3 src/analyze_corpus.py \
  --corpus vendor/toddcolsen-indus-script/data/txt/indus_corpus_alt.csv \
  --object-types vendor/toddcolsen-indus-script/data/txt/indus_object_types.csv \
  --candidate-anchors vendor/glossa-lab/research/indus/anchor_table.csv \
  --output results

python3 src/validate_wells_corpus.py \
  --wells-csv 'vendor/plos-wells-s2-data/25_Undeciphered(Indus).csv' \
  --features vendor/mayig-indus-valley-script-corpus/features \
  --mahadevan-profiles results/sign_profiles.csv \
  --output-json results/wells_replication.json \
  --output-csv results/wells_crosswalk_profiles.csv

python3 src/audit_ross_model.py \
  --corpus-root vendor/mayig-indus-valley-script-corpus \
  --output results/ross_model_audit.json
```

`results/` is gitignored: it is derived from corpora this repository does not
redistribute, so it is regenerated rather than committed.

## Methodological rule

A proposed translation is not supported merely because plausible words can be
assigned to every sign. It must make risky predictions: sign position,
substitution class, iconographic association, site/object distribution,
allography, or a reading on material held out before the assignment was made.

## Main result

Read [`research/decipherment_attempt.md`](research/decipherment_attempt.md) for
the attempted translations, evidence levels, independent-corpus replication,
and explicit failure conditions.

## Licence and data

- Code (`src/`, `scripts/`): [MIT](LICENSE).
- Prose and results write-ups (`research/`, `hypotheses/`, this README,
  `SOURCE_MANIFEST.md`): [Creative Commons Attribution 4.0](LICENSE-docs)
  (CC BY 4.0). Attribute as: Javed, *Indus decipherment laboratory*,
  https://github.com/javdhu/indus-decipherment.
- Third-party data keeps its own terms. The PLOS Wells data in `vendor/` is
  CC BY 4.0 (Ashraf & Sinha 2018). The corpora fetched by
  `scripts/fetch_inputs.sh` are not redistributed:
  [toddcolsen/indus_script](https://github.com/toddcolsen/indus_script)
  declares no licence and derives from Mahadevan 1977;
  [mayig/indus-valley-script-corpus](https://github.com/mayig/indus-valley-script-corpus)
  is MIT for its code, which does not relicense its CISI-derived content;
  [BitConcepts/glossa-lab](https://github.com/BitConcepts/glossa-lab) is MIT,
  and one table of it is read.
