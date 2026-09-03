# Findings

Numbered, each with the measurement that forced it. A finding without a number it can be
recomputed from is an opinion.

**The rule of this file: the hypothesis is written before the result.** Where an entry records
that a prediction was wrong, that is the entry doing its job. Roughly half of the case study's
work produced a measured *no*, and two of those refutations corrected claims that had already
been written down as true.

---

## E01 — What an ensemble of readers buys, and what a majority rule costs

Three independent readers over 56 pages, fourteen confirmed structural defects.
Per-reader recall **0.67**; union of three found **14 of 14**; a two-of-three majority would
have found **9 of 14** and shipped the other five.

The prediction going in was that a majority rule would lose little. It loses a third.
An ensemble is a recall device; a vote is a filter; putting the filter on the device throws
away the rare finding the device was bought for.

Secondary, and more useful than the headline: the misses are not harder to see than the hits.
They differ in whether something on the page had already drawn the reader's attention nearby.
**Spend the next unit of effort on directing attention, not on adding a reader.**

[experiments/E01-the-cost-of-voting.md](experiments/E01-the-cost-of-voting.md)

---

## E02 — Characterising one instrument by planting, and what it is worth beside a reader

Sixteen real defects put back into a separate worktree, the book rebuilt, the gate run.
**Precision 5/5 = 1.00. Recall 3/16 = 0.19.** Both halves of the prediction were wrong and in
opposite directions: it was expected to be broad and a little noisy, and it is narrow and
exact. It judged 14 pages of 59 and skipped 40, and every skip is an admission.

It is worth keeping anyway, for the reason the whole design rests on: **it recovered two
defects that six reader-passes over those same pages had missed.** Blind spots that do not
coincide are worth more than either instrument's accuracy. An instrument with recall 0.19 and
precision 1.00 should be made to cover more, not to be more careful.

[experiments/E02-characterising-one-instrument.md](experiments/E02-characterising-one-instrument.md)
---

## E03 — Counting indented paragraphs per page: designed, built, REFUTED

An instrument to cover the nine-in-fifteen defects that page openings miss. It counts, per
page, how many paragraphs the scan indents and how many the book does, on the argument that a
count needs no correspondence between the two.

**It does not measure what it names.** Ground truth on one page, established by two readers
against a second printing, is three indents too many and two too few - our page should carry
one MORE than the plate. The instrument reports five fewer.

The count is dominated by rows that are not paragraphs, and the two sides accumulate different
amounts of that because they break lines differently - the very difference the count was meant
to be immune to. **A count is only correspondence-free if the things counted are identified
reliably.** Dropping the correspondence hid the identification problem rather than removing it.

Four real faults were found in the building and two of them are general: a deskew for a tilt of
twenty points per thousand, and the merging of PDF line fragments into typographic lines.

[experiments/E03-a-refuted-instrument.md](experiments/E03-a-refuted-instrument.md)
---

## E04 — Two defects in the surviving primitives, found by constructed pages

The four primitives extracted from E03 had been read carefully and had produced the measurements
E02 and E03 report. They had never been run on an input whose right answer was known in advance.
**Two of the four were wrong**, and one of them in exactly the case its own docstring named: the
agreement test that refuses a frame when the following lines disagree accepted a three-three
split, which is the very page that motivated writing it.

The prediction going in was that the tests would be regression cover. A component is only tested
by an input whose answer is known independently of it, and an instrument that reports a worklist
already known to be part wrong has nowhere for one more wrong entry to show up.

[experiments/E04-two-defects-found-by-construction.md](experiments/E04-two-defects-found-by-construction.md)

---

## E05 — Does directing a reader's attention raise recall? IN FLIGHT

E01's secondary finding said the next unit of effort belongs in directing attention rather than
in adding a reader. There is now something to direct it with. Twelve readers over printed pages
142 to 173; one of the three on each block is given that block's census rows and the other two
are not, so the wave is a normal wave whatever the experiment shows.

Four predictions fixed before the first reader was launched, including the specific risk: **a
reader that trusts a list of mechanisms inherits that list's blind spots**, so the blind pair is
predicted to catch a structural defect the aided reader misses.

[experiments/E05-directing-attention.md](experiments/E05-directing-attention.md)

---

## E06 — A layout's continuous parameters fit from the ink. Its indent quantum does not, yet

Q2, answered in part. On thirty leaves chosen by ink fraction alone — no page numbers, no trim,
no answer — the measure fits to **1.2 %**, the baseline pitch to **0.1 %**, the text block comes
out **1.3 % short exactly as predicted**, and the indent quantum lands **15 % low**, which fails
its prediction and is the first time in this project that quantity has been recovered to the
right order of magnitude at all.

**The pitch check corrected the answer instead of matching it.** Measured against a recorded
13.87 pt the fitter was 12 % out, so the estimator was rebuilt — and then the built book was
measured and its baseline steps are 12.7 to 12.8 pt. The fitter had been right to a tenth of a
per cent all along. *An experiment whose ground truth is a number someone wrote down is testing
the note.*

Two faults that generalise: **a layout parameter that is a difference must be computed within a
leaf before anything is pooled** — leaves are not registered, and pooling their positions
measures the union of their text blocks; and **the left ink edge is not the margin**, it is the
margin plus a side bearing, whose spread here is 1.79 % of the leaf, about 7 pt, a quarter of the
quantum it is trying to resolve.

[experiments/E06-fitting-a-layout.md](experiments/E06-fitting-a-layout.md)

---

## Open, in the order they are worth attacking

**Q1. The instrument matrix.** For each defect class, the measured recall of each instrument and
the residual after all of them. Recall is measured by planting; independence by planting once
and seeing which instruments fail together. E01 is the first row of one column. This is the
claim the whole thing rests on and it is mostly unmeasured.

**Q2. Can a page layout be fitted rather than chosen? ANSWERED IN PART — E06.** The continuous
parameters fit from the leaves alone to about one per cent. The discrete one, the indent quantum,
comes out 15 per cent low against a named obstacle of measured size: the side bearing, which is a
quarter of the quantum here. What remains is not a better clustering but a different measurement
— the quantum recovered from pairs of lines inside one paragraph, where both edges' glyphs are
known, rather than from margins.

**Q3. Where does attention go, and can it be aimed? UNDER TEST — E05.** E01's secondary finding
says the marginal return is in telling a reader where to look. Twelve readers are in flight with
one of every three given a census of places worth measuring, and the predictions are fixed.

**Q4. What is the cost curve?** The case study is expensive per page. Which stages carry the
cost, and which of them fall away with scale rather than repeating per book? A method that is
only affordable once is a demonstration, not a product.

**Q5. Verification of a generative transcriber.** If a model transcribes a page, it is a fourth
reader and not a source. What does the apparatus have to add before its output can enter at all,
and what is the measured recall of the gates against *its* characteristic failures, which are
not the same as a scanner's?
