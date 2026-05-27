# Multi-Language Documentation Management Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the branch-per-language + duplicated-folder approach with the canonical Sphinx gettext (`sphinx-intl`) translation workflow, so a single source tree drives every language and translation drift becomes visible and trackable.

**Architecture:** Keep **one** canonical source tree (`docs/source/`). Translations live as gettext `.po` catalogs under `docs/source/locale/<lang>/LC_MESSAGES/` on the *same* branch — never as a forked folder or branch. Each language is built by overriding `-D language=<lang>`. Version management (git branches/tags + `sphinx-multiversion`) stays a separate, orthogonal axis. On Read the Docs, each language becomes its own "translation" project linked to a main project, giving a language selector in the published flyout.

**Tech Stack:** Sphinx 5.3.0, `sphinx_rtd_theme`, `sphinx-multiversion`, `sphinx-intl`, gettext catalogs (`.pot`/`.po`), Read the Docs for Business, Windows PowerShell build host (Python 3.10).

---

## Decision 0: Canonical source language (CONFIRMED 2026-05-26)

**Decided:** **Chinese (`zh_CN`)** is the canonical source language; **English (`en`)** is a translation.

**Why this default:** All real `.rst` content currently lives in Chinese in `docs/source/`. Making Chinese the source means **no content has to move** — we only add translation catalogs. The gettext `msgid`s will be Chinese strings, which is fully supported.

**If you instead want English as the source** (some teams prefer English `msgid`s for tooling/translator familiarity): every `.rst` in `docs/source/` must first be rewritten in English and the Chinese moved into a `zh_CN` catalog. That is a much larger, content-heavy effort and is **out of scope for this plan** — flag it and re-plan if chosen.

Everywhere below, **SOURCE_LANG = `zh_CN`** and **TARGET_LANG = `en`**.

---

## Current State (what we are migrating away from)

- `docs/source/` — Chinese `.rst` content (the real source of truth).
- `conf.py:43` — `language = 'EN'` is **hardcoded** (only sets Sphinx UI strings; does not translate prose). Must be changed to the source language and overridden per build.
- `conf.py:24` — uses `sphinx_multiversion`, but it is **missing from `docs/requirements.txt`** (build aborts without it).
- Branch `lateset_EN` — an in-progress manual English fork: English edited directly into `docs/source/` with Chinese copied into a parallel `docs/source_cn/`. **This is the anti-pattern being retired.** Only `introduce/quick_start/index.rst` is fully translated; `support/faq.rst` is partially translated.
- Branch `latest` — tracks Chinese `main` content.

---

## File Structure

| File | Responsibility | Action |
|------|----------------|--------|
| `docs/requirements.txt` | Pin all build deps | Modify — add `sphinx-intl`, `sphinx-multiversion` |
| `docs/source/conf.py` | Sphinx config | Modify — set `language = 'zh_CN'`, add `locale_dirs`, `gettext_compact = False` |
| `docs/source/locale/en/LC_MESSAGES/*.po` | English translation catalogs (one per source `.rst`) | Create (generated) |
| `docs/source/locale/.gitignore` | Ensure `.po` tracked, `.mo` ignored | Create |
| `docs/Makefile` / `docs/make.bat` | Per-language build + i18n targets | Modify — add `gettext`, `intl-update`, `html-en`, `html-cn` targets |
| `docs/i18n_build.ps1` | Windows one-shot build-all-languages helper | Create |
| `README.md` | Document the translation workflow | Modify — add "Translating the docs" section |
| `lateset_EN` branch / `docs/source_cn/` | Duplicated language fork | **Kept** — owner deletes manually later (Task 8 only verifies salvage) |

---

## Task 1: Pin the missing build dependencies

**Files:**
- Modify: `docs/requirements.txt`

- [ ] **Step 1: Add the two missing packages**

Edit `docs/requirements.txt` to append (keep existing pins intact):

```
sphinx-multiversion==0.2.4
sphinx-intl==2.1.0
```

- [ ] **Step 2: Install into the active environment**

Run:
```powershell
pip install -r docs/requirements.txt
```
Expected: `Successfully installed ... sphinx-intl-2.1.0 sphinx-multiversion-0.2.4` (or "Requirement already satisfied").

- [ ] **Step 3: Verify both import**

Run:
```powershell
python -c "import sphinx_multiversion, sphinx_intl; print('ok')"
```
Expected: `ok`

- [ ] **Step 4: Commit**

```powershell
git add docs/requirements.txt
git commit -m "build: pin sphinx-multiversion and sphinx-intl"
```

---

## Task 2: Make `conf.py` translation-ready

**Files:**
- Modify: `docs/source/conf.py` (line 43 region, and the HTML-options block)

