# Documentation ↔ Software Gap Analysis & Update Plan

**Goal:** Bring the user manual in line with the current AOI software UI and feature set.

**Scope (confirmed):** Everything **except** the online / multi-backend inspection mode and MES integration (Live-Online, Review-Online, multi-backend review devices, MES export) — those are noted as out-of-scope gaps only.

**2D-only (confirmed):** 3D inspection is **out of scope** — *remove all 3D content* (sections, prose, and screenshots) from the docs. 3D appears in 7 files: `detection_config_3d.rst` (whole file), `manual_programming.rst`, `create_product.rst`, `system_management/index.rst`, `quick_start/index.rst`, `faq.rst`, `config/index.rst` (toctree). The many `*_3d.png` images become unused and should be removed too.

**Decisions on open questions:** 2D detection reference = separate later effort (Phase 3, 2D-only); operator feature flags = **deferred** (listed as known gaps, not documented now); screenshots = **recapture all** on each touched page in Chinese; `case_study` = **remove**.

**UPDATE (max-effort pass):** Document **every** standalone page/feature in the frontend (`aoi_pcb_web_client`). The previously-deferred feature flags are now **in scope**. New detection-tool screenshots are captured by drawing ROI boxes on the teach page. Online/multi-backend + MES remain out of scope. See §7 (FE Coverage Audit) and Phase 6.

**Method:** Source language is **Chinese (`zh_CN`)**; the running app is set to **Chinese UI**. Update zh_CN prose + screenshots first; refresh the English `.po` catalog in a later pass. Screenshots are captured via headless Edge + Playwright (the `webapp-testing` skill / persistent logged-in profile). Each page is verified by a clean `sphinx-build`.

**Status of this document:** Gap analysis + plan only. No doc edits beyond Quick Start (already done this session).

---

## 1. How the software is structured today

| Area | Route / location | Notable current UI |
|------|------------------|--------------------|
| Home | `/`, `/home` | Cards: 新建检测任务 / 训练PCBA / 工作列表; 传送带状态; 最近的检测任务; Manage PCBA table (编辑/复制/删除/重命名/导出为文件) |
| Login | `/login` | **Always English** (ignores system language) |
| Teach wizard | `/auto-programming-setup` | 自动编程向导, 5 steps: 基本信息 / 将PCB放置在传送带上 / 获取尺寸 / 拍摄 / 添加CAD(可选) |
| Programming | `/teach` | Left: 设置(Recipe)/元件(Component). Tabs: 标记/对齐PCB · 模板编辑器 · PCB拼板 · 整板检测. Train via **+ 训练** / **生成参数** |
| Worklist | `/worklist` | **数据分析报告**: 总结 / 检测结果 / 不良元件 / 误判元件; PPM/DPU; NG/OK donut; date filters; Review = 查看 |
| Inspection (standalone) | `/inspection/live`, `/inspection/review` | Live: 产品统计/元件统计/检测时长, Board/Sub-board; Review: NG list + defect zoom + feedback |
| Models | `/models` | 数据集 / 训练 tabs; 导出/导入数据集; 查看训练/测试分布; 训练模型 |
| Settings | `/settings` | Sidebar: 团队 / 管理模型 / 系统设置(→ 语言·主机·系统配置·捕获模块·模型更新器·编程默认参数·错误类型翻译·校准·关于·日志) / 登出 |
| **Out of scope** | `/inspection/live-online`, `/inspection/review-online`, `/inspection-detail-export` | Multi-backend online inspection + MES export |

---

## 2. Gap analysis (per documentation page)

Legend — **Drift**: UI/terms/screenshots stale · **Missing**: feature absent · **OK**: largely current.

