本体检测（Mounting）
=======================

**此页面的用途**

检测元件本体的贴装缺陷，包括缺件、错件、损件、偏移、旋转与极性等。ROI 应覆盖元器件主体表面。

**如何进入**

模板编辑器中绘制对应 ROI 后，在参数面板中配置该工具的参数。

**操作流程**

   .. image:: ../images/tool_body_roi.png
      :scale: 50%
      :alt: 本体检测ROI示例

**位置与姿态**

- **旋转角度 (°)（Max Rotation Angle）**：元件本体相对标准姿态的角度偏差；当偏差超过该阈值时判定为 NG。
- **X 偏移 (mm)（Shift X）/ Y 偏移 (mm)（Shift Y）**：样本元件与标准元件本体的平移偏差；超过阈值判 NG。

**缺陷检测（AI）**

- **常规检测（Significant Defect Check）**：对元件本体的明显缺陷（缺件、错件、方向严重错误等）进行 AI 异常分数判定。

   .. image:: ../images/tool_body_ai.png
      :scale: 60%
      :alt: 本体AI分数分布示例

   .. image:: ../images/tool_body_ai2.png
      :scale: 70%
      :alt: 本体AI分数分布示例2

- **损件检测（Subtle Defect Check）**：针对本体的破损、缺口等细微异常；检测前先将元件图像与标准样本自动对齐，再以 AI 异常分数判定，避免位置偏移导致误判。

   .. image:: ../images/tool_body_align.png
      :scale: 120%
      :alt: 损件检测

   .. image:: ../images/tool_body_align_inference.png
      :scale: 60%
      :alt: 本体对齐后检测

   .. image:: ../images/tool_body_align_inference2.png
      :scale: 80%
      :alt: 本体对齐后检测2

- **缺件检测（Missing Check）**：判定该位置是否缺少元件。
- **增强缺件检测（Enhanced Missing Check）**：利用对位结果在元件疑似缺失时提前告警；属实验性功能，当对位误判导致误报时可关闭。

**极性检测（AI，对齐后）**

- **极性检测（Polarity Check）**：判断元件极性方向是否正确。检测前先对齐，并在 **极性 ROI** 区域内学习与判定极性特征，以识别极性反转。判定方式同样基于 AI 异常分数。
- **极性检测灵敏度（Polarity Sensitivity）**：调节极性判定的灵敏度；灵敏度越高越容易报出极性异常。
- **极性 ROI（Polarity ROI）**：点击 *设置 ROI* 或在显示窗口中直接拖拽，框选用于极性判定的局部区域（通常为极性标识所在处）。

   .. image:: ../images/tool_body_polarity.png
      :scale: 50%
      :alt: 极性检测框

   .. image:: ../images/tool_body_polarity_inference.png
      :scale: 60%
      :alt: 极性检测

   .. image:: ../images/tool_body_polarity_inference2.png
      :scale: 70%
      :alt: 极性检测2

**其它**

- **启用遮罩（Enable Mask）**：对含有不固定字符 / 图案的区域进行遮蔽，避免其影响 AI 检测。

   .. image:: ../images/tool_body_mask.png
      :scale: 50%
      :alt: 遮罩
