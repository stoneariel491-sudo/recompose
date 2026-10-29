# recompose

> **En bref (français).** recompose étudie comment transformer le scan d'un livre imprimé en
> source composée (LaTeX) dont on peut *prouver* qu'elle dit la même chose que l'original. Ce
> n'est pas un moteur d'OCR : c'est l'appareil de vérification autour de lui (instruments dont
> on mesure les angles morts en y plantant des défauts, hypothèses écrites avant les résultats,
> réfutations publiées) et le code Python des premières étapes du pipeline.

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
   slogan - it is measured: on structural defects, three readers together found all fourteen,
   and a two-of-three majority would have shipped five of them (36 %), every one of them real.
   See `RESEARCH/experiments/E01`.

## What this is not

Not an OCR engine. Not a layout reconstructor. Not a model. It is **the apparatus around them
that makes their output trustworthy, and the measurement that says how trustworthy** — which is
the part nobody ships.

## Provenance

Every method here was derived on a real book and not designed in the abstract: Walter Rudin,
*Principles of Mathematical Analysis*, 3rd ed., 338 printed pages, from a damaged 1-bit Internet
Archive scan, recomposed to a declared standard of **contains nothing false**. That work produced
104 numbered principles, each with the measurement that forced it, and about sixty tools.

The case study itself (the scan, the recomposed pages and its tools) lives in a separate
repository that is not public. What lives here is the general form: what transfers, what was
specific to one book, and what is still an open question.

**The discipline of this repository is the discipline of that one.** A hypothesis is written
down before the result. A refutation is a deliverable. A number is a fact about its population.
An instrument that cannot decide must never be the one that condemns.

## Layout

    DESIGN/          the pipeline and its stages; what is automated, what is not, and why
    RESEARCH/        numbered findings, each with its evidence
      experiments/   one file per experiment: hypothesis BEFORE result, always
    src/             the code
    tests/           including PLANTED defects, which is how recall is measured at all

## Run it

Python 3.10 or newer. The tests need only NumPy and build their own pages, so they run without
any scan:

    pip install -r requirements.txt
    python -m unittest discover -s tests -v

The pipeline stages also need Pillow, and stage 1 needs PyMuPDF to open the PDF
(`pip install pillow pymupdf`; they are not in `requirements.txt` yet):

    python src/ingest.py <scan.pdf> <output directory> [--pages 40-80]   # stage 1: leaves + manifest
    python src/fit_layout.py <directory of page images> [--json]        # stage 2: fit the layout
    python src/plant.py <config module>                                  # the instrument matrix

`src/case_study_plants.py` is the adapter that wires the planting harness to the case study's
own instruments; it expects that private case-study checkout on disk and is not runnable on
its own.

## What the code is

| | |
|---|---|
| `src/ingest.py` | stage 1: classify each leaf of a scanned PDF by ink fraction, composite mixed-raster pages at the native resolution of their top layer, per-leaf Otsu threshold with a separability check, and a manifest that records how each leaf was obtained |
| `src/fit_layout.py` | stage 2: fit measure, baseline pitch, text block and indent quantum from the leaves alone |
| `src/geometry.py`, `src/frame.py` | the geometric primitives (deskew, ink rows, margins, line frames) the stages are built on |
| `src/plant.py` | the planting harness: inject one known defect, rebuild, run each instrument, count what changed |
| `tests/` | 27 unit tests on constructed pages whose right answer is known in advance |

## Status

Early. The case study is at 94 % machine-verified and 8 % read line by line; the general form is
being extracted from it while that reading proceeds. Nothing here is claimed to work on a book it
has not been run on.

Honest limits: one book has been processed end to end (the case study). Stages 3 to 6 of
`DESIGN/ARCHITECTURE.md` are partly automated in that case study, but their code is not in this
repository yet. Several results rest on small samples, and the research files say so (E07 and
Q1 in `RESEARCH/00-INDEX.md`: six trials per defect class is "far too few" for correlation).

## How it was built

I built this project by directing AI coding agents (Claude Code): I set the goals, the
constraints and the verification method, and reviewed the results; the agents wrote most of the
code and documentation. The independent readers counted in E01, E02 and E05 were also separate
agent runs, each given the scan and the source.
