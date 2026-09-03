# The pipeline

Six stages. For each: what it does, what runs without a person today, what does not, and the
question that has to be answered before it can.

The stage numbers are not a schedule. Stage 4 runs against the output of stage 5 and feeds back
into stage 3, and that loop is the product.

---

## 1. Ingest

Take the scan apart without believing any of it.

**Separate the leaves by kind.** A photographic leaf and a bilevel stencil want opposite
treatment, and a pipeline that treats them alike destroys one of them. The discriminator is ink
fraction: a threshold at 0.11 separated the two photographic leaves of the case study from the
354 stencils, and the fraction is a property of the leaf, not of a guess about it.

**Composite each page at the native resolution of its highest layer.** The reason is unchanged
and is the whole point: a 1-bit stencil re-rendered at 300 dpi has already lost the evidence that
decides whether a mark broke or merely thinned.

**But "extract the image, never re-render the page" is wrong, and it was written here and
refuted by running it.** A scanned PDF is normally mixed raster content: each page carries a
blurred background at 200 dpi and a stencil at 600, and the foreground layer pulled out ALONE is
not the leaf — measured, it never rises above grey 167 where paper would be 255. Composited at
the dpi the top layer implies, the same pages come out byte for byte the size the case study's
plates were extracted at by hand, with 0.017 per cent of pixels differing. Native resolution is
preserved because the dpi is READ OFF the layer rather than chosen.

Three rules were needed and each looked sufficient until it was tried. **Counting images is not
enough**: every page of one processed PDF carries two, and both are one pixel square. **Covering
the page is not enough either**: a 1×1 image stretched over the leaf has a perfect placement
rectangle and carries nothing — so an image is a leaf when it covers the page *and* resolves it.
**And a real scan carries two of them**, which is the normal structure and not an anomaly.

**A stencil's polarity is not guaranteed, and the discriminator is true of every book: a page of
type is never more than half ink.** A fraction above a half is a stored polarity running the
other way, not a very black page. Stronger than sniffing the colour space, because it is a fact
about the leaf rather than about how someone encoded it.

**And the ink threshold is the leaf's own.** A fixed 128 read a full page of type as 0.26 per
cent ink and called it blank, because that leaf was scanned faint under a gradient; half a test
range was classified blank that way and the other half was not, purely from the scanner's
exposure alternating. Otsu per leaf — **and refused where Otsu's own two-mode assumption fails**,
which a faint gradient-lit leaf violates. Below a separability of 0.70 the leaf is reported as
*unbinarised*: not blank, not photographic, not a guess. It needs a local threshold, and that is
named as work rather than faked with a global number that happens to run.

**Take the text layer as a hint and never as truth.** In the case study the OCR read commas as
full stops throughout an index, read the figure one as a capital I, gave every word on four
leaves an identical synthesised height of 5.0 pt, and put two adjacent lines in the wrong order.
It was still useful: its geometry located the columns. **What a bad instrument is good for is a
question with an answer, and the answer is rarely "nothing".**

*Automated.* All of it, and runnable: `python src/ingest.py <scan.pdf> <out>` writes the leaves
and a manifest carrying, per leaf, its ink fraction, its separability, its kind, and **how it was
obtained** — composited, rendered, polarity inverted — so a later stage can refuse rather than
guess. Verified end to end against the case study's original: 41 of 41 leaves classified, and
stage 2 fits the layout from what stage 1 produced.

---

## 2. Measure the design

Recover the book's own typography from the ink, as **ratios between two measurements on the same
leaf**.

This used to read "as fractions of the leaf so that scan resolution cancels", and E06 refuted it
by measuring. **Resolution cancels. Registration and crop do not.** The case study's plates are
2691 × 4060 px at an aspect of 1.5087 against a 6 × 9 trim's 1.5000, they are cropped inside the
trim by about one per cent of the width, and every leaf sits at its own offset — body margins
vary by sixty pixels across thirty leaves while their justified spans agree to one per cent. A
fraction of the leaf is invariant to the scanner's dpi and to nothing else about the scanner.

Two rules follow, and both were bought with a wrong answer:

  * **Within a leaf first, across leaves second.** A parameter that is a DIFFERENCE — a measure,
    a quantum, a pitch — is a within-leaf quantity. Pooling positions from unregistered leaves
    measures the UNION of their text blocks: it gave a measure wider than the justified span of
    any single leaf in the sample, and a text block half a per cent too *long* where a page's
    ink, ending at its last line, should have made it short. Two errors of opposite sign nearly
    cancelling is the worst way for a number to be right.
  * **The left ink edge is not the margin.** It is the margin plus the first glyph's left side
    bearing: a T, an x, an L and a u flush at one margin land at four different ink edges.
    Measured rather than assumed — from the spread within a leaf's densest cluster of line
    starts — that noise is 1.79 per cent of the leaf in the case study, about 7 pt, **a quarter
    of the indent quantum it is trying to resolve.** Below that floor no margin difference
    recovered from ink can be believed, whatever tolerance the clustering is given.

What has to come out: trim, text block, measure, leading, the indent quantum, type size, column
structure and gutters, head positions, the drop of an opening, footnote geometry.

