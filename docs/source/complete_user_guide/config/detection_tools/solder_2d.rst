焊料检测 2D（Solder 2D，基于颜色比例）
==========================================

**此页面的用途**

在焊料 ROI 内用 HSV 颜色范围对像素二值化，计算有效比例并与设定范围比较以判定 OK/NG，适用于 SMD 焊点的焊料检测。

**如何进入**

模板编辑器中绘制对应 ROI 后，在参数面板中配置该工具的参数。

**操作流程**

**核心思路**：在焊料 ROI 内用 **HSV 颜色范围** 对像素二值化，计算 **有效比例** 并与设定范围比较以判定 OK/NG。一个 ROI 可配置多组颜色范围（如蓝通道斜面焊料、红通道平面焊盘），分别独立设阈值。

   .. image:: ../images/solder2d_roi.png
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
- **使用共享参数（Use Shared Parameters）**：开启后，对同一组件下所有同类型特征共用一套参数；关闭后可对单个特征单独调参。

   .. image:: ../images/solder2d_hsv_pick.png
      :scale: 80%
      :alt: HSV颜色范围挑选
   .. image:: ../images/solder2d_color_ranges.png
      :scale: 80%
      :alt: 多颜色范围示例（蓝/红）
   .. image:: ../images/solder2d_binarize.png
      :scale: 80%
      :alt: 颜色范围二值化与比例统计
