"""
配置界面GUI工具
作者：是凌云诶
抖音：是凌云诶
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from PIL import ImageGrab
import threading

class ConfigGUI:
    """配置界面GUI"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("自动点击监控系统 - 配置工具")
        self.root.geometry("600x750")
        self.root.resizable(False, False)
        
        self.config_path = "config.json"
        self.config = self.load_config()
        self.selecting = False
        self.start_x = 0
        self.start_y = 0
        
        self.create_widgets()
        self.load_values()
    
    def load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "window_title": "",
            "detection_area": {"x": 538, "y": 587, "width": 812, "height": 352},
            "click_offset": {"x": 0, "y": 0},
            "target_text": "点击前往",
            "click_text": "点击前往",
            "similarity_threshold": 0.8,
            "loop_interval": 0.05,
            "max_retries": 10,
            "retry_delay": 5,
            "standby_interval": 30,
            "max_failure_count": 3,
            "use_image_recognition": True,
            "template_image_path": "点击前往.png",
            "image_match_threshold": 0.8,
            "image_scale_factor": 0.5,
            "use_fast_match_method": True,
            "fast_mode": True,
            "click_count": 10,
            "click_interval": 0.01,
            "enable_sound": True
        }
    
    def create_widgets(self):
        """创建界面组件"""
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        basic_frame = ttk.Frame(notebook)
        image_frame = ttk.Frame(notebook)
        advanced_frame = ttk.Frame(notebook)
        
        notebook.add(basic_frame, text='基本设置')
        notebook.add(image_frame, text='图像识别')
        notebook.add(advanced_frame, text='高级设置')
        
        self.create_basic_tab(basic_frame)
        self.create_image_tab(image_frame)
        self.create_advanced_tab(advanced_frame)
        
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(button_frame, text="保存配置", command=self.save_config, width=15).pack(side='left', padx=5)
        ttk.Button(button_frame, text="重置默认", command=self.reset_config, width=15).pack(side='left', padx=5)
        ttk.Button(button_frame, text="退出", command=self.root.quit, width=15).pack(side='right', padx=5)
    
    def create_basic_tab(self, parent):
        """创建基本设置标签页"""
        frame = ttk.LabelFrame(parent, text="检测区域", padding=10)
        frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(frame, text="X坐标:").grid(row=0, column=0, sticky='w', pady=5)
        self.area_x = ttk.Entry(frame, width=15)
        self.area_x.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="Y坐标:").grid(row=0, column=2, sticky='w', pady=5)
        self.area_y = ttk.Entry(frame, width=15)
        self.area_y.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(frame, text="宽度:").grid(row=1, column=0, sticky='w', pady=5)
        self.area_width = ttk.Entry(frame, width=15)
        self.area_width.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="高度:").grid(row=1, column=2, sticky='w', pady=5)
        self.area_height = ttk.Entry(frame, width=15)
        self.area_height.grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Button(frame, text="选择区域", command=self.select_area).grid(row=2, column=0, columnspan=4, pady=10)
        
        frame2 = ttk.LabelFrame(parent, text="点击设置", padding=10)
        frame2.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(frame2, text="点击次数:").grid(row=0, column=0, sticky='w', pady=5)
        self.click_count = ttk.Entry(frame2, width=15)
        self.click_count.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame2, text="点击间隔(秒):").grid(row=0, column=2, sticky='w', pady=5)
        self.click_interval = ttk.Entry(frame2, width=15)
        self.click_interval.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(frame2, text="偏移X:").grid(row=1, column=0, sticky='w', pady=5)
        self.offset_x = ttk.Entry(frame2, width=15)
        self.offset_x.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame2, text="偏移Y:").grid(row=1, column=2, sticky='w', pady=5)
        self.offset_y = ttk.Entry(frame2, width=15)
        self.offset_y.grid(row=1, column=3, padx=5, pady=5)
        
        frame3 = ttk.LabelFrame(parent, text="其他设置", padding=10)
        frame3.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(frame3, text="检测间隔(秒):").grid(row=0, column=0, sticky='w', pady=5)
        self.loop_interval = ttk.Entry(frame3, width=15)
        self.loop_interval.grid(row=0, column=1, padx=5, pady=5)
        
        self.enable_sound_var = tk.BooleanVar()
        ttk.Checkbutton(frame3, text="启用提示音", variable=self.enable_sound_var).grid(row=0, column=2, columnspan=2, sticky='w', padx=5, pady=5)
        
        self.fast_mode_var = tk.BooleanVar()
        ttk.Checkbutton(frame3, text="快速模式", variable=self.fast_mode_var).grid(row=1, column=0, columnspan=2, sticky='w', padx=5, pady=5)
    
    def create_image_tab(self, parent):
        """创建图像识别标签页"""
        frame = ttk.LabelFrame(parent, text="图像识别设置", padding=10)
        frame.pack(fill='x', padx=10, pady=10)
        
        self.use_image_var = tk.BooleanVar()
        ttk.Checkbutton(frame, text="启用图像识别模式", variable=self.use_image_var, 
                       command=self.toggle_image_mode).grid(row=0, column=0, columnspan=4, sticky='w', pady=10)
        
        ttk.Label(frame, text="模板图像路径:").grid(row=1, column=0, sticky='w', pady=5)
        self.template_path = ttk.Entry(frame, width=30)
        self.template_path.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        ttk.Button(frame, text="浏览", command=self.browse_template).grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Label(frame, text="匹配阈值:").grid(row=2, column=0, sticky='w', pady=5)
        self.image_threshold = ttk.Entry(frame, width=15)
        self.image_threshold.grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(frame, text="(0.7-0.95)").grid(row=2, column=2, sticky='w')
        
        frame2 = ttk.LabelFrame(parent, text="性能优化", padding=10)
        frame2.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(frame2, text="图像缩放因子:").grid(row=0, column=0, sticky='w', pady=5)
        self.scale_factor = ttk.Entry(frame2, width=15)
        self.scale_factor.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame2, text="(0.5=快速, 1.0=精确)").grid(row=0, column=2, sticky='w')
        
        self.fast_method_var = tk.BooleanVar()
        ttk.Checkbutton(frame2, text="使用快速匹配算法", variable=self.fast_method_var).grid(row=1, column=0, columnspan=3, sticky='w', pady=5)
        
        info_frame = ttk.LabelFrame(parent, text="说明", padding=10)
        info_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        info_text = """图像识别模式说明：
• 比OCR模式快10-20倍
• 需要准备模板图像（截取要点击的按钮/图标）
• 缩放因子越小速度越快，但可能影响准确度
• 推荐设置：缩放因子0.5，快速算法开启"""
        
        ttk.Label(info_frame, text=info_text, justify='left').pack(anchor='w')
    
    def create_advanced_tab(self, parent):
        """创建高级设置标签页"""
        frame = ttk.LabelFrame(parent, text="OCR设置", padding=10)
        frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(frame, text="目标文字:").grid(row=0, column=0, sticky='w', pady=5)
        self.target_text = ttk.Entry(frame, width=30)
        self.target_text.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
        
        ttk.Label(frame, text="相似度阈值:").grid(row=1, column=0, sticky='w', pady=5)
        self.similarity = ttk.Entry(frame, width=15)
        self.similarity.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(frame, text="(0.7-0.95)").grid(row=1, column=2, sticky='w')
        
        frame2 = ttk.LabelFrame(parent, text="重试设置", padding=10)
        frame2.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(frame2, text="最大重试次数:").grid(row=0, column=0, sticky='w', pady=5)
        self.max_retries = ttk.Entry(frame2, width=15)
        self.max_retries.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame2, text="重试延迟(秒):").grid(row=0, column=2, sticky='w', pady=5)
        self.retry_delay = ttk.Entry(frame2, width=15)
        self.retry_delay.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(frame2, text="待机间隔(秒):").grid(row=1, column=0, sticky='w', pady=5)
        self.standby_interval = ttk.Entry(frame2, width=15)
        self.standby_interval.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame2, text="最大失败次数:").grid(row=1, column=2, sticky='w', pady=5)
        self.max_failure = ttk.Entry(frame2, width=15)
        self.max_failure.grid(row=1, column=3, padx=5, pady=5)
    
    def toggle_image_mode(self):
        """切换图像识别模式"""
        pass
    
    def browse_template(self):
        """浏览模板图像"""
        filename = filedialog.askopenfilename(
            title="选择模板图像",
            filetypes=[("图像文件", "*.png *.jpg *.jpeg *.bmp"), ("所有文件", "*.*")]
        )
        if filename:
            self.template_path.delete(0, tk.END)
            self.template_path.insert(0, os.path.basename(filename))
    
    def select_area(self):
        """选择检测区域"""
        self.root.withdraw()
        messagebox.showinfo("提示", "请在屏幕上拖动鼠标选择检测区域\n选择完成后会自动返回")
        
        def do_select():
            import time
            time.sleep(0.5)
            
            selection_window = tk.Toplevel()
            selection_window.attributes('-fullscreen', True)
            selection_window.attributes('-alpha', 0.3)
            selection_window.attributes('-topmost', True)
            selection_window.configure(bg='black')
            
            canvas = tk.Canvas(selection_window, cursor='cross', bg='black', highlightthickness=0)
            canvas.pack(fill='both', expand=True)
            
            rect = None
            start_x = start_y = 0
            
            def on_press(event):
                nonlocal start_x, start_y, rect
                start_x, start_y = event.x, event.y
                if rect:
                    canvas.delete(rect)
                rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='red', width=2)
            
            def on_drag(event):
                nonlocal rect
                if rect:
                    canvas.coords(rect, start_x, start_y, event.x, event.y)
            
            def on_release(event):
                nonlocal start_x, start_y
                end_x, end_y = event.x, event.y
                
                x = min(start_x, end_x)
                y = min(start_y, end_y)
                width = abs(end_x - start_x)
                height = abs(end_y - start_y)
                
                self.area_x.delete(0, tk.END)
                self.area_x.insert(0, str(x))
                self.area_y.delete(0, tk.END)
                self.area_y.insert(0, str(y))
                self.area_width.delete(0, tk.END)
                self.area_width.insert(0, str(width))
                self.area_height.delete(0, tk.END)
                self.area_height.insert(0, str(height))
                
                selection_window.destroy()
                self.root.deiconify()
            
            canvas.bind('<ButtonPress-1>', on_press)
            canvas.bind('<B1-Motion>', on_drag)
            canvas.bind('<ButtonRelease-1>', on_release)
        
        threading.Thread(target=do_select, daemon=True).start()
    
    def load_values(self):
        """加载配置值到界面"""
        area = self.config.get('detection_area', {})
        self.area_x.insert(0, str(area.get('x', 0)))
        self.area_y.insert(0, str(area.get('y', 0)))
        self.area_width.insert(0, str(area.get('width', 800)))
        self.area_height.insert(0, str(area.get('height', 600)))
        
        offset = self.config.get('click_offset', {})
        self.offset_x.insert(0, str(offset.get('x', 0)))
        self.offset_y.insert(0, str(offset.get('y', 0)))
        
        self.click_count.insert(0, str(self.config.get('click_count', 10)))
        self.click_interval.insert(0, str(self.config.get('click_interval', 0.01)))
        self.loop_interval.insert(0, str(self.config.get('loop_interval', 0.05)))
        
        self.enable_sound_var.set(self.config.get('enable_sound', True))
        self.fast_mode_var.set(self.config.get('fast_mode', True))
        
        self.use_image_var.set(self.config.get('use_image_recognition', True))
        self.template_path.insert(0, self.config.get('template_image_path', '点击前往.png'))
        self.image_threshold.insert(0, str(self.config.get('image_match_threshold', 0.8)))
        self.scale_factor.insert(0, str(self.config.get('image_scale_factor', 0.5)))
        self.fast_method_var.set(self.config.get('use_fast_match_method', True))
        
        self.target_text.insert(0, self.config.get('target_text', '点击前往'))
        self.similarity.insert(0, str(self.config.get('similarity_threshold', 0.8)))
        self.max_retries.insert(0, str(self.config.get('max_retries', 10)))
        self.retry_delay.insert(0, str(self.config.get('retry_delay', 5)))
        self.standby_interval.insert(0, str(self.config.get('standby_interval', 30)))
        self.max_failure.insert(0, str(self.config.get('max_failure_count', 3)))
    
    def save_config(self):
        """保存配置"""
        try:
            config = {
                "window_title": "",
                "detection_area": {
                    "x": int(self.area_x.get()),
                    "y": int(self.area_y.get()),
                    "width": int(self.area_width.get()),
                    "height": int(self.area_height.get())
                },
                "click_offset": {
                    "x": int(self.offset_x.get()),
                    "y": int(self.offset_y.get())
                },
                "target_text": self.target_text.get(),
                "click_text": self.target_text.get(),
                "similarity_threshold": float(self.similarity.get()),
                "loop_interval": float(self.loop_interval.get()),
                "max_retries": int(self.max_retries.get()),
                "retry_delay": int(self.retry_delay.get()),
                "standby_interval": int(self.standby_interval.get()),
                "max_failure_count": int(self.max_failure.get()),
                "use_image_recognition": self.use_image_var.get(),
                "template_image_path": self.template_path.get(),
                "image_match_threshold": float(self.image_threshold.get()),
                "image_scale_factor": float(self.scale_factor.get()),
                "use_fast_match_method": self.fast_method_var.get(),
                "fast_mode": self.fast_mode_var.get(),
                "click_count": int(self.click_count.get()),
                "click_interval": float(self.click_interval.get()),
                "enable_sound": self.enable_sound_var.get()
            }
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            
            messagebox.showinfo("成功", "配置已保存！")
        except Exception as e:
            messagebox.showerror("错误", f"保存配置失败：{str(e)}")
    
    def reset_config(self):
        """重置配置"""
        if messagebox.askyesno("确认", "确定要重置为默认配置吗？"):
            self.config = self.load_config()
            for widget in self.root.winfo_children():
                widget.destroy()
            self.create_widgets()
            self.load_values()
    
    def run(self):
        """运行GUI"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ConfigGUI()
    app.run()