**Type size is calibrated on WIDTH, not on the height of the ink.** In the case study the height
of the ink said 6.25 pt and the width of a line said over 8, and no single size reconciles them.
The difference was weight: the index is bold, measured at 1.91 times the body's ink density. The
resolution was to set the same ten lines at four candidate sizes and compare each against the
scan — 6.5 pt gave 0.860 of the plate's width, 7 pt 0.926, 7.5 pt 0.992, 8 pt 1.059. Width is
also the quantity that decides which lines turn, so it is the one that matters.

**And the scale must be derived from something known, not from the leaf's dimensions.** The
body is set justified to a chosen measure, so the ink of a body leaf spans exactly that measure
and nothing has to be assumed: four leaves gave 266.4 scan pt for a 360 pt measure, so 1.3514.
The leaf's own dimensions gave 1.330, out by 1.6 per cent — small until it is multiplied through
a column width.

*Automated.* **The continuous parameters, yes** — `src/fit_layout.py` takes a directory of leaves,
chooses body leaves by ink fraction alone, and returns the measure to 1.2 per cent, the baseline
pitch to 0.1 per cent and the text block to 1.3 per cent, against a case study whose answers were
established over weeks by other means. It is given no page numbers, no trim and no answer.

**The indent quantum, not yet**: 15 per cent low, which is the first time this project has
recovered it to the right order of magnitude and is still not good enough to set type by. The
obstacle is named and measured rather than shrugged at, and the next move is a different
measurement rather than a better clustering — the quantum taken from pairs of lines inside one
paragraph, where both edges' glyphs are known, instead of from margins whose glyphs are not.

The trim itself is not recoverable and should stop being asked for: a leaf of ink says nothing
about the paper it was cut from. It enters from outside, and everything else is a ratio until it
does.

---

## 3. Transcribe

Produce source that carries its own claims.

Every page file opens with a header that states what was checked and how, in machine-checkable
forms: an identity that must be true, an inequality whose strictness must be decided, a set
identity provable by truth table, a string the page must contain, a confidence declaration.

**The declaration is calibrated, not believed.** Effort follows difficulty, but indexing effort
on the transcriber's own confidence is worthless because transcribers are overconfident. So the
third component of the scale is what readers actually found on pages of each declared level: if
"high" keeps yielding findings, the declaration is worthless and the floor rises. That number is
printed on every run so the scale cannot drift into wishful thinking.

*Automated.* The checking is. The transcription is not, and the honest position is that a
generative model transcribing a page is a fourth reader, not a source — its output enters the
same adjudication as everyone else's.

---

## 4. Verify

The part nobody ships.

**Instruments, and the blind spot of each, measured.** In the case study, on one four-page index:

| instrument | what it found | what it cannot see |
|---|---|---|
| the sort — the list is alphabetical | four misread letters that move an entry | a misreading that files in the same place |
| the page — every entry claims a term is on a page we hold | `poinl` for `point` | drowns real faults among legitimate synonyms; silent on entries whose page it cannot fail |
| the vocabulary — does this word occur anywhere in the book | three words that exist nowhere | a word that exists and is still wrong |
| the ink count — rows of ink against lines recovered | an entry the source never contained at all | anything about the entries it did contain |

**The fourth is the one to keep in mind.** A test can only report on what it is given; to find
what you were never given, you have to count something else.

**Coverage is published with its bias.** Not "89 per cent of marks were examined" but "89 per
cent, and the eleven never reached are not a random eleventh: a mark that merely thins still
pairs and is ranked, while a mark that breaks clean through leaves the examined set entirely.
The instrument is least able to see exactly where the damage is worst."

**Ensembles are unioned, never voted.** Measured: E01.

*Automated.* The mechanical gates are. The reading is not, and the reading is where every
correction of the case study's first chapter came from.

---

## 5. Compose

Typeset to the measured design, then **close the loop on the finished page**.

The distinction that matters: a value measured on the source is not the value to supply. What
was measured on the case study's index was where the first entry's ink begins, 46.248 per cent
of the leaf. What had to be supplied was a skip, and between them lie the material a column head
inserts and the metrics it inserts them in. Asking for the difference outright put the ink
fourteen points low — five entries, and a fifth leaf. **Build once, measure where the ink landed,
subtract the error.**

Three traps, each found by being fallen into:

  * **A global setting is applied to you whether you asked or not.** A `\linespread` measured for
    the body multiplied an index leading measured for the index, and the correct number produced
    the wrong result. Cancel the ambient setting inside any block set at a different size, and
    cancel it *before* the size.
  * **A setting has a moment as well as a scope.** `\textheight` is read when a page is built, so
    a change made on an open page reaches the page after it.
  * **A definition made for one place is in scope everywhere.** Three separate instances in one
    project: an equation-tag redefinition inherited by every cross-reference, a second page style
    clobbering the first through shared registers, a linespread multiplying an unrelated size.

*Automated.* Yes, including the closed loop.

---

## 6. Account

State what is known, what is not, and how much of each.

A refutation is a deliverable. In the case study more than half of one day's work produced a
measured **no**, and two of those refutations corrected claims already written down. A gate that
cannot decide must never be the one that condemns.

---

## The instrument matrix

The claim this repository exists to support is not "we check a lot of things". It is:

> For each class of defect, here is the measured recall of each instrument, here is the residual
> after all of them, and here is the argument that their failures are not correlated.

Recall is measured by **planting**: take a correct page, introduce a defect of a known class,
and see which instruments report it. Independence is measured the same way — plant one defect
and see whether two instruments fail together.

That matrix does not exist yet. E01 is its first row.
