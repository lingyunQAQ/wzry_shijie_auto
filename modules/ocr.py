"""
OCR文字识别模块
"""

import pytesseract
from PIL import Image
from difflib import SequenceMatcher
from typing import Tuple, Optional, List, Dict
import os

class OCRError(Exception):
    """OCR识别异常"""
    pass

class OCRManager:
    """OCR识别管理器，负责文字识别和关键词匹配"""
    
    def __init__(self, similarity_threshold: float = 0.8, tesseract_cmd: Optional[str] = None):
        """
        初始化OCR管理器
        
        Args:
            similarity_threshold: 相似度阈值，范围0.7-0.95
            tesseract_cmd: Tesseract可执行文件路径（可选）
        """
        self.similarity_threshold = max(0.7, min(0.95, similarity_threshold))
        
        if tesseract_cmd and os.path.exists(tesseract_cmd):
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        elif os.path.exists(r'C:\Program Files\Tesseract-OCR\tesseract.exe'):
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    def set_threshold(self, threshold: float) -> None:
        """
        设置相似度阈值
        
        Args:
            threshold: 新的阈值
        """
        self.similarity_threshold = max(0.7, min(0.95, threshold))
    
    def extract_text(self, image: Image.Image) -> str:
        """
        从图像中提取文字
        
        Args:
            image: PIL图像对象
            
        Returns:
            提取的文字
            
        Raises:
            OCRError: 识别失败时抛出
        """
        try:
            custom_config = r'--oem 3 --psm 6 -l chi_sim'
            text = pytesseract.image_to_string(image, config=custom_config)
            return text.strip()
        except Exception as e:
            raise OCRError(f"OCR识别失败: {str(e)}") from e
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        计算两个字符串的相似度
        
        Args:
            text1: 第一个字符串
            text2: 第二个字符串
            
        Returns:
            相似度值 (0-1)
        """
        return SequenceMatcher(None, text1, text2).ratio()
    
    def find_text_position(self, image: Image.Image, target_text: str, fast_mode: bool = False) -> Optional[Tuple[int, int]]:
        """
        在图像中查找目标文字的位置
        
        Args:
            image: PIL图像对象
            target_text: 目标文字
            fast_mode: 快速模式，减少输出
            
        Returns:
            文字中心坐标 (x, y)，未找到返回None
        """
        try:
            custom_config = r'--oem 3 --psm 6 -l chi_sim'
            data = pytesseract.image_to_data(image, config=custom_config, output_type=pytesseract.Output.DICT)
            
            found_texts = []
            text_positions = []
            n_boxes = len(data['text'])
            
            for i in range(n_boxes):
                text = data['text'][i].strip()
                if text:
                    found_texts.append(text)
                    text_positions.append({
                        'text': text,
                        'x': data['left'][i] + data['width'][i] // 2,
                        'y': data['top'][i] + data['height'][i] // 2,
                        'left': data['left'][i],
                        'top': data['top'][i],
                        'width': data['width'][i],
                        'height': data['height'][i]
                    })
            
            if found_texts:
                all_text = ''.join(found_texts)
                
                if not fast_mode:
                    if len(found_texts) > 20:
                        print(f"[OCR识别] 检测到 {len(found_texts)} 个文字块（过多，可能检测区域太大）")
                        print(f"[OCR识别] 前20个: {', '.join(found_texts[:20])}...")
                    else:
                        print(f"[OCR识别] 检测到的文字: {', '.join(found_texts)}")
                    
                    print(f"[OCR识别] 组合文字长度: {len(all_text)} 字符")
                    if len(all_text) > 100:
                        print(f"[OCR识别] 组合文字（前100字符）: {all_text[:100]}...")
                    else:
                        print(f"[OCR识别] 组合文字: {all_text}")
                
                if target_text in all_text:
                    if not fast_mode:
                        print(f"[OCR匹配] 在组合文字中找到目标: '{target_text}'")
                    
                    target_start = all_text.index(target_text)
                    target_end = target_start + len(target_text)
                    
                    char_count = 0
                    start_idx = -1
                    end_idx = -1
                    
                    for idx, text in enumerate(found_texts):
                        if char_count <= target_start < char_count + len(text):
                            start_idx = idx
                        if char_count < target_end <= char_count + len(text):
                            end_idx = idx
                        char_count += len(text)
                    
                    if start_idx >= 0 and end_idx >= 0:
                        positions = text_positions[start_idx:end_idx+1]
                        
                        min_left = min(p['left'] for p in positions)
                        max_right = max(p['left'] + p['width'] for p in positions)
                        min_top = min(p['top'] for p in positions)
                        max_bottom = max(p['top'] + p['height'] for p in positions)
                        
                        center_x = (min_left + max_right) // 2
                        center_y = (min_top + max_bottom) // 2
                        
                        return (center_x, center_y)
                
                for pos in text_positions:
                    similarity = self.calculate_similarity(pos['text'], target_text)
                    if similarity >= self.similarity_threshold:
                        if not fast_mode:
                            print(f"[OCR匹配] 通过相似度匹配找到: '{pos['text']}' (相似度: {similarity:.2f})")
                        return (pos['x'], pos['y'])
                
                if not fast_mode:
                    print(f"[OCR匹配] 未找到目标文字 '{target_text}'")
            else:
                if not fast_mode:
                    print(f"[OCR识别] 未检测到任何文字")
            
            return None
        except Exception as e:
            raise OCRError(f"查找文字位置失败: {str(e)}") from e
    
    def has_text(self, image: Image.Image, target_text: str) -> bool:
        """
        检查图像中是否包含目标文字
        
        Args:
            image: PIL图像对象
            target_text: 目标文字
            
        Returns:
            包含返回True，否则返回False
        """
        text = self.extract_text(image)
        return self.calculate_similarity(text, target_text) >= self.similarity_threshold
    
    def find_multiple_texts(self, image: Image.Image, texts: List[str], fast_mode: bool = False) -> Dict[str, Optional[Tuple[int, int]]]:
        """
        在图像中查找多个文字的位置
        
        Args:
            image: PIL图像对象
            texts: 要查找的文字列表
            fast_mode: 快速模式
            
        Returns:
            文字到坐标的映射字典
        """
        results = {}
        for text in texts:
            results[text] = self.find_text_position(image, text, fast_mode)
        return results