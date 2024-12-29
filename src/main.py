import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from pathlib import Path
from ocr_handler import OCRHandler
from ai_handler import AIHandler
from file_handler import FileHandler
from config import Config
import threading
import logging
import logging.handlers
from typing import List, Tuple, Optional, Dict
from queue import Queue
import queue

# DeepSeek API 密钥
API_KEY = "sk-fdebc76759574fdc849ed0fd2cf79480"

# 配置日志
def setup_logging() -> None:
    """配置日志系统"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / "app.log"
    
    # 配置根日志记录器
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=1024*1024,  # 1MB
                backupCount=5,
                encoding='utf-8'
            ),
            logging.StreamHandler()
        ]
    )

class ScreenshotRenamer(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 加载配置
        self.config = Config()
        
        # 处理状态
        self.is_processing = False
        
        # 设置窗口主题
        ctk.set_appearance_mode(self.config.get("theme", "dark"))
        ctk.set_default_color_theme("blue")
        
        # 设置窗口
        self.title("截图智能重命名工具")
        self.geometry("800x600")
        self.minsize(600, 400)  # 设置最小窗口大小
        
        # 初始化处理器
        try:
            self.ocr_handler = OCRHandler()
            self.ai_handler = AIHandler(api_key=API_KEY)
            self.file_handler = FileHandler(log_dir="logs")
        except Exception as e:
            messagebox.showerror("初始化错误", f"程序初始化失败: {str(e)}")
            self.destroy()
            return
            
        # 用于在线程间传递更新
        self.update_queue: Queue = Queue()
        
        # 存储文件预览信息
        self.file_previews: Dict[str, Dict] = {}
        
        self._create_ui()
        self._start_update_checker()
    
    def _create_ui(self) -> None:
        # 创建主框架
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # 顶部按钮区域
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(fill="x", padx=10, pady=5)
        
        # 选择文件夹按钮
        self.select_dir_btn = ctk.CTkButton(
            self.button_frame,
            text="选择文件夹",
            command=self._select_directory
        )
        self.select_dir_btn.pack(side="left", padx=5)
        
        # 选择文件按钮
        self.select_btn = ctk.CTkButton(
            self.button_frame,
            text="选择文件",
            command=self._select_files
        )
        self.select_btn.pack(side="left", padx=5)
        
        # 清空列表按钮
        self.clear_btn = ctk.CTkButton(
            self.button_frame,
            text="清空列表",
            command=self._clear_list,
            state="disabled"
        )
        self.clear_btn.pack(side="left", padx=5)
        
        # 文件列表区域
        list_frame = ctk.CTkFrame(self.main_frame)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # 创建文件列表
        self.file_list = ctk.CTkTextbox(
            list_frame,
            font=("微软雅黑", 10),
            wrap="none"
        )
        self.file_list.pack(fill="both", expand=True)
        
        # 提示标签
        hint_label = ctk.CTkLabel(
            self.main_frame,
            text='选择文件或文件夹后将自动开始处理',
            text_color="gray"
        )
        hint_label.pack(pady=5)
        
        # 进度显示
        self.progress_var = tk.StringVar(value="等待处理...")
        self.progress_label = ctk.CTkLabel(
            self.main_frame,
            textvariable=self.progress_var
        )
        self.progress_label.pack(pady=5)
        
        # 处理进度条
        self.progress_bar = ctk.CTkProgressBar(self.main_frame)
        self.progress_bar.pack(pady=5)
        self.progress_bar.set(0)
    
    def _add_files(self, files: Tuple[str, ...]) -> None:
        """添加文件到列表并自动开始处理"""
        if self.is_processing:
            messagebox.showinfo("提示", "正在处理文件，请等待当前任务完成")
            return
            
        valid_extensions = {'.png', '.jpg', '.jpeg', '.bmp'}
        for file in files:
            file_path = Path(file)
            if file_path.suffix.lower() in valid_extensions:
                if not file_path.exists():
                    logging.warning(f"文件不存在: {file_path}")
                    continue
                    
                if str(file_path) not in self.file_previews:
                    self.file_previews[str(file_path)] = {
                        'status': '待处理',
                        'new_name': ''
                    }
                    self.file_list.insert("end", f"{file_path.name} - 待处理\n")
            else:
                logging.warning(f"不支持的文件类型: {file_path}")
        
        if self.file_previews:
            self.clear_btn.configure(state="normal")
            # 自动开始处理
            self._start_processing()
    
    def _clear_list(self) -> None:
        """清空文件列表"""
        self.file_list.delete("1.0", "end")
        self.file_previews.clear()
        self.clear_btn.configure(state="disabled")
        self.progress_bar.set(0)
        self.progress_var.set("等待处理...")
    
    def _select_files(self) -> None:
        """选择文件对话框"""
        files = filedialog.askopenfilenames(
            title="选择截图文件",
            filetypes=[
                ("图片文件", "*.png *.jpg *.jpeg *.bmp")
            ]
        )
        
        if files:
            self._add_files(files)
    
    def _select_directory(self) -> None:
        """选择文件夹对话框"""
        directory = filedialog.askdirectory(
            title="选择包含图片的文件夹"
        )
        
        if directory:
            # 获取文件夹中的所有图片文件
            image_files = []
            valid_extensions = {'.png', '.jpg', '.jpeg', '.bmp'}
            
            try:
                for file in Path(directory).rglob("*"):
                    if file.suffix.lower() in valid_extensions:
                        image_files.append(str(file))
                
                if image_files:
                    self._add_files(tuple(image_files))
                    logging.info(f"从文件夹添加了 {len(image_files)} 个图片文件")
                else:
                    messagebox.showinfo("提示", "所选文件夹中没有找到图片文件")
                    
            except Exception as e:
                logging.error(f"扫描文件夹失败: {e}")
                messagebox.showerror("错误", f"扫描文件夹失败: {str(e)}")
    
    def _update_file_status(self, index: int, status: str) -> None:
        """更新文件状态显示"""
        # 计算行的位置
        start = f"{index + 1}.0"
        end = f"{index + 2}.0"
        self.file_list.delete(start, end)
        self.file_list.insert(start, f"{status}\n")
    
    def _start_processing(self) -> None:
        """开始处理文件"""
        if not self.file_previews or self.is_processing:
            return
        
        self.is_processing = True
        total = len(self.file_previews)
        self.select_btn.configure(state="disabled")
        self.select_dir_btn.configure(state="disabled")
        self.clear_btn.configure(state="disabled")
        
        # 在新线程中处理文件
        thread = threading.Thread(
            target=self._process_files,
            args=(list(self.file_previews.keys()),),
            daemon=True
        )
        thread.start()
    
    def _process_files(self, files: List[str]) -> None:
        """处理文件"""
        total = len(files)
        success_count = 0
        skipped_count = 0
        
        try:
            for i, file in enumerate(files):
                try:
                    # 更新状态为处理中
                    self.update_queue.put(("status", i, f"{Path(file).name} - 处理中..."))
                    
                    # 1. 识别文字
                    text = self.ocr_handler.extract_text(file)
                    if not text:
                        skipped_count += 1
                        self.update_queue.put(("status", i, f"{Path(file).name} - 未识别到文字"))
                        continue
                    
                    # 2. AI 生成文件名
                    new_name = self.ai_handler.generate_filename(text)
                    
                    # 3. 重命名文件
                    new_path = self.file_handler.rename_file(file, new_name)
                    
                    success_count += 1
                    self.update_queue.put(("status", i, f"{Path(file).name} -> {Path(new_path).name}"))
                    
                    # 更新进度
                    progress = (i + 1) / total
                    self.update_queue.put((
                        "progress",
                        progress,
                        f"已处理: {i+1}/{total} (成功: {success_count}, 跳过: {skipped_count})"
                    ))
                    
                except ValueError as e:
                    # 图片验证失败
                    skipped_count += 1
                    logging.warning(f"跳过文件: {file}, 原因: {str(e)}")
                    self.update_queue.put(("status", i, f"{Path(file).name} - 跳过: {str(e)}"))
                except Exception as e:
                    logging.error(f"处理文件失败: {file}, 错误: {str(e)}")
                    self.update_queue.put(("status", i, f"{Path(file).name} - 处理失败: {str(e)}"))
                    
        finally:
            self.is_processing = False
            self.select_btn.configure(state="normal")
            self.select_dir_btn.configure(state="normal")
            self.clear_btn.configure(state="normal")
            self.update_queue.put((
                "done",
                f"处理完成! 共 {total} 个文件，成功: {success_count}，跳过: {skipped_count}，"
                f"失败: {total - success_count - skipped_count}"
            ))

    def _check_updates(self) -> None:
        """检查并应用UI更新"""
        try:
            while True:
                update = self.update_queue.get_nowait()
                if update[0] == "status":
                    _, index, status = update
                    self._update_file_status(index, status)
                elif update[0] == "progress":
                    _, progress, message = update
                    self.progress_bar.set(progress)
                    self.progress_var.set(message)
                elif update[0] == "done":
                    _, message = update
                    self.progress_var.set(message)
        except queue.Empty:
            pass
        finally:
            self.after(100, self._check_updates)

    def _start_update_checker(self) -> None:
        """启动UI更新检查器"""
        self.after(100, self._check_updates)

def main():
    try:
        app = ScreenshotRenamer()
        app.mainloop()
    except Exception as e:
        logging.error(f"程序运行错误: {str(e)}")
        messagebox.showerror("错误", f"程序运行错误: {str(e)}")

if __name__ == "__main__":
    main() 