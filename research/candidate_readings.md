# First candidate functional readings

These are **not sentence translations**. They are the strongest functional
glosses supported by the clean corpus plus sign shape and archaeological use.
The goal is to narrow the problem until a future phonetic proposal has fewer
degrees of freedom.

## Sign-level working glossary

| Sign | Working gloss | Confidence | Basis | What remains unknown |
|---|---|---:|---|---|
| M267 | INITIAL CLASS A | 0.93 structural | Reading-initial in 78% of 209 clean lines; begins `M267-M099` 145 times | person, office, commodity class, demonstrative, or something else |
| M391 | INITIAL CLASS B | 0.90 structural | Reading-initial in 75% of 123 clean lines; parallel `M391-M099` formula 51 times | exact semantic contrast with M267 |
| M293 | INITIAL CLASS C | 0.78 structural | Reading-initial in 62% of 85 clean lines; recurrent `M293-M123(-M343)` | exact semantic role |
| M342 | JAR/MEASURE TERMINAL | 0.74 functional | Classic jar glyph; terminal in 74% of 707 clean lines; found across seven sites and seven media classes | container, capacity unit, tax class, connective, or general phrase-final marker |
| M176 | TERMINAL OPERATOR B | 0.90 structural | Terminal in 90% of 152 clean lines | tax/license/title/case/classifier semantics |
| M211 | TERMINAL OPERATOR C | 0.84 structural | Terminal in 84% of 136 clean lines; closes `M059-M211` and `M336-M089-M211` | exact administrative or grammatical value |
| M099 | TWO / DUAL / CONNECTIVE | 0.70 functional | Two-stroke glyph; fixed after initial classes in the normalized reading sequence | whether it is numeral 2, duality, or a two-stroke connective |
| M089 | THREE | 0.88 functional | Three-stroke glyph and membership in the independently argued numerical class | whether cardinal, ordinal, metrological tier, or quality grade |
| M059 | FISH; possible `*mīn` rebus | 0.95 pictorial / 0.25 phonetic | Unmodified fish glyph; recurrent before M211; Proto-Dravidian fish/star proposal is testable but not independently confirmed | fish, star, gemstone/commodity, title, phonetic value, or classifier |
| M336 | RIMLESS-JAR/UNIT OR CONNECTIVE | 0.60 functional | Jar-like glyph; repeatedly begins the fixed terminal chain `M336-M089-M211` | independent unit, connective, or compound sign value |

Confidence is about the stated level only: a 0.93 **structural** role is not a
0.93 semantic translation.

## Independent transcription check

The edge roles replicate in the openly released PLOS Wells-family corpus using
the mayig Wells/Mahadevan crosswalk. Across 49 adequately frequent exact
crosswalks, initial rates correlate at **r=0.955** and terminal rates at
**r=0.984**. In particular, M267/W817+W861 is initial in 78.5%/79.7% of lines,
M342/W740 is terminal in 74.4%/72.6%, and M211/W520 is terminal in
83.8%/83.0%. This validates the slot assignments across transcriptions; it
does not validate the English semantics.

## Formula-level readings

The two most productive initial frames are:

```text
M267 M099 [X] M342
M391 M099 [X] M342
```

Attested examples include M77 artifact 1086 (`M267-M099-M124-M342`) and
artifact 1074 (`M391-M099-M289-M342`). They occur mainly on seals but also on
Harappan pottery. A defensible functional English rendering is:

> Class/authority A or B — dual/connection marker — variable account item X —
> jar/measure terminal.

A riskier administrative paraphrase is:

> Office A/B records or authorizes two/of category X under the jar-measure
> standard.

The corpus does **not** yet choose among “office,” “owner,” “guild,” “commodity
class,” or a grammatical particle.

Two productive terminal chains are:

```text
[X] M336 M089 M211     (31 clean inscriptions)
[X] M059 M211          (28 clean inscriptions)
```

Examples:

- artifact 1094: `M267-M099-M171-M059-M336-M089-M211`;
- artifact 1019: `M267-M099-M104-M059-M211`;
- artifact 6207 from Chanhu-daro: `M267-M099-M053-M067-M336-M089-M211`.

Minimum functional readings:

> [account/identity content] — rimless-jar/unit — THREE — terminal operator.

> [account/identity content] — FISH-domain — terminal operator.

A deliberately risky semantic hypothesis, suitable for falsification, is:

> [Authority/holder] — [commodity or assessed item] — three standardized units
> — licensed/assessed.

and for the fish chain:

> [Authority/holder] — [fish, fish-named commodity, star/astral class, or
> gemstone] — licensed/assessed.

The words “licensed/assessed” are placeholders motivated by seal and tablet
administration, not recovered phonetic translations.

## What the first pass actually advances

1. It reconstructs the published EBUDS statistics almost exactly: 1,549 unique
   clean lines, 7,003 tokens, and 377 signs versus the published 1,548/7,000/377.
2. It makes the right-to-left orientation executable and catches models that
   silently reverse it.
3. It identifies three initial classes, three major terminal operators, and
   two recurrent terminal chains that any full translation must explain.
4. It preserves the Dravidian fish/star hypothesis as a live, low-confidence
   phonetic anchor while rejecting models that misidentify the fish sign.

## Next decisive tests

- Obtain an authorized current ICIT export and crosswalk it to Mahadevan/CISI.
- Restore duplicate-object contexts and stratigraphy instead of discarding
  them after the structural pass.
- Pre-register an animal/field-symbol holdout: infer candidate semantic classes
  without one site, then predict the withheld site's iconography and artifact
  type.
- Test stroke and jar variants as a coherent number/metrology grammar against
  Proto-Elamite and proto-cuneiform numerical systems.
- Score Dravidian, Elamite, Indo-Aryan, and language-neutral administrative
  models on grouped held-out artifacts with frozen sign keys.
- Require any proposed phonetic key to predict an inscription or context not
  used during key construction.
