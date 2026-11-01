# 0007 — Layout of the standard's section pages

Date: 2026-11-01. Status: accepted. Decided by: Ellad Tadmor.

*Implemented 2026-11-01: the markup of `render.py` is now produced by `scripts/build_docs.py` (tests in `tests/test_build_docs.py`), and `layout.css` and `layout.js` are in `docs/assets/matcore/`; `render.py` was removed. `logo.png` moved to `docs/assets/matcore/logo.png` and is the site logo (decision 0008), so the folder `0007-reference/` no longer exists; paths below that name it refer to these new locations. Decision 0008 places the property tree (item 7) under the page's entry in the left menu, without its section title, which also puts it in the menu drawer on narrow screens. Property `notes` (part of the standard, not migration text) are shown in every block after the values text, with or without `--show-legacy`.*

## Context
Status step 2 (website cleanup) left the presentation of properties open, to be chosen after options were seen rendered (0004 items 21 and 22). Candidate layouts were rendered in a preview from schema/minimal.yaml, plus one entry (dft `k-point-mesh`) with illustrative typed fields, and compared in the browser at desktop, tablet and phone widths.

Layouts considered and not chosen:
- **A. Heading per top-level property, one table per nesting level.** Faithful to the baseline .docx, but long and hard to navigate at depth.
- **B. Nested headings, one per property.** The longest page; the structure is hard to see.
- **C. Collapsible subproperties under top-level headings.** Treats top-level properties differently from the rest.
- **D. Every property a collapsible block, attributes in the block title.** Titles crowded with type, extent and kind.
- **Ways of marking required and repeatable in the title:** labelled pills ("required", "repeatable") drew the eye away from the name; cardinality badges (`1`, `0..1`, `1..*`, `0..*`) were too abstract for readers who are not schema authors; small muted words were readable but weak; single card versus stacked cards did not read as "repeats"; square repeat arrows were replaced by circular arrows; the `sync` / `sync-off` pair was close but suggests synchronising.

## Decision
The chosen layout (option "E4" in the preview) is the following. The reference implementation is in `docs/decisions/0007-reference/`: `render.py` (markup), `layout.css` (styles), `layout.js` (behaviour), and `logo.png` (the logo the palette was sampled from). The reference was built and checked at 1400, 768 and 375 px width with the full minimal section. build_docs.py is to produce this markup, and the site is to load these styles and scripts.

1. **One page per section**, as now (Standard → Minimal, DFT, …). The page has the section title, a key to the symbols, then one block per top-level property in schema order. Section introductions and examples (0004 item 23) are placed on the same page; their position is open (item 15 below).
2. **Property block.** Every property, at every depth, is the same collapsible block: a `<details class="note mc-property">` element whose subproperties are blocks nested inside it, in schema order. All blocks are closed on load except those on the path to a cited address (item 6).
3. **Title bar.** It holds only:
   - the property **name**, bold, 0.8rem;
   - a **red asterisk** directly after the name if the property is required (`#C62828`, the one colour not taken from the logo, chosen because red reads as "required");
   - a **repeat icon** right-aligned, just left of the expand arrow: Material Design Icons `autorenew` (circular arrows, charcoal) if the property is repeatable, `autorenew-off` (the same, struck through, slate) if it appears at most once.
   The asterisk and both icons carry a tooltip and an `aria-label` in words ("required", "repeatable: may appear more than once", "appears at most once"). The theme's admonition icon (a pencil) is removed; it carried no meaning.
4. **Key.** Below the section title, one line explains the symbols: `*` required, the struck-through icon "appears at most once", the plain icon "repeatable".
5. **Block body**, in this order:
   - the description;
   - an attribute table with six columns: **Required, Repeatable, Type, Extent, Kind, Rec. unit**. Required and Repeatable deliberately repeat the title-bar symbols in words, for readers who do not know the symbols. Unfilled typed fields show "—";
   - the values text: allowed values (`values.enum`), notes, required `convention` choices; legacy text in grey italics, labelled "Legacy:", only when build_docs.py runs with `--show-legacy`. The legacy prose "Contains SubProperties as listed below" (and its Sub…Sub variants) is never shown, since the nesting shows it;
   - the nested subproperty blocks.
