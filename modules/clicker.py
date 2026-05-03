"""
鼠标点击操作模块

"""

import pyautogui
from typing import Tuple, Optional

class Clicker:
    """点击操作器，负责自动点击功能"""
    
    def __init__(self, click_interval: float = 0.5):
        """
        初始化点击器
        
        Args:
            click_interval: 点击间隔（秒），用于防止快速连续点击
        """
        self.click_interval = click_interval
        pyautogui.PAUSE = click_interval
    
    def click(self, x: int, y: int, button: str = 'left') -> None:
        """
        执行点击操作
        
        Args:
            x: 点击的X坐标
            y: 点击的Y坐标
            button: 鼠标按钮，'left' 或 'right'
        """
        pyautogui.click(x, y, button=button)
    
    def click_relative(self, base_x: int, base_y: int, offset_x: int, offset_y: int) -> None:
        """
        相对于基准坐标执行点击
        
        Args:
            base_x: 基准X坐标
            base_y: 基准Y坐标
            offset_x: X偏移量
            offset_y: Y偏移量
        """
        pyautogui.click(base_x + offset_x, base_y + offset_y)
    
    def double_click(self, x: int, y: int) -> None:
        """
        执行双击操作
        
        Args:
            x: 点击的X坐标
            y: 点击的Y坐标
        """
        pyautogui.doubleClick(x, y)
    
    def move_to(self, x: int, y: int, duration: float = 0.25) -> None:
        """
        移动鼠标到指定位置
        
        Args:
            x: 目标X坐标
            y: 目标Y坐标
            duration: 移动持续时间（秒）
        """
        pyautogui.moveTo(x, y, duration=duration)
    
    def get_mouse_position(self) -> Tuple[int, int]:
        """
        获取当前鼠标位置
        
        Returns:
            当前鼠标坐标 (x, y)
        """
        return pyautogui.position()
    
    def click_in_region(self, region_x: int, region_y: int, relative_x: int, relative_y: int) -> None:
        """
        在指定区域内的相对位置点击
        
        Args:
            region_x: 区域左上角X坐标
            region_y: 区域左上角Y坐标
            relative_x: 区域内相对X坐标
            relative_y: 区域内相对Y坐标
        """
        absolute_x = region_x + relative_x
        absolute_y = region_y + relative_y
        pyautogui.click(absolute_x, absolute_y)