- [ ] **Step 1: Set the source language and locale settings**

In `docs/source/conf.py`, replace:

```python
language = 'EN'
html_search_language = 'en'
```

with:

```python
# Canonical SOURCE language of the .rst files (see PLAN.md Decision 0).
# Per-language builds override this with `-D language=en`.
language = 'zh_CN'

# gettext translation catalogs live next to the source tree.
locale_dirs = ['locale/']
# One .po file per source document (not a single merged catalog) so
# translation drift is attributable to a specific page.
gettext_compact = False
```

Note: do **not** hardcode `html_search_language`; Sphinx derives it from `language` per build.

- [ ] **Step 2: Verify the source-language build still succeeds**

Run:
```powershell
python -m sphinx -b html docs/source docs/_build/html/zh_CN
```
Expected: `build succeeded` (warnings about duplicate labels are pre-existing and acceptable).

- [ ] **Step 3: Commit**

```powershell
git add docs/source/conf.py
git commit -m "docs: set zh_CN as source language and enable gettext locale dirs"
```

---

## Task 3: Generate the gettext template (`.pot`) files

**Files:**
- Create (generated, build artifact — not committed): `docs/_build/gettext/**/*.pot`

- [ ] **Step 1: Extract translatable strings from the source**

Run:
```powershell
python -m sphinx -b gettext docs/source docs/_build/gettext
```
Expected: `build succeeded`; `docs/_build/gettext/` now contains a `.pot` file mirroring each source doc (e.g. `introduce/quick_start/index.pot`).

- [ ] **Step 2: Spot-check a template contains Chinese msgids**

Run:
```powershell
Get-Content docs/_build/gettext/introduce/quick_start/index.pot -TotalCount 30
```
Expected: `msgid` lines containing the Chinese source strings (e.g. `msgid "快速开始"` or similar), with empty `msgstr ""`.

*(No commit — `.pot` files are regenerable build artifacts and stay out of git.)*

---

## Task 4: Create the English (`en`) catalog skeleton

**Files:**
- Create: `docs/source/locale/en/LC_MESSAGES/*.po` (one per source doc)
- Create: `docs/source/locale/.gitignore`

- [ ] **Step 1: Generate the empty English `.po` catalogs**

Run:
```powershell
sphinx-intl update -p docs/_build/gettext -l en -d docs/source/locale
```
Expected: `Create: docs/source/locale/en/LC_MESSAGES/....po` lines for every document.

- [ ] **Step 2: Ignore compiled catalogs but track sources**

Create `docs/source/locale/.gitignore` with:

```
# Compiled message catalogs are build artifacts; regenerate from .po
*.mo
```

- [ ] **Step 3: Verify catalog layout**

Run:
```powershell
Get-ChildItem -Recurse docs/source/locale/en/LC_MESSAGES -Filter *.po | Select-Object -First 5 FullName
```
Expected: at least the `introduce/quick_start/index.po` and `support/faq.po` catalogs exist among others.

- [ ] **Step 4: Commit the empty catalogs**

```powershell
git add docs/source/locale
git commit -m "docs(i18n): scaffold empty English (en) gettext catalogs"
```

---

## Task 5: Seed the English catalog from existing `lateset_EN` translations

**Goal:** Salvage the already-translated English prose on the `lateset_EN` branch (`introduce/quick_start`, `support/faq` headings) into the new `.po` catalogs instead of throwing it away. Translation is done by filling `msgstr` entries — manually or via a tool.

**Files:**
- Modify: `docs/source/locale/en/LC_MESSAGES/introduce/quick_start/index.po`
- Modify: `docs/source/locale/en/LC_MESSAGES/support/faq.po`

- [ ] **Step 1: Pull the existing English text for reference**

Run (from the main worktree, reading the branch without checkout):
```powershell
git show origin/lateset_EN:docs/source/introduce/quick_start/index.rst | Out-File -Encoding utf8 docs/_build/_seed_quickstart_en.rst
git show origin/lateset_EN:docs/source/support/faq.rst | Out-File -Encoding utf8 docs/_build/_seed_faq_en.rst
```
Expected: two reference files written; the quick_start one begins with `Quick Start`.

- [ ] **Step 2: Fill `msgstr` entries for quick_start**

Open `docs/source/locale/en/LC_MESSAGES/introduce/quick_start/index.po` in a `.po` editor (Poedit) or a text editor. For each `msgid "<Chinese>"`, paste the matching English from `docs/_build/_seed_quickstart_en.rst` into `msgstr ""`. Example:

```po
msgid "快速开始"
msgstr "Quick Start"
```

Leave entries with no English equivalent yet as empty `msgstr ""` (they will fall back to the Chinese source at build time).

