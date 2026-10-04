# Build scripts (not published: GitHub Pages skips folders starting with "_")

- `pdflines.swift` extracts each PDF line with its position into `lines/` (reading order).
- `build.py` + `pages.py` turn those into chapter blocks; `render.py` writes `read/*.html`.
- `overview.py` writes `read/overview.html` (set by hand). `read/seven-white-days.html` is hand-built.
- `tools_build.py` writes `tools/*.html` and `tools.html` from `tools-src.html`.

Regenerate: `python3 _build/render.py && python3 _build/overview.py && python3 _build/tools_build.py`
Per-chapter corrections (typos, removed notes) live in `pages.py` (`fix_text`, `fix_fn`, `fix_html`).
