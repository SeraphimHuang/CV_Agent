"""
JSON格式自动修复工具
"""

import re


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
        # 去除markdown标记
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        
        # 去除多余的空白字符
        text = text.strip()
        
        # 修复中文标点
        text = text.replace('，', ',')
        text = text.replace('：', ':')
        text = text.replace('“', '"')
        text = text.replace('”', '"')
        
        # 修复多余的逗号（在}或]前）
        text = re.sub(r',\s*([}\]])', r'\1', text)
        
        # 修复缺失的逗号（在字符串后跟"的情况）
        text = re.sub(r'"\s*\n\s*"', '",\n    "', text)
        
        return text 