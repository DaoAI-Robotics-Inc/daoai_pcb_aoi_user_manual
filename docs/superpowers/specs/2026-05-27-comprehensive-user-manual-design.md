# Comprehensive User Manual — Design

**Status:** Approved design (brainstorming complete). Implementation plan is a separate step.

**Date:** 2026-05-27

**Repo:** `daoai_pcb_aoi_user_manual` (Sphinx + Read the Docs)

---

## 1. Goal

Produce a **comprehensive, reference-grade user manual** for the PCB AOI web client
(`aoi_pcb_web_client`) — documenting **every page, every button, every editable field**
that an operator/programmer encounters in the UI, in the style of the LMI GoPxl and Zivid
reference manuals. Claude reads the frontend codebase directly to understand the UI and
generates the documentation; the entire codebase is available as ground truth.

This is a **one-time comprehensive rewrite**, not a reusable doc-generation system. The
output is the manual itself.

---

## 2. Confirmed scope decisions

| Decision | Choice |
|----------|--------|
| Deliverable | One-time comprehensive rewrite (the docs themselves) |
| Coverage | Comprehensive **within** the existing exclusions |
| Excluded | Online / multi-backend inspection mode, MES integration, **all 3D** content |
| Source language | **Chinese (`zh_CN`)**; English `.po` catalog refreshed in a final pass |
| Screenshots | **Prose-first** — author complete prose now with screenshot placeholders/captions; dedicated capture pass later |
| Doc style | **Narrative walkthroughs** — step-by-step prose covering every control inline; no separate per-control reference tables |
| Structure | Operator-journey-based IA (see §4), approved as-is |
| Detection tools | **One page per tool** |
| Execution | Parallel subagents, one section at a time, clean-build verification |

**Explicitly out of scope (document as "not covered" only if cross-referenced):**
`LiveOnline`, `ReviewOnline`, `MultiBackendHome/LiveOnline/ReviewOnline`,
`ReviewDeviceConveyorPicker`, MES (`MesProfileEditor`, `TrackLabelsEditor`,
`OnlineSystemConfig`, `InspectionDetailExport`, `MesAlarmModal`), and every 3D inspection
feature/section/screenshot.

---

## 3. Sources of truth (the generation engine)

For **each** documented page, the authoring subagent works from three grounded sources and
never invents UI:

1. **The page component + its render tree.** The route's top-level `.jsx`
   (e.g. `src/pages/Home.jsx`) plus every child component and modal it renders. This yields
   the real controls, their on-screen order, conditional visibility (role gates such as
   `ADMIN`/`OPERATOR`/`PROGRAMMER`, mode gates such as `isOnlineVersion`), and each control's
   behavior. Routes are enumerated from `src/Router.jsx`; deeper architecture from
   `aoi_pcb_web_client/CONTEXT.md`.
2. **The translation files** (`src/translations/*.js`). Authoritative source for every
   button/label/field string in **both** `cn` and `en`. Every documented control is named
   using the exact Chinese string from here, so prose matches the live UI and Chinese
   authoring is correct by construction.
3. **The reference PDFs** (`apps/ref/*.pdf`). Used for AOI **domain terminology** and phrasing
   conventions only — not for structure or control inventory.

Rationale: the component tree enumerates the controls, the translation files name them, and a
fixed page template (see §5) guarantees each control is described. This is what makes the
effort exhaustive and repeatable across subagents.

---

## 4. Information architecture (approved)

