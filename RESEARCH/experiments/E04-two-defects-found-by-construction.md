# E04 — Two defects in the surviving primitives, found by constructed pages

The four primitives in `src/geometry.py` are the part of E03 that survived its refutation. They
had been read carefully, they had produced the measurements E02 and E03 report, and they had
never been run against an input whose right answer was known in advance.

**Hypothesis, written before the tests were run:** the primitives are correct. They were
extracted from working instruments rather than written fresh, and the faults E03 catalogued were
faults of the *instrument built on them* rather than of the primitives themselves. The tests are
expected to pass, and their value is expected to be regression cover — holding the primitives
still while the pipeline above them changes.

**Result: two of the four are wrong, and one is wrong in exactly the case it was written for.**

---

## Method

Sixteen tests over four primitives, on pages constructed rather than observed. A page is built
from a stated geometry — a body margin at 100, an indent quantum of 26, a tilt of twenty points
per thousand down the leaf, every third line indented — so the answer is known before the
function is called and a wrong answer is a failure rather than a difference.

Running a primitive over a real scan and checking today's answer against yesterday's tests
nothing: it locks in whatever was already wrong. That is precisely how these two survived.

Where a simpler alternative exists — the mode instead of the clusters, the raw edges instead of
the deskewed ones, a plain least-squares fit instead of the iterated envelope — the test runs the
alternative too and asserts that it fails. A test that only shows the code doing what the code
does is worth less than the time it takes to run.

---

## Defect 1 — `local_frame` accepted the exact tie it was built to reject

The primitive returns the margin a line should be measured against, taken from the lines that
follow it, and returns nothing when those lines do not agree. The whole point is that the
following lines routinely cross out of the opening's block, and the modal edge of a mixed
population is not a margin.

The agreement test read

    if best < agreement * len(tail): return None

with `agreement` 0.5 over the six following lines. A three-three split gives `best` = 3 against a
threshold of 3, `3 < 3` is false, the guard passes, and `min()` then returns the smaller of the
two margins.

A three-three split is not a near miss here. **It is the case the guard was written for**, and it
is written down in the source of the instrument that motivated it: on printed page 87 the six
lines following an opening are three at the body margin of 28.9 and three at an indented block's
48.6. The guard was pointed at that page and let it through.

Corrected to `best <= agreement * len(tail)`, so agreement means a strict majority.

**What made it invisible.** The instrument built on this primitive reports a *worklist*, and its
own status banner says a third of its reports are false. A frame returned where none exists
produces one more entry on a list already known to contain false ones. The failure had nowhere
to show up as a failure.

## Defect 2 — `pdf_lines` bucketed where its docstring said it grouped

The primitive merges the fragments an extractor makes of one printed line — a fragment per
fraction, per superscript, per radical — and the docstring states the rule: *fragments within
`tol` points of one another in y on the same leaf are one line.*

It did not do that. It rounded y to a multiple of `tol` and merged what landed in one bucket,
which is a different rule: two fragments two points apart, straddling a bucket edge, come back as
two lines. On the constructed page, a fragment at y = 102 sat between its own line's 100 and
101.5 and was split off from both, giving three lines where the page has two.

Grouped by the gap instead, with the group's anchor its first fragment rather than its last, so a
run of fragments each just under `tol` apart cannot chain into a line of unbounded height.

**A second thing, not a defect but a loss.** The old code kept only the leftmost fragment's
*text* and discarded the rest, so a line of mathematics came back as a numerator. The use this
primitive exists for is locating a paragraph by the words it opens with — measured at 98 matches
in 100 — and a match on the opening words fails whenever those words span two fragments. The
fragments are now joined in the order they are set.

---

## What this is evidence for

The primitives were extracted from instruments that worked, and were trusted on that ground. But
an instrument that reports a worklist can carry a broken primitive indefinitely: its output is
already known to be part wrong, so one more wrong entry changes nothing anyone looks at. **A
component is only tested by an input whose answer is known independently of it.**

That is the same finding as E03, one level down. E03 refuted an instrument for dropping the
correspondence between the two sides and thereby hiding the identification problem instead of
removing it. Here the correspondence between a primitive and its own docstring was dropped, and
the docstring — `local_frame`'s naming the three-three page, `pdf_lines` stating the tolerance
rule — turned out to be the correct specification in both cases. **Both primitives were tested
against what they say they do, and both were found not to do it.**

The practical consequence for the pipeline: every primitive gets constructed inputs before
anything is built on it, and the tests run on every push rather than when someone remembers.