| Doc page | Verdict | Specific gaps |
|----------|---------|---------------|
| `introduce/quick_start` | **DONE** (1 follow-up) | Recaptured (Chinese) + rewritten this session. Follow-up: remove the 3D `.. note::` and 3D mentions. |
| `features/create_product` | Drift + de-3D | "训练PCBA" not "训练PCB"; wizard is now a single **基本信息** step (name + AI types + 自动编程参数) then conveyor/dimension/capture/CAD; **remove 3D camera-settings/filters content + `*_3d`/`3d_*` images**; screenshots English/old. |
| `features/auto_programming` | Drift | CAD upload is wizard step 5 (添加CAD); verify 字段映射 + 运行自动编程 UI; screenshots old. |
| `features/manual_programming` | Drift + de-3D | Tab renamed **模板编辑器**; element list 元件/料号 toggle; ROI editing tools UI changed; **remove 3D programming examples + `*_3d` images**; many old screenshots. Largest features page. |
| `features/part_library_and_grouping` | Drift | Verify 封装/料号/分组 against current **元件** view + grouping toggles; screenshots old. |
| `features/pcb_array` | Drift | App **PCB拼板** tab has 管理子板模板 / 手动生成拼板 (矩形/多边形) / 自动调整拼板 — doc covers 拼版新建/继承同步/条形码 only; verify + add 手动/自动生成; screenshots old. |
| `config/detection_config_3d` | **REMOVE** | 3D out of scope — delete the file, its `images/`, and the toctree entry in `config/index`. |
| `config/index` + `config/detection_config_2d` | Drift + **build errors** | The big per-tool **2D** detection-parameter reference (body/solder/lead/text/barcode). `detection_config_2d.rst` has reST **ERRORS** (unexpected indentation ~L193/207, title underline ~L82) and duplicate labels. Remove 3D toctree entry. Verify each tool's params vs current UI; recapture tool screenshots. Biggest chunk (Phase 3, later). |
| `config/component_settings` | Drift + Missing | 元件配置 (ComponentInfo panel) — add new operator options: **badmark** 3-option selector, **skip inspection** switch, **must-capture-centered** switch, AI-alignment options; recapture. |
| `inspection/index` | Drift | Worklist section describes the old list — now **数据分析报告** (总结/检测结果/不良元件/误判元件). New-task dialog has **以演示模式运行**. Add Board/Sub-board FPY toggle. Recapture worklist/live/review/defect screenshots. |
| `system_management/index` | Drift + Missing + de-3D | Settings reorganized into a **sidebar** (团队/管理模型/系统设置→…); recapture all settings screenshots; **remove 3D/sensor-3D bits**. **Missing**: 错误类型翻译 (Error Type Translation) and 管理模型 / Models. |
| `support/faq` | Verify + de-3D | Confirm the 6 Q&As still accurate; **remove 3D mentions**; the two referenced images are fine. |
| `case_study/index` | **REMOVE** | Orphan (build warning), empty/placeholder — delete the page + image folder. |

---

## 3. Missing pages / topics (no current coverage)

1. **Model management** (`/models` + Settings → 管理模型): datasets, train/upload, import/export, train-test distribution, set-default/rename/delete models.
2. **Error Type Translation** (Settings → 错误类型翻译): 错误类型 / 英文标签 / 中文标签 / MES 厂商代码 mapping.
3. **Whole Board Inspection** (整板检测 programming tab).
4. **Operator feature flags** — **DEFERRED** (known gaps, not documented in this effort): badmark / bad-board detection · per-instance skip-inspection · must-capture-centered · sub-board first-pass yield (Board/Sub-board toggle).

---

## 4. Cross-cutting issues (fix once, apply everywhere)

- **Screenshots:** Essentially every screenshot outside Quick Start is English-UI / old. **Recapture ALL** screenshots on each touched page in **Chinese UI** (app already set to Chinese; login page stays English by design).
- **Remove 3D:** strip all 3D sections/prose and delete the `*_3d.png` / `3d_*.png` images across every page (see scope note).
- **Branding:** App is neutral "AOI系统"; keep "DaoAI" product naming in prose.
- **Build hygiene (currently 17 warnings + 2 errors):**
  - `detection_config_2d.rst` reST **ERRORS** (unexpected indentation) — fix.
  - Duplicate `autosectionlabel` labels (创建产品, 本体工具, 文本工具, 条形码工具, 电容、电阻, …) — disambiguate or set `autosectionlabel_prefix_document = True`.
  - Missing image `complete_user_guide/inspection/images/program_page.png` — recapture or remove ref.
  - `case_study/index` orphan — add to toctree or drop.