```
介绍 Introduction
 ├─ 快速开始 Quick Start                         (exists — already rewritten)
 └─ 系统概览与界面导航 Overview & UI orientation  (NEW: login, header/footer shell, user roles)

主页 Home / Dashboard
 ├─ 产品目录管理 (编辑 / 复制 / 删除 / 重命名 / 导出为文件; 标签; 上传 PCBA .zip)
 ├─ 传送带状态 / 重置轨道
 └─ 最近检测任务 + 任务入口 (新建检测任务 / 训练PCBA / 工作列表)

创建与编程产品 Create & Teach a Product
 ├─ 自动编程向导 (基本信息 → 传送带 → 获取尺寸 → 拍摄 → 添加CAD)
 ├─ CAD 上传与坐标对齐
 └─ 标记 / 对齐 PCB (markAlignPCB)

模板编辑器 Template Editor  (programming core)
 ├─ 元件列表与分组 (按元件 / 料号 / 封装)
 ├─ 产品设置 Recipe (传送带 / PCB详情 / 尺寸 / 拍摄 / 检测设置含 badmark)
 ├─ 元件配置 ComponentInfo (对齐 / AI对齐 / 跳过检测 / 中心拍摄 / badmark)
 ├─ 检测工具参考 Detection tools  — ONE PAGE PER TOOL:
 │     本体 body · 焊点 solder · IC引脚 lead · 文本/OCV text · 条码 barcode ·
 │     桥连 bridge · 颜色 color · 胶点 glue-on-pad · DIP 焊点/桥连 dip
 ├─ 共线检测 Collinearity inspection (collinearityInspection — confirmed 2D)
 ├─ PCB 拼板 PCB Array (子板模板 / 手动生成 / 自动生成 / 自动调整)
 ├─ 整板检测 Whole Board Inspection
 ├─ 训练与生成参数
 └─ 变体 / 替代元件 Variations (alter components)

检测 Inspection
 ├─ 新建检测任务对话框 (演示模式 / A·B 面)
 ├─ 实时检测 Live (产品统计 / 元件统计 / 检测时长 / FPY 整板·子板 / 传送带控制)
 └─ 复检 Review (NG列表 / 反馈 / 标注 / 变体)

数据分析报告 Data Analysis Report  (worklist)
 └─ 总结 / 检测结果 / 不良元件 / 误判元件 (PPM / DPU)

模型管理 Models
 └─ 数据集 / 训练 / 导入·导出 / 训练-测试分布 / 设为默认·重命名·删除

系统设置 Settings
 ├─ 团队·账号 Team · 管理模型 Manage Models · 标签 Tags
 └─ 系统设置 systemSettings:
       语言 Language · 主机 Host · 系统配置 SystemConfig · 捕获模块 CaptureAgent ·
       模型更新器 ModelUpdater · 编程默认参数 ProgramDefaultParams ·
       错误类型翻译 ErrorTypeTranslation · 校准 Calibration · 关于 About · 日志 Log

支持 Support
 └─ 常见问题 FAQ
```

The existing `complete_user_guide/{home,features,config,inspection,system_management}` files
are **reorganized/expanded** into this tree (reusing prose/labels/screenshots where still
accurate). The top-level `docs/source/index.rst` toctree is rewritten to match.

---

## 5. Per-page narrative template

Every page is authored to the same skeleton so coverage is uniform and reviewable:

```
<页面标题>
==========

此页面的用途
   1–2 sentences: what the page is for and who uses it.

如何进入
   How to reach it — route and/or button path from a parent page.

[screenshot placeholder + caption]   ← prose-first; real capture is a later pass

操作流程
   Narrative walkthrough in the UI's own top-to-bottom / left-to-right order.
   EVERY button, input, toggle, dropdown, slider, and field is named by its exact
   Chinese label and described: what it does, valid values / ranges / defaults inline,
   and any role-/mode-gated visibility.

注意事项 / 提示
   Warnings, gotchas, side effects (e.g. "edits take effect only after 训练/reload"),
   degenerate states.

相关页面
   Cross-references (use Chinese heading labels as :ref: targets — autosectionlabel).
```

Screenshot placeholders use a consistent directive + caption so the later capture pass can
slot images in without prose edits.

---

## 6. Execution plan (phased)

Each page-task = (a) read sources (§3), (b) write `zh_CN` prose to the template (§5),
(c) clean `sphinx-build -D language=zh_CN`, (d) commit.

