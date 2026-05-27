# Authoring conventions (comprehensive-manual delta)

- Source language is **zh_CN**. Author Chinese first; English is a `.po` catalog refreshed last.
- **Only the page title is a reST section heading.** Template blocks (此页面的用途 / 如何进入 /
  操作流程 / 注意事项 / 相关页面) are **bold leads** (`**…**`), never `---` sub-sections —
  `autosectionlabel` has no doc-prefix, so repeated block headings would cause duplicate-label
  build warnings.
- Name every control by its **exact Chinese string from `aoi_pcb_web_client/src/translations/*.js`**.
- Screenshots: `.. image:: images/<name>.png` with `:scale:` and a Chinese `:alt:`. Reuse existing
  shots; for missing ones, write the prose + the `.. image::` line (capture is a later pass).
- Cross-references: `:ref:`<目标页面中文标题>`` (autosectionlabel keys off the Chinese heading).
- Scope: NO online/multi-backend, NO MES, NO 3D.
- Build check (from `docs/`): `sphinx-build -E -a -b html -D language=zh_CN source _build/html/zh_CN 2>&1 | grep -E "WARNING|ERROR"` must print nothing.
