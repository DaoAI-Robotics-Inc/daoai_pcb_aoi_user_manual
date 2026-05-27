检测参数 2D
=================

本章节详细介绍 2D 检测工具（检测项）及其参数含义。每个元件可包含一个或多个检测项；在 **模板编辑器** 中选中元件后，可在右侧面板查看并编辑各检测项的参数。

   .. image:: images/params_overview.png
      :scale: 180%
      :alt: 检测参数总览

.. contents::
   :local:
   :depth: 2

通用概念
---------------------

在阅读各工具参数前，先了解几个贯穿全篇的通用概念：

- **AI 异常分数**：基于 AI 模型的检测会输出一个 0~1 的异常分数；接近 0 表示与正常样本相似，接近 1 表示差异大。可通过统计图表对比正常 / 异常样本的分数分布，选择合适的判定阈值。
- **颜色范围与有效比例（Valid Ratio）**：基于颜色的检测在 ROI 内用 **HSV 颜色范围** 将像素二值化为“有效点”，有效比例定义为 :math:`100 \times \dfrac{\text{有效点数}}{\text{ROI 面积}}`。判定时检查有效比例是否落入设定的 **有效比例范围**。一个 ROI 可配置多组颜色范围，分别独立判定。
- **颜色公式（Color Formula）**：定义如何从像素计算颜色特征。可选 HSV（中心 / 起止色调 + 明度范围），或三色公式（Tricolor，如 ``2B-R-G`` 线性组合，配合 X/Y/Z/A 系数与阈值）。
- **对齐（Alignment）**：部分检测在判定前先将元件图像与标准样本自动对齐，以消除位置偏移带来的误判。
- **启用可视化（Enable Visualization）**：评估后叠加显示二值化 / 检测中间结果，便于调参；因有额外计算开销，建议仅在调试阶段开启。
- **使用共享参数（Use Shared Parameters）**：元件加入封装 / 料号分组后默认与组内共享参数；关闭后可对该实例单独调参，不再继承分组设置。

1. 本体检测（Mounting）
---------------------------

**用途**：检测元件本体的贴装缺陷，包括缺件、错件、损件、偏移、旋转与极性等。ROI 应覆盖元器件主体表面。

   .. image:: images/tool_body_roi.png
      :scale: 50%
      :alt: 本体检测ROI示例

**位置与姿态**

- **旋转角度 (°)（Max Rotation Angle）**：元件本体相对标准姿态的角度偏差；当偏差超过该阈值时判定为 NG。
- **X 偏移 (mm)（Shift X）/ Y 偏移 (mm)（Shift Y）**：样本元件与标准元件本体的平移偏差；超过阈值判 NG。

**缺陷检测（AI）**

- **常规检测（Significant Defect Check）**：对元件本体的明显缺陷（缺件、错件、方向严重错误等）进行 AI 异常分数判定。

   .. image:: images/tool_body_ai.png
      :scale: 60%
      :alt: 本体AI分数分布示例
   .. image:: images/tool_body_ai2.png
      :scale: 70%
      :alt: 本体AI分数分布示例2

- **损件检测（Subtle Defect Check）**：针对本体的破损、缺口等细微异常；检测前先将元件图像与标准样本自动对齐，再以 AI 异常分数判定，避免位置偏移导致误判。

   .. image:: images/tool_body_align.png
      :scale: 120%
      :alt: 损件检测
   .. image:: images/tool_body_align_inference.png
      :scale: 60%
      :alt: 本体对齐后检测
   .. image:: images/tool_body_align_inference2.png
      :scale: 80%
      :alt: 本体对齐后检测2

- **缺件检测（Missing Check）**：判定该位置是否缺少元件。
- **增强缺件检测（Enhanced Missing Check）**：利用对位结果在元件疑似缺失时提前告警；属实验性功能，当对位误判导致误报时可关闭。

**极性检测（AI，对齐后）**

- **极性检测（Polarity Check）**：判断元件极性方向是否正确。检测前先对齐，并在 **极性 ROI** 区域内学习与判定极性特征，以识别极性反转。判定方式同样基于 AI 异常分数。
- **极性检测灵敏度（Polarity Sensitivity）**：调节极性判定的灵敏度；灵敏度越高越容易报出极性异常。
- **极性 ROI（Polarity ROI）**：点击 *设置 ROI* 或在显示窗口中直接拖拽，框选用于极性判定的局部区域（通常为极性标识所在处）。

   .. image:: images/tool_body_polarity.png
      :scale: 50%
      :alt: 极性检测框
   .. image:: images/tool_body_polarity_inference.png
      :scale: 60%
      :alt: 极性检测
   .. image:: images/tool_body_polarity_inference2.png
      :scale: 70%
      :alt: 极性检测2

