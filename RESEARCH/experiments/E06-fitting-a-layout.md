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
