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

## Open, in the order they are worth attacking

**Q1. The instrument matrix.** For each defect class, the measured recall of each instrument and
the residual after all of them. Recall is measured by planting; independence by planting once
and seeing which instruments fail together. E01 is the first row of one column. This is the
claim the whole thing rests on and it is mostly unmeasured.

**Q2. Can a page layout be fitted rather than chosen?** Stage 2 of the pipeline currently
measures whatever a person thinks to measure. A book's layout is a small grammar — margins, a
quantum, a leading, a set of block styles — and fitting a grammar to observations is well posed.
If it can be fitted, stage 2 becomes automatic and the rest follows.

**Q3. Where does attention go, and can it be aimed?** E01's secondary finding says the marginal
return is in telling a reader where to look. One sub-class already has an instrument that does
this and it found a defect on a page nobody had opened. How far does that generalise, and what
is the right unit — a line, a paragraph, a page?

**Q4. What is the cost curve?** The case study is expensive per page. Which stages carry the
cost, and which of them fall away with scale rather than repeating per book? A method that is
only affordable once is a demonstration, not a product.

**Q5. Verification of a generative transcriber.** If a model transcribes a page, it is a fourth
reader and not a source. What does the apparatus have to add before its output can enter at all,
and what is the measured recall of the gates against *its* characteristic failures, which are
not the same as a scanner's?
