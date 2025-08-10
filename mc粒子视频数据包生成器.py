import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import zipfile
import json
import re
import shutil
import sys

class ParticleDataPackGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("粒子效果数据包生成器")
        self.root.geometry("550x450") 
        
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 标题
        title_label = tk.Label(
            self.main_frame, 
            text="Minecraft 粒子数据包生成器", 
            font=("Arial", 16, "bold"),
            pady=10
        )
        title_label.pack()
        
        # 说明
        desc_label = tk.Label(
            self.main_frame, 
            text="输入坐标并选择包含有序图片的文件夹\n将生成1.16.5数据包，执行/start触发粒子序列",
            fg="#555555",
            pady=5
        )
        desc_label.pack()
        
        # 坐标输入部分
        coord_frame = tk.LabelFrame(self.main_frame, text="坐标设置", padx=10, pady=10)
        coord_frame.pack(fill="x", pady=10, padx=5)
        
        tk.Label(coord_frame, text="坐标 (x y z):", font=("Arial", 10)).pack(anchor="w", pady=(0, 5))
        self.coord_entry = tk.Entry(coord_frame, width=30, font=("Arial", 12))
        self.coord_entry.pack(fill="x", pady=5, ipady=3)
        # 移除了默认坐标，现在为空
        
        # 示例标签
        example_label = tk.Label(
            coord_frame, 
            text="示例: 145 154 458 (三个数字用空格分隔)",
            fg="#666666",
            font=("Arial", 9),
            anchor="w"
        )
        example_label.pack(fill="x", pady=(0, 5))
        
        # 文件夹选择区域
        folder_frame = tk.LabelFrame(self.main_frame, text="图片文件夹", padx=10, pady=10)
        folder_frame.pack(fill="x", pady=10, padx=5)
        
        self.folder_btn = tk.Button(
            folder_frame, 
            text="选择文件夹", 
            command=self.browse_folder,
            padx=10,
            pady=5,
            bg="#2196F3",
            fg="white"
        )
        self.folder_btn.pack(pady=5, fill="x")
        
        self.folder_label = tk.Label(
            folder_frame, 
            text="未选择文件夹",
            relief="sunken", 
            padx=10,
            pady=5,
            wraplength=400,
            justify="center",
            height=3,
            bg="#f0f0f0"
        )
        self.folder_label.pack(fill="x", padx=5, pady=5)
        
        # 进度条
        self.progress_frame = tk.LabelFrame(self.main_frame, text="进度", padx=10, pady=10)
        self.progress_frame.pack(fill="x", padx=5, pady=10)
        
        self.progress_label = tk.Label(self.progress_frame, text="准备就绪", fg="gray", anchor="w")
        self.progress_label.pack(fill="x", pady=(0, 5))
        
        self.progress = ttk.Progressbar(
            self.progress_frame, 
            orient="horizontal", 
            length=400, 
            mode="determinate"
        )
        self.progress.pack(fill="x", pady=(0, 5))
        
        # 生成按钮框架 - 放在窗口底部
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        self.generate_btn = tk.Button(
            button_frame, 
            text="生成数据包", 
            command=self.generate_datapack, 
            state="disabled",
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=8
        )
        self.generate_btn.pack(fill="x", pady=5)
        
        # 状态标签
        self.status_label = tk.Label(
            self.main_frame, 
            text="© 2025 Minecraft粒子视频生成器 By bilibili疯狂的夕阳", 
            fg="gray",
            font=("Arial", 8)
        )
        self.status_label.pack(side="bottom", pady=5)
        
        self.folder_path = ""

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path = folder
            # 缩短显示的文件夹路径
            folder_display = folder
            if len(folder_display) > 50:
                folder_display = "..." + folder_display[-47:]
            self.folder_label.config(text=folder_display)
            self.check_ready()

    def check_ready(self, event=None):
        if self.folder_path and self.coord_entry.get().strip():
            self.generate_btn.config(state="normal", bg="#4CAF50")
            self.progress_label.config(text="准备生成数据包", fg="green")
        else:
            self.generate_btn.config(state="disabled", bg="#cccccc")
            self.progress_label.config(text="请选择文件夹并输入坐标", fg="gray")

    def generate_datapack(self):
        # 获取并验证坐标
        coord_text = self.coord_entry.get().strip()
        if not re.match(r"^-?\d+ -?\d+ -?\d+$", coord_text):
            messagebox.showerror("错误", "坐标格式不正确！请使用 'x y z' 格式（例如：145 154 458）")
            return
        
        self.coords = coord_text
        
        # 获取图片文件
        try:
            image_files = self.get_sorted_images()
            if not image_files:
                messagebox.showerror("错误", "文件夹中没有找到图片文件！")
                return
        except Exception as e:
            messagebox.showerror("错误", f"读取图片时出错:\n{str(e)}")
            return
        
        # 更新UI状态
        self.generate_btn.config(state="disabled", bg="#cccccc", text="生成中...")
        self.progress_label.config(text="正在创建数据包...", fg="blue")
        self.root.update()
        
        # 创建数据包
        try:
            self.create_datapack(image_files)
            messagebox.showinfo("成功", "数据包生成成功！\n文件已保存为: particle_datapack.zip")
        except Exception as e:
            messagebox.showerror("错误", f"创建数据包时出错:\n{str(e)}")
        finally:
            # 清理临时文件
            if os.path.exists("temp_datapack"):
                shutil.rmtree("temp_datapack")
            # 重置UI
            self.generate_btn.config(state="normal", bg="#4CAF50", text="生成数据包")
            self.progress_label.config(text="准备就绪", fg="gray")
            self.progress["value"] = 0
            self.root.update()

    def get_sorted_images(self):
        valid_exts = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
        files = []
        
        for f in os.listdir(self.folder_path):
            if f.lower().endswith(valid_exts):
                try:
                    # 提取文件名中的数字部分
                    num = int(''.join(filter(str.isdigit, os.path.splitext(f)[0])))
                    files.append((num, f))
                except:
                    # 如果无法提取数字，使用文件名排序
                    files.append((f, f))
        
        # 按数字排序
        files.sort(key=lambda x: x[0] if isinstance(x[0], int) else x[0])
        return [f[1] for f in files]

    def create_datapack(self, image_files):
        # 创建临时文件夹结构
        os.makedirs("temp_datapack/data/minecraft/tags/functions", exist_ok=True)
        os.makedirs("temp_datapack/data/particle/functions", exist_ok=True)
        
        # 创建pack.mcmeta
        with open("temp_datapack/pack.mcmeta", "w", encoding="utf-8") as f:
            json.dump({
                "pack": {
                    "pack_format": 6,
                    "description": "粒子效果数据包"
                }
            }, f, indent=2)
        
        # 创建load.json (空标签)
        with open("temp_datapack/data/minecraft/tags/functions/load.json", "w", encoding="utf-8") as f:
            json.dump({"values": []}, f, indent=2)
        
        # 创建start.mcfunction - 现在只调用第一个粒子函数
        with open("temp_datapack/data/particle/functions/start.mcfunction", "w", encoding="utf-8") as f:
            f.write("# 粒子效果序列 - 执行 /start 触发\n")
            f.write("# 从第一个粒子开始，然后每1tick执行下一个\n\n")
            f.write("function particle:show_0\n")
        
        # 创建粒子指令文件 - 添加1tick延迟
        total_files = len(image_files)
        for i, img in enumerate(image_files):
            # 更新进度条
            progress_value = (i + 1) / total_files * 100
            self.progress["value"] = progress_value
            self.progress_label.config(text=f"处理图片: {img} ({i+1}/{total_files})")
            self.root.update()
            
            with open(f"temp_datapack/data/particle/functions/show_{i}.mcfunction", "w", encoding="utf-8") as f:
                f.write(f"# 图片: {img}\n")
                # 使用完整的文件名（包含扩展名）
                f.write(f'particleex image end_rod {self.coords} "{img}" 0.1 0 0 0 not 10 0 0 0 1 null\n')
                
                # 如果不是最后一张图片，安排下一个粒子在1tick后执行
                if i < total_files - 1:
                    f.write(f"schedule function particle:show_{i+1} 1t\n")
        
        # 压缩为zip文件
        self.progress_label.config(text="正在压缩数据包...")
        self.root.update()
        
        with zipfile.ZipFile('particle_datapack.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk("temp_datapack"):
                for file in files:
                    path = os.path.join(root, file)
                    arcname = os.path.relpath(path, "temp_datapack")
                    zipf.write(path, arcname)
        
        # 清理临时文件
        if os.path.exists("temp_datapack"):
            shutil.rmtree("temp_datapack")

def main():
    root = tk.Tk()
    
    # 设置窗口图标（如果可用）
    try:
        if sys.platform.startswith('win'):
            root.iconbitmap(default='favicon.ico')
    except:
        pass
    
    app = ParticleDataPackGenerator(root)
    app.coord_entry.bind("<KeyRelease>", app.check_ready)
    
    # 设置窗口居中
    window_width = 550
    window_height = 450  # 增加高度
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
