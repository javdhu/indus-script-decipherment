# Audit of two 2026 full-reading claims

## Outcome

Neither examined model is admissible as a translation model. Both fail before
linguistic interpretation: their sign identities and/or reading direction do
not match their named corpora.

## Ross, *Reading the Indus Valley Script* (March 2026)

The preprint says it uses `mayig/indus-valley-script-corpus`. That corpus's own
README says graphemes are stored from the artifact's physical left to right and
that the writing is read right to left. The preprint nevertheless calls P324 an
opener because it occurs 77 times at the **stored-left** edge. In the documented
reading direction P324 is reading-initial only once and reading-terminal 77
times. Its P385 "terminal" count has the same reversal: 29 stored-right versus
zero stored-left.

The contextual dictionary also uses incompatible glyph descriptions:

| Sign | Preprint description | Source corpus description | Mahadevan mapping |
|---|---|---|---|
| P122 | fish | two adjacent half-height vertical strokes | M099/M100 |
| P385 | crab/scorpion | diamond/leaf with a small diamond on top | M267 |
| P086 | man with arms raised | tree with branches at top | M161/M162/M167–169 |
| P050 | arrow/spear | unmodified fish | M059 |
| P217 | bearer/yoke | triangle on a vertical line, arrow/spear | M211 |

Because the paper's four-part formula, social classes, and constellation
catalogue are inferred from those reversed positions and incorrect sign
identities, they do not survive input validation. The reported treewidth may
still describe the graph built from those sequences, but treewidth is not a
language detector: a structured non-phonetic administrative system can have an
arbitrarily dense co-occurrence graph.

Reproduction: `python3 src/audit_ross_model.py --corpus-root
vendor/mayig-indus-valley-script-corpus --output
results/ross_model_audit.json`.

## Glossa-Lab/Pierson anchor table (May–June 2026)

The table describes itself as Mahadevan-numbered, but several high-confidence
labels conflict with Mahadevan-numbered glyphs in the corpus:

- M099 is two short strokes, not a jar.
- M059 is the unmodified fish sign, not the numeral seven.
- M342 is the classic jar sign.
- M267 is the diamond/leaf sign with a smaller diamond on top, not the fish.

Its grammatical orientation also fails a clean corpus test. M267 is assigned a
genitive/functionally suffixal reading, yet it is reading-initial in 78% of its
209 clean lines and terminal in 3%. M014, M015, and M001 are described as
initial assignments but occur overwhelmingly at the reading-terminal edge.

The model's advertised HIGH/MEDIUM dictionary covers 68.1% of tokens in the
reconstructed clean Mahadevan corpus. That is not independent evidence: a
dictionary selected on the corpus is expected to cover it. Given the upstream
identity/orientation failures, its proposed sound values are rejected.

## General lesson

AI helps here when it is used to make every mapping inspectable and every claim
falsifiable. It hurts when plausible glosses are generated faster than the sign
IDs, orientation, and held-out evidence are checked.

