# Non-destructive restructuring plan

Branch: `refactor/research-project-layout`.

1. Copy project files to dedicated `projects/` directories and keep canonical legacy files unchanged.
2. Verify byte-for-byte source copies and JSON results, and compile Python source files.
3. Next: migrate imports into proper packages, update workflow paths, rerun complete public-data experiments and compare saved metrics.
4. Only after those tests pass: merge and remove legacy duplicates in a separate cleanup PR.

**Do not delete or move original files in this PR.** The layout is intentionally transitional and should not be mistaken for a completed runtime migration.
