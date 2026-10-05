# Build scripts (not published: GitHub Pages skips folders starting with "_")

- `pdflines.swift` extracts each PDF line with its position into `lines/` (reading order).
- `build.py` + `pages.py` turn those into chapter blocks; `render.py` writes `read/*.html`.
- `overview.py` writes `read/overview.html` (set by hand). `read/seven-white-days.html` is hand-built.
- `tools_build.py` writes `tools/*.html` and `tools.html` from `tools-src.html`.

Regenerate: `python3 _build/render.py && python3 _build/overview.py && python3 _build/tools_build.py`
Per-chapter corrections (typos, removed notes) live in `pages.py` (`fix_text`, `fix_fn`, `fix_html`).

## Expanded-edition chapters (from the author's RTF)
- The author's Nisus RTF goes in `review/sources/` (gitignored: it holds tracked changes and deleted drafts). Configure it in `CHAPTERS` in `rtf_chapter.py`.
- `python3 _build/rtf_chapter.py` keeps only the final wording (deleted text dropped, insertions kept), places every footnote, saves diagrams to `images/chN/`, and marks the page "From the forthcoming expanded edition" (no PDF; the end card offers the current edition and Notify me).
- Then add the slug to `ORDER` in render.py and search_index.py, run `python3 _build/render.py && python3 _build/overview.py && python3 _build/search_index.py`, and update the homepage card and sitemap.xml.
