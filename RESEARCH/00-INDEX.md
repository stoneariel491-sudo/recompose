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

## E05 — Directing a reader's attention does not raise recall. It subtracts breadth.

Twelve readers over printed pages 142 to 173, one of every three given a census of places worth
measuring. **The aided reader found the same structural defects as the blind ones on every block
and fewer of everything else.** On one block all twelve census rows were cleared by the plate
while nine real structural defects stood on those same eight pages, by a mechanism the census is
blind to by construction — a paragraph break that is MISSING, invisible to an instrument that
enumerates blank lines. The blind readers found a mathematically false sentence, a correction of
the author's prose sitting in the book with no record at all, and a record written backwards; the
aided reader found none of those three.

E01 concluded the next unit of effort belongs in directing attention. **On this evidence that is
wrong**, and the reason matters more than the correction: a census is a COMPLETENESS device and a
reader is a DISCOVERY device. Giving one to the other converts discovery into checking, at a
straight loss. Run them against each other instead — and when readers find what the census did
not report, that gap is the specification for the next class, which is how three of its six
classes were obtained.

[experiments/E05-directing-attention.md](experiments/E05-directing-attention.md)

---

## E06 — A book's layout fits from its own ink, once identification and measurement are separated

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

## E07 — The instrument matrix, measured at last, and what it says is uncomfortable

Q1, mechanically, for the first time. Six defect classes planted one at a time against the five
instruments that read the source.

**A reversed inequality in the body is essentially uncovered** — one instrument catches one plant
in five and no other sees it at all. The class with the worst consequences has the weakest
mechanical cover in the project. **A wrong number in a CHECK line is caught one time in three**,
by the mechanism written specifically to catch it.

The harness learned two things about itself before it could measure anything, and both generalise.
**It must invoke an instrument the way the work invokes it** — invoked bare, the census prints
totals and no rows, and scored zero on its own classes. **And a hit is a difference, not a
mention** — the census names every page in every run, so on a mention test it scored perfectly on
six classes including two that are not its own. Each instrument is now run on the clean corpus
first and a plant counts only if it produces a line that was not there before: *measure the
change, not the state*, which is the same correction the layout fitter needed a level down.

[experiments/E07-the-instrument-matrix.md](experiments/E07-the-instrument-matrix.md)

---

## Open, in the order they are worth attacking

**Q1. The instrument matrix. FIRST TABLE MEASURED — E07.** Six classes against the five
source-reading instruments, planted mechanically. Two results stand out: a reversed inequality is
essentially uncovered, and a wrong number in a CHECK line is caught one time in three. What
remains unmeasured is precision, the instruments that read the plate (they cannot run in a
temporary copy), and correlation — for which the per-plant record is kept but six trials a class
is far too few.

**Q2. Can a page layout be fitted rather than chosen? ANSWERED — E06.** Measure, margins,
baseline pitch, text block and indent quantum all fit from the leaves alone, given no page
numbers, no trim and no answer, to within about two per cent. Stage 2 can run without a person.
The quantum took two attempts and the second is the general lesson: **the measurement and the
identification must not come from the same evidence.** Recovering it from left edges asks them
to say which lines are openings *and* how far they are indented, and the side bearing corrupts
both. The right edge identifies a paragraph — a short line ends one, the next begins one — and
knows nothing about indents, after which the bearing is unbiased noise that a mean removes.

**Q3. Where does attention go, and can it be aimed? UNDER TEST — E05.** E01's secondary finding
says the marginal return is in telling a reader where to look. Twelve readers are in flight with
one of every three given a census of places worth measuring, and the predictions are fixed.

**Q4. What is the cost curve?** The case study is expensive per page. Which stages carry the
cost, and which of them fall away with scale rather than repeating per book? A method that is
only affordable once is a demonstration, not a product.

**Q6. Does the automation agree with a person? FIRST LAW — E08.** For months this was not
asked, because "does the instrument run" and "does the instrument agree with a reader" were treated
as one question. They are not. The first time a sweep and a human reading landed on the same line
independently, the cause was identifiable: **both measured the same physical difference in the same
frame, and neither used anything else.** Every instrument that has never agreed substitutes a
representation the reader never touches — a compilation of the source in isolation, a statistical
rule with count floors, a markup environment stack, a positional index.

The design rule that follows is testable before a line is written: *state what the instrument
measures as a sentence a person could execute against the page with a ruler.* If you cannot, it
measures a model of the page.

Used deliberately once since: a check that "could never have failed" was restated as *break it on
purpose and see whether the prover notices*, and the resulting mutation test reproduced the
reader's two findings exactly before finding seven more. **A gate that cannot fail prints the same
word as one that can**, and there had been no way to tell them apart but by hand.

Three predictions are fixed in E08 against evidence that has not arrived.

**Q7. When does a published law survive? FIRST REFUTATION - E09.** E08's design rule held and its
worked example did not:  published "the frame is the densest cluster, never the
minimum" and a human reader refuted it three hours later on a page whose window held more indented
lines than flush ones. Two further rules followed, each fixing the last and breaking the next, and
every one was the same failure - a page carries three rules, so **"the frame" is not a property of
the leaf** and any rule picking one number picks the wrong level somewhere.

The correction is a change of question: the instrument needs the ANSWER, not the frame, and the
answer has two admissible values, so test both and refuse when neither holds. A single line then
witnesses a rule, because the hypothesis says where the rule must be - a search needs support where
a test needs only a witness. Control: 4 right and 8 refused, to 12 right and 0 refused.

And the result that generalises furthest: **a test whose cases all share one answer cannot detect an
error that preserves that answer.** The control could not catch the refuted version because all
twelve of its cases had the same verdict.

**Q5. Verification of a generative transcriber.** If a model transcribes a page, it is a fourth
reader and not a source. What does the apparatus have to add before its output can enter at all,
and what is the measured recall of the gates against *its* characteristic failures, which are
not the same as a scanner's?
