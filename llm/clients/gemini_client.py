"""
Google Gemini 客户端实现
使用 OpenAI SDK 通过 Gemini 的 OpenAI 兼容接口
"""

from openai import AsyncOpenAI
from config.prompt_manager import PromptManager
from llm.base_client import BaseLLMClient


class GeminiClient(BaseLLMClient):
    """Google Gemini 客户端（通过 OpenAI 兼容接口）"""
    
    def __init__(self, api_key: str, prompt_manager: PromptManager):
        super().__init__(prompt_manager, 'gemini')
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
    
    async def _call_llm(self, prompt: str) -> str:
        """调用 Gemini API（通过 OpenAI 兼容接口）"""
        print(f"🟡 Gemini API 调用开始 (OpenAI 兼容模式)...")
        
        response = await self.client.chat.completions.create(
            model=self.config['model'],
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=self.config['temperature'],
            max_tokens=self.config.get('max_tokens', 2000)
        )
        
        print(f"🟡 Gemini API 调用完成")
        return response.choices[0].message.content
