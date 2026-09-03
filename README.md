# recompose

**Turn a scan of a printed book into typeset source that provably says the same thing.**

---

## The problem

A scanned book is an image. OCR turns it into text that is *mostly* right, and mostly right is
worthless for a book of mathematics: one lost bar over a variable, one inequality that turns
round, one subscript that did not print, and the page is false while looking perfect.

Every pipeline on offer — OCR engines, layout reconstructors, a large model asked to transcribe
— produces an artifact whose errors are **invisible by construction**, because the only thing
that could reveal them is the thing that produced them. The output is confident and unfalsifiable,
which is the worst combination an artifact can have.

## The claim

You can do much better, and the way is **not a better recogniser**. It is four things:

1. **Every editorial decision is written as a machine-checkable assertion, inline with the text
   it concerns.** Documentation that can be refuted stops being documentation and becomes a test
   suite. Documentation kept in a separate file always drifts, and nobody ever finds out.

2. **Verification uses several instruments whose blind spots are measured and do not overlap.**
   Not "we ran some checks" — a matrix of *measured* recalls, instrument against defect class,
   with the residual computed.

3. **Coverage is published with its bias.** Not "89 % of marks were examined" but "89 %, and the
   11 % never reached are not a random eleventh: a mark that breaks clean through leaves the
   examined set entirely, so the instrument is least able to see exactly where the damage is
   worst."

4. **Nothing is decided by a vote.** An ensemble buys *recall*; the source decides. This is not a
   slogan - it is measured, and voting costs 43 points of recall on the one defect class that
   matters most. See `RESEARCH/experiments/E01`.

## What this is not

Not an OCR engine. Not a layout reconstructor. Not a model. It is **the apparatus around them
that makes their output trustworthy, and the measurement that says how trustworthy** — which is
the part nobody ships.

## Provenance

Every method here was derived on a real book and not designed in the abstract: Walter Rudin,
*Principles of Mathematical Analysis*, 3rd ed., 338 printed pages, from a damaged 1-bit Internet
Archive scan, recomposed to a declared standard of **contains nothing false**. That work produced
104 numbered principles, each with the measurement that forced it, and about sixty tools.

The case study lives in `../rudin-recompose`. What lives here is the general form: what
transfers, what was specific to one book, and what is still an open question.

**The discipline of this repository is the discipline of that one.** A hypothesis is written
down before the result. A refutation is a deliverable. A number is a fact about its population.
An instrument that cannot decide must never be the one that condemns.

## Layout

    DESIGN/          the pipeline and its stages; what is automated, what is not, and why
    RESEARCH/        numbered findings, each with its evidence
      experiments/   one file per experiment: hypothesis BEFORE result, always
      measurements/  raw numbers, so a claim can be recomputed rather than believed
    src/             the code
    tests/           including PLANTED defects, which is how recall is measured at all

## Status

Early. The case study is at 94 % machine-verified and 8 % read line by line; the general form is
being extracted from it while that reading proceeds. Nothing here is claimed to work on a book it
has not been run on.
