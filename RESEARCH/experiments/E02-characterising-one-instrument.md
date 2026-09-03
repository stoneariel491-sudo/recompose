# E02 — Characterising one instrument by planting, and what it is worth beside a reader

## Why

E01 measured what three readers find. It said nothing about what an *instrument* finds, and
nothing about whether the two miss the same things. Without that, "several instruments with
disjoint blind spots" is a slogan.

This measures one instrument on one defect class, by planting: take a book with sixteen known
defects of that class removed, put them back, and see how many it reports.

## Hypothesis, written before the run

The instrument compares where a page's first line of ink begins on the source scan against
where it begins in the built book, each measured against its own block's margin. It was written
after readers found the class, and it had already found one page nobody had opened.

The expectation was **high recall and moderate precision**: the rule is mechanical and the
signal is a whole indent quantum, so it should catch most of them, while the ragged geometry of
a real page should throw some false alarms.

**Both halves were wrong, and in opposite directions.**

## Method

A separate git worktree, so nothing touched the book while three readers were working in it.
Sixteen page files whose paragraph openings had been corrected were checked out at the commit
before the correction — restoring sixteen real defects, of the exact shape the class contains,
in their original positions. The book was rebuilt from that tree and the gate run over printed
pages 22 to 80.

Sixteen planted: 25, 28, 43, 45, 47, 50, 53, 54, 60, 62, 63, 65, 67, 69, 75, 77.

## Result, first run

Ten reports. Four were planted defects. **Six were pages that had not been planted**, and each
was checked by hand against the scan:

  * **printed 33 and 38 are real defects** the gate had found on its own. Both are the same
    class: a proof paragraph running on from the previous page, set flush on the plate and
    indented a full quantum here. Each of those two pages had been read by three independent
    readers and none of the six reported it.
  * **four were false positives**, and all four shared one signature: the offset measured in
    the built book was large and NEGATIVE — up to −130 pt. The block margin is taken from the
    lines that follow the opening, and on those four pages what followed was a centred display.
    A frame taken from a display is not a frame.

## Two repairs, each aimed at a signature rather than at a case

1. If the offset in the built book exceeds one and a half indent quanta in either direction,
   there is no frame to measure in, and the page is skipped rather than judged.
2. If the page's source opens on a structure — an item, a chapter, a section, an environment, a
   display — it is not opening a paragraph. The built text alone cannot see this: printed 51
   opens on the lettered part (b) of a theorem and its built line begins "Suppose {x_n}...",
   with the label a separate element, so the item body's offset from its own label reads as a
   paragraph indent.

## Result after the repairs

Five reports, **all five true**: three planted defects, and printed 33 and 38.

|  | value |
|---|---|
| precision | **5 / 5 = 1.00** |
| recall against the planted set | **3 / 16 = 0.19** |
| defects found that three readers each had missed | **2** |

## What this says, which is not what was expected

**The instrument is precise and nearly blind.** It reports almost nothing false and it misses
four fifths of the class it was built for. The reason is visible in the skip counts: it judged
14 pages of 59 and skipped 40. Its coverage is not the book; it is the subset of pages whose
opening it can frame at all.

**And it is not redundant with the readers, which is the point.** Per-reader recall on this
class is 0.67 (E01) and this gate's is 0.19, but the two found different things: the gate
recovered two defects that six reader-passes over those pages had missed. Blind spots that do
not coincide are worth more than either instrument's accuracy.

**The economics are the argument for keeping it.** A reader costs about twenty minutes for
eight pages and is the only thing that finds four fifths of this class. The gate costs seconds
for three hundred and thirty-eight and finds a fifth of it — including, twice here, a fifth the
readers did not have.

## What follows

Recall of 0.19 with precision of 1.00 is an instrument that should be made to *cover* more, not
to be more careful. Forty of fifty-nine pages were skipped, and every skip is an admission. The
next question is how many of those forty could be framed by a better rule rather than dropped —
and, since a skip is not a pass, the count of skips belongs in the gate's own output, where it
now is.

## Method note, recorded because it nearly went wrong

The planting was done in a separate worktree because three readers were reading the main tree at
the time. An earlier batch had been corrected mid-read and one reader reported that four of its
findings described files that no longer existed in that form. Nothing was lost, by luck. A
harness that mutates the artifact must not share a tree with anything reading it.

---

## CORRECTION, made the same day, and it is the more useful half of this file

The precision above is **1.00 on the population it was measured in, and that population was
the wrong one.** Those five reports came from printed pages 22 to 80 - a range where three
readers had already been over every page and where sixteen defects had already been found and
corrected. Running the same gate over the whole book gave forty-three reports, and a sample of
five of them, chosen across the book and checked by hand against the scan, came back **two
real and three not**.

So the honest figure on the unread population is nearer 0.4 than 1.0, and E01's own rule was
the one broken: **a number is a fact about its population.** The five-case sample was not
small, it was drawn from the wrong urn.

### What the three false ones had in common, and the fix

Every one had an implausible frame: a block margin reported as 0, or as 276 on a page whose
visible lines all stand at 434. The frame is the modal left edge of the six lines FOLLOWING
the opening, and those six routinely cross out of the opening's block - into a display, out of
a proof, into an exercise. **The modal edge of a mixed population is not a margin.**

The repair is to require the frame to be agreed: where fewer than half of the following lines
share an edge, there is no frame and the page is skipped.

### Two operating points, both measured

| | reports over the book | of five sampled |
|---|---|---|
| frame taken from the mode, whatever its spread | 43 | 2 real |
| frame required to be agreed by half | 17 | (retains p.97, which a reader then confirmed) |

The tightening cost two of the true positives I had checked by hand, printed 189 and 250, both
real. **So this is not a free improvement and the conclusion at the end of this file was too
simple.** "Make it cover more, not be more careful" is right about where the effort should go;
it is wrong if it is read as saying the loose setting was better. The loose setting reports
three false pages for every two true ones, and a worklist like that is not read.

What both settings share is the real limitation: the frame. An instrument that decides whether
a line is indented by looking at six lines below it will be wrong whenever those six are not
its neighbours in the same block. The next version should take the frame from the SOURCE - the
environment the line is actually in is known exactly - and use the scan only for the plate's
side. That removes the guess from the half of the comparison where the answer is already known.
