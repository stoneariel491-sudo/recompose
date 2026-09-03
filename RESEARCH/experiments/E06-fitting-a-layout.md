# E06 — Can a page layout be fitted rather than chosen? (hypothesis, written before the run)

This is Q2, and it is the question that decides whether stage 2 of the pipeline can run without
a person. Today it measures whatever someone thinks to measure. A book's layout is a small
grammar — a text block, a measure, a leading, an indent quantum, a set of block margins — and
fitting a grammar to observations is well posed. If it can be fitted, stage 2 becomes automatic
and everything downstream follows.

**The case study is the right test because its answers are already known and were established
by other means.** They were derived over weeks, one at a time, several of them the hard way, and
none of them from the procedure being tested here.

## The known answer

| quantity | value | how it was established, NOT by this fitter |
|---|---|---|
| trim | 6 × 9 in | the publisher's series |
| measure | 360 pt (5.0 in) | the justified span of body ink on four leaves |
| text height | 540 pt (7.5 in) | the composed page |
| top margin | 0.81 in | measured, then corrected on the built page |
| side margins | 0.5 in each | trim less measure, halved |
| indent quantum | 25.7 pt | measured on the plate, confirmed in the build |
| baseline pitch | 10 pt on 13, times a linespread of 1.0667 | the composed page |
| scale, scan to book | 1.3514 | four body leaves, each giving 266.4 scan pt for the 360 pt measure |

Expressed as fractions of the leaf, which is the form that survives a change of scanner:

    measure / trim width        0.8333
    side margin / trim width    0.0833
    text height / trim height   0.8333
    quantum / measure           0.0714
    baseline pitch / trim ht    0.0214

The plates are 2691 × 4060 px, a ratio of 1.5087 against a 6 × 9 trim's 1.5000 — **the scan
carries 0.6 per cent more height than the trim**, which is either bleed or a scanner that did
not crop to the trim, and the fitter must not be told which.

## Hypothesis, fixed before the fitter was run

1. **The measure and the side margins fit to within 1 per cent** of the known values. The body is
   justified, so the right edge of body ink is a hard edge repeated on hundreds of leaves; this
   is the easiest quantity in the grammar and if it does not come out, nothing will.

2. **The baseline pitch fits to within 2 per cent.** It is the strongest periodicity on the leaf
   and a Fourier or autocorrelation argument should find it without seeding.

