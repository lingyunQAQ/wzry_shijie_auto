"""
窗口管理和截图模块
"""

import pyautogui
import pygetwindow as gw
from PIL import Image
from typing import Tuple, Optional, Any

class WindowNotFoundError(Exception):
    """窗口未找到异常"""
    pass

class WindowManager:
    """窗口管理器，负责窗口定位和截图"""
    
    def __init__(self):
        """初始化窗口管理器"""
        self.screen_width, self.screen_height = pyautogui.size()
    
    def find_window(self, title: str) -> Optional[Any]:
        """
        根据标题查找窗口
        
        Args:
            title: 窗口标题（支持模糊匹配）
            
        Returns:
            窗口对象，如果未找到返回None
        """
        if not title:
            return None
            
        try:
            windows = gw.getWindowsWithTitle(title)
            if windows:
                return windows[0]
            return None
        except Exception:
            return None
    
    def get_window_region(self, window: Any = None, 
                          custom_region: Optional[Tuple[int, int, int, int]] = None) -> Tuple[int, int, int, int]:
        """
        获取窗口区域或自定义区域
        
        Args:
            window: 窗口对象
            custom_region: 自定义区域 (x, y, width, height)
            
        Returns:
            区域元组 (x, y, width, height)
            
        Raises:
            WindowNotFoundError: 窗口不存在时抛出
        """
        if custom_region:
            x, y, w, h = custom_region
            return (x, y, w, h)
        
        if window:
            if not window.isActive:
                window.activate()
            return (window.left, window.top, window.width, window.height)
        
        raise WindowNotFoundError("未找到目标窗口")
    
    def capture_region(self, region: Tuple[int, int, int, int]) -> Image.Image:
        """
        截取指定区域的屏幕图像
        
        Args:
            region: 区域元组 (x, y, width, height)
            
        Returns:
            PIL图像对象
        """
        x, y, w, h = region
        # 确保区域不超过屏幕边界
        x = max(0, x)
        y = max(0, y)
        w = min(w, self.screen_width - x)
        h = min(h, self.screen_height - y)
        
        screenshot = pyautogui.screenshot(region=(x, y, w, h))
        return screenshot
    
    def get_window_screenshot(self, window_title: str = "", 
                             custom_region: Optional[Tuple[int, int, int, int]] = None) -> Image.Image:
        """
        获取窗口截图
        
        Args:
            window_title: 窗口标题
            custom_region: 自定义区域
            
        Returns:
            PIL图像对象
            
        Raises:
            WindowNotFoundError: 窗口不存在时抛出
        """
        if custom_region:
            return self.capture_region(custom_region)
        
        window = self.find_window(window_title)
        if not window:
            raise WindowNotFoundError(f"未找到窗口: {window_title}")
        
        region = self.get_window_region(window)
        return self.capture_region(region)
    
    def is_window_exists(self, title: str) -> bool:
        """
        检查窗口是否存在
        
        Args:
            title: 窗口标题
            
        Returns:
            窗口存在返回True，否则返回False
        """
        return self.find_window(title) is not None