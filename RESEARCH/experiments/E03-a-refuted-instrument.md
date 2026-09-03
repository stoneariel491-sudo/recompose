# E03 — Counting indented paragraphs per page: designed, built, refuted

## The idea, and why it looked right

E02 left one instrument with recall 0.19 on page openings. But openings are not where the class
lives: of fifteen structural defects corrected in the second reading wave, three were page
joins, three were lines after a display, and **nine were paragraphs inside a block** whose
environment suppressed an indent the source takes or added one it does not — four of them from
a single wrongly chosen environment. An opening-only gate is blind to nine of fifteen by
construction.

The proposal was to compare, per page, **the number of indented paragraphs** on the scan and in
the built book. Its appeal was that it needs no correspondence between the two: matching our
paragraphs to the plate's one by one would require a text alignment the scan's OCR cannot
support, but a count is a property of the page and survives any difference in line breaking.

## Hypothesis, written before the run

If the scan indents four paragraphs on a page and the book indents none, the count will say so.
The expectation was a coarse but honest instrument: **low precision about WHICH paragraph, high
reliability about WHETHER the page is wrong.**

## What was built, and three real defects found in the building

1. **A page has several margins, not one** — the body's, and those of whatever proof, example
   or exercise is open on it. Margins are found by clustering the left edges; a cluster of three
   rows or more is a margin, and a row is indented when it stands between 0.6 and 1.4 quanta
   right of the nearest margin at or before it.

2. **The scan is not square to the scanner.** A column's left edge drifts by up to twenty points
   per thousand down the leaf, which splits one margin into two clusters. A robust line fitted
   to the lower envelope and subtracted fixes it — the same technique that made the index's
   sub-entries legible.

3. **A printed page does not correspond to a leaf of the book,** because the pagination has
   drifted by up to fourteen pages, so a printed page routinely straddles two leaves. The first
   version sliced each page's rows out of the marker's own leaf and reported "0 of 0" for two
   pages and about a third of the truth for a dozen more.

4. **A line of PyMuPDF is not a line of type.** Mathematics breaks a printed line into a
   fragment per fraction, per superscript, per radical. Counting those gave a median of
   fifty-two rows a page against the scan's thirty-five, and one page with seven hundred and
   forty-eight. Merging fragments within four points of one another in y brought the median to
   forty.

Each of those was a real fault and each was worth finding. **None of them saved the instrument.**

## The refutation

The reading wave established ground truth on printed page 91 independently, two readers
agreeing and both checking against a second printing: **three paragraphs indented that the plate
sets flush, and two set flush that the plate indents.** Our page should therefore carry one MORE
indent than the plate.

The instrument reports the plate indenting nine and the book four — **five fewer**, where the
truth is one more. It is not measuring the quantity it names.

## Why, and what it says about counting instruments in general

The count is dominated by rows that are not paragraphs. Displays, equation numbers, the
continuation lines of hanging items and the fragments of tall mathematics all land at various
offsets from various margins, and a sizeable share of them fall in the 0.6-to-1.4-quantum band
by accident. The two sides accumulate different amounts of that contamination because they break
lines differently — which is exactly the difference the count was supposed to be immune to.

**A count is only correspondence-free if the things counted are identified reliably.** Dropping
the correspondence did not remove the identification problem; it hid it, and the instrument
inherited a bias it could not see. The counting was never the hard part.

## What survives

The four defects found while building it are real and are fixed in the tool that failed, which
is kept for them. Two of them — the deskew, and the merging of fragments into typographic lines
— are general and belong in any instrument that reads geometry off this kind of scan.

And the direction E02 pointed at is now the only one left: **take our side from the source,
where the enclosing environment and every paragraph break are known exactly, and use the scan
only for the half where nothing else is available.** The failure here was trying to recover from
a rendered page a fact the source states outright.
