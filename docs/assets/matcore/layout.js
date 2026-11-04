// Version of the page (decision 0010). build_docs.py writes <p class="mc-version" data-version="X.Y.Z">
// under each standard page's title. mike serves each version under its own path segment of the site:
// 'dev' (unreleased main), 'latest' (alias of the newest release), or 'X.Y.Z'; a local preview has none.
function mcVersion() {
  const line = document.querySelector('.mc-version[data-version]');
  const config = JSON.parse(document.getElementById('__config')?.textContent || '{}');
  const base = new URL((config.base || '.') + '/', location.href).pathname.replace(/\/+$/, '/');
  const segment = base.split('/').filter(Boolean).pop() || '';
  return {line, version: line?.dataset.version, base, segment, isDev: segment === 'dev'};
}

// On the dev site, the version line says the page is unreleased.
document.addEventListener('DOMContentLoaded', () => {
  const v = mcVersion();
  if (v.line && v.isDev) {
    v.line.textContent = `Development version: unreleased changes after ${v.version}`;
    v.line.classList.add('mc-version--dev');
  }
});

// The current page's menu entry shows what lies under it: the page's headings, or on a schema section
// page its property tree (decision 0008 item 3). Clicking the entry collapses that list; clicking again
// expands it. Without this the click would only reload the page.
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.md-nav--primary li > a.md-nav__link--active').forEach(a => {
    const li = a.parentElement;
    a.addEventListener('click', e => {
      if (!li.querySelector(':scope > nav, :scope > .mc-tree')) return;
      e.preventDefault();
      li.classList.toggle('mc-collapsed');
    });
  });
});

