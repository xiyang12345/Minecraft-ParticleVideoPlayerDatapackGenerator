# Minecraft 粒子视频播放器

这个项目是一个将Premiere Pro逐帧导出的视频序列在Minecraft中通过粒子效果播放的工具。它允许你在Minecraft游戏中创建动态的视频播放效果，将静态图像序列转换为游戏内的动画体验。

## 系统要求

- **游戏环境**:
  - Minecraft 1.16.5 fabirc
  - Java8（必须使用Java8）
  - 必须安装 [ColorBlock模组](https://pan.baidu.com/s/1pFi82Wx7vJ5bnQTE4p9cIA?pwd=f3jx)

## 使用教程

🎬 视频教程

点击下方图片观看详细使用教程：

[![MC粒子视频教程封面](https://i1.hdslb.com/bfs/archive/1026d0fd91df1680c6b602cfe1fbdab6efd1c510.jpg)](https://www.bilibili.com/video/BV1psthzyETk/)

### 1. 准备视频帧
1. 在Premiere Pro中导出视频为PNG序列
2. 将所有帧图片放入一个文件夹中
3. 确保文件名包含数字序号（如test_001.png, test_002.png）

### 2. 运行脚本（.exe直接双击运行）
```bash
python mc粒子视频数据包生成器.py
```

### 3. 配置参数
1. 输入粒子效果坐标（格式：x y z）
2. 选择包含图片序列的文件夹
3. 点击"生成数据包"按钮

### 4. 在Minecraft中使用
1. 将生成的`particle_datapack.zip`放入存档的`datapacks`文件夹
2. 在游戏中输入`/reload`重新加载数据包
3. 输入`/function particle:start`开始播放

## 🔬 实现原理

### 核心技术：ColorBlock模组的粒子指令

ColorBlock模组提供了一条强大的粒子指令：
```minecraft
particleex image <颗粒> <坐标> <路径> [比例] [x轴旋转] [y轴旋转] [z轴旋转] [翻转] [DPB] [速度] [寿命] [速度表达式] [计算间隔] [组]
```

### 核心工作流程

1. **视频帧导出**：
   - 从Premiere Pro导出视频为图像序列（如test_0001.png, test_0002.png等）
   
2. **指令生成**：
   ```python
   for frame in frames:
       command = f"particleex image end_rod {coords} \"{frame}\" 0.1 0 0 0 not 10 0 0 0 1 null"
   ```
   - 自动替换坐标和图片路径
   - 保持其他参数优化设置

3. **时间序列控制**：
   - 每帧指令后添加1tick延迟：
   ```minecraft
   schedule function particle:show_{next_frame} 1t
   ```

4. **数据包封装**：
   - 创建完整的Minecraft数据包结构
   - 包含启动函数和帧序列函数

## 常见问题

**Q: 粒子效果不显示怎么办？**  
A: 请确保：
1. 已安装ColorBlock模组
2. 游戏版本为1.16.5 fabirc
3. 数据包已正确加载（/reload）

**Q: 图片序列播放顺序错误？**  
A: 确保文件名包含连续数字序号，如：
- test_001.png
- test_002.png
- test_003.png

**Q: 粒子效果卡顿？**  
A: 减少图片分辨率或减少帧数可以提高性能

## 下载链接

- [ColorBlock模组下载（下载1.16.5 支持fabirc）](https://pan.baidu.com/s/1pFi82Wx7vJ5bnQTE4p9cIA?pwd=f3jx)
- [最新版本发布](https://github.com/xiyang12345/Minecraft-ParticleVideoPlayerDatapackGenerator/releases/tag/Minecraft)

---
