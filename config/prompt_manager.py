"""
Prompt配置管理器
负责加载和管理YAML配置文件中的prompt模板
"""

import yaml
from langchain.prompts import PromptTemplate


class PromptManager:
    """Prompt配置管理器"""
    
    def __init__(self, config_path: str = "prompts.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """加载YAML配置文件"""
        with open(self.config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    
    def get_prompt(self, prompt_type: str, llm_name: str, **variables) -> str:
        """
        生成特定LLM的完整prompt
        
        Args:
            prompt_type (str): prompt类型 (screen_jd, rank_experiences)
            llm_name (str): LLM名称 (gemini, gpt, claude)
            **variables: 模板变量
            
        Returns:
            str: 完整的prompt文本
        """
        prompt_config = self.config['prompts'][prompt_type]
        base_template = prompt_config['base_template']
        output_format = prompt_config['output_formats'][llm_name]
        
        # 组合基础模板和输出格式
        full_template = base_template + "\n\n" + output_format
        
        # 替换变量
        prompt_template = PromptTemplate.from_template(full_template)
        return prompt_template.format(**variables)
    
    def get_llm_config(self, llm_name: str) -> dict:
        """获取LLM配置"""
        return self.config['llm_configs'][llm_name]
    
    def get_retry_config(self) -> dict:
        """获取重试配置"""
        return self.config['retry_config'] 