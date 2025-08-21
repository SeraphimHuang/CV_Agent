"""
统一LLM管理器
协调多个LLM客户端的调用
"""

import asyncio
from typing import Dict, List, Any

from config.prompt_manager import PromptManager
from llm.clients import GeminiClient, GPTClient, ClaudeClient


class UnifiedLLMManager:
    """统一LLM管理器"""
    
    def __init__(self, gemini_key: str, openai_key: str, anthropic_key: str, 
                 prompts_config: str = "prompts.yaml"):
        self.prompt_manager = PromptManager(prompts_config)
        
        # 创建三个客户端
        self.gemini = GeminiClient(gemini_key, self.prompt_manager)
        self.gpt = GPTClient(openai_key, self.prompt_manager)
        self.claude = ClaudeClient(anthropic_key, self.prompt_manager)
        
        self.clients = {
            'gemini': self.gemini,
            'gpt': self.gpt,
            'claude': self.claude
        }
    
    async def screen_jd_all(self, jd_text: str) -> Dict[str, Dict[str, Any]]:
        """并发调用所有LLM进行职位筛选"""
        tasks = [
            self.gemini.screen_jd(jd_text),
            self.gpt.screen_jd(jd_text), 
            self.claude.screen_jd(jd_text)
        ]
        
        results = await asyncio.gather(*tasks)
        
        return {
            'gemini': results[0],
            'gpt': results[1],
            'claude': results[2]
        }
    
    async def rank_experiences_all(self, jd_text: str, experiences: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """并发调用所有LLM进行经历排名"""
        tasks = [
            self.gemini.rank_experiences(jd_text, experiences),
            self.gpt.rank_experiences(jd_text, experiences),
            self.claude.rank_experiences(jd_text, experiences)
        ]
        
        results = await asyncio.gather(*tasks)
        
        return {
            'gemini': results[0],
            'gpt': results[1],
            'claude': results[2]
        } 