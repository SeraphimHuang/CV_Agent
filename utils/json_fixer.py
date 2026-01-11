"""
JSON格式自动修复工具
"""

import re
import json


class JSONFixer:
    """JSON格式自动修复工具"""
    
    @staticmethod
    def fix_json(text: str) -> str:
        """
        自动修复常见的JSON格式问题
        
        Args:
            text (str): 原始文本
            
        Returns:
            str: 修复后的JSON文本
        """
        if not text:
            return text
            
        # 去除markdown标记
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        
        # 去除多余的空白字符
        text = text.strip()
        
        # 尝试直接解析，如果成功就直接返回
        try:
            json.loads(text)
            return text
        except json.JSONDecodeError:
            pass
        
        # 修复多余的逗号（在}或]前）
        text = re.sub(r',\s*([}\]])', r'\1', text)
        
        # 尝试再次解析
        try:
            json.loads(text)
            return text
        except json.JSONDecodeError:
            # 如果仍然失败，返回原文本，让上层处理
            return text
