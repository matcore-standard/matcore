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
The environment is managed by [uv](https://docs.astral.sh/uv/). Run every command from the
repository root; there is no environment to activate.

```
uv sync
uv run python scripts/validate_schema.py
uv run python scripts/build_docs.py --show-legacy
uv run mkdocs serve
```

- `uv sync` installs the dependencies pinned in `uv.lock`. It is needed once, and again after
  `pyproject.toml` or `uv.lock` changes. `uv run` also syncs before each command.
- `--show-legacy` adds the `legacy_*` text from the baseline migration to the pages. CI builds
  with it until every section's typed fields are filled, so use it locally too; without it the
  regenerated pages differ from the committed ones and CI fails.
- `mkdocs serve` serves the site at http://127.0.0.1:8000/matcore/ until stopped with Ctrl-C.
- Edits to prose pages (`docs/index.md`, `docs/standard/index.md`,
  `docs/standard/annex-u-units.md`, …) reload in the browser on save.
- Edits to `schema/*.yaml` do not. The chapters `docs/standard/02-*.md` … `08-*.md`, and Tables
  U.3 and U.4 in `annex-u-units.md` (between `generated` markers), are generated from the YAML;
  never edit them by hand. After a YAML edit,
  regenerate them in a second terminal while `mkdocs serve` keeps running:
  ```
  uv run python scripts/validate_schema.py && uv run python scripts/build_docs.py --show-legacy
  ```
- Commit the regenerated files with the YAML. CI regenerates them and fails if they differ from
  the committed copies.
- The local site is a single unversioned copy, so it has no version selector. The `latest` and
  `dev` versions exist only on the published site, where `mike` deploys them.

Before committing, run the checks CI runs:
```
uv run python scripts/validate_schema.py
uv run python scripts/build_docs.py --show-legacy
uv run mkdocs build --strict
```

## Changing the standard
The standard lives in `schema/*.yaml`; the pages under `docs/standard/` are generated from it. A
change reaches the website only when the YAML and the regenerated pages are committed together and
merged into `main` through a pull request, where CI checks them first (decision record 0004).

1. **Start a branch from an up-to-date `main`:**
   ```
   git switch main && git pull --ff-only
   git switch -c short-description-of-change
   ```
2. **Edit the YAML.** Wording lives in a property's `description` (and, until a section's typed
   fields are filled, in `legacy_values`). Keep the indentation. Changing a property's `name`,
   `required`, `repeatable` or subproperties changes the standard itself: record the decision in
   `docs/decisions/` and review every example in `examples/`, updating any that no longer conform
   (decision record 0012).
3. **Regenerate the pages and run the checks:**
   ```
   uv run python scripts/validate_schema.py
   uv run python scripts/build_docs.py --show-legacy
   uv run mkdocs build --strict
   ```
   To look at the result, run `uv run mkdocs serve` and open http://127.0.0.1:8000/matcore/.
4. **Commit the YAML together with every file the generator changed,** then check that nothing is
   left over:
   ```
   git add schema docs/standard examples
   git commit -m "Reword the creator description"
   git status
   ```
5. **Push the branch and open a pull request** (on GitHub, or with `gh pr create --fill`):
   ```
   git push -u origin short-description-of-change
   ```
   CI runs the checks on the pull request. If it fails at "fail if generated docs are stale", the
   regenerated pages were not committed: repeat steps 3–4 and push again.
6. **Merge the pull request** once CI passes. The site's `dev` version shows the change within a few
   minutes (a browser may keep the old page for up to 10 minutes; reload or use a private window).
   The released version (`latest`) shows it after the next release (below).
7. **Clean up:**
   ```
   git switch main && git pull --ff-only
   git branch -d short-description-of-change
   ```

## Releasing a version
Versions follow semantic versioning and are cut per milestone (decision record 0010).

1. Add the new release at the top of `schema/releases.yaml` (version, date, change type, sections,
   description, approved by), run the checks above, and commit it to `main`.
2. Tag that commit and push the tag, e.g. `git tag v0.5.0 && git push origin v0.5.0`.

CI checks that the tag matches `releases.yaml`, then publishes the version at `…/matcore/0.5.0/` and
points `latest` to it. Pushes to `main` update only the unreleased `dev` version.

## License
Standard text and schema: CC BY 4.0. Code: Apache-2.0.

The MatCore effort is funded by the NSF Division of Materials Research through Award #2404283 and supported through the KIM Initiative.
