import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import pillow_heif

# 注册 HEIF 插件，使 Pillow 能够读取 HEIC 格式
pillow_heif.register_heif_opener()

def select_folder():
    """打开文件夹选择对话框"""
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path_var.set(folder_selected)

def start_conversion():
    """开始将选定文件夹中的 HEIC 转换为 JPG"""
    folder = folder_path_var.get()
    if not folder:
        messagebox.showwarning("警告", "请先选择一个文件夹！")
        return
    
    if not os.path.exists(folder):
        messagebox.showerror("错误", "所选文件夹不存在！")
        return
        
    # 查找所有 .heic 或 .HEIC 文件
    heic_files = [f for f in os.listdir(folder) if f.lower().endswith('.heic')]
    
    if not heic_files:
        messagebox.showinfo("提示", "该文件夹中没有找到 .heic 格式的照片。")
        return
        
    # 重置进度条
    progress['maximum'] = len(heic_files)
    progress['value'] = 0
    convert_btn.config(state=tk.DISABLED)
    
    success_count = 0
    for i, filename in enumerate(heic_files):
        heic_path = os.path.join(folder, filename)
        # 将后缀改为 .jpg
        jpg_filename = os.path.splitext(filename)[0] + '.jpg'
        jpg_path = os.path.join(folder, jpg_filename)
        
        try:
            status_var.set(f"正在转换: {filename} ({i+1}/{len(heic_files)})")
            root.update_idletasks()
            
            # 打开并转换图片
            image = Image.open(heic_path)
            # 转换为 RGB 模式，避免带有 Alpha 通道时无法保存为 JPG
            image = image.convert('RGB')
            # 也可以在这里加上质量参数，例如 quality=95
            image.save(jpg_path, 'JPEG', quality=95)
            success_count += 1
            
        except Exception as e:
            print(f"转换 {filename} 失败: {e}")
            
        progress['value'] = i + 1
        root.update_idletasks()
        
    status_var.set("转换完成！")
    convert_btn.config(state=tk.NORMAL)
    messagebox.showinfo("完成", f"转换完毕！\n共成功转换 {success_count} 张照片。")

# --- GUI 界面设置 ---
root = tk.Tk()
root.title("HEIC 转 JPG 批量转换工具")
root.geometry("600x400")
root.resizable(False, False)

# 变量
folder_path_var = tk.StringVar()
status_var = tk.StringVar()
status_var.set("等待操作...")

# 主框架
frame = tk.Frame(root, padx=20, pady=20)
frame.pack(fill=tk.BOTH, expand=True)

# 提示标签
tk.Label(frame, text="请选择包含 HEIC 照片的文件夹:", font=("Arial", 12)).pack(anchor=tk.W, pady=(0, 5))

# 文件夹选择区域
folder_frame = tk.Frame(frame)
folder_frame.pack(fill=tk.X, pady=(0, 15))

folder_entry = tk.Entry(folder_frame, textvariable=folder_path_var, state='readonly')
folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

browse_btn = tk.Button(folder_frame, text="浏览...", command=select_folder)
browse_btn.pack(side=tk.RIGHT)

# 转换按钮
convert_btn = tk.Button(frame, text="开始转换", command=start_conversion, font=("Arial", 14))
convert_btn.pack(fill=tk.X, pady=(0, 15))

# 进度条
progress = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
progress.pack(fill=tk.X, pady=(0, 5))

# 状态文本
status_label = tk.Label(frame, textvariable=status_var, fg="gray", font=("Arial", 10))
status_label.pack(anchor=tk.W)

# 启动主循环
root.mainloop()
