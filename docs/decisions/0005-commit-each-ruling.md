# 0005 — Commit each ruling as it is made; the human pushes

Date: 2026-10-31. Status: accepted. Decided by: Ellad Tadmor.

## Context
A ruling that exists only in a conversation is lost when the session ends, and batching several rulings into one change mixes unrelated edits in the same files.

## Decision
- When the human rules on an item, the ruling is written into the repository (CLAUDE.md, plus a decision record where one is needed) before the next item is taken up.
- The diff is shown to the human and committed once approved.
- Claude never pushes. The human pushes, since every push to main redeploys the site.

## Consequences
Each ruling is a small, separately reviewable commit, and no ruling depends on the conversation surviving.
