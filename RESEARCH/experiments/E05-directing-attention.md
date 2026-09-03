# E05 — Does directing a reader's attention raise recall? (hypothesis, written before the run)

E01's headline was that an ensemble of readers is a recall device and a majority vote destroys
it. Its secondary finding was more useful and has never been tested: **the defects a reader
misses are not harder to see than the ones it finds.** They differ in whether something nearby
had already drawn the reader's attention. E01 concluded that the next unit of effort belongs in
directing attention rather than in adding a reader, and Q3 in the index has stood open since.

There is now something to direct attention *with*. `tools/para_census.py` enumerates every place
in the source where one of five mechanisms could have decided a paragraph's indent without
anyone choosing it — 586 openings over the whole book, and between 3 and 12 on a block of eight
pages. It finds 16 of the 16 structural defects that three readers established over printed
pages 126 to 141. It does not say which of the 586 are wrong; the plate says that.

## Design

Printed pages 142 to 173, four blocks of eight, three readers each — the same protocol as every
previous wave, so the comparison is against a measured baseline rather than an impression.

**The only difference: reader C in each block is given its block's census rows. Readers A and B
are not, and are not told the census exists.** Two blind readers per block preserve the
independence the ensemble is built on, so the wave is still a normal wave whatever the
experiment shows.

## Hypothesis, written before any reader was launched

1. **The aided reader will find more structural defects than the median blind reader on the same
   pages.** This is the whole claim of attention-direction and the only reason to run it.

2. **The aided reader will find fewer non-structural findings** — mathematics, wording, damaged
   glyphs, false header claims — than the median blind reader. Attention is finite; a list of
   places to look is also a list of places not to look. If this does not happen, the census is
   free, which would be a better result than expected and should be distrusted until repeated.

3. **The union of the two blind readers will contain at least one structural defect the aided
   reader misses.** The census flags a *mechanism*, not a defect, and a defect that arrives by
   some sixth mechanism is invisible to it. A reader that trusts the list inherits the list's
   blind spots, and this is the specific risk of the whole idea.

4. **On the blocks where the census is nearly empty — printed 150 to 157 has three rows — the
   aided and blind readers will not differ.** If the aided reader is better there too, the
   effect is not the census and the experiment has measured something else.

## What would refute the idea outright

If (3) holds and (1) does not — the aided reader finds no more than the blind ones and misses
what they catch — then directing attention with a source-side census is worse than not directing
it, and E01's secondary finding does not generalise to this instrument.

## Measurement

Per block: structural defects found by each reader, non-structural findings by each reader,
which of the census rows each reader independently condemned, and the union. Adjudicated the
usual way, against the plate and the second printing rather than by vote.

Results are recorded below when the wave closes. Nothing above may be edited after the readers
were launched; a correction, if one is needed, goes in a CORRECTION section as E02 has.

---

# Result

Twelve readers over printed pages 142 to 173, four blocks of eight, three readers each. On each
block the reader labelled C was given that block's census rows; A and B were not and were not
told the census existed. All four blocks closed with the readers agreeing on every structural
finding.

| block | structural defects found by A (blind) | by B (blind) | by C (aided) | census rows |
|---|---|---|---|---|
| 142–149 | 9 | 10 | 9 | 12 |
| 150–157 | 3 | 2 | 2 | 3 |
| 158–165 | 5 | 5 | 5 | 8 |
| 166–173 | 9 | 9 | 9 | 12 |

| prediction | outcome |
|---|---|
| 1. the aided reader finds MORE structural defects | **refuted.** It found the same set on every block, and one fewer on 142–149 |
| 2. the aided reader finds FEWER non-structural findings | **held, and by a wide margin** |
| 3. the blind pair catches a structural defect the aided reader misses | **held on 142–149 and 166–173** |
| 4. no difference where the census is nearly empty (150–157) | **held** — 3, 2, 2 |

## What actually happened

**Directing attention did not add recall. It subtracted breadth.**

On 142–149 the blind readers found, between them, a page that was mathematically false — our
plate reads "*f* is continuous at *x*" where the second printing reads "at **a limit point** *x*",
without which the sentence is untrue at every isolated point — plus four wrong claims in our own
page headers and a paragraph indented to three-fifths of a quantum in both printings. The aided
reader found one header claim and the sub-quantum indent, and did not find the false sentence.

On 158–165 the blind pair found that a correction of Rudin's own prose sat in the book with **no
entry in ERRATA at all**, against a page header asserting it was recorded; that a third damaged
comma existed where the record counted two; and that the record of a page-161 decision was
written **backwards**. The aided reader found the backwards record and the third comma but not
the missing entry.

On 166–173, both blind readers and the aided reader found the same nine — and the aided reader
wrote the sentence that settles this experiment: *"The census saw none of the twelve findings
above, because eleven of them arrive through mechanisms it does not cover."* **Every one of the
twelve census rows on that block was cleared by the plate, while nine real structural defects
stood on the same eight pages.**

## The mechanism the census could not have

Those nine arrive by a fault the census is blind to *by construction*: the source runs text on
after a display with **no** blank line, where the plate opens an indented paragraph. An instrument
that enumerates blank lines after displays cannot see a blank line that is absent. It is now a
sixth class, RUN-ON, counted at sixty places in the book — found by reading what the tool did not
report, which is the third time in this project that a class has been found that way.

## What this changes

E01 concluded that the next unit of effort belongs in directing attention rather than in adding a
reader. **On this evidence that is wrong, and the reason is worth more than the correction.**

A census is not an attention aid. It is a *completeness* device: it enumerates a finite population
over the whole book, which no reader can do, and it hands over a list that can be checked to
exhaustion. A reader is a *discovery* device: it finds the class nobody has named yet, which no
census can do, because a census can only count the mechanisms someone has already thought of.

Giving the census to a reader converts a discovery device into a checking device — and the
measurements above say the conversion is a straight loss, because the same structural defects
were found without it while everything outside its five classes went unfound.

**So the two should not be combined; they should be run against each other.** The census produces
a population and clears or condemns it mechanically, page by page. The readers stay blind and
keep doing the thing only they do. And when readers find defects the census did not report — as
they did on printed page 173 — that gap is not a reader's win, it is **the specification for the
next class**, which is exactly how RUN-ON, SUPPRESSED-JOIN and PARTS-FIRST were all obtained.

The instrument matrix (Q1) gains its second measured row, and it is a row about *coverage* rather
than accuracy: the census's recall is 16 of 16 within its classes and 0 of 9 outside them, on the
same wave.