- [ ] **Step 3: Fill `msgstr` entries for faq headings**

Repeat Step 2 for `docs/source/locale/en/LC_MESSAGES/support/faq.po` using `docs/_build/_seed_faq_en.rst` (only the translated headings exist; bodies stay empty for now).

- [ ] **Step 4: Build the English site and verify the seeded pages render in English**

Run:
```powershell
python -m sphinx -b html -D language=en docs/source docs/_build/html/en
```
Expected: `build succeeded`. Then:
```powershell
Select-String -Path docs/_build/html/en/introduce/quick_start/index.html -Pattern "Quick Start" -SimpleMatch | Select-Object -First 1
```
Expected: a match (the English heading rendered from the catalog).

- [ ] **Step 5: Commit the seeded translations**

```powershell
git add docs/source/locale/en/LC_MESSAGES/introduce/quick_start/index.po docs/source/locale/en/LC_MESSAGES/support/faq.po
git commit -m "docs(i18n): seed English catalog from lateset_EN quick_start and faq"
```

---

## Task 6: Add per-language and i18n build targets

**Files:**
- Modify: `docs/Makefile`
- Modify: `docs/make.bat`
- Create: `docs/i18n_build.ps1`

- [ ] **Step 1: Add i18n targets to `docs/Makefile`**

Append to `docs/Makefile`:

```makefile
# --- i18n / multi-language targets ---
LANGUAGES = zh_CN en

gettext:
	$(SPHINXBUILD) -b gettext "$(SOURCEDIR)" "$(BUILDDIR)/gettext" $(SPHINXOPTS)

intl-update: gettext
	sphinx-intl update -p "$(BUILDDIR)/gettext" -l en -d "$(SOURCEDIR)/locale"

html-cn:
	$(SPHINXBUILD) -b html -D language=zh_CN "$(SOURCEDIR)" "$(BUILDDIR)/html/zh_CN" $(SPHINXOPTS)

html-en:
	$(SPHINXBUILD) -b html -D language=en "$(SOURCEDIR)" "$(BUILDDIR)/html/en" $(SPHINXOPTS)

html-all: html-cn html-en
```

- [ ] **Step 2: Add the same targets to `docs/make.bat`**

In `docs/make.bat`, add handling before the final `:end` (mirror existing target style):

```bat
if "%1" == "gettext" (
	%SPHINXBUILD% -b gettext %SOURCEDIR% %BUILDDIR%\gettext %SPHINXOPTS%
	goto end
)
if "%1" == "intl-update" (
	%SPHINXBUILD% -b gettext %SOURCEDIR% %BUILDDIR%\gettext %SPHINXOPTS%
	sphinx-intl update -p %BUILDDIR%\gettext -l en -d %SOURCEDIR%\locale
	goto end
)
if "%1" == "html-cn" (
	%SPHINXBUILD% -b html -D language=zh_CN %SOURCEDIR% %BUILDDIR%\html\zh_CN %SPHINXOPTS%
	goto end
)
if "%1" == "html-en" (
	%SPHINXBUILD% -b html -D language=en %SOURCEDIR% %BUILDDIR%\html\en %SPHINXOPTS%
	goto end
)
```

- [ ] **Step 3: Create a PowerShell build-and-serve helper**

Create `docs/i18n_build.ps1`:

```powershell
# Build every language and (optionally) serve one for preview.
# Usage: .\i18n_build.ps1            # build all
#        .\i18n_build.ps1 -Serve en  # build all, then serve the en site on :8001
param([string]$Serve)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path

# 1. refresh catalogs from current source
python -m sphinx -b gettext "$root/source" "$root/_build/gettext"
sphinx-intl update -p "$root/_build/gettext" -l en -d "$root/source/locale"

# 2. build each language into its own subfolder
foreach ($lang in @('zh_CN','en')) {
    python -m sphinx -b html -D language=$lang "$root/source" "$root/_build/html/$lang"
}

# 3. optional preview
if ($Serve) {
    Set-Location "$root/_build/html/$Serve"
    python -m http.server 8001 --bind 127.0.0.1
}
```

- [ ] **Step 4: Verify the all-languages build works end to end**

Run:
```powershell
powershell -ExecutionPolicy Bypass -File docs/i18n_build.ps1
```
Expected: both `docs/_build/html/zh_CN/index.html` and `docs/_build/html/en/index.html` exist.

Run:
```powershell
Test-Path docs/_build/html/zh_CN/index.html; Test-Path docs/_build/html/en/index.html
```
Expected: `True` then `True`.

- [ ] **Step 5: Commit**

```powershell
git add docs/Makefile docs/make.bat docs/i18n_build.ps1
git commit -m "build(i18n): add gettext, intl-update, and per-language html targets"
```

