"""
音频播放模块
"""

import os
import sys
from typing import Optional

class SoundPlayer:
    """音频播放器，负责播放提示音"""
    
    def __init__(self):
        """初始化音频播放器"""
        self.available = self._check_availability()
    
    def _check_availability(self) -> bool:
        """检查音频播放功能是否可用"""
        try:
            if sys.platform == 'win32':
                import winsound
                return True
            else:
                return False
        except ImportError:
            return False
    
    def play_sound(self, sound_file: str) -> bool:
        """
        播放音频文件
        
        Args:
            sound_file: 音频文件路径
            
        Returns:
            播放成功返回True，失败返回False
        """
        if not self.available:
            print("[音频] 音频播放功能不可用")
            return False
        
        if not os.path.exists(sound_file):
            print(f"[音频] 音频文件不存在: {sound_file}")
            return False
        
        try:
            if sys.platform == 'win32':
                import winsound
                winsound.PlaySound(sound_file, winsound.SND_FILENAME | winsound.SND_ASYNC)
                print(f"[音频] 正在播放: {sound_file}")
                return True
        except Exception as e:
            print(f"[音频] 播放失败: {str(e)}")
            return False
        
        return False
    
    def play_beep(self, frequency: int = 1000, duration: int = 500) -> bool:
        """
        播放系统提示音（蜂鸣声）
        
        Args:
            frequency: 频率（Hz），范围37-32767
            duration: 持续时间（毫秒）
            
        Returns:
            播放成功返回True，失败返回False
        """
        if not self.available:
            return False
        
        try:
            if sys.platform == 'win32':
                import winsound
                winsound.Beep(frequency, duration)
                print(f"[音频] 播放提示音: {frequency}Hz, {duration}ms")
                return True
        except Exception as e:
            print(f"[音频] 播放提示音失败: {str(e)}")
            return False
        
        return False
    
    def play_success_sound(self) -> bool:
        """
        播放成功提示音（三声短促的蜂鸣）
        
        Returns:
            播放成功返回True，失败返回False
        """
        if not self.available:
            return False
        
        try:
            if sys.platform == 'win32':
                import winsound
                import time
                for i in range(3):
                    winsound.Beep(1000, 200)
                    time.sleep(0.1)
                print("[音频] 播放成功提示音")
                return True
        except Exception as e:
            print(f"[音频] 播放成功提示音失败: {str(e)}")
            return False
        
        return False