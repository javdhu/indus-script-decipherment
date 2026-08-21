# Pre-registered hypothesis families

These hypotheses are stated before inspecting the generated results. They are
not mutually exclusive: Indus inscriptions could mix language, metrology, and
administrative notation.

## H1 — Administrative formula

Canonical reading-order texts follow a reusable schema such as
`[authority/identity] [name or institution] [commodity/domain] [quantity/unit]
[transaction or terminal marker]`.

Predictions:

- strong but imperfect positional classes;
- substitution frames with many alternatives in one slot;
- generic high-frequency terminals and more context-specific content signs;
- position-aware models outperform bag-of-signs baselines on held-out artifacts;
- some slots associate with field symbols, sites, and object types.

## H2 — Metrological subsystem

Some stroke-like signs are numerals and some pictorial signs are units,
containers, or commodities. Mahadevan M342 (the jar-shaped sign) is a prime
candidate for a unit/container/determinative role, not yet a phonetic value.

Predictions:

- stroke signs occupy constrained positions near a smaller class of unit or
  commodity signs;
- numeral-like alternatives substitute in the same frames;
- ordering and co-occurrence should be compatible with a coherent number
  system rather than arbitrary rebus assignments;
- the subsystem should be enriched on accounting-related artifact classes.

## H3 — Logo-syllabic language

At least some signs encode a spoken language, possibly with logograms,
phonetic complements, and grammatical affixes.

Predictions:

- sign order contains held-out predictive information beyond length and
  frequency;
- frequent signs include reusable grammatical or determinative functions;
- candidate phonetic assignments should improve likelihood under one
  historically plausible language family without being selected on the same
  texts used to score them;
- allographs and compounds behave consistently across sites and media.

## H4 — Dravidian fish rebus

The fish-shaped M059 may have had a Proto-Dravidian reading related to
`*mīn` (fish, and in later Dravidian traditions also star). This is a candidate
anchor, not an accepted fact.

Predictions:

- M059 compounds form coherent and recurring classes;
- modifiers around M059 show stable ordering and contrast;
- a proposed fish/star reading predicts iconographic, calendrical, titular, or
  lexical contexts that were not used to invent the reading;
- M059 must not be silently renumbered or confused with a different glyph.

## H5 — Non-linguistic or mixed emblem system

The inscriptions may encode administrative categories without continuously
representing speech, or combine emblems with a narrower written subsystem.

Predictions:

- structure remains strong, but linguistic phonotactic assignments do not
  generalize;
- signs have unusually rigid positions and strong icon/object associations;
- formula templates explain the corpus at least as well as language-family
  projections;
- no proposed phonetic system makes independent, discriminating predictions.

## Rejection rules

- A reading is rejected if it depends on a wrong sign identity or orientation.
- Corpus coverage is not validation; a dictionary can always be made to cover
  a finite corpus.
- Positional structure validates structure, not a particular language.
- Rebus similarity without independent constraints is hypothesis generation,
  not decipherment.
- Training and evaluation artifacts must be separated by object, and exact
  duplicate inscriptions must not leak across the split.