### Phase 0 — Build hygiene, removals, structure
- Remove all **3D** content (sections, prose, `*_3d.*` / `3d_*.*` screenshots) and the
  `config/detection_config_3d.rst` file + toctree entry.
- Remove `case_study/` (orphan/placeholder).
- Fix existing reST errors in `detection_config_2d.rst` and duplicate-label warnings
  (prefer `autosectionlabel_prefix_document = True` in `conf.py`; verify `:ref:` targets).
- Resolve missing-image references.
- Rewrite `docs/source/index.rst` toctree to the §4 IA.
- Establish a clean `make html-cn` baseline.

### Phase 1 — Introduction & Home
- 系统概览与界面导航 (NEW), 主页 Home (catalog actions, tags, upload, conveyor status,
  recent tasks, task entry points).

### Phase 2 — Create & Teach a Product
- 自动编程向导, CAD 上传与坐标对齐, 标记/对齐 PCB.

### Phase 3 — Template Editor (largest)
- 元件列表与分组, 产品设置 Recipe (含 InspectionSettings/badmark), 元件配置 ComponentInfo
  (含 skip-inspection / must-capture-centered / badmark / AI alignment),
  共线检测, PCB 拼板, 整板检测, 训练与生成参数, 变体/替代元件.

### Phase 4 — Detection tools reference (one page per tool)
- 本体 · 焊点 · IC引脚 · 文本/OCV · 条码 · 桥连 · 颜色 · 胶点 · DIP.

### Phase 5 — Inspection & Report
- 新建检测任务 (演示模式 / A·B 面), 实时检测 Live (含 Board/Sub-board FPY),
  复检 Review, 数据分析报告 worklist (总结/检测结果/不良元件/误判元件).

### Phase 6 — Models & Settings
- 模型管理 Models, 系统设置 (Team / ManageModels / Tags / systemSettings sub-pages,
  excluding online/MES sub-pages).

### Phase 7 — Support, polish, English catalog
- FAQ verify/expand, full `make html-cn` + `make html-en` clean build,
  English `.po` catalog refresh (`make intl-update` + translate fuzzy entries).

### Subagent fan-out
Within a phase, independent pages are written by **parallel subagents**, each handed: the
target route, the component file list, the relevant `src/translations/*.js` files, the §5
template, and the §2 scope rules. One section is completed (built clean, committed) before
the next begins.

---

## 7. Verification

- Each page: clean `sphinx-build -D language=zh_CN` — no new warnings or errors.
- End of each phase: section builds clean and is committed.
- Final: clean `make html-cn` **and** `make html-en`; English catalog refreshed.
- Cross-reference integrity: `:ref:` targets resolve (autosectionlabel keys off the Chinese
  source heading).

---

## 8. Cross-cutting rules

- **Labels are quoted from `src/translations/*.js`** (cn), never paraphrased from memory.
- **Chinese is the source of truth**; English is the translated catalog (final pass).
- **Branding:** neutral "AOI系统" in chrome; keep "DaoAI" product naming in prose.
- **Out-of-scope features** (online/MES/3D) are omitted; if an in-scope page references one,
  note it briefly as "not covered in this manual" rather than documenting it.
- **Effect-timing caveats** are documented where the code shows them (e.g. golden-region /
  component-flag edits require 训练 / `reloadInference` to take effect mid-session).
- Screenshots are placeholders this pass; a later capture pass (headless Edge + Playwright,
  Chinese UI, logged-in profile) fills them in.

---

## 9. Relationship to existing `PLAN.md`

`daoai_pcb_aoi_user_manual/PLAN.md` is a prior **gap-analysis + update** plan (lighter scope,
some features deferred). This design **supersedes** it for the comprehensive rewrite but
**reuses** its FE Coverage Audit (§7 of PLAN.md) and its build-hygiene findings. PLAN.md can
be archived once this design's implementation plan is in place.
