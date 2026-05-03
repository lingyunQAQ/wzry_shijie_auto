"""
自动点击监控系统 - 主程序
作者：是凌云诶
抖音：是凌云诶
"""

import logging
import logging.handlers
import time
import os
from typing import Tuple

from modules import (
    ConfigManager,
    WindowManager,
    OCRManager,
    Clicker,
    SoundPlayer
)

class Monitor:
    """监控主类，检测目标文字并自动点击"""
    
    def __init__(self):
        """初始化监控器"""
        self.config_manager = ConfigManager()
        self.window_manager = WindowManager()
        self.ocr_manager = OCRManager()
        self.clicker = Clicker()
        self.sound_player = SoundPlayer()
        self.logger = self._setup_logger()
        self.config = {}
        self.is_running = False
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger('monitor')
        logger.setLevel(logging.INFO)
        
        os.makedirs('logs', exist_ok=True)
        
        handler = logging.handlers.RotatingFileHandler(
            'logs/monitor.log',
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding='utf-8'
        )
        
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def load_config(self) -> bool:
        """加载配置"""
        try:
            self.config = self.config_manager.load_config()
            self.ocr_manager.set_threshold(self.config.get('similarity_threshold', 0.8))
            self.logger.info("配置加载成功")
            return True
        except Exception as e:
            self.logger.warning(f"配置加载失败，使用默认配置: {str(e)}")
            self.config = self.config_manager.get_config()
            return False
    
    def _get_detection_region(self) -> Tuple[int, int, int, int]:
        """获取检测区域"""
        area = self.config.get('detection_area', {})
        return (
            area.get('x', 400),
            area.get('y', 240),
            area.get('width', 800),
            area.get('height', 600)
        )
    
    def _get_click_offset(self) -> Tuple[int, int]:
        """获取点击偏移量"""
        offset = self.config.get('click_offset', {})
        return (offset.get('x', 0), offset.get('y', 0))
    
    def detect_and_click(self) -> bool:
        """执行检测和点击操作"""
        target_text = self.config.get('target_text', '点击前往')
        region = self._get_detection_region()
        fast_mode = self.config.get('fast_mode', True)
        
        try:
            screenshot = self.window_manager.capture_region(region)
            position = self.ocr_manager.find_text_position(screenshot, target_text, fast_mode)
            
            if position is not None:
                click_x, click_y = position
                offset_x, offset_y = self._get_click_offset()
                
                absolute_x = region[0] + click_x + offset_x
                absolute_y = region[1] + click_y + offset_y
                
                click_count = self.config.get('click_count', 10)
                click_interval = self.config.get('click_interval', 0.01)
                
                self.logger.info(f"检测到目标: '{target_text}'，立即点击")
                
                for i in range(click_count):
                    self.clicker.click(absolute_x, absolute_y)
                    if i < click_count - 1:
                        time.sleep(click_interval)
                
                self.logger.info(f"已完成 {click_count} 次点击，坐标: ({absolute_x}, {absolute_y})")
                print(f"[成功] 已完成 {click_count} 次快速点击")
                
                if self.config.get('enable_sound', True):
                    self.sound_player.play_success_sound()
                
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"检测错误: {str(e)}")
            return False
    
    def run(self) -> None:
        """启动监控主循环"""
        self.is_running = True
        self.logger.info("监控系统启动")
        print("\n" + "="*60)
        print("监控系统已启动，正在检测目标...")
        print("="*60 + "\n")
        
        self.load_config()
        
        loop_interval = self.config.get('loop_interval', 0.1)
        
        while self.is_running:
            try:
                if self.detect_and_click():
                    print("\n" + "="*60)
                    print("✓ 点击成功！")
                    print("="*60 + "\n")
                    self.logger.info("点击成功，程序即将退出")
                    self.stop()
                    return
                
                time.sleep(loop_interval)
                
            except Exception as e:
                self.logger.error(f"未预期的错误: {str(e)}")
                time.sleep(loop_interval)
    
    def stop(self) -> None:
        """停止监控"""
        self.is_running = False
        self.logger.info("监控系统停止")

def main():
    """主函数"""
    print("\n" + "="*60)
    print("  自动点击监控系统")
    print("  作者：是凌云诶")
    print("  抖音：是凌云诶")
    print("="*60 + "\n")
    
    monitor = Monitor()
    try:
        monitor.run()
        print("程序已正常退出")
    except KeyboardInterrupt:
        monitor.stop()
        print("\n监控已手动停止")
    except Exception as e:
        print(f"\n程序异常退出: {str(e)}")
        monitor.logger.error(f"程序异常: {str(e)}")

if __name__ == "__main__":
    main()