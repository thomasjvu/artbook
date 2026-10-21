# artbook

A white-paper, monospace artbook and working design bible for game projects.
Project data and artwork stay in the consuming project. This repository contains
only reusable tooling and a neutral typographic example. No hosted service,
JavaScript framework or network request is required.

## Build

Python 3.10+:

    python3 -m artbook.build examples/catalogue.json --output dist

Optional PDF export requires ReportLab:

    python3 -m pip install -r requirements-pdf.txt
    python3 -m artbook.build examples/catalogue.json --output dist --pdf

Open dist/index.html for the curated artbook and dist/bible.html for working
records. Browser print styles produce another PDF route. The generated site
copies only included images, with content-addressed filenames and provenance.
Review exported content before publishing; your project controls art licensing.

## Catalogue format

See examples/catalogue.json. Schema 1 has title, subtitle, edition, date,
rights, optional cover_id, and chapters. A chapter has title, intro, optional
layout=gallery and items. Each item has id, title, image (relative to catalogue),
caption, status, optional pixel=true and include=false. Additional metadata is
preserved in the working catalogue. Status is descriptive, not an approval gate.
Curating a plate never grants copyright or production approval.

## Integrate

Template/vendor mode: copy artbook/ into tools/vendor/artbook/ and record the
upstream commit. Keep the catalogue outside this folder.
Submodule mode: add the upstream repository under tools/vendor/artbook and set
PYTHONPATH to that directory when running python3 -m artbook.build. Pin a commit;
update deliberately. Both modes use the same catalogue and preserve project art.

## Outputs

- index.html: curated chapter/plate artbook, print styles
- bible.html: detailed project-owned item records
- catalogue.json: portable source data
- provenance.json: image hashes and original catalogue references
- artbook.pdf: optional A4 book, one artwork per page

PDF exports are review editions, without commercial press bleed, CMYK conversion
or printer profiles. Pixel art retains nearest rendering in HTML. For print,
review resolution and intended reproduction size with your printer.

## Development

    python3 -m unittest discover -s tests

MIT license applies to the tooling and neutral demo only. Consumer artwork has
its own rights. Canonical hosting is Forgejo; GitHub is a Git mirror. Push normal
branches/tags to both remotes; never force-mirror unrelated refs.
