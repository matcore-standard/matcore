# MatCore — Material Core Metadata Standard

MatCore is a metadata standard for computational materials science (DFT, MBPT, MD, phase field, ML, derived properties). This repository is the source of truth for the standard and the generator for https://matcore.org.

- **Standard schema:** `schema/*.yaml` (one file per section) and `schema/units.yaml` (Annex U).
- **Rendered standard:** https://matcore.org/standard/ (built from the YAML on every push).
- **Contribute:** open an issue or pull request. See `CONTRIBUTING.md`.

## Layout
```
schema/            YAML source of the standard + meta-schema + unit table
docs/standard/     prose chapters and generated chapters (MkDocs)
docs/decisions/    committee decision records
scripts/           validate_schema.py, build_docs.py
examples/          example MatCore instance files
tests/             CI tests
```

## Build locally
```
uv sync
uv run python scripts/validate_schema.py
uv run python scripts/build_docs.py
uv run mkdocs serve
```

## License
Standard text and schema: CC BY 4.0. Code: Apache-2.0.

The MatCore effort is funded by the NSF Division of Materials Research through Award #2404283 and supported through the KIM Initiative.
