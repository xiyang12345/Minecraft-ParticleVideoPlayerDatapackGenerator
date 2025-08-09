# Minecraft 粒子视频播放器

这个项目是一个将Premiere Pro逐帧导出的视频序列在Minecraft中通过粒子效果播放的工具。它允许你在Minecraft游戏中创建动态的视频播放效果，将静态图像序列转换为游戏内的动画体验。

## 系统要求

- **游戏环境**:
  - Minecraft 1.16.5
  - Java8（必须使用Java8）
  - 必须安装 [ColorBlock模组](https://pan.baidu.com/s/1pFi82Wx7vJ5bnQTE4p9cIA?pwd=f3jx)
  
- **软件环境**:
  - Python 3.x
  - 标准库（无需额外安装）

## 使用教程

### 1. 准备视频帧
1. 在Premiere Pro中导出视频为PNG序列
2. 将所有帧图片放入一个文件夹中
3. 确保文件名包含数字序号（如frame_001.png, frame_002.png）

### 2. 运行脚本
```bash
python particle_video_player.py
```

### 3. 配置参数
1. 输入粒子效果坐标（格式：x y z）
2. 选择包含图片序列的文件夹
3. 点击"生成数据包"按钮

### 4. 在Minecraft中使用
1. 将生成的`particle_datapack.zip`放入存档的`datapacks`文件夹
2. 在游戏中输入`/reload`重新加载数据包
3. 输入`/function particle:start`开始播放

## 常见问题

**Q: 粒子效果不显示怎么办？**  
A: 请确保：
1. 已安装ColorBlock模组
2. 游戏版本为1.16.5
3. 数据包已正确加载（/reload）

**Q: 图片序列播放顺序错误？**  
A: 确保文件名包含连续数字序号，如：
- frame_001.png
- frame_002.png
- frame_003.png

**Q: 粒子效果卡顿？**  
A: 减少图片分辨率或减少帧数可以提高性能

## 下载链接

- [ColorBlock模组下载](https://pan.baidu.com/s/1pFi82Wx7vJ5bnQTE4p9cIA?pwd=f3jx)
- [最新版本发布](https://github.com/yourusername/minecraft-particle-video-player/releases)

---
