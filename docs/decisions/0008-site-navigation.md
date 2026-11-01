# 0008 — Site navigation

Date: 2026-11-01. Status: accepted. Decided by: Ellad Tadmor.

## Context
0004 item 21 decided a menu with navigation tabs (Home · About · Standard · Contact across the top). Reviewing the draft site, the left menu was chosen instead, laid out like matcore.org: its menu (About ▸ About MatCore, Leadership; Standard ▸ Browse Standard, Revision History; Contact) and the numbered contents of its standard page (1. Preamble, 1.1–1.3; 2. Schema for the MatCore Standard, 2.1–2.7).

## Decision
1. **Left menu, collapsed.** On first load the menu shows only Home, About, Standard and Contact; About and Standard open to their pages. The theme opens the branch that holds the current page. No navigation tabs: this replaces the "navigation tabs" part of 0004 item 21. (mkdocs.yml: `navigation.sections` and `navigation.tabs` off.)
2. **Menu tree:**
   - Home
   - About ▸ About MatCore, Leadership
   - Standard ▸
     - Browse Standard (opens the Preamble page, `docs/standard/index.md`) ▸
       - 1. Preamble (the same page; 1.1 Objectives, 1.2 Scope, 1.3 Format, from its headings)
       - 2. Schema for the MatCore Standard ▸ 2.1 Minimal MatCore Metadata, 2.2 Density Functional Theory (DFT) Metadata, 2.3 Molecular Dynamics (MD) Metadata, 2.4 Many-Body Perturbation Theory (MBPT) Metadata, 2.5 Machine Learning (ML) Metadata, 2.6 Phase Field (PF) Metadata, 2.7 Derived Property Metadata
       - Annex U. MatCore Unit Table; Annex U. Unit Table (generated)
     - Revision History
   - Contact (replaces the Feedback placeholder, which is removed; text from matcore.org/contact)
   Menu labels carry the section numbers. The 2.x entries take their labels from the section titles (`title` in schema/<section>.yaml, also the page headings), so menu and page cannot differ; the other labels are set in mkdocs.yml `nav`.
3. **No right-hand table of contents.** A page's headings appear in the left menu under the page's entry (`toc.integrate`), to depth 2 (`toc_depth: 2`, kept from 0004 item 21). On the schema section pages, which have no subheadings, the property tree of 0007 takes that place: it sits under the page's menu entry, so it is also in the menu drawer on phones and tablets.
4. **Menu title.** The logo (`docs/assets/matcore/logo.png`, also the header logo via `theme.logo`) stands before "MatCore", set larger and bold (1.1rem) on wide screens.
5. **Browse Standard opens on the Preamble.** Selecting Browse Standard shows the Preamble page in the main window. The page (`docs/standard/index.md`, formerly `01-introduction.md`; wording unchanged) is titled "1. Preamble" with 1.1–1.3 as its subheadings. Above the title, the document title "Material Core Metadata (MatCore) Standard" is a styled line (`<p class="mc-doc-title">`), not a heading, so the menu does not list it.
6. **Section introductions.** Each section page opens with its introduction from the baseline .docx (the text between the section heading and its table), under the title and before the symbol key; stored as `introduction` in `schema/<section>.yaml` (0004 item 23) and rendered by build_docs.py. The docx table captions ("Table Min-1: …") are not carried over: the property blocks replace the tables.
7. **Home page.** No visible title and no links line: the page starts with the description of MatCore. It keeps a visually hidden "MatCore" heading (class `mc-visually-hidden`), because the theme otherwise adds a visible title taken from the menu label ("Home").

### Implementation constraint
A section's index page (the page that opens when the section is selected, here Browse Standard) is not listed among the section's entries by mkdocs-material, so neither the page nor its headings would appear in the menu. `overrides/partials/nav-item.html` is a copy of the theme's template (mkdocs-material 9.8.0) with one condition changed, so the index page is also listed under its nav label ("1. Preamble"); mkdocs.yml sets `custom_dir: overrides`. When mkdocs-material is upgraded, re-copy the template and re-apply the change marked "MatCore:".

## Consequences
mkdocs.yml, `overrides/partials/nav-item.html`, `docs/standard/index.md`, `docs/contact.md`, `docs/index.md`, `schema/meta-schema.yaml` and `schema/<section>.yaml` (introduction), scripts/build_docs.py, `docs/assets/matcore/layout.css` (menu title, tree indent, document title, hidden title) and `layout.js` (tree placement) change. 0007's open item 14 "the full tree in the narrow-screen drawer" is met by item 3. `logo.png` is a screenshot of the logo; replacing it with the original file remains open (0007 item 16).
