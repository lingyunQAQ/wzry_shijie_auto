"""
配置管理模块
"""

import json
import os
from typing import Dict, Any, Optional

class ConfigError(Exception):
    """配置文件相关异常"""
    pass

class ConfigManager:
    """配置管理器，负责配置的加载、保存和验证"""
    
    def __init__(self, config_path: str = "config.json"):
        """
        初始化配置管理器
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path
        self.default_config = self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        screen_width = 1920
        screen_height = 1080
        return {
            "window_title": "",
            "detection_area": {
                "x": (screen_width - 800) // 2,
                "y": (screen_height - 600) // 2,
                "width": 800,
                "height": 600
            },
            "click_offset": {
                "x": 0,
                "y": 0
            },
            "target_text": "正在求救",
            "click_text": "点击前往",
            "similarity_threshold": 0.8,
            "loop_interval": 2,
            "max_retries": 10,
            "retry_delay": 5,
            "standby_interval": 30,
            "max_failure_count": 3
        }
    
    def load_config(self) -> Dict[str, Any]:
        """
        加载配置文件
        
        Returns:
            配置字典
            
        Raises:
            ConfigError: 配置文件损坏时抛出
        """
        if not os.path.exists(self.config_path):
            self.save_config(self.default_config)
            return self.default_config
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return self._validate_config(config)
        except json.JSONDecodeError as e:
            raise ConfigError(f"配置文件损坏: {str(e)}") from e
        except Exception as e:
            raise ConfigError(f"加载配置失败: {str(e)}") from e
    
    def _validate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证配置有效性，缺失的配置项使用默认值
        
        Args:
            config: 待验证的配置字典
            
        Returns:
            验证后的配置字典
        """
        validated = self.default_config.copy()
        
        # 合并用户配置
        for key in validated.keys():
            if key in config:
                if isinstance(validated[key], dict) and isinstance(config[key], dict):
                    validated[key] = {**validated[key], **config[key]}
                else:
                    validated[key] = config[key]
        
        # 验证阈值范围
        if not (0.7 <= validated["similarity_threshold"] <= 0.95):
            validated["similarity_threshold"] = 0.8
        
        # 验证循环间隔
        if validated["loop_interval"] < 1:
            validated["loop_interval"] = 1
        
        # 验证检测区域大小
        if validated["detection_area"]["width"] > 1920:
            validated["detection_area"]["width"] = 1920
        if validated["detection_area"]["height"] > 1080:
            validated["detection_area"]["height"] = 1080
        
        return validated
    
    def save_config(self, config: Dict[str, Any]) -> None:
        """
        保存配置到文件
        
        Args:
            config: 要保存的配置字典
            
        Raises:
            ConfigError: 保存失败时抛出
        """
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            raise ConfigError(f"保存配置失败: {str(e)}") from e
    
    def get_config(self) -> Dict[str, Any]:
        """
        获取当前配置（安全加载，失败时返回默认配置）
        
        Returns:
            配置字典
        """
        try:
            return self.load_config()
        except ConfigError:
            return self.default_config.copy()