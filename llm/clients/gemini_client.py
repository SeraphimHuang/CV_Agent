"""
Google Gemini客户端实现
"""

import asyncio
import google.generativeai as genai
from config.prompt_manager import PromptManager
from llm.base_client import BaseLLMClient


class GeminiClient(BaseLLMClient):
    """Google Gemini客户端"""
    
    def __init__(self, api_key: str, prompt_manager: PromptManager):
        super().__init__(prompt_manager, 'gemini')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(self.config['model'])
    
    async def _call_llm(self, prompt: str) -> str:
        """调用Gemini API"""
        print(f"🟡 Gemini API 调用开始...")
        generation_config = {
            "temperature": self.config['temperature'],
            "max_output_tokens": self.config['max_output_tokens'],
        }
        
        response = await asyncio.to_thread(
            self.model.generate_content,
            prompt,
            generation_config=generation_config
        )
        print(f"🟡 Gemini API 调用完成")
        return response.text 