IC 引脚检测 2D v2（Lead 2D v2，基于颜色比例）
================================================

**此页面的用途**

将引脚区域划分为焊料、焊盘、引脚尖端三类子区域，分别用颜色范围二值化并计算有效比例，再结合均值/邻域统计对桥接、翘脚等缺陷做鲁棒判定。

**如何进入**

模板编辑器中绘制对应 ROI 后，在参数面板中配置该工具的参数。

**操作流程**

**核心思路**：将引脚区域划分为 **焊料（Solder）/ 焊盘（Pad）/ 引脚尖端（Tip）** 三类子区域，分别用颜色范围二值化并计算有效比例，再结合 **均值 / 邻域** 统计对桥接、翘脚（Lifted Lead）等缺陷做鲁棒判定。

   .. note::
      区域划分：上 = **焊盘区（Pad，橙色框）**，下 = **引脚尖端（Tip，红色框）**，中间 = **焊料区（Solder）**。

   .. image:: ../images/lead2d_v2_layout.png
      :scale: 80%
      :alt: V2区域划分与子ROI

**通用参数**

   .. image:: ../images/lead2d_v2_general.png
      :scale: 100%
      :alt: V2通用参数

- **焊盘长度 (像素)（Pad Length / ext_top）/ 引脚长度 (像素)（Lead Length / ext_bottom）**：沿引脚法线方向向上 / 向下扩展 ROI，使其完整覆盖焊盘与引脚区域。可手动输入或在窗口中拖拽调整。
- **引脚尖端长度 (像素)（Tip Length）**：引脚末端 Tip 子区域的长度。
- **引脚数量（Lead Count）/ 引脚宽度 (mm)（Lead Width）**：在 ROI 内自动均分生成子框并与实体引脚对齐。
- **引脚角度（Lead Angle）**：引脚相对 ROI 的方向角。
- **引脚阈值（Lead Threshold）**：基于每个引脚子 ROI 的 AI 分数判定缺陷。
- **桥接阈值（Bridge Threshold）**：相邻引脚间连锡（短路）的 AI 判定阈值。
- **桥接宽度 (mm)（Bridge Width (mm)）**：相邻引脚间桥接检测带的绝对宽度（毫米）。
- **间隙宽度 (%)（Gap Width）**：相邻引脚间桥接检测带宽度（按间隙百分比），居中裁剪以减少引脚边缘干扰。
- **引脚忽略列表 / 桥接忽略列表**：选择不参与检测的引脚 / 桥接（从左到右编号）。
- **启用可视化（Enable Visualization）**：显示各子区域二值化结果与比例统计（仅建议调试时开启）。
- **使用共享参数（Use Shared Parameters）**：开启后，对同一组件下所有同类型引脚特征共用一套参数；关闭后可对单个特征单独调参。

   .. image:: ../images/lead2d_v2_visualizae.png
      :scale: 60%
      :alt: V2 可视化

**焊料 / 焊盘 / 引脚尖端的颜色范围**

   .. image:: ../images/lead2d_v2_solder.png
      :scale: 80%
      :alt: V2焊料参数

- **焊料颜色范围（Solder Color Range）/ 焊盘颜色范围（Pad Color Range）/ 引脚尖端颜色范围（Tip Color Range）**：分别为三类子区域配置 HSV 或三色颜色公式。
- **焊料 / 焊盘 / 引脚 有效比例范围（Valid Ratio Range）**：各子区域有效比例的 OK 区间。
- **桥接颜色公式（Bridge Color Formula）**：选择用于间隙区连锡检测的颜色公式（如 ``2B-R-G`` 或三色）；选择三色时配置 **三色 X / Y / Z / A** 系数。
- **灵敏度（Sensitivity）**：间隙桥接颜色检测灵敏度（0–1），值越大检测范围越大。
- **桥接颜色范围（Bridge Color Range）/ 桥接有效比例范围（Bridge Valid Ratio Range）**：用于连锡检测。

   .. image:: ../images/lead2d_v2_solder_color.png
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

   .. image:: ../images/lead2d_v2_pad.png
      :scale: 100%
      :alt: V2焊盘参数

   .. image:: ../images/lead2d_v2_tip.png
      :scale: 80%
      :alt: V2 Tip参数
