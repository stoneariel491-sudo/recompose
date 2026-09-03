# E08 — When an instrument and a reader agree, and whether that can be engineered

**Status: one observation, one law extracted, three predictions fixed in writing before the
evidence that would test them arrives.**

## What happened, unpredicted

On one day of the case study, a human reader measuring a scanned plate and an automated sweep of
the whole book reported the same defect on the same line of the same page, independently. In
several months of the case study that had never happened. Every instrument built for that fault
class had, until then, produced findings no reader confirmed and missed findings every reader made.

This file exists because *an accident that can be explained is a design rule, and one that cannot
is a coincidence.*

## The law, and the evidence that it is not a coincidence

**An instrument converges with a human reader exactly when it measures the same physical
difference, in the same frame, and refuses where the reader would say "I cannot tell."**

The one instrument that agreed measured a line's left ink edge against the left ink edges of the
prose lines around it, on that one leaf, and used nothing else. Every instrument that has never
agreed substitutes a representation the reader never touches:

| what it measures | agrees |
|---|---|
| the ink, as a within-leaf difference | yes |
| a compilation of the page source **in isolation** | never — and the defect it hunts is introduced by the assembler, which is not in that source |
| line populations clustered into rules with count floors | never — the floors delete exactly the one-line differences that are the fault class |
| a markup environment stack | never — the stack resets per page file and the environment opens on an earlier page |
| a page index built by position | never — and worse, it discarded answers it had already computed correctly |

The corollary is a test you can apply before writing any instrument: **state what it measures as a
sentence a person could execute against the page with a ruler.** If you cannot, it is measuring a
model of the page, and it will not converge however sophisticated it is.

## What was needed to make it measurable rather than admirable

A principle is not repeatable. Two artefacts turn it into a number:

- **a ground-truth ledger** — reader findings as rows rather than prose, each keyed by the *text of
  the line* and not by a line number, carrying the measurement, its frame, how many readers agreed,
  and the sub-domain the finding belongs to. Rows recording lines readers examined and confirmed
  **correct** matter as much as the faults; they are the only way to catch an instrument that
  reports them anyway.
- **a scorer** that runs each instrument against those rows and reports, separately, its recall
  *on its own domain* and *over the whole class*. Those are one measurement against two
  denominators and only the first is about the instrument; the gap between them is coverage.
  **Coverage and accuracy are different facts and a single recall number hides which one you have.**

### Three ways the scorer lied before it worked

Each was caught by a number that could not be what it claimed, and each generalises.

1. **It scored the instruments against the repaired document.** The one tool that had found the
   defect that morning scored zero — correctly reporting the nothing that was left. *An instrument
   can only be scored against the state that contained the defect.*
2. **Pinning that state pinned the instruments too**, and the same tool scored zero again because
   it had not existed at that commit. **Pin the data, float the instrument.**
3. **It demanded the identifier and the evidence on one output line**, and the tool prints them on
   two. A scorer that cannot see a two-line report measures the report's shape, not the instrument.

## The second convergence, this one engineered

The law was then used deliberately, on a different question. A reader had found that one of the
document's machine-proved claims was an instance of a general algebraic law — true under every
substitution, so the gate could never refuse it, and, decisively, *neither of the two errors that
page's own annotation warns about would have made it fail.*

Stating that as something a reader does: **break the claim on purpose and see whether the prover
notices.** Swap two of its symbols, perturb an integer, flip a sign. A claim that survives every
mutation constrains nothing that could have gone wrong.

The instrument built from that sentence **reproduced the reader's two findings exactly and then
found seven more**: of 119 machine-proved claims in the document, 109 can fail, 9 cannot, and 1 the
mutations could not reach — which is reported as unattacked, not as sound, because *an empty
mutation set is not a passing grade.*

This is the same architecture as `plant.py` (E07) pointed at a different target. E07 asks whether an
instrument can see a defect planted in the **document**; this asks whether a **check** can fail at
all. The second question is sharper and much cheaper, and nothing in E07 could have answered it.

## Predictions, fixed before the evidence

Two readers are working printed pages 254–261 and a third is replacing the nine hollow claims. None
has reported. The following are recorded now so they can be wrong.

**P1 — the law is complete for instrument faults.** Every instrument fault the 254–261 readers
report will be traceable either to the instrument using a representation the reader does not
(compiled source, statistical rule, environment stack, positional index), or to a frame constructed
from the wrong lines. *A reported fault whose cause is neither refutes the law as stated* and the
table above is then incomplete rather than merely short.

**P2 — the repaired frame holds outside its calibration range.** The sweep will judge, rather than
refuse, at least 2 of the 8 page openings in 254–261, and will report no defect on a line the
readers confirm correct. The second half is the one that matters: the frame repairs were fitted on
a range the readers had already settled, and a fix that only works where it was fitted is a fit.

**P3 — vacuity is usually a property of the page, not of the claim.** At least 2 of the 9 hollow
claims will come back as "this page has no falsifiable arithmetic", rather than as a claim that
could have been written better. If instead all nine get good replacements, then vacuity was
carelessness and the fix is a habit; if several pages genuinely have nothing to state, then the
document has *structural* pages that no arithmetic gate can cover, and that is a coverage hole to
be named rather than a defect to be repaired.

## Why this matters beyond the case study

The pipeline's whole claim is that its output contains nothing false. That claim rests on gates,
and **a gate that cannot fail prints the same word as one that can.** Before this experiment there
was no way to tell the two apart except by reading every gate by hand — which is the labour the
pipeline exists to remove.

More generally: this is the first measurement in the project of *whether the automation and the
human agree*, as opposed to whether the automation runs. Those had been treated as the same
question. They are not, and the ledger is what keeps them apart from here on.
