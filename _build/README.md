# Build scripts (not published: GitHub Pages skips folders starting with "_")

- `pdflines.swift` extracts each PDF line with its position into `lines/` (reading order).
- `build.py` + `pages.py` turn those into chapter blocks; `render.py` writes `read/*.html`.
- `overview.py` writes `read/overview.html` (set by hand). `read/seven-white-days.html` is hand-built.
- `tools_build.py` writes `tools/*.html` and `tools.html` from `tools-src.html`.

Regenerate: `python3 _build/render.py && python3 _build/overview.py && python3 _build/rtf_chapter.py && python3 _build/finish_read.py && python3 _build/tools_build.py`
- `finish_read.py` gives the hand-built seven-white-days.html the shared breadcrumbs, byline, quiz card and related chapters, and writes `read/index.html` (all chapters, quizzes and tools). Related chapters, link text, quiz cards, H1 terms and "Last updated" dates are set at the top of `render.py`.
Per-chapter corrections (typos, removed notes) live in `pages.py` (`fix_text`, `fix_fn`, `fix_html`).

## Expanded-edition chapters (from the author's RTF)
- The author's Nisus RTF goes in `review/sources/` (gitignored: it holds tracked changes and deleted drafts). Configure it in `CHAPTERS` in `rtf_chapter.py`.
- `python3 _build/rtf_chapter.py` keeps only the final wording (deleted text dropped, insertions kept), places every footnote, saves diagrams to `images/chN/`, and marks the page "From the forthcoming expanded edition" (no PDF; the end card offers the current edition and Notify me).
- Then add the slug to `ORDER` in render.py and search_index.py, run `python3 _build/render.py && python3 _build/overview.py && python3 _build/search_index.py`, and update the homepage card and sitemap.xml.

## Common questions (FAQ) on chapter pages
- Drafts live in `faq.py`: each answer is quoted word for word from the same chapter (only the questions are new).
  `python3 _build/faq_check.py` verifies the quotes and writes `review/faq-drafts.html` for Rabbi Jacobs.
- A page shows its "Common questions" section (with matching FAQPage data) only after its entry is set to `approved=True`;
  then rebuild the chapter pages (see Regenerate above).

## Questions and answers (/questions/)
- `questions.py` holds the questions (Rabbi Jacobs writes every answer); `python3 _build/questions.py` writes
  `questions/<slug>.html` and `questions/index.html`, then run `python3 _build/sitemap.py`.
- Until the first answer is published the index is noindex and left out of the sitemap and menus.
  With the first answer: add "Questions" to the site menus (index.html, start-here.html, search.html,
  recommended-sites.html and the calendar templates in hidden-tools/).
