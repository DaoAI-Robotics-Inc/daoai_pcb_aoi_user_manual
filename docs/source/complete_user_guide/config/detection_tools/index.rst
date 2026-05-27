检测工具参考
================

本章逐一介绍每种 2D 检测工具的参数与配置方法。每个工具单独成页。

在阅读各工具参数前，先了解几个贯穿全篇的通用概念：

- **AI 异常分数**：基于 AI 模型的检测会输出一个 0~1 的异常分数；接近 0 表示与正常样本相似，接近 1 表示差异大。可通过统计图表对比正常 / 异常样本的分数分布，选择合适的判定阈值。
- **颜色范围与有效比例（Valid Ratio）**：基于颜色的检测在 ROI 内用 **HSV 颜色范围** 将像素二值化为"有效点"，有效比例定义为 :math:`100 \times \dfrac{\text{有效点数}}{\text{ROI 面积}}`。判定时检查有效比例是否落入设定的 **有效比例范围**。一个 ROI 可配置多组颜色范围，分别独立判定。
- **颜色公式（Color Formula）**：定义如何从像素计算颜色特征。可选 HSV（中心 / 起止色调 + 明度范围），或三色公式（Tricolor，如 ``2B-R-G`` 线性组合，配合 X/Y/Z/A 系数与阈值）。
- **对齐（Alignment）**：部分检测在判定前先将元件图像与标准样本自动对齐，以消除位置偏移带来的误判。
- **启用可视化（Enable Visualization）**：评估后叠加显示二值化 / 检测中间结果，便于调参；因有额外计算开销，建议仅在调试阶段开启。
- **使用共享参数（Use Shared Parameters）**：元件加入封装 / 料号分组后默认与组内共享参数；关闭后可对该实例单独调参，不再继承分组设置。

.. toctree::
   :maxdepth: 1

   mounting
   solder_2d
   lead_2d
   lead_2d_v2
   bridge
   color
   glue_on_pad
   dip_solder
   dip_bridge
   open_solder
   surface_contamination
   text
   barcode
