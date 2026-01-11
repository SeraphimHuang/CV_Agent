"""
OpenAI GPT 客户端实现
使用 OpenAI SDK 原生接口
"""

from openai import AsyncOpenAI
from config.prompt_manager import PromptManager
from llm.base_client import BaseLLMClient


class GPTClient(BaseLLMClient):
    """OpenAI GPT 客户端"""
    
    def __init__(self, api_key: str, prompt_manager: PromptManager):
        super().__init__(prompt_manager, 'gpt')
        self.client = AsyncOpenAI(api_key=api_key)
    
    async def _call_llm(self, prompt: str) -> str:
        """调用 OpenAI GPT API"""
        print(f"🟢 GPT API 调用开始...")
        
        # GPT-5.x 系列使用 max_completion_tokens，而不是 max_tokens
        response = await self.client.chat.completions.create(
            model=self.config['model'],
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=self.config['temperature'],
            max_completion_tokens=self.config.get('max_tokens', 5000)
        )
        
        print(f"🟢 GPT API 调用完成")
        return response.choices[0].message.content