**其它**

- **启用遮罩（Enable Mask）**：对含有不固定字符 / 图案的区域进行遮蔽，避免其影响 AI 检测。

   .. image:: images/tool_body_mask.png
      :scale: 50%
      :alt: 遮罩

2. 焊料检测 2D（Solder 2D，基于颜色比例）
--------------------------------------------------

**核心思路**：在焊料 ROI 内用 **HSV 颜色范围** 对像素二值化，计算 **有效比例** 并与设定范围比较以判定 OK/NG。一个 ROI 可配置多组颜色范围（如蓝通道斜面焊料、红通道平面焊盘），分别独立设阈值。

   .. image:: images/solder2d_roi.png
      :scale: 50%
      :alt: 焊料2D ROI

**参数说明**

- **颜色公式（Color Formula）**：选择 HSV 或三色（Tricolor）公式；选择三色时配置 **三色 X / Y / Z / A** 系数。
- **中心色调（Center Hue）/ 中心饱和度（Center Saturation）**：HSV 模式下色相基准点（位于色盘内部）。
- **起始色调（Start Hue）/ 终止色调（End Hue）**：色盘圆环边缘的两点，与中心点共同构成扇形有效色相范围。
- **起始明度（Start Value）/ 终止明度（End Value）**：限定有效像素的明度区间。
- **有效比例范围（Valid Ratio Ranges）**：每组颜色范围对应的有效比例上下限；落入范围内判 OK。
- **有效比例列表（Valid Ratio List）**：评估样本得到的各 ROI 有效比例统计，辅助设定合理范围。
- **启用可视化（Enable Visualization）**：显示二值化 Mask 与比例统计（仅建议调试时开启）。

   .. image:: images/solder2d_hsv_pick.png
      :scale: 80%
      :alt: HSV颜色范围挑选
   .. image:: images/solder2d_color_ranges.png
      :scale: 80%
      :alt: 多颜色范围示例（蓝/红）
   .. image:: images/solder2d_binarize.png
      :scale: 80%
      :alt: 颜色范围二值化与比例统计

3. IC 引脚检测 2D（Lead 2D，AI）
------------------------------------

**用途**：在引脚阵列上自动生成引脚子框，结合 AI 缺陷检测识别桥接、缺焊、虚焊、少锡等。检测框上的三角箭头指向引脚 *外侧*。

   .. image:: images/lead2d_ai_overview.png
      :scale: 60%
      :alt: 引脚2D(AI)示意

**参数说明**

- **引脚数量（Lead Count）**：在 ROI 内自动均分生成对应个数的子 ROI。
- **引脚宽度 (mm)（Lead Width）**：匹配实际引脚宽度，使子 ROI 与实体引脚对齐。
- **引脚角度（Lead Angle）**：引脚相对 ROI 的方向角。
- **引脚阈值（Lead Threshold）**：基于每个引脚子 ROI 的 AI 分数判定缺陷。
- **桥接阈值（Bridge Threshold）**：相邻引脚间连锡（短路）的判定阈值。
- **桥接宽度 (mm)（Bridge Width）/ 间隙宽度 (%)（Gap Width）**：定义相邻引脚间桥接检测带的宽度；可按毫米或按引脚间隙百分比设定，居中裁剪以避免引脚边缘干扰。
- **引脚忽略列表（Lead Ignore List）/ 桥接忽略列表（Bridge Ignore List）**：选择不参与检测的引脚 / 桥接（从左到右编号，注意特征框角度）。
- **启用可视化（Enable Visualization）**：显示引脚子框与检测结果。

   .. image:: images/lead2d_ai_inference.png
      :scale: 80%
      :alt: 引脚2D AI检测示意

4. IC 引脚检测 2D v2（Lead 2D v2，基于颜色比例）
------------------------------------------------------

**核心思路**：将引脚区域划分为 **焊料（Solder）/ 焊盘（Pad）/ 引脚尖端（Tip）** 三类子区域，分别用颜色范围二值化并计算有效比例，再结合 **均值 / 邻域** 统计对桥接、翘脚（Lifted Lead）等缺陷做鲁棒判定。

   .. note::
      区域划分：上 = **焊盘区（Pad，橙色框）**，下 = **引脚尖端（Tip，红色框）**，中间 = **焊料区（Solder）**。

   .. image:: images/lead2d_v2_layout.png
      :scale: 80%
      :alt: V2区域划分与子ROI

**通用参数**

   .. image:: images/lead2d_v2_general.png
      :scale: 100%
      :alt: V2通用参数

- **焊盘长度 (像素)（Pad Length / ext_top）/ 引脚长度 (像素)（Lead Length / ext_bottom）**：沿引脚法线方向向上 / 向下扩展 ROI，使其完整覆盖焊盘与引脚区域。可手动输入或在窗口中拖拽调整。
- **引脚尖端长度 (像素)（Tip Length）**：引脚末端 Tip 子区域的长度。
- **引脚数量（Lead Count）/ 引脚宽度 (mm)（Lead Width）**：在 ROI 内自动均分生成子框并与实体引脚对齐。
- **间隙宽度 (%)（Gap Width）**：相邻引脚间桥接检测带宽度（按间隙百分比），居中裁剪以减少引脚边缘干扰。
- **引脚忽略列表 / 桥接忽略列表**：选择不参与检测的引脚 / 桥接（从左到右编号）。
- **启用可视化（Enable Visualization）**：显示各子区域二值化结果与比例统计（仅建议调试时开启）。

   .. image:: images/lead2d_v2_visualizae.png
      :scale: 60%
      :alt: V2 可视化

**焊料 / 焊盘 / 引脚尖端的颜色范围**

   .. image:: images/lead2d_v2_solder.png
      :scale: 80%
      :alt: V2焊料参数

- **焊料颜色范围（Solder Color Range）/ 焊盘颜色范围（Pad Color Range）/ 引脚尖端颜色范围（Tip Color Range）**：分别为三类子区域配置 HSV 或三色颜色公式。
- **焊料 / 焊盘 / 引脚 有效比例范围（Valid Ratio Range）**：各子区域有效比例的 OK 区间。
- **桥接颜色范围（Bridge Color Range）/ 桥接有效比例范围（Bridge Valid Ratio Range）**：用于连锡检测。

   .. image:: images/lead2d_v2_solder_color.png
      :scale: 80%
      :alt: V2焊料色盘

**高级设置（Enable Advanced Settings）**

开启 **启用高级设置（enable_advanced_solder_criteria）** 后，当某引脚的有效比例未落入其 **有效比例范围** 时，会进入二次判定，结合下列阈值降低误报：

- **焊料平均阈值（Solder Mean Threshold）**：比较该引脚焊料有效比例与所有引脚的平均值；差异大于阈值视为正常。
- **焊料邻域阈值（Solder Neighbor Threshold）**：比较该引脚焊料有效比例与相邻引脚；差异大于阈值视为正常。
- **焊盘平均阈值（Pad Mean Threshold）/ 焊盘邻域阈值（Pad Neighbor Threshold）**：对焊盘区做同样的均值 / 邻域比较，用于翘脚判定。
- **最小焊料焊盘差异（Min Solder Pad Difference）**：比较同一引脚的焊料区与焊盘区；正常时焊料 > 焊盘，差距过小说明焊盘暴露、焊料不足，可能翘脚。
- **引脚尖端有效比例范围（Tip Valid Ratio Range）**：引脚尖端区域的 OK 比例区间。
- **引脚平均上限阈值（Tip Mean Upper Threshold）/ 平均下限阈值（Tip Mean Lower Threshold）**：所有引脚尖端平均有效比例高于上限或低于下限时判异常。

   .. note::
      判定流程：先检查有效比例是否在 **有效比例范围** 内，若在范围内 ⇒ OK；若超出，则进入二次判定——满足 **平均阈值** 或 **邻域阈值** 任一条件 ⇒ OK，两者都不满足 ⇒ NG。

   .. image:: images/lead2d_v2_pad.png
      :scale: 100%
      :alt: V2焊盘参数
   .. image:: images/lead2d_v2_tip.png
      :scale: 80%
      :alt: V2 Tip参数

5. 桥接检测（Bridge）
---------------------------

**用途**：独立检测相邻引脚 / 焊点之间的连锡（短路）。

**参数说明**

- **桥接颜色公式（Bridge Color Formula）**：选择用于识别连锡的颜色公式（如 ``2B-R-G``）；选择三色时配置 **三色 X / Y / Z / A**。
- **值范围（Value Range）**：``2B-R-G`` 等公式的阈值范围（0–100），落入该范围的像素被检出。
- **灵敏度（Sensitivity）**：桥接颜色检测灵敏度（0–1），值越大检测范围越大。
- **启用可视化（Enable Visualization）**：显示桥接检测中间结果。

6. 颜色检测（Color）
---------------------------

**用途**：基于颜色比例校验目标区域颜色特征（如带色标识、色环等）。

- **颜色有效比例范围（Valid Color Ratio Ranges）**：配置一组或多组颜色范围及其有效比例区间，落入范围内判 OK。

7. 焊盘沾胶检测（Glue on Pad）
--------------------------------------

**用途**：检测焊盘上是否存在点胶 / 残胶等，通过颜色比例判定。

- **有效比例范围（Valid Ratio Ranges）**：胶体颜色范围对应的有效比例区间。

8. DIP 焊点检测（DIP Solder）
--------------------------------------

**用途**：针对插装（DIP）器件的焊点检测，可结合颜色范围与自定义模型。

**参数说明**

- **DIP 类型（DIP Type）/ 子类型（Sub Type）**：选择 DIP 焊点形态类别。
- **自定义模型（Custom Model）**：选用为该焊点类型训练的自定义分类模型。
- **置信度阈值（Confidence Threshold）**：模型判定的置信度门限。
- **焊点数量（Solder Count）/ 焊点宽度 (mm)（Solder Width）**：在 ROI 内均分生成焊点子框。
- **桥接宽度 (%)（Bridge Width）**：相邻焊点连锡检测带宽度。
- **启用焊点颜色范围检测（Enable Solder Color Range Criteria）**：开启后按颜色范围辅助判定。
- **焊点颜色中心色调 / 饱和度、起止色调、起止明度**：HSV 焊点颜色范围定义。
- **焊点颜色有效比率范围（Solder Color Valid Ratio Range）**：焊点颜色有效比例的 OK 区间。

9. DIP 桥接检测（DIP Bridge）
--------------------------------------

**用途**：检测 DIP 器件相邻引脚 / 焊点之间的连锡。

- **桥接颜色公式（Bridge Color Formula）/ 灵敏度（Sensitivity）**：连锡颜色识别公式与灵敏度。
- **桥接有效比率范围（Bridge Valid Ratio Range）**：连锡有效比例 OK 区间。
- **桥接宽度 (%)（Bridge Width）**：桥接检测带宽度。
- **焊点数量（Solder Count）/ 焊点宽度 (mm)（Solder Width）**：焊点子框划分。
- **启用可视化（Enable Visualization）**。

10. 开焊检测（Open Solder）
--------------------------------------

**用途**：检测焊点开路 / 未连接（虚焊、空焊）等缺陷。

- **启用开焊检测（Enable Open Solder Inspection）**：开关该检测项。
- **置信度阈值（Confidence Threshold）**：模型判定门限。
- **自定义模型（Custom Model）/ 自定义模型路径（Custom Model Path）**：选用自定义训练模型。

11. 表面污染检测（Surface Contamination）
--------------------------------------------------

**用途**：检测元件 / 焊盘表面的污渍、异物、残留等污染缺陷。通常作为开关型检测项启用，并基于 AI 模型给出判定；具体可检范围随模型与产品配置而定。

12. 文本检测（Text / OCR · OCV）
--------------------------------------

**用途**：识别并校验检测框内文本（丝印、字符、批次 / 日期等）。检测框上的三角箭头表示文本阅读方向，应与实际字符方向一致。同时支持 OCR（识别字符内容）与 OCV（与参考图像比对）两种方式。

   .. image:: images/text_tool.png
      :scale: 70%
      :alt: 文本工具参数

**参数说明**

- **期望文本（Expected Text）/ 期望文本 (反向)（Expected Text Reverse）**：目标字符串；反向用于 180° 方向。
- **启用 OCR（Enable OCR）**：识别检测框内字符内容并与期望文本比对。
- **启用 OCV（Enable OCV）**：将检测框与 **OCV 参考（OCV References）** 图像比对，输出 **OCV 最佳匹配分数（OCV Best Match Score）**。
- **OCV 接受阈值（OCV Acceptance Threshold）**：提高阈值可降低漏报（false negative）。
- **OCR/OCV 通过条件（Pass Condition）**：可选 **OCR 与 OCV 均须通过** 或 **OCR 或 OCV 任一通过**。
- **最大不匹配字符数（Max Mismatch Count）**：与期望文本比较时允许的最大不匹配字符数（仅当识别与参考长度相同时才显示不匹配计数）。
- **模糊模式（Blur Mode）**：启用后形状相似的字符（如 ``1`` / ``l``）视为正确，可通过反馈加入模糊表。
- **双向检测（Bidirectional Inspection）**：进行 0° / 180° 两次识别，任一方向匹配即判 OK。
- **启用旋转（Enable Rotation）/ 自动搜索文本位置（Auto search text location）**：当文本在框内位置有偏移时，加强搜索以提升识别稳定性。

13. 条形码检测（Barcode）
---------------------------

**用途**：识别一维条码 / 二维码，并将读出的序列号用于与历史检测记录关联（如 PCB 唯一序列号），支持批次追溯与按子板归档。

   .. image:: images/barcode_tool.png
      :scale: 80%
      :alt: 条码工具参数

框选包含条码的区域即可；系统在检测时自动读取并记录条码内容，无需额外阈值参数。