// Standard-page behaviour of decision record 0007, for pages whose property blocks
// scripts/build_docs.py writes (details.mc-property, id = citable address). Adds: a permalink button on each block,
// a property tree in the left sidebar, a breadcrumb bar for narrow screens, opening the block
// named by the address (on load and on change), and column labels for the phone table layout.
document.addEventListener('DOMContentLoaded', () => {
  const article = document.querySelector('.md-content__inner');
  const sidebar = document.querySelector('.md-sidebar--primary .md-sidebar__scrollwrap');
  if (!article || !article.querySelector('details.mc-property')) return;

  const name = d => d.querySelector(':scope > summary').firstChild.textContent.replace('*', '').trim();
  const children = d => [...d.querySelectorAll(':scope > details.mc-property')];
  const entries = new Map();  // details element -> tree <li>
  // The copied address names the concrete version: 'latest' is replaced by the page's version (0010 item 6).
  const ver = mcVersion();
  const uri = d => {
    const base = ver.segment === 'latest' && ver.version ? ver.base.replace(/latest\/$/, `${ver.version}/`) : ver.base;
    return location.origin + base + location.pathname.slice(ver.base.length) + '#' + d.id;
  };

  // Link button in each block title: copies the URI without toggling the block.
  article.querySelectorAll('details.mc-property').forEach(d => {
    const a = document.createElement('a');
    a.className = 'mc-permalink';
    a.href = '#' + d.id;
    a.title = ver.isDev ? 'Copy link (development version: not a stable, citable address)' : 'Copy link to this property';
    // Icon: Material Design Icons "link-variant", as bundled with mkdocs-material; intrinsic size set.
    a.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true"><path d="M10.59 13.41c.41.39.41 1.03 0 1.42-.39.39-1.03.39-1.42 0a5.003 5.003 0 0 1 0-7.07l3.54-3.54a5.003 5.003 0 0 1 7.07 0 5.003 5.003 0 0 1 0 7.07l-1.49 1.49c.01-.82-.12-1.64-.4-2.42l.47-.48a2.98 2.98 0 0 0 0-4.24 2.98 2.98 0 0 0-4.24 0l-3.53 3.53a2.98 2.98 0 0 0 0 4.24m2.82-4.24c.39-.39 1.03-.39 1.42 0a5.003 5.003 0 0 1 0 7.07l-3.54 3.54a5.003 5.003 0 0 1-7.07 0 5.003 5.003 0 0 1 0-7.07l1.49-1.49c-.01.82.12 1.64.4 2.43l-.47.47a2.98 2.98 0 0 0 0 4.24 2.98 2.98 0 0 0 4.24 0l3.53-3.53a2.98 2.98 0 0 0 0-4.24.973.973 0 0 1 0-1.42"/></svg>';
    a.setAttribute('aria-label', 'Copy link to this property');
    a.addEventListener('click', e => {
      e.preventDefault();
      e.stopPropagation();
      navigator.clipboard?.writeText(uri(d));
      reveal(d);
      a.classList.add('copied');
      setTimeout(() => a.classList.remove('copied'), 1200);
    });
    const summary = d.querySelector(':scope > summary');
    const label = summary.querySelector('.mc-name');
    if (label) label.after(a); else summary.appendChild(a);
  });

  function build(d) {
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.textContent = name(d);
    a.href = '#' + d.id;
    // A click opens the block; a second click on the current, open block closes it again.
    a.addEventListener('click', e => {
      e.preventDefault();
      if (d.open && li.classList.contains('current')) d.open = false; else reveal(d);
    });
    li.appendChild(a);
    const kids = children(d);
    if (kids.length) {
      li.classList.add('has-kids');
      const ul = document.createElement('ul');
      kids.forEach(k => ul.appendChild(build(k)));
      li.appendChild(ul);
    }
    entries.set(d, li);
    return li;
  }

  const tree = document.createElement('nav');
  tree.className = 'mc-tree';
  let list = null;
  for (const el of article.children) {
    if (el.tagName === 'H1') {  // each section title starts a tree section
      const h = document.createElement('div');
      h.className = 'mc-tree-section';
      h.textContent = el.textContent.replace('¶', '').trim();
      tree.appendChild(h);
      list = document.createElement('ul');
      tree.appendChild(list);
    } else if (el.matches('details.mc-property') && list) {
      list.appendChild(build(el));
    }
  }
  // The tree goes under the current page's entry in the left menu, where the page's headings
  // would be (decision 0008); the menu entry already names the section, so its title is dropped.
  const pageLink = document.querySelector('.md-nav--primary .md-nav__link--active');
  const host = pageLink && pageLink.closest('li');
  if (host) {
    tree.querySelectorAll('.mc-tree-section').forEach(h => h.remove());
    tree.classList.add('mc-tree--in-menu');
    // Before the page's own heading entries (its example), matching the page's order.
    host.insertBefore(tree, host.querySelector(':scope > nav'));
  } else if (sidebar) {
    sidebar.appendChild(tree);
  }

  function ancestors(d) {
    const out = [];
    for (let p = d.parentElement.closest('details'); p; p = p.parentElement.closest('details')) out.push(p);
    return out;
  }

  // Breadcrumb bar for narrow screens, where the sidebar tree is hidden: shows the path to the
  // current block, each part tappable. CSS shows it only below the sidebar breakpoint.
  const crumbs = document.createElement('nav');
  crumbs.className = 'mc-crumbs';
  crumbs.setAttribute('aria-label', 'Location in the standard');
  article.prepend(crumbs);
  const wide = window.matchMedia('(min-width: 76.25em)');  // Material shows the sidebar from here up

  function updateCrumbs(d) {
    crumbs.replaceChildren();
    crumbs.classList.toggle('empty', !d);
    if (!d) return;
    const section = document.createElement('span');
    section.className = 'mc-crumb-section';
    section.textContent = d.id.split('.')[0];
    crumbs.appendChild(section);
    [...ancestors(d).reverse(), d].forEach(p => {
      crumbs.appendChild(document.createTextNode(' › '));
      const a = document.createElement('a');
      a.textContent = name(p);
      a.href = '#' + p.id;
      if (p === d) a.className = 'here';
      a.addEventListener('click', e => { e.preventDefault(); reveal(p); });
      crumbs.appendChild(a);
    });
  }

  let current = null;
  function mark(d) {
    current = d;
    updateCrumbs(d);
    tree.querySelectorAll('.current, .open-branch').forEach(e => e.classList.remove('current', 'open-branch'));
    if (!d) { history.replaceState(null, '', location.pathname); return; }
    const li = entries.get(d);
    li.classList.add('current', 'open-branch');
    ancestors(d).forEach(p => entries.get(p).classList.add('open-branch'));
    if (wide.matches) li.scrollIntoView({block: 'nearest'});
    history.replaceState(null, '', '#' + d.id);
  }

  function reveal(d) {
    ancestors(d).forEach(p => { p.open = true; });
    d.open = true;
    mark(d);
    d.scrollIntoView({block: 'start'});  // offset for the header and breadcrumb bar: scroll-margin-top in CSS
  }

  // Opening a block marks it; closing one marks its parent. Toggle events arrive after the change,
  // so opening a block's ancestors in reveal() reports them late: an ancestor of the current block
  // that reports opening is ignored, or it would take the mark (and the address) from its descendant.
  article.addEventListener('toggle', e => {
    const d = e.target;
    if (!entries.has(d)) return;
    if (d.open) {
      if (current && d !== current && d.contains(current)) return;
      mark(d);
    } else {
      mark(d.parentElement.closest('details'));
    }
  }, true);

  // Stacked table layout on phones needs each cell to know its column label.
  article.querySelectorAll('details.mc-property table').forEach(t => {
    const labels = [...t.querySelectorAll('thead th')].map(th => th.textContent.trim());
    t.querySelectorAll('tbody tr').forEach(tr => [...tr.cells].forEach((td, i) => { td.dataset.label = labels[i]; }));
  });

  // A cited URI opens its block, with all its ancestors: on load, and when the address changes
  // while the page is open (a followed link, or a URI pasted into the address bar).
  function openFromHash() {
    const target = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (target && entries.has(target)) reveal(target);
  }
  window.addEventListener('hashchange', openFromHash);
  openFromHash();
});