---

## Task 7: Document the translation workflow in README

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add a "Translating the documentation" section**

Insert into `README.md` (after the existing build section):

```markdown
## Translating the documentation (multi-language)

The source language is **Chinese (`zh_CN`)** — all `.rst` files in `docs/source/`
are written in Chinese. Other languages are **gettext translation catalogs**, not
copies of the source. Never fork `docs/source/` per language.

### Update catalogs after editing source
```powershell
cd docs
make intl-update      # or: .\i18n_build.ps1 to also rebuild HTML
```
This re-extracts strings and refreshes `docs/source/locale/en/LC_MESSAGES/*.po`.
Changed source paragraphs become "fuzzy" entries — that is your translation to-do list.

### Translate
Edit the `.po` files (e.g. with [Poedit](https://poedit.net/)) and fill each
`msgstr`. Empty `msgstr` entries fall back to the Chinese source at build time.

### Build a specific language
```powershell
cd docs
make html-cn    # Chinese -> _build/html/zh_CN
make html-en    # English -> _build/html/en
```

### Versions vs. languages
Versions (latest/stable/tags) are managed by git branches/tags + sphinx-multiversion.
Languages are managed by catalogs + separate Read the Docs translation projects.
The two axes are independent — never put a language on its own git branch.
```

- [ ] **Step 2: Commit**

```powershell
git add README.md
git commit -m "docs: document gettext-based multi-language workflow"
```

---

## Task 8: Confirm English content is salvaged (branch retained)

**Goal:** Verify the existing English work on `lateset_EN` is fully captured in the catalogs (Task 5). **The `lateset_EN` branch is intentionally KEPT — the repo owner will delete it manually later.** This task does NOT delete any branch.

**Files:**
- None deleted by this plan.

- [ ] **Step 1: Confirm no untranslated content is lost**

Run:
```powershell
git diff --stat main origin/lateset_EN -- docs/source
```
Expected: review the list; confirm every English edit on `lateset_EN/docs/source` has a corresponding `msgstr` in the catalogs (from Task 5). If anything is missing, return to Task 5.

- [ ] **Step 2: Verify the `(?!chinese)` multiversion whitelist still matches intent**

`conf.py:72` has `smv_branch_whitelist = r'^(?!chinese).*$'`. With `lateset_EN` retained, decide whether it should appear as a *version* in the multiversion build. If it should NOT (it is a soon-to-be-deleted language fork, not a real doc version), tighten the whitelist, e.g.:

```python
smv_branch_whitelist = r'^(main|latest)$'
```

Otherwise leave as-is. No content change — this is a config/verification decision.

> **Manual follow-up (owner, not this plan):** once satisfied the catalogs cover everything, delete the fork yourself:
> ```powershell
> git push origin --delete lateset_EN
> git worktree remove ../daoai_pcb_aoi_user_manual_EN   # if the temp worktree still exists
> ```

---

## Task 9: Read the Docs translation-project setup (hosting, manual console steps)

**Goal:** Surface the language selector on the published site. These are Read the Docs admin-console actions, not repo changes — listed here so the migration is complete.

- [ ] **Step 1: Confirm the main project builds `zh_CN`**

On Read the Docs, the existing project's *Settings → Language* = **Simplified Chinese (`zh_CN`)**. This is the main project.

- [ ] **Step 2: Create the English translation project**

Add a **new** RTD project from the **same repository**, *Settings → Language* = **English (`en`)**. It builds the same repo; RTD passes the language to Sphinx.

- [ ] **Step 3: Link it as a translation**

On the main (Chinese) project: *Settings → Translations → Add translation* → select the English project. RTD then renders a **language selector** in the flyout menu, and `/en/` / `/zh_CN/` URL prefixes resolve to each.

- [ ] **Step 4: Verify published output**

After both projects build, confirm the flyout shows a language dropdown and that switching changes the prose (not just the UI chrome).

---

## Self-Review Notes

- **Spec coverage:** gettext workflow (Tasks 2–6), removing hardcoded `language` (Task 2), fixing missing deps (Task 1), salvaging existing English work (Task 5), verifying salvage with branch retained (Task 8), RTD per-language projects (Task 9), keeping versioning orthogonal (Tasks 7 & 8 Step 2) — all covered.
- **Decision dependency:** Decision 0 = Chinese source is CONFIRMED. No content-rewrite effort needed.
- **Non-destructive:** This plan deletes nothing. The `lateset_EN` branch and `docs/source_cn/` fork are retained; the owner deletes them manually after reviewing the salvaged catalogs.
- **Verification model:** Docs have no unit tests; "verification" is a successful `sphinx-build` plus a `Select-String`/`Test-Path` assertion on the rendered HTML for each language.
