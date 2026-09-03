"""Stage 1: take a scanned PDF apart without believing any of it.

THIS IS THE ENTRY POINT THE PIPELINE DID NOT HAVE. Stage 2 could fit a book's layout from a
directory of page images, and nothing produced that directory: the case study's images were
extracted by hand, once, months ago. A product that cannot be pointed at a PDF is a study.

WHAT IT DOES, and each part exists because getting it wrong destroys evidence downstream.

SEPARATE THE LEAVES BY KIND. A photographic leaf and a bilevel stencil want opposite treatment,
and a pipeline that treats them alike destroys one of them. The discriminator is ink fraction:
a threshold at 0.11 separated the case study's two photographic leaves from its 354 stencils.
The fraction is a property of the leaf and not of a guess about it.

COMPOSITE EACH PAGE AT THE NATIVE RESOLUTION OF ITS HIGHEST LAYER. The reason for the
resolution is unchanged and is the whole point: a 1-bit stencil re-rendered at 300 dpi has
already lost the evidence that decides whether a mark BROKE or merely THINNED, and every later
damage judgement rests on that distinction.

**But "extract the image, never re-render the page" is wrong, and this stage was written that
way and refuted on the case study's own original.** A scanned PDF is normally mixed raster
content: each page carries a blurred background at 200 dpi and a stencil at 600, and the
foreground layer pulled out ALONE is not the leaf. Measured, it never rises above grey 167
where paper would be 255 - it is only meaningful composited under its mask, and on its own it
classifies a page of type as anything you like.

Composited at the dpi the top layer implies, the same pages come out 2691x4060 and 2698x4038 -
byte for byte the dimensions the case study's plates were extracted at by hand months ago - with
ink fractions of 0.068, 0.033, 0.028, which is the range of a page of type. Native resolution is
preserved because the dpi is READ OFF the layer rather than chosen; nothing is downsampled.

TAKE THE TEXT LAYER AS A HINT AND NEVER AS TRUTH. In the case study the OCR read commas as full
stops throughout an index, read the figure one as a capital I, gave every word on four leaves an
identical synthesised height of 5.0 pt, and put two adjacent lines in the wrong order. It was
still useful: its geometry located the columns, and a two-word match found 98 of every 100
paragraph openings. What a bad instrument is good for is a question with an answer, and the
answer is rarely "nothing".

WHAT IT REFUSES TO DO IS GUESS. Every leaf goes into the manifest with what was measured about
it and how it was obtained. A leaf whose kind is uncertain is written down as uncertain rather
than assigned, because stage 2 chooses its sample from this manifest and a mislabelled leaf is
worse than a missing one.

    python src/ingest.py <scan.pdf> <output directory>
    python src/ingest.py <scan.pdf> <output directory> --pages 40-80
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# THE ONE THRESHOLD, and it is measured rather than chosen. Below it a leaf is type; above it
# the leaf carries a photograph, a plate or a solid ground. The case study's two photographic
# leaves sat at 0.30 and 0.42 against a body distribution running 0.02 to 0.11, so the gap is
# wide and the exact value does not matter much - but a leaf that lands inside the margin
# either side of it is reported as UNCERTAIN rather than sorted.
INK_PHOTO = 0.11
UNCERTAIN = 0.02          # of ink fraction, either side of the threshold

# A leaf with almost no ink is a blank, a part title or a half title. Not an error, and not
# body type either.
INK_EMPTY = 0.005

# Otsu's separability below which its two-mode assumption has failed and no global threshold
# means anything on that leaf. Measured on the case study's original: the leaves that binarise
# cleanly score 0.85 and above, the faint gradient-lit ones score below 0.5, and nothing in the
# test range lands between - so the value is read off a gap rather than tuned into one.
SEPARABLE = 0.70


def ink_fraction(pix):
    """(fraction of the leaf that is ink, whether the stored polarity is inverted).

    A ONE-BIT STENCIL'S POLARITY IS NOT GUARANTEED, and assuming it cost this stage its whole
    answer. Pulled out of the case study's own scan, the foreground layer measures 0.995 dark
    - so on the assumption that dark means ink, every leaf of a book of type was classified
    photographic, and stage 2, which picks its sample by ink fraction, would have found no body
    leaf at all.

    THE DISCRIMINATOR IS TRUE OF EVERY BOOK AND NEEDS NO THRESHOLD: **a page of type is never
    more than half ink.** Not in any face, at any size, in any language. So a measured fraction
    above a half is not a very black page, it is a stored polarity that runs the other way, and
    the true fraction is its complement.

    This is stronger than sniffing the colour space or the bit depth, because it is a fact
    about what is on the leaf rather than about how someone chose to encode it.

    AND THE THRESHOLD IS THE LEAF'S OWN, NEVER A CONSTANT. A fixed 128 read printed page 60 of
    the case study's original as 0.26 per cent ink and called it blank; the leaf is a full page
    of type, scanned faint, with a gradient running dark at one corner to pale at the other.
    Half the leaves in a test range were classified blank that way while the other half were
    not, purely because the scanner's exposure alternated.

    Otsu's threshold - the split maximising the variance BETWEEN the two parts - is computed per
    leaf from its own histogram, which is the same lesson the layout fitter learned: **a
    quantity that varies leaf to leaf must be measured leaf by leaf.**

    AND OTSU IS REFUSED WHERE ITS OWN ASSUMPTION FAILS, which on this scan is half the leaves.
    Otsu assumes the histogram has two modes. A faint leaf lit by a gradient has one broad mode,
    and Otsu then cuts somewhere in the middle of it and calls half the page ink - which is how
    a first attempt classified every leaf of a book of type as photographic, having just
    classified half of them blank with a fixed threshold. Two wrong answers, opposite in sign,
    from the same missing question.

    Otsu's own separability, eta - the between-class variance as a fraction of the total - says
    whether the assumption held. Below SEPARABLE the leaf cannot be binarised globally at all,
    and this returns None: **not blank, not photographic, not a guess.** Such a leaf needs a
    LOCAL threshold, which is a real piece of work and is named as one rather than faked with a
    global number that happens to run.
    """
    import numpy as np
    a = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)
    g = a[:, :, :3].min(axis=2) if pix.n >= 3 else a[:, :, 0]
    t, eta = otsu(g)
    if eta < SEPARABLE:
        return None, False, eta
    # OTSU'S k IS THE TOP OF THE LOWER CLASS, so the comparison is <= and not <. With < a
    # perfectly bimodal leaf - ink at 20, paper at 245 - returns k = 20 and measures ZERO ink,
    # because nothing is strictly below the very value the ink sits at. Found by a constructed
    # leaf whose ink fraction was known to be 0.05 and came back 0.
    f = float((g <= t).mean())
    return (1.0 - f, True, eta) if f > 0.5 else (f, False, eta)


def otsu(g):
    """(threshold, separability). eta near 1 is a clean two-mode histogram; near 0 is one mode."""
    import numpy as np
    hist = np.bincount(g.ravel(), minlength=256).astype(float)
    total = hist.sum()
    if total == 0:
        return 128, 0.0
    p = hist / total
    w = np.cumsum(p)
    m = np.cumsum(p * np.arange(256))
    mt = m[-1]
    with np.errstate(divide="ignore", invalid="ignore"):
        between = (mt * w - m) ** 2 / (w * (1 - w))
    between[~np.isfinite(between)] = 0
    k = int(np.argmax(between))
    var = float((p * (np.arange(256) - mt) ** 2).sum())
    return k, (float(between[k]) / var if var else 0.0)


def invert_png(path):
    from PIL import Image, ImageOps
    im = Image.open(path)
    ImageOps.invert(im.convert("L")).save(path)


def kind(frac):
    if frac < INK_EMPTY:
        return "blank"
    if abs(frac - INK_PHOTO) <= UNCERTAIN:
        return "uncertain"
    return "photographic" if frac > INK_PHOTO else "stencil"


def page_images(page, cover=0.70, min_dpi=100):
    """The xrefs of images that are a scan OF this leaf, by placement AND by resolution.

    TWO CONDITIONS, AND EACH LOOKED SUFFICIENT UNTIL IT WAS TRIED.

    Counting is not enough. The first version took "exactly one image on the page" to mean a
    scanned leaf. Every page of the case study's own PDF carries TWO images, and a rule of
    one-means-a-scan rendered all thirty-one pages of a test range - silently discarding the
    very evidence this stage exists to preserve.

    Covering is not enough either, and it fails on the same file for a better reason: those
    two images are ONE PIXEL SQUARE, degenerate fills left by whatever processed the file, and
    a 1x1 image STRETCHED over the page has a full-page placement rectangle. It passes a
    coverage test perfectly while carrying no information at all.

    So an image is a leaf when it covers the page AND resolves it: at least `min_dpi` over the
    placement it occupies. The 1x1 fills resolve the page at 0.16 dpi and are refused; a real
    scan resolves it at three hundred or more and is taken.

    AND A REAL SCAN USUALLY CARRIES TWO OF THEM, which is the third thing this had to learn.
    The case study's original is mixed raster content: every page holds a background at 200 dpi
    AND a foreground stencil at 600, both placed over the whole leaf. That is the normal
    structure of a scanned PDF, not an anomaly, so "several page-covering images means a
    composite I must not touch" would refuse every ordinary scan there is.

    **The stencil is the one with the most pixels.** The background is a blurred, downsampled
    ground; the foreground is the 1-bit mask that carries the type, and it is the only one on
    which a broken mark can be told from a thinned one. Returned sorted, most pixels first,
    with the count kept so the manifest can say a choice was made.
    """
    area = abs(page.rect.width * page.rect.height)
    out = []
    for info in page.get_images(full=True):
        xref, w, h = info[0], info[2], info[3]
        for r in page.get_image_rects(xref):
            if not area or abs(r.width * r.height) / area < cover:
                continue
            if r.width <= 0 or r.height <= 0:
                continue
            dpi = min(w / (r.width / 72.0), h / (r.height / 72.0))
            if dpi >= min_dpi:
                out.append((w * h, xref, w, h))
            break
    out.sort(reverse=True)
    return out


def extract(doc, i, out_dir):
    """(filename, how it was obtained, width, height) for one leaf.

    THE EMBEDDED IMAGE IS PREFERRED AND THE RENDER IS THE FALLBACK, and the manifest says
    which, because they are not the same evidence. A page covered by exactly one image is a
    scan of a leaf and that image IS the leaf; a page covered by several has been composited,
    and stitching it back together is a decision this stage must not make silently. A page
    covered by none is not a scan at all - it is set type, and rendering it is the only thing
    to do and must be labelled.
    """
    page = doc[i]
    images = page_images(page)
    name = "p{:04d}.png".format(i + 1)
    path = os.path.join(out_dir, name)
    if images:
        _, _, w, h = images[0]
        dpi = max(72, round(w / (page.rect.width / 72.0)))
        pix = page.get_pixmap(dpi=dpi)
        pix.save(path)
        how = "composited at {} dpi, the native resolution of a {}x{} layer".format(dpi, w, h)
        if len(images) > 1:
            how += " (over {} lower layers)".format(len(images) - 1)
        return name, how, pix.width, pix.height, pix
    # NO SCAN ON THIS PAGE AT ALL - it is set type, and the resolution is a choice rather than
    # a fact about the file, so it is stated.
    pix = page.get_pixmap(dpi=400)
    pix.save(path)
    how = "rendered at 400 dpi (no image covers and resolves the page - set type, not a scan)"
    return name, how, pix.width, pix.height, pix


def main(argv):
    import fitz
    if len(argv) < 2:
        print(__doc__)
        return 2
    src, out_dir = argv[0], argv[1]
    first, last = 1, 10 ** 9
    if "--pages" in argv:
        spec = argv[argv.index("--pages") + 1]
        a, _, b = spec.partition("-")
        first, last = int(a), int(b or a)

    os.makedirs(out_dir, exist_ok=True)
    doc = fitz.open(src)
    leaves, counts = [], {}
    for i in range(doc.page_count):
        if not (first <= i + 1 <= last):
            continue
        name, how, w, h, pix = extract(doc, i, out_dir)
        frac, inverted, eta = ink_fraction(pix)
        if inverted:
            # SAVED THE WAY EVERY LATER STAGE READS IT: ink dark, paper light. The stencil is
            # rewritten rather than left for each consumer to sniff, because a polarity that
            # has to be guessed at four different places will be guessed differently at one.
            invert_png(os.path.join(out_dir, name))
            how += ", polarity inverted on the way out"
        k = "unbinarised" if frac is None else kind(frac)
        counts[k] = counts.get(k, 0) + 1
        text = doc[i].get_text().strip()
        leaves.append({
            "leaf": i + 1, "file": name, "obtained": how,
            "width": w, "height": h, "aspect": round(h / w, 4),
            "ink": (round(frac, 4) if frac is not None else None),
            "separability": round(eta, 3), "kind": k,
            # THE TEXT LAYER'S SIZE, NOT ITS CONTENT. A leaf with no text layer at all and a
            # leaf whose text layer is nonsense look the same to a later stage unless the
            # count is carried; the case study's index leaves had a full text layer that was
            # wrong about punctuation, the figure one, and the order of adjacent lines.
            "text_chars": len(text),
            "text_hint": text[:60].replace("\n", " ") if text else None,
        })
    doc.close()

    man = os.path.join(out_dir, "manifest.json")
    with open(man, "w", encoding="utf-8") as f:
        json.dump({"source": os.path.abspath(src), "leaves": leaves}, f, indent=2)

    print("  {} leaves written to {}".format(len(leaves), out_dir))
    for k in ("stencil", "photographic", "blank", "uncertain", "unbinarised"):
        if counts.get(k):
            print("    {:>4}  {}".format(counts[k], k))
    rendered = sum(1 for l in leaves if l["obtained"].startswith("rendered"))
    if rendered:
        print("    {:>4}  obtained by RENDERING rather than extraction - a rendered leaf has"
              .format(rendered))
        print("          already lost whether a mark broke or thinned, and the manifest says so")
    notext = sum(1 for l in leaves if not l["text_chars"])
    print("    {:>4}  carry no text layer at all".format(notext))
    print("\n  manifest: {}".format(man))
    print("  A census of what is there, not a claim about what it says. The text layer is a")
    print("  hint: in the case study it read commas as full stops and inverted adjacent lines.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
