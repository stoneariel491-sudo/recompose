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

**Extract each page at its native resolution.** Not a re-render of the composited page — the
stencil itself. A 1-bit JBIG2 stencil re-rendered at 300 dpi has already lost the evidence that
decides whether a mark broke or merely thinned.

**Take the text layer as a hint and never as truth.** In the case study the OCR read commas as
full stops throughout an index, read the figure one as a capital I, gave every word on four
leaves an identical synthesised height of 5.0 pt, and put two adjacent lines in the wrong order.
It was still useful: its geometry located the columns. **What a bad instrument is good for is a
question with an answer, and the answer is rarely "nothing".**

*Automated.* All of it.

---

## 2. Measure the design

Recover the book's own typography from the ink, as fractions of the leaf so that scan
resolution cancels.

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

*Automated.* Partly. The measurements exist as tools; choosing which to make is still a person.
**Open question: can the set of measurements be derived from the page rather than chosen? A
layout is a small grammar, and fitting a grammar is a well-posed problem.**

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
