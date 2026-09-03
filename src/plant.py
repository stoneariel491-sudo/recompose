"""Measure what each instrument can actually see, by planting defects it ought to find.

THIS IS Q1, AND THE REPOSITORY SAYS IT IS THE CLAIM EVERYTHING RESTS ON. The argument this
method makes is not "we check a lot of things". It is:

    for each class of defect, here is the measured recall of each instrument, here is the
    residual after all of them, and here is the argument that their failures are not correlated.

That matrix did not exist. E01 measured one column of it by hand and E02 characterised one
instrument by planting sixteen real defects into a worktree - by hand, once, over a day.

WHY IT IS URGENT AND NOT MERELY DUE. On one day of the case study, four instruments were found
to be reporting on nothing at all: two would not compile, a census class had never once reported
a member because its branch sat behind a catch-all, and a gate scored a falsified page exactly as
it scored the true one because its canonicaliser deleted the very operator being checked. **All
four were found by a person asking why a tool said what it said.** Every one of them would have
come out of this harness in seconds as a row of zeros.

**An instrument with recall zero and an instrument with nothing to report look identical from
outside.** The only thing that separates them is a defect you put there on purpose.

HOW IT WORKS. A defect class is a function that injects ONE instance into a copy of the corpus
and says where it put it. An instrument is a command and a way of asking whether its output
named that place. The harness plants one defect at a time - never two, so attribution is never
ambiguous - runs each instrument, and records hit or miss.

WHAT IT MEASURES AND WHAT IT DOES NOT. Recall, per class, per instrument. Not precision: a
planted corpus says nothing about how often an instrument cries wolf on a clean one, and that
has to be measured the other way round, by running the instruments on the corpus as it stands
and adjudicating what they say. Not correlation either, yet - though the per-plant record kept
here is exactly what a correlation needs, since two instruments failing on the SAME plant is the
observation that says their blind spots coincide.

    python src/plant.py <config module>        # the whole matrix
    python src/plant.py <config module> --class AFTER-DISPLAY
"""

import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


class Defect:
    """One class of defect, and a way to introduce a single instance of it.

    `inject(root)` mutates the copy at `root` and returns a list of the places it changed, each
    a (file, line) pair - or an empty list if it could not find anywhere to plant. A class that
    can never plant is reported as such rather than silently scoring nothing.
    """

    def __init__(self, name, inject, describes):
        self.name = name
        self.inject = inject
        self.describes = describes


class Instrument:
    """One instrument, and a way to ask whether it reported a given place.

    `run(root)` returns the instrument's output as text. `reports(output, file, line)` decides
    whether that output names the place - which is deliberately the instrument's own idea of a
    place, since a tool that reports a page and a tool that reports a line are both useful and
    neither should be forced into the other's shape.

    A HIT IS NOT A PASS. An instrument that reports every page reports every plant and scores a
    perfect recall while being worthless; that is why precision has to be measured separately
    and why this file says so twice.
    """

    def __init__(self, name, run, reports):
        self.name = name
        self.run = run
        self.reports = reports


def copy_corpus(src, dst, include):
    """A working copy of only what the instruments read.

    NEVER PLANT INTO THE LIVE TREE. The case study learned this twice the expensive way: an
    edit made while three readers were reading destroyed four of their findings, and the fix
    was a frozen worktree. A harness that mutates a corpus must own its copy outright.
    """
    for rel in include:
        s = os.path.join(src, rel)
        d = os.path.join(dst, rel)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        elif os.path.exists(s):
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(s, d)


def matrix(cfg, only=None):
    """The recall matrix: {(defect, instrument): (hits, plants)}, plus what could not plant."""
    results, unplantable, detail = {}, [], []
    for d in cfg.DEFECTS:
        if only and d.name != only:
            continue
        for trial in range(cfg.TRIALS):
            with tempfile.TemporaryDirectory(prefix="plant-") as tmp:
                copy_corpus(cfg.ROOT, tmp, cfg.INCLUDE)
                where = d.inject(tmp, trial)
                if not where:
                    unplantable.append((d.name, trial))
                    continue
                for inst in cfg.INSTRUMENTS:
                    try:
                        out = inst.run(tmp)
                    except Exception as e:                    # noqa: BLE001
                        out = "INSTRUMENT FAILED: {}".format(e)
                    hit = any(inst.reports(out, f, ln) for f, ln in where)
                    key = (d.name, inst.name)
                    h, n = results.get(key, (0, 0))
                    results[key] = (h + int(hit), n + 1)
                    detail.append((d.name, trial, inst.name, hit))
    return results, unplantable, detail


def report(cfg, results, unplantable, detail):
    names = [i.name for i in cfg.INSTRUMENTS]
    classes = [d.name for d in cfg.DEFECTS if any(k[0] == d.name for k in results)]
    w = max([len(c) for c in classes] + [12])
    print("  RECALL, per defect class, per instrument. Planted one at a time.\n")
    print("  {:<{w}}".format("", w=w) + "".join("{:>16}".format(n[:15]) for n in names)
          + "{:>10}".format("union"))
    for c in classes:
        row = "  {:<{w}}".format(c, w=w)
        for n in names:
            h, t = results.get((c, n), (0, 0))
            row += "{:>16}".format("{}/{}".format(h, t) if t else "-")
        # THE UNION IS THE NUMBER THAT MATTERS AND THE PER-INSTRUMENT COLUMNS ARE THE DIAGNOSIS.
        # E01 measured that a majority vote over an ensemble loses a third of its findings; the
        # same holds here. What a class needs is for SOMETHING to see it, and the columns say
        # which something and whether it is alone.
        trials = {t for (dc, t, _, _) in detail if dc == c}
        seen = {t for (dc, t, _, hit) in detail if dc == c and hit}
        row += "{:>10}".format("{}/{}".format(len(seen), len(trials)) if trials else "-")
        print(row)

    blind = [c for c in classes
             if not any(t for (dc, t, _, hit) in detail if dc == c and hit)]
    print()
    if blind:
        print("  {} class(es) NO INSTRUMENT SEES AT ALL:".format(len(blind)))
        for c in blind:
            print("      {}".format(c))
        print("  A class with an empty union is a class the reading is the only cover for.")
    dead = [n for n in names
            if not any(h for (dc, i), (h, _) in results.items() if i == n)]
    if dead:
        print("  {} instrument(s) reported NOTHING on any plant: {}".format(
            len(dead), ", ".join(dead)))
        print("  An instrument with recall zero and an instrument with nothing to report look")
        print("  identical from outside. This is the only thing that separates them.")
    if unplantable:
        print("  {} plant(s) could not be placed and are excluded, not counted as misses:"
              .format(len(unplantable)))
        for name, t in unplantable[:8]:
            print("      {} trial {}".format(name, t))
    print("\n  RECALL ONLY. A tool that reports every page scores a perfect row here and is")
    print("  worthless; precision has to be measured on the corpus as it stands.")


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    path = argv[0]
    only = argv[argv.index("--class") + 1] if "--class" in argv else None
    spec = importlib.util.spec_from_file_location("plantcfg", path)
    cfg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cfg)
    results, unplantable, detail = matrix(cfg, only)
    if not results:
        print("  nothing was planted - check the config's DEFECTS and INCLUDE")
        return 1
    report(cfg, results, unplantable, detail)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