3. **The indent quantum fits to within 5 per cent, and it is the hardest of the four.** It is
   recovered from a histogram of line-start positions, and those carry the body's margin, every
   open block's margin and every indent at once — the same superposition that refuted two
   instruments already (E03, and `para_indent.py`'s first two architectures). I expect this to be
   where the experiment either succeeds interestingly or fails.

4. **The text height will NOT fit to 1 per cent, and will come out short.** A page's ink ends
   where its last line ends, not where the text block does, and a page ending mid-paragraph
   leaves the block's foot unmarked. The fit should be taken over the MAXIMUM across many leaves
   rather than the median, and even then I expect it low.

5. **The number of distinct left margins on a page will fit, and this is the prediction I hold
   most loosely.** A page has the body's margin and one for each block open on it. If clustering
   line starts recovers that count reliably it would settle a problem three instruments have now
   failed at; I expect it to work on pages with one or two blocks and to smear on pages with more.

## What would refute the idea

If (1) fails — the easiest quantity in the grammar, on the most redundant evidence a page offers
— then a layout is not fittable from ink alone and stage 2 stays manual. If (1) and (2) hold and
(3) fails badly, the grammar is fittable in its continuous parameters and not in its discrete
ones, which is a narrower but still useful result and says exactly where a person is still
needed.

## Method

`src/fit_layout.py`, run over a sample of body leaves chosen by ink fraction alone — no page
numbers, no knowledge of which leaves are body and which are front matter, since a real ingest
would not have that. Output in fractions of the leaf. Compared afterwards against the table
above, which the fitter is not given.

Results below when the run is done. Nothing above may be edited after the fitter is first run;
a correction goes in a CORRECTION section, as E02 has.

---

# Result

    fitted on 30 leaves chosen by ink fraction alone, 2691 px wide
      leaf aspect              1.5087
      left margin              0.0902   of the leaf's width
      measure                  0.8236   of the leaf's width
      right margin             0.0861   of the leaf's width
      baseline pitch           0.0197   of the leaf's height
      text block, top          0.0931   of the leaf's height
      text block, height       0.8224   of the leaf's height
      indent quantum           0.0500   of the leaf's width   (0.0607 of the measure)
                               on 21 leaves of 30, above a side-bearing floor of 0.0179

| prediction | outcome |
|---|---|
| 1. measure within 1 % | **just outside** — 0.8236 against 0.8333, 1.2 % low |
| 2. pitch within 2 % | **held, at 0.1 %** — and see below, because the target moved |
| 3. quantum within 5 % | **failed** — 0.0607 of the measure against 0.0714, 15 % low |
| 4. block height fails, and short | **held** — 1.3 % short |
| 5. count of margins per page | **not tested.** It was not implemented and is not claimed |

**The grammar's continuous parameters fit. Its discrete one does not, yet.** That is the narrower
result E06 named in advance as the likely one, and it says where a person is still needed: not
in measuring the page, but in deciding what an indent is.

## The measurement that corrected the answer instead of matching it

Prediction 2 was checked against a recorded baseline pitch of 13.87 pt — 10 pt on 13, times the
book's linespread of 1.0667. The fitter returned the equivalent of 12.18 pt and was 12 per cent
out, so the fitter was assumed wrong and the estimator was rebuilt.

Then the built book itself was measured. **Its baseline steps are 12.7 to 12.8 pt.** The recorded
13.87 was arithmetic on the wrong quantity; the composed page never had that pitch. Against the
book's real pitch of 12.75 pt over a 648 pt leaf — 0.01968 — the fitter's 0.0197 is right to a
tenth of a per cent, and was right before the estimator was touched.

**An experiment whose ground truth is a number someone wrote down is testing the note.** The
plate and the built page are evidence; a table in a document is a claim, and this one was false.
The estimator was rebuilt anyway, on its own merits — a truncated median is biased low by
construction — but the rebuild was done for the wrong reason and would have been abandoned had
the check come first.

## Three faults, and two of them are general

**Within a leaf first, across leaves second.** The first version pooled every line of every leaf
and took one pair of percentiles for the measure. It returned 0.8785 — *wider than the justified
span of any single leaf in the sample*, which was the tell. The leaves are not registered: their
body margins vary by sixty pixels across thirty leaves while their justified spans agree to one
per cent. **Pooling positions from unregistered leaves measures the union of their text blocks
and calls it the block.** The same fault, unnoticed, made the text block 0.5 per cent too *long*
where a page's ink — ending at its last line — should have made it short: two errors of opposite
sign nearly cancelling, which is the worst way for a number to be right. Corrected, the block
comes out 1.3 per cent short, as predicted.

A layout parameter that is a DIFFERENCE — a measure, a quantum, a pitch — is a within-leaf
quantity and must be computed inside a leaf before anything is pooled. Only a POSITION needs
registration, and a position is what this stage cannot recover.

**The left ink edge is not the margin.** It is the margin plus the first glyph's left side
bearing, and a T, an x, an L and a u flush at one margin land at four different ink edges. The
first quantum fit returned 0.010 of the leaf against a true 0.063 — it had found the spacing
between neighbouring clusters, which is side-bearing noise. Measured rather than assumed, from
the spread of ink edges within a leaf's densest cluster of line starts, that noise is **1.79 per
cent of the leaf here, about 48 px, about 7 pt** — a quarter of the quantum it is trying to
resolve. Below that floor no margin difference recovered from ink can be believed, whatever the
tolerance passed to the clustering.

Two readers met the same fact independently on one page of the case study, where four lines of a
proof measured below a range a header claimed for it, on the side bearings of x, u, L and T.

## What this says about the architecture

Stage 2's own document says measurements are taken *"as fractions of the leaf so that scan
resolution cancels"*. **Resolution cancels. Registration and crop do not.** These plates are 2691
× 4060 px at an aspect of 1.5087 against a 6 × 9 trim's 1.5000, they are cropped inside the trim
by about one per cent of the width, and each leaf sits at its own offset. A fraction of the leaf
is therefore not the invariant the document claims it is: it is invariant to the scanner's dpi
and to nothing else about the scanner.

The quantity that IS invariant is a ratio between two measurements on the same leaf — the
quantum as a fraction of the measure, the pitch as a fraction of the block height. Those are what
stage 2 should emit, and what a later stage can turn into points once the trim is known from
outside the ink.

## Where this leaves Q2

Answered in part, and the part matters: **the continuous parameters of a book's layout can be
fitted from its own leaves, without being told which measurements to make, to about one per
cent.** The discrete parameter — the indent quantum, which is what every structural instrument
in this project has needed and none has recovered — comes out to the right order of magnitude
and 15 per cent low, and it now has a named obstacle with a measured size rather than a shrug.

The next move is not a better clustering. It is to stop recovering the quantum from margins at
all and recover it from *pairs of lines within one paragraph*, where the difference is between
two edges whose glyphs are both known.

---

# Continuation: the quantum, by the move this document named

The result above closed with a sentence about what to do next: *"stop recovering the quantum from
margins at all and recover it from pairs of lines within one paragraph, where the difference is
between two edges whose glyphs are both known."* That was written before it was tried. It works.

    quantum, by paragraph    0.0598 of the leaf's width   (0.0727 of the measure)
                             from 42 indented openings of 159 found by the right edge

**0.0727 against a true 0.0714 — 1.8 per cent.** Prediction 3 asked for 5 per cent and the
margin histogram missed it by 15. The same leaves, the same primitives, the same sample.

## Why it works, and it is one idea

**The measurement and the identification must not come from the same evidence.** Recovering the
quantum from a histogram of left edges asks the left edge to say which lines are paragraph
openings *and* how far they are indented. The side bearing corrupts both jobs at once, and no
amount of clustering separates a signal from the noise that defined it.

The right edge answers the first question and knows nothing about the second. **The body is set
justified, so every line but a paragraph's last reaches the measure: a short line ENDS a
paragraph and the line after it BEGINS one.** That identification is free, it is hard, and it is
independent of the quantity being measured.

Then the side bearing stops being an obstacle and becomes noise. Each pair contributes the
opening's edge less its own paragraph's margin, and both carry a bearing drawn from the same
distribution of initial glyphs — so the difference is *unbiased* and only its variance is
inflated. **What is a hopeless quarter-quantum on one paragraph is a small fraction of one over
forty.** A mean removes it; the mode that the histogram method needed would have kept it.

## The estimator still had to be right, and its first version was not

The first paragraph-based version returned 0.0615 of the measure — 14 per cent low, barely better
than the histogram. The difference was not the idea but the statistic: it kept every positive
difference above half the median and averaged those.

The histogram of the 159 differences says why, and it should have been looked at first:

    -0.04  ######                          6
    -0.03  ######                          6
    -0.02  ####                            4
    -0.01  ###############################  31
    +0.00  ####################            20
    +0.01  #                               1
    +0.02  #################               17
    +0.03  ######                          6
    +0.04  #                               1
    +0.05  ##############################  30
    +0.06  ################                16

**Three populations, not two.** A mass at zero, which is every paragraph the book opens flush — after a display, at the head of a block. The indent itself at 0.05 to 0.07. And a third mass at 0.02 to 0.03, twenty-three of them, which a threshold at half the median swept in with the indents and which pulled the mean down by a seventh.

A threshold cannot separate three populations. The clusters have to be found. Taking the *highest* well-populated cluster rather than the largest one matters too: **a book opens more paragraphs flush than indented**, so the mass at zero outweighs the quantum and the mode is the wrong statistic.

## Q2, now

**Answered.** A book's layout — measure, margins, baseline pitch, text block, indent quantum — can be fitted from its own scanned leaves, given no page numbers, no trim and no answer, to within about two per cent on every parameter. Stage 2 can run without a person.

What it cannot recover is the trim, and it should stop being asked to: a leaf of ink says nothing about the paper it was cut from. Everything is a ratio until the trim enters from outside.
