# Annex I — Identifier Schemes

<!-- BEGIN generated: version from schema/releases.yaml by scripts/build_docs.py; do not edit -->
<p class="mc-version" data-version="0.5.0">Version 0.5.0</p>
<!-- END generated -->

*(Normative)*

## I.1 Purpose

This annex defines the identifier schemes whose values a MatCore validator checks. An `identifier` property has two subproperties: `value`, the identifier itself, and `scheme`, the name of the scheme it belongs to. The `scheme` names the rule that `value` follows.

## I.2 Rules

1. When `scheme` is a scheme listed in Table I.1, `value` SHALL be written in that scheme's form, SHALL match its pattern in full, and SHALL pass its check digit if the scheme has one.
2. A `scheme` not listed in Table I.1 is permitted. Its `value` is not checked, and a validator reports it as user-specified.
3. Scheme names are written exactly as in Table I.1.
4. Check digits:
    - *ISO/IEC 7064 MOD 11-2*: computed over the 16 characters of the identifier, hyphens removed; the last character is the check character, where `X` stands for 10.
    - *ISO/IEC 7064 MOD 97-10 (ROR)*: the last two digits of a ROR ID are the MOD 97-10 check of the number encoded, in Crockford base 32, by the six characters after the leading `0`.
5. A scheme is added, or its rule changed, only by revision of this annex. Every field of an entry is traced to the scheme's own documentation, named in the Source column.

## I.3 Schemes

Table I.1 is generated from `schema/identifier-schemes.yaml`, which prevails.

<!-- BEGIN generated: Table I.1 from schema/identifier-schemes.yaml by scripts/build_docs.py; do not edit -->
| Scheme | Identifies | Form | Pattern | Check digit | Example | Source |
|---|---|---|---|---|---|---|
| ORCID | person | The full https URI. | `https://orcid\.org/[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[0-9X]` | ISO/IEC 7064 MOD 11-2 | `https://orcid.org/0000-0001-5727-2427` | [support.orcid.org](https://support.orcid.org/hc/en-us/articles/360006897674-Structure-of-the-ORCID-Identifier) |
| ROR | organization | The full URL, the form ROR prefers. | `https://ror\.org/0[a-hj-km-np-tv-z0-9]{6}[0-9]{2}` | ISO/IEC 7064 MOD 97-10 (ROR) | `https://ror.org/02mhbdp94` | [ror.readme.io](https://ror.readme.io/docs/identifier) |
| DOI | software, dataset, publication | The https URI at doi.org. | `https://doi\.org/10\.[^/]+/.+` | — | `https://doi.org/10.1000/182` | [www.doi.org](https://www.doi.org/doi_handbook/2_Numbering.html) |
| SWHID | software | The core identifier, optionally followed by qualifiers. | `swh:1:(snp|rel|rev|dir|cnt):[0-9a-f]{40}(;.+)?` | — | `swh:1:rel:22ece559cc7cc2364edc5e5593d63ae8bd229f9f` | [www.swhid.org](https://www.swhid.org/specification/v1.2/) |
| ISNI | person, organization | The https URI at isni.org. | `https://isni\.org/isni/[0-9]{15}[0-9X]` | ISO/IEC 7064 MOD 11-2 | `https://isni.org/isni/0000000121491740` | [isni.org](https://isni.org/page/linked-data/) |
| AFLOW | crystal structure | The AFLOW prototype label (stoichiometry, Pearson symbol, space group number and Wyckoff positions, joined by underscores), without the library's enumeration suffix. | `[A-Z][A-Za-z0-9]*_[amothc][PCSABIFR][0-9]+_[0-9]{1,3}(_[A-Za-z0-9]+)+` | — | `ABC3_oP20_62_c_c_cd` | [arxiv.org](https://arxiv.org/abs/1607.02532) |
| InChI | molecule | The Standard InChI, which begins InChI=1S/. | `InChI=1S/.+` | — | `InChI=1S/C5H5N5O/c6-5-9-3-2(4(11)10-5)7-1-8-3/h1H,(H4,6,7,8,9,10,11)` | [github.com](https://github.com/IUPAC-InChI/InChI/blob/main/INCHI-1-DOC/FAQ/html/inchi-faq.html) |
| SMILES | molecule | A SMILES string as the OpenSMILES grammar defines it. | `[A-Za-z0-9@+\-\[\]()=#$:/\\.%*]+` | — | `CCO` | [github.com](https://github.com/opensmiles/OpenSMILES/blob/master/opensmiles.asciidoc) |
<!-- END generated -->