- **Cross-references:** `autosectionlabel` keys `:ref:` targets off the **source (Chinese) heading** — keep Chinese labels inside `:ref:` even when prose is English (learned during Quick Start).
- **English catalog:** zh_CN edits flip the matching `en` `.po` entries to fuzzy; refresh `en` in a dedicated later pass (`make intl-update` + translate).

---

## 5. Execution plan (phased, prioritized)

Each page-task = **(a)** recapture the needed Chinese screenshots, **(b)** rewrite/verify prose against current UI, **(c)** `sphinx-build -D language=zh_CN` clean, **(d)** commit. Phases are ordered by operator impact.

### Phase 0 — Build hygiene, 3D removal & cleanup (do first)
- [ ] **Delete `case_study/`** (page + images); remove any references.
- [ ] **Delete `config/detection_config_3d.rst`** + its `images/`; remove the 3D toctree entry in `config/index.rst`.
- [ ] **De-3D pass** across `quick_start`, `create_product`, `manual_programming`, `system_management`, `faq` — strip 3D sections/prose; delete now-unused `*_3d.png` / `3d_*.png` images.
- [ ] Fix `detection_config_2d.rst` reST indentation errors.
- [ ] Resolve duplicate-label warnings (prefer `autosectionlabel_prefix_document = True` in `conf.py`; verify no `:ref:` breaks).
- [ ] Resolve the missing `program_page.png` (recapture or remove ref).
- [ ] Confirm clean `make html-cn` baseline before content edits.

### Phase 1 — Core operator workflow (highest impact)
- [ ] `inspection/index` — rewrite worklist section to **数据分析报告**; add 以演示模式运行, Board/Sub-board FPY; recapture live/review/defect/worklist screens.
- [ ] `features/create_product` — align to 训练PCBA + 基本信息 wizard; recapture.
- [ ] `features/auto_programming` — verify CAD step + 字段映射; recapture.

### Phase 2 — Programming & component configuration
- [ ] `features/manual_programming` — 模板编辑器 + ROI editing tools; recapture (large).
- [ ] `features/part_library_and_grouping` — 元件/料号/分组; recapture.
- [ ] `features/pcb_array` — add 手动生成拼板 (矩形/多边形) / 自动调整拼板 / 管理子板模板; recapture.
- [ ] `config/component_settings` — add badmark / skip-inspection / must-capture-centered / AI-alignment; recapture.

### Phase 3 — 2D detection-parameter reference (largest; separate later effort)
- [ ] `config/index` + `detection_config_2d` — per-tool **2D** param audit (body/solder/lead/text/barcode) vs current UI; recapture tool screenshots. Consider splitting per-tool tasks. (3D already removed in Phase 0.)

### Phase 4 — System management & new topic pages
- [ ] `system_management/index` — recapture sidebar-based settings; add **错误类型翻译** + **管理模型/Models** sections.
- [ ] New page: **Model management** (`/models`) — full how-to: datasets, training a model, import/export datasets, viewing train/test distribution, set-default / rename / delete, upload model.
- [ ] New section/page: **整板检测** (Whole Board Inspection).
- [ ] _(Deferred)_ operator feature flags (badmark / skip / must-center / sub-board FPY) — not in this effort.

### Phase 5 — FAQ, polish, English catalog
- [ ] `support/faq` — verify accuracy; add new FAQs if warranted (e.g., demo mode, sub-board FPY).
- [ ] Full `make html-cn` + `make html-en` clean build.
- [ ] **English catalog refresh** (`make intl-update`, translate fuzzy entries) across all updated pages.

---

## 6. Decisions (resolved)

- **case_study** → remove entirely (Phase 0).
- **Operator feature flags** → deferred (known gaps, not documented now).
- **Detection-config reference** → 2D-only, separate later effort (Phase 3, after operator pages).
- **3D** → removed doc-wide (Phase 0 de-3D pass + delete `detection_config_3d`).
- **Screenshots** → recapture all on each touched page, Chinese UI.

