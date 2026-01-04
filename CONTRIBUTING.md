# Contributing to MolSysSuite Papers

Thanks for contributing!

## Add a new paper

1. Create a directory:
   - `<tool>/<year>-<slug>/` (e.g. `molsysmt/2026-molsysmt-foundation/`)
2. Add a `README.md` using the template in `templates/paper-README.md`.
3. Add manuscript sources in `manuscript/` and any figures/bib files.
4. Update the corresponding tool repository pointer (`resources/papers.yml`).

## Naming

- Use lowercase tool directories: `molsysmt`, `molsysviewer`, `molsys-ai`
- Use `YYYY-<short-slug>` for paper directories

## Large files

Prefer keeping large binaries to a minimum. PDFs can go into `artifacts/` if needed.
