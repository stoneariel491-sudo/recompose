# E09 — A law refuted three hours after it was published, and the two it left standing

**Status: E08's central design rule survived. Its worked example did not, and was refuted by the
same kind of reader the rule is about.**

## What was published, and what happened to it

E08 recorded that an instrument agrees with a careful human reader exactly when it measures the same
physical difference in the same frame. That rule held. Alongside it, `src/frame.py` published a
worked instance:

> **The frame is the densest cluster, never the minimum.**

Three hours later a reader working the case study refuted it on one page. The window there is
`[595, 579, 413, 413, 580]` — one display row and **two indented openings** against two flush lines
— so the densest cluster is 584.7, which is the *indent* rule. A line at 411 was measured against it
and reported flush. **Flush is the right answer, for a reason that has nothing to do with the page.**

Two more rules followed, each fixing the last and breaking the next:

| rule | what refuted it |
|---|---|
| `min(window)` | a numbered display hangs its number a full quantum left of every line of type |
| the densest cluster | a window may hold more indented lines than flush ones |
| the leftmost cluster | the leftmost rule on the leaf is not the rule the line belongs to |
| the rightmost at or left of the line | that rule may carry a single line, so no cluster forms on it |

**Every one is the same failure.** A page in a mathematical book carries three rules — equation
numbers, the proof block, the block's own indent — so *"the frame" is not a property of the leaf*,
and any rule that picks one number will pick the wrong level on some page.

## The correction, which is a change of question

The instrument does not need the frame. It needs the answer, and the answer has exactly two
admissible values:

    FLUSH     some rule in the window stands level with the line
    INDENTED  some rule stands one quantum to its left
    neither   REFUSE

**A single line is enough to witness a rule, because the hypothesis being tested already says where
that rule must be.** The four earlier versions needed a cluster because they were *searching* for
the frame rather than *testing* for it, and a search needs support where a test needs only a
witness.

Measured on the case study: the control went from 4 right and 8 refused to **12 right, 0 wrong, 0
refused**, and the instrument's reach over the whole book went from 31 page openings judged to 127.

## The result that generalises furthest

**A test whose cases all share one answer cannot detect an error that preserves that answer.**

The control that should have caught the second version could not. Its twelve cases had all been
settled by hand and all had the same verdict — the plate runs the line on — so a frame displaced one
quantum to the *right* still returns "flush" on every one of them. The third version was caught by
that same control only because it happened to err in the other direction.

This is not a fact about margins. **Any control assembled from cases that were interesting for one
reason will share that reason**, and the errors it cannot see are exactly the ones that respect it.
A control needs cases with both answers, and if the corpus only offers one, that is a property of
the control to be written down and not a property of the instrument.

## Two more laws from the same day, both about the toolchain rather than the document

**A mangled command typesets as English.** A tool wrote a LaTeX command in a non-raw Python string;
the escape was eaten and what reached thirteen files was the command's name with its first letter
removed. It printed, on twelve pages of the built book, and nineteen lines meant to run flush were
indented instead — the exact opposite of the cure being applied.

Nothing could see it: a missing brace is a build error and **a missing backslash is prose**. The
class is exactly definable, which is what makes it a gate rather than a habit: a backslash
disappears only before the escape letters, so a command lost this way is always its own name minus
one letter. And the corpus is its own dictionary — an English word appears elsewhere mid-line, and a
bare command appears nowhere but at the head of one.

*The comment written to document this was itself eaten while being written*, arriving with a BEL
that stopped the file compiling. The rule is not care; it is **write no backslash through a shell**.

**A pipeline's input can silently become its own output.** The case study's cleaning tool reads a
path that came to hold the *recomposed book* under the source scan's filename. It would have cleaned
our own output and written a laundered copy of the document being checked, with no error at any
step, because a PDF is a PDF and every operation is defined on it. Every gate downstream would have
gone on passing while comparing the book with itself.

The guard needed two attempts, and the first is the instructive one: it asked whether the first
twelve pages carry the project's own page marker, and they do not — the markers begin after the
front matter, so it read the title page and let the book through. **The discriminator has to hold on
every page, not on the pages you happened to sample.** The one that does is blunt: a scan is images
and a recomposition is type.