- **Models / model management** → **full how-to** (train a model, dataset import/export, train-test distribution, set-default/rename/delete, upload) — dedicated page in Phase 4.

All open questions resolved — the plan is ready to execute.

---

## 7. FE Coverage Audit (every page/feature in `aoi_pcb_web_client`)

Legend — **Done**: documented & current · **Thin**: mentioned but incomplete · **GAP**: undocumented · **OOS**: out of scope (online/multi-backend/MES).

### Routes / pages
| FE page / route | Doc | Status |
|-----------------|-----|--------|
| `Login`, `LandingVideo`, `SystemInitializing` | quick_start | Done (login); splash pages trivial |
| `Home` | quick_start (home shot) | **Thin** → Home features undocumented (below) |
| `MultiBackendHome`, `inspection/*Online`, `ReviewDeviceConveyorPicker` | — | **OOS** |
| `MES`, `MES/InspectionDetailExport`, MesAlarm | system_management (MES export path) | **OOS** (only export-path config kept) |
| `autoProgramming` (+`uploadCAD`) | create_product, auto_programming | Done |
| `inspection/Live`, `inspection/Review` | inspection | Done |
| `models` | system_management/models | Done |
| `settings` (+`systemSettings`) | system_management | Done |
| `teach/components/templateEditor` | manual_programming, component_settings, detection_config_2d, part_library | Done (flags pending below) |
| `teach/components/PCBArray` | pcb_array | Done |
| `teach/recipe` (设置 tab: ConveyorSetup, PCBDetail, PCBDimension, fullCapture, **InspectionSettings**) | create_product (partial) | **GAP** → Recipe/产品设置 + badmark recipe config |
| `teach` Whole Board Inspection tab | manual_programming (note) | **Thin** → expand |
| `worklist` (Data Analysis Report) | inspection | Done |

### Features / modals → GAP items to document
| Feature (FE source) | Action |
|---------------------|--------|
| **Component feature flags** — badmark / skip-inspection / must-capture-centered / AI alignment (`ComponentInfo.jsx`) | Add to `component_settings` |
| **Recipe → InspectionSettings** — badmark combine logic, recipe-level inspection config | New section in `manual_programming` (or recipe) |
| **Sub-board FPY** + badmark in live/worklist (`fpyMode*`, `subboardFPY`, `badmarkVerdictActive`) | Expand `inspection` |
| **AI Detect ROI** (`AIDetectROI.jsx`, `GenerateROIComfirmation`) | Add to `manual_programming` |
| **Home page** — tags (add/remove), Upload PCBA `.zip`, Copy / Export product, Recent Inspection Task, Conveyor status / Reset Device | New `Home/主页` section |
| **Detection tools w/o screenshots** — bridge, color, glue-on-pad, DIP solder, DIP bridge, open solder, surface contamination, text OCV | Draw ROI boxes on teach page → capture param panels for `detection_config_2d` |
| Private library (`AddFromLibrary`), alternative/substitute component | Done (manual_programming / inspection) — verify |

---

## Phase 6 — FE-complete coverage (max-effort pass)
- [ ] **detection_config_2d screenshots** — draw a box for each new tool on the teach page; capture bridge / color / glue-on-pad / DIP / open-solder / surface-contamination / text-OCV param panels.
- [ ] **component_settings** — document badmark, skip-inspection, must-capture-centered, AI-alignment flags (Chinese labels from `ComponentInfo`).
- [ ] **Recipe / 产品设置** — document the 设置 tab (re-access conveyor/PCB detail/dimension/capture) + **InspectionSettings** (badmark combine logic, recipe-level config).
- [ ] **inspection** — expand sub-board FPY (Board/Sub-board) + badmark verdict behavior in live + Data Analysis Report.
- [ ] **Home / 主页** — new section: product list actions (编辑/复制/删除/重命名/导出为文件), tags, Upload PCBA `.zip`, Recent Inspection Task, 传送带状态 / 重置轨道.
- [ ] **Whole Board Inspection** — expand the brief note into a proper section.
- [ ] **AI Detect ROI** — document AI-assisted ROI generation in manual_programming.
- [ ] Full build (zh_CN + en) clean + refresh en catalog.
