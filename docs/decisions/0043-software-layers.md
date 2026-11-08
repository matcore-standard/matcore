# 0043 — Software as layers, with identification, dependencies and file encoding

Date: 2026-11-08. Status: accepted. Decided by: Ellad Tadmor.

## Context
Community feedback on minimal `computation › software` (name, version, file):
- A name and a version do not identify a build from a branch or a Git tag rather than an official release.
- Compilers, MPI, linear-algebra and FFT libraries and LibXC can change results; they belong in the provenance, and are needed to trace results back to a buggy component. A group with the data-management team at the Barcelona Supercomputing Center (BSC) is defining a software metadata standard for HPC environments and offers to contribute.
- How do wrappers fit (OpenKIM tests, iprPy calculations, pyiron, MedeA, ASE scripts)? Is a wrapper a software entry; is its input its code or what it reads; is an ASE script "Python" or "ASE"; when does a script become software? At least `description`, a DOI and a URL should be added. Separate `wrapper-script` and `standard-calculation-method` properties were suggested.
- `file › contents`: is it a Unicode string or a byte stream, and in which encoding?

Principles applied:
- A MatCore record documents a dataset. A wrapper or method with no data of its own gets no MatCore record; its own metadata describes it, and a record cites it by identifier. Each use of a wrapper that produces data is a dataset, in whose record the wrapper is a software entry.
- Every layer that took part is a `software` entry, and a `role` says which layer it is. Separate properties for wrappers and methods would share most fields and ask writers to classify borderline tools; a role term does that, and an unlisted case is still a valid open term.
- A string in the data model is Unicode text; the serialization of the record fixes its bytes. A field naming a character encoding would repeat or contradict the serialization. What a string cannot carry is a binary file, or a text file whose exact bytes matter (e.g. one in a legacy encoding, whose checksum would change when decoded).

## Decision
1. **`software`**'s description becomes: "A program, package or script used to perform the calculations: the simulation code, a calculation method or workflow framework that drives it, or a custom script." A note: "Note: Give one entry for each layer that took part, outermost first. A file is given under the entry that reads it; for a script, its own code is its file." `software` stays required and repeatable.
2. **New subproperties of `software`**, after `name`, in this order (all optional):
   - **`role`**: string, open terms Calculation method, Script, Simulation code, Workflow framework. Description: "The part this software played in the calculations." Note: "One of: "Calculation method" – A packaged procedure that computes a defined property, e.g. an OpenKIM test or an iprPy calculation. "Script" – Custom code written for the calculations, e.g. a Python script using ASE. "Simulation code" – A program that performs the simulation or calculation itself, e.g. LAMMPS or VASP. "Workflow framework" – A system that sets up, runs and manages calculations with other software, e.g. pyiron, AiiDA or MedeA."
   - **`description`**: string. Description: "What this software did in the calculations."
   - **`version`**: kept, after `description`. Its note becomes: "Note: Give the version for an official release. For any other state of the code, e.g. a branch or a tag, give link and revision."
   - **`link`**: string, format uri. Description: "A URI for the software, e.g. its source repository or home page."
   - **`revision`**: string. Description: "A tag or commit in the repository given in link." Note: "Note: Give the full commit hash where possible; a tag or a branch can move."
   - **`identifier`**: repeatable container of `value*` and `scheme*` as in creator's identifier, with scheme terms DOI and SWHID (Annex I). Description: "A persistent identifier of the software or of the exact state of its code."
   - **`dependency`**: repeatable container. Description: "A component the software was built with or ran on that can change its results." Note: "Note: List the components that can change results, e.g. the compiler, the MPI, linear-algebra and FFT libraries, and libraries such as LibXC." Subproperties: `name*` (string, "The name of the component."), `version` (string, "The version of the component."), `role` (string, open terms Compiler, FFT library, Interpreter, Library, Linear algebra library, MPI library; description "The kind of component."; note defining each term).
   - **`build-options`**: string. Description: "The options the software was built or run with that can change its results, e.g. compiler flags or enabled features."
   - **`file`**: kept, last.
3. **`file`** gains **`encoding`** after `contents`: optional; string, open terms Base64. Description: "How contents is encoded." Note: "Note: Without encoding, contents is the file's text. With Base64, contents is the file's bytes encoded as Base64 (RFC 4648); use it for a binary file, or for a text file whose exact bytes matter." `contents`'s description becomes: "The contents of the file: its text, or its bytes encoded as given in encoding. Not required in case a link to the file is provided instead."
4. **examples/minimal.xml**: CASTEP gains `<role>Simulation code</role>`. No version or build is invented for the Si GAP data.

## Consequences
- One pull request applies items 1–4 (schema, tests, regenerated page, example). No instance is broken: every addition is optional.
- The full software environment (dependency graph, modules, hardware) is outside MatCore; a record points to a document holding it, as a `file` or a `link`. PROPOSED, NOT DECIDED: naming a recommended format for that document, e.g. the HPC software metadata standard in preparation at BSC, once it exists. Candidate formats to check against their specifications: CodeMeta, SPDX and CycloneDX software bills of materials, Spack specifications.
- PROPOSED, NOT DECIDED: KIM IDs as an Annex I scheme, so an OpenKIM test or model can be cited by its KIM ID.