6. **Citable addresses.** Each block's `id` is its address: the section key and the property path joined by dots, e.g. `#minimal.computation.software.file`. The id is written into the HTML at build time (Markdown-in-HTML, `markdown="1"`), not by script. Opening a page at an address opens that block and all its ancestors, scrolls to it and marks it; so does a change of address while the page is open (a followed link, a pasted URI). The address bar always shows the address of the marked block; closing a top-level block clears it. A **permalink button** (Material Design Icons `link-variant`) follows the name in each title bar: it copies the full URI to the clipboard and shows "copied", without opening or closing the block. It appears on hover, and permanently (at 60 % opacity) on touch screens.
7. **Property tree** (screens 76.25em wide and up, where the theme shows the left sidebar). The sidebar holds a tree mirroring the blocks: section title (underlined in gold), then property names. Properties with subproperties have a triangle after the name (▸ closed, ▾ open), larger than the text, in bronze. Opening a block anywhere marks its entry (bold, dark bronze) and unfolds its path; closing a block marks its parent. Clicking an entry opens its block; clicking the marked entry of an open block again closes it.
8. **Breadcrumb bar** (below 76.25em, where the sidebar is hidden). A bar pinned under the header shows the path to the marked block, e.g. `MINIMAL › computation › software › file`; each part opens its block. The bar is hidden when nothing is marked, and on wide screens.
9. **Phones** (below 45em). Each attribute table is shown as six "label value" lines instead of a row, so nothing scrolls sideways. Tablets and desktops show the table.
10. **Palette**, sampled from the MatCore logo (`0007-reference/logo.png`), applied site-wide through Material's custom colours (`palette: primary: custom, accent: custom`; variables on `:root > *`):

    | Name | Value | Logo source | Use |
    |---|---|---|---|
    | charcoal | `#404040` | left shape | header bar, headings, names, expand arrows, repeat icon |
    | gold | `#D9B266` | middle shape | header underline, left edge of open blocks, tree section underline, table-header tint (22 %); never text, too light on white |
    | blue | `#A4BCE7` | right shape | block borders, title-bar tint (22 %), table borders |
    | bronze | `#AA8237` | charcoal over gold | tree triangles |
    | bronze text | `#7F5F22` | bronze, darkened | links, marked tree entry, breadcrumb "here", Material accent |
    | slate | `#91969C` | gold over blue | unmarked tree entries, at-most-once icon, legacy text |
    | red | `#C62828` | not from the logo | required asterisk only |

11. **Icons.** All icons are Material Design Icons as bundled with mkdocs-material (`material/templates/.icons/material/`), inlined as SVG. The collection is distributed under the Pictogrammers Free License: some icons under Apache-2.0, the rest under their respective licenses (see the LICENSE file in that folder). No other icon or font is added.

### Implementation constraints
The reference implementation meets these; build_docs.py and the site must keep meeting them.
- **Inline SVGs carry `width` and `height` attributes** (18 px title icons, 16 px permalink). An SVG without an intrinsic size renders page-wide until a stylesheet sizes it. CSS that sizes icons must not depend on a class added by script.
- **Scroll offset uses `scroll-margin-top` on `.md-typeset details.mc-property[id]`**: 64 px from 76.25em up, 100 px below (header plus breadcrumb bar). The selector must outrank the theme's `.md-typeset [id]` rule, and the values are in pixels because the theme's rem size varies with screen width.
- **`toggle` events are asynchronous.** Opening a block's ancestors reports them after the block itself; an ancestor of the marked block that reports opening is ignored, or it takes the mark and the address from its descendant.
- **The phone table needs column labels on cells**: the script copies each header into `data-label` on its cells, and CSS shows it with `::before`.
- **mkdocs.yml** needs, besides `extra_css` and `extra_javascript` for the two files: `palette: {primary: custom, accent: custom}`, and markdown extensions `tables`, `admonition`, `pymdownx.details`, `attr_list`, `md_in_html`.
- **The breakpoints are the theme's**: 76.25em (sidebar shown) and 45em (tablet). If the theme changes them, change both the CSS and `layout.js` (`matchMedia('(min-width: 76.25em)')`).

### Open (PROPOSED, NOT DECIDED)
12. Whether container properties (those with subproperties and no value of their own) keep an attribute table of dashes, or show only Required and Repeatable.
13. Address stability across renames: once addresses are cited, a renamed property would need its old address kept as an alias. The 0001 Part B renames should land before the site is announced.
14. Optional additions: an "Expand all" control (also for printing and find-in-page, which do not see closed blocks); moving the tree highlight with scrolling; the full tree in the narrow-screen drawer; a dark colour scheme.
15. Where the section introduction and examples sit relative to the property blocks.
16. The logo as a site asset (header and favicon): needs the original logo file; `0007-reference/logo.png` is a screenshot, used only for colour sampling.

## Consequences
build_docs.py is rewritten (step 2) to emit the markup of `render.py`, test first; `layout.css` and `layout.js` move to `docs/assets/` (or similar) and are loaded by mkdocs.yml with the settings above. The palette and the header changes apply to every page of the site, not only the standard. Versioned URLs (mike) contain the version, so a citation of a released version keeps working; a citation of `latest` follows the current version.
