# A falsifiable first-pass translation of Indus inscriptions

**Run date:** 2026-08-09  
**Status:** functional decipherment attempt, not a recovered spoken language

## Verdict

The evidence supports a narrow translation of several recurring inscription
frames as **formulaic administrative/accounting labels**. It does not yet
support continuous English sentences or secure sound values. The inscriptions
may encode language, a notation system, or a mixture; the functional templates
below survive that uncertainty.

My strongest working schema is:

```text
[initial authority/class] [link or quantity] [variable identity/account item]
[commodity/unit] [terminal operator]
```

Not every text uses every slot, and “authority,” “account,” and “operator” are
role labels—not translated Indus words.

## Proposed translations

Canonical reading order is right-to-left on the object and is written here as
Mahadevan sign IDs from first-read to last-read.

### 1. Two parallel seal/pottery frames

```text
M267 M099 [X] M342
M391 M099 [X] M342
```

Minimum defensible translation:

> **Class/authority A or B — dual/link marker — account item X — jar/measure
> terminal.**

Riskier administrative English:

> **Office/holder A or B records or authorizes two/of item X under a
> jar-measure standard.**

Examples:

| M77 artifact | Site / medium | Reading-order signs | Working translation |
|---:|---|---|---|
| 1086 | Mohenjo-daro seal | M267 M099 M124 M342 | Class A · link/two · item 124 · jar/measure closure |
| 1074 | Mohenjo-daro seal | M391 M099 M289 M342 | Class B · link/two · item 289 · jar/measure closure |
| 5508 | Harappa pottery | M267 M099 M194 M342 | Class A · link/two · item 194 · jar/measure closure |
| 4813 | Harappa pottery | M391 M099 M053 M342 | Class B · link/two · item 053 · jar/measure closure |

The A/B frame therefore is not confined to one site or seal medium.

### 2. A three-unit terminal chain

```text
[X] M336 M089 M211
```

Minimum translation:

> **[identity/account content] — rimless-jar/unit — THREE — terminal operator.**

Riskier English:

> **[Holder/account] — [assessed commodity] — three standardized units —
> licensed/assessed.**

This chain occurs in 31 clean inscriptions across Mohenjo-daro, Harappa,
Chanhu-daro, and Lothal and on three medium classes. Artifact 1094 reads
`M267 M099 M171 M059 M336 M089 M211`; artifact 6207 from Chanhu-daro reads
`M267 M099 M053 M067 M336 M089 M211`.

### 3. A fish-domain terminal chain

```text
[X] M059 M211
```

Minimum translation:

> **[identity/account content] — FISH-domain — terminal operator.**

Riskier English:

> **[Holder/account] — fish, fish-named commodity, star/astral class, or
> gemstone — licensed/assessed.**

This occurs in 28 clean inscriptions. Artifact 1019 is
`M267 M099 M104 M059 M211`. M059 is securely the fish pictograph; the classic
Proto-Dravidian `*mīn` fish/star rebus remains a live but low-confidence
phonetic hypothesis. Nothing in this run independently recovers the sound
`mīn`.

## Working sign glossary

| Sign | Defensible role | Structural evidence | Semantic status |
|---|---|---|---|
| M267 | INITIAL CLASS A | initial 78.5% in M77; 79.7% in Wells | exact meaning open |
| M391 | INITIAL CLASS B | initial 74.8%; 77.9% in Wells | exact meaning open |
| M293 | INITIAL CLASS C | initial 62.4%; 63.2% in Wells | exact meaning open |
| M342 | JAR/MEASURE TERMINAL | jar glyph; terminal 74.4%; 72.6% in Wells | container, unit, determinative, or closure |
| M176 | TERMINAL OPERATOR B | terminal 90.1%; 91.2% in Wells | meaning open |
| M211 | TERMINAL OPERATOR C | terminal 83.8%; 83.0% in Wells | meaning open |
| M099 | TWO / DUAL / LINK | two-stroke glyph fixed after initial classes | numeral versus connective open |
| M089 | THREE | three-stroke glyph; numerical-class evidence | cardinal, grade, or unit count open |
| M059 | FISH | secure pictograph, recurrent domain sign | phonetic `*mīn` only 0.25 confidence |
| M336 | RIMLESS-JAR / UNIT / LINK | jar-like glyph in a fixed `M336-M089-M211` chain | exact function open |

## Why these claims survive a hard audit

1. **Corpus reconstruction.** The code reconstructs an EBUDS-like clean subset
   of 1,549 lines, 7,003 tokens, and 377 signs, essentially the published
   1,548/7,000/377 result.
2. **Ordered structure.** Bigram cross-entropy improves over unigram from 6.247
   to 5.229 bits/token on a deterministic five-fold artifact split. Positional
   concentration is 0.246 versus 0.059 under 300 token shuffles.
3. **Cross-transcription replication.** An openly released Wells-family corpus
   has 1,837 lines and 8,359 tokens. Across 49 frequent exact crosswalks,
   Mahadevan/Wells initial rates correlate at 0.955 and terminal rates at 0.984.
4. **Cross-context recurrence.** The proposed frames occur at multiple sites
   and on multiple object classes rather than being a single-cache artifact.
5. **Orientation is executable.** Source strings are preserved in physical
   left-to-right order and explicitly reversed for the majority right-to-left
   reading, preventing a common silent error.

These results establish **formula slots**, not spoken language. Current work
demonstrates that nonphonetic synthetic systems can reproduce many statistics
previously treated as language evidence, so semantic confidence cannot be
obtained just by adding more classifiers or a larger language model.

## Two seductive 2026 models rejected

- Ross's four-part reading uses the mayig corpus backward: its claimed P324
  “opener” occurs 77 times at the stored-left edge but only once at the
  canonical reading-initial edge. Four of five other named pictographs conflict
  with the source corpus dictionary (fish/arrow/tree/diamond are swapped).
- Glossa-Lab's Mahadevan anchor table calls M099 a jar and M059 a numeral seven,
  although they are the two-stroke and fish signs. Its suffixal M267 is actually
  reading-initial 78% of the time. Its sound values are therefore rejected.

The lesson is not “AI cannot decipher it.” It is that fluent glosses are cheap;
orientation, sign identity, held-out prediction, and artifact context are the
work.

## What would upgrade this to a real linguistic decipherment

A phonetic key has to predict evidence unavailable when the key was invented:

- a proper name, title, commodity, or quantity on held-out artifacts;
- stable morphology across site, phase, and medium;
- consistent ancient lexemes under a frozen Dravidian, Elamite, Indo-Aryan, or
  other language model;
- iconographic or archaeological context not used during fitting;
- preferably a bilingual or a substantially longer text.

Until then, the translations above are deliberately bracketed functional
readings: meaningful progress, but not a claim that we can hear an Indus scribe
speak.

## Reproducibility map

- `results/structural_report.md` — generated M77 audit and model scores
- `results/wells_replication.md` — independent-transcription replication
- `research/candidate_model_audit.md` — rejected-model evidence
- `research/primary_sources.md` — source and corpus map
- `src/` — standard-library analysis/audit code; rendering uses Pillow
- `SOURCE_MANIFEST.md` — exact revisions and checksums
