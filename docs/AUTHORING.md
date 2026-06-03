# Authoring conventions (comprehensive-manual delta)

- Source language is **zh_CN**. Author Chinese first; English is a `.po` catalog refreshed last.
- **Only the page title is a reST section heading.** Template blocks (此页面的用途 / 如何进入 /
  操作流程 / 注意事项 / 相关页面) are **bold leads** (`**…**`), never `---` sub-sections —
  `autosectionlabel` has no doc-prefix, so repeated block headings would cause duplicate-label
  build warnings.
- Name every control by its **exact Chinese string from `aoi_pcb_web_client/src/translations/*.js`**.
- Screenshots: reuse an **existing** image with `.. image:: images/<name>.png` (`:scale:` + Chinese
  `:alt:`). For a screenshot that does **not exist yet**, do NOT use a live `.. image::` directive —
  Sphinx warns on a missing image file and breaks the 0-warning build. Instead leave a reST **comment
  placeholder** so the build stays clean and the later capture pass can find it:
  `.. screenshot-todo: images/<name>.png — <中文说明>` (single colon = a comment, not a directive).
- Cross-references: `:ref:`<目标页面中文标题>`` (autosectionlabel keys off the Chinese heading).
- Scope: online / multi-backend content IS in scope — wrap online-only **sections** in
  ``.. only:: online`` and put online-only **whole pages** under a ``.../online/`` directory
  (``conf.py`` excludes them from offline builds). MES is **common** content (no tag). 3D
  (``VITE_AOI_VERSION=3d_smt``) is still out of scope.
- Cross-references: common (untagged) content must **never** ``:ref:`` an online-only heading
  (the offline build drops the target and warns). Online → common refs are fine.
- Build check (from `docs/`): `sphinx-build -E -a -b html -D language=zh_CN source _build/html/zh_CN 2>&1 | grep -E "WARNING|ERROR"` must print nothing.
