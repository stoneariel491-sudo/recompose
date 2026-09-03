# E01 — What an ensemble of readers buys, and what a majority rule costs

## Hypothesis, written before the data were counted

Three independent readers were set on the same pages to raise the recall of a class of defect
no machine in the apparatus can see: structural typography — a paragraph indented where the
source sets it flush, or flush where the source indents it, or a paragraph break present or
absent. The working assumption when the pass began was the ordinary one: **that agreement
between readers is evidence, and that a finding raised by one reader of three is weak.**

The prediction that follows from that assumption is that a two-of-three majority rule should
lose little — that most real defects would be seen by at least two readers, because a real
defect is there to be seen.

**This turned out to be false, and the size of the error is the finding.**

## Method

Fifteen readings: printed pages 22 to 77 of a 338-page book, in seven batches of eight pages,
three readers to a batch, each given the 600 dpi scan and the composed source and told to
measure rather than judge by eye. No reader saw another's report. Every finding was then
adjudicated against the scan by hand, and only findings confirmed against the scan are counted
here — a reader's claim is not evidence of a defect, the leaf is.

Counted below are the fourteen confirmed structural defects for which the per-reader outcome is
recorded unambiguously in all three reports.

## Result

| printed page | what was wrong | readers who found it |
|---|---|---|
| 25 | indent where the plate sets flush | 2 of 3 |
| 28 | indent where the plate sets flush | **1 of 3** |
| 36 | paragraph break missing | 2 of 3 |
| 43 | paragraph break missing | **1 of 3** |
| 45 | indent lost, exercise 23 | **1 of 3** |
| 45 | indent lost, exercise 27 | **1 of 3** |
| 47 | indent lost after a display | 3 of 3 |
| 50 | indent where the plate sets flush | **1 of 3** |
| 53 | indent where the plate sets flush | 3 of 3 |
| 53 | first-line indent lost in a block | 3 of 3 |
| 54 | first-line indent lost in a block | 3 of 3 |
| 60 | indent one quantum short | 3 of 3 |
| 75 | indent where the plate sets flush | 2 of 3 |
| 77 | indent where the plate sets flush | 2 of 3 |

Twenty-eight detections out of forty-two reader-opportunities: **a per-reader recall of 0.67**.

|  | predicted from r = 0.67 | observed |
|---|---|---|
| union of three readers | 0.96 | **14 of 14** |
| two-of-three majority | 0.74 | **9 of 14** |

**A majority rule would have shipped five of the fourteen — thirty-six per cent of the real
structural defects in that range of the book.** Every one of the five was confirmed on the leaf
afterwards; none was a false alarm.

## Two things this does not say

It does not say the readers are unreliable. Their union found everything. It says that
**the ensemble is a recall device and a vote is a filter**, and that putting a filter on the
output of a recall device throws away exactly the rare finding the device was bought for.

It does not say a lone reader is right. On printed pages 75 and 77 two readers reported a
defect with measurements and the third reported the pages clean, also with measurements. The
majority happened to be correct there, and it was not the majority that settled it: the plate
sets those lines at the block margin and the built book set them a quantum in, and that is why
they were corrected. **Adjudication against the source is not a formality that usually agrees
with the vote. It is the only thing deciding anything.**

## Why the recall is only two thirds, which is the more useful question

The defects the readers missed are not harder to see than the ones they found. What separates
them is that the found ones sit near something the reader was already looking at. A reader who
measures a page's margins because a display drew their attention finds the indent below it; a
reader whose attention was on a subscript does not, and reports the page clean **having looked
at it**. Attention is the scarce resource, not capability, and it is allocated by whatever the
page happens to make salient.

That is a claim about how to spend the next reader rather than how to count the last one:
**tell the reader where to look**. The instrument built after this pass, `page_open.py`, does
exactly that for one sub-class, and found an error on a page no reader had yet opened.

## What follows for the design

1. Never resolve an ensemble by vote. Collect the union, adjudicate every member against the
   source, and report the adjudication.
2. Report per-reader recall, not agreement. Agreement measures the readers against each other,
   which is the one comparison that cannot tell you whether the artifact is right.
3. A reader who reports a page clean has reported that they did not find anything there, and
   nothing more. Six of these fourteen pages were called clean by a reader who had measured them.
4. Spend the marginal effort on directing attention, not on adding readers. A fourth reader
   buys 1 − 0.33⁴ = 0.988 against 0.963; an instrument that names the suspect lines buys more.
