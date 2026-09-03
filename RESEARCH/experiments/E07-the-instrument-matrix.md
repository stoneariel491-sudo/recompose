# E07 — The instrument matrix, measured at last, and what it says is uncomfortable

Q1 has stood open since this repository was created: *for each class of defect, the measured
recall of each instrument, the residual after all of them, and the argument that their failures
are not correlated.* E01 measured one column by hand. E02 characterised one instrument by
planting sixteen defects into a worktree over a day.

`src/plant.py` measures it mechanically. Six defect classes, planted one at a time into a
temporary copy, against the five instruments that read the source.

## Result

```
                  para_census  header_vs_body   eqnumbers  record_check  limits_scope   union
AFTER-DISPLAY             5/5             0/5         0/5           0/5           0/5     5/5
RUN-ON                    2/2             0/2         0/2           0/2           0/2     2/2
SUPPRESSED-JOIN           5/5             0/5         0/5           0/5           0/5     5/5
HEADER-NUMBER             0/3             1/3         0/3           0/3           0/3     1/3
SIGN-FLIP                 0/5             1/5         0/5           0/5           0/5     1/5
LOST-EMPHASIS             1/1             0/1         0/1           0/1           0/1     1/1
```

**A reversed inequality in the body is essentially uncovered.** One instrument catches one plant
in five, and no other sees it at all. That is the sharpest thing in the table: the defect class
with the worst consequences — a wrong relation direction changes what a theorem says — has the
weakest mechanical cover in the project, and the only thing standing between it and the reader is
whether a header happens to name that particular relation.

**A wrong number in a CHECK line is caught one time in three.** The mechanism written to close
the printed-page-67 hole — a header claiming what the body denies — finds a third of them.

The three classes with full recall are all `para_census`'s own, which is the shape one expects
and is worth stating rather than assuming: it does what it says, on what it says, and nothing
else. Its 1/1 on LOST-EMPHASIS is an artefact — stripping an `\emph` shifted a line and moved a
census row — and a single trial is not a measurement.

## Two things the harness learned about itself before it could measure anything

**A harness must invoke an instrument the way the work invokes it.** The first run scored
`para_census` ZERO on its own two classes. Invoked bare it prints class totals and no per-page
rows, so nothing in its output could name the planted page. The instrument was working and the
harness was asking it the wrong way.

**A hit is a difference, not a mention.** The second run scored `para_census` a perfect row on
all six classes, including two that are not its classes and one it has no machinery to see. It
lists about fifteen hundred candidate rows over the book, so every page is named in every run and
every plant looks like a hit. The harness's own docstring had warned that a tool reporting
everything scores perfectly and is worthless; one run turned the warning into a measurement.

Each instrument is now run once on the clean corpus and a plant counts only if it produces a line
the clean run did not have. **That is the same correction the layout fitter needed a level down:
measure the change, not the state.**

## What this does not measure

**Precision.** A planted corpus says nothing about how often an instrument cries wolf on a clean
one; that has to be measured the other way round.

**The instruments that read the plate.** `indents.py`, `margins.py` and `left_edges.py` cannot
run inside a temporary copy without carrying six hundred megabytes of images into it. Their
absence is a gap in the measurement, not a judgement — `margins.py` saw two faults in one wave
that the tool named for them did not.

**Correlation.** The per-plant record kept here is what a correlation needs — two instruments
failing on the SAME plant is the observation that says their blind spots coincide — but six
trials per class is too few to say anything.

## Why this was urgent rather than merely due

On one day of the case study, four instruments were found to be reporting on nothing at all: two
would not compile, a census class had never once reported a member because its branch sat behind
a catch-all, and a gate scored a falsified page exactly as it scored the true one because its
canonicaliser deleted the very operator being checked. **All four were found by a person asking
why a tool said what it said.** Every one of them comes out of this table as a row of zeros in a
minute and a half.

**An instrument with recall zero and an instrument with nothing to report look identical from
outside. The only thing that separates them is a defect you put there on purpose.**
