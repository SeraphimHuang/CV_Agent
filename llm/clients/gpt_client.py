"""
OpenAI GPT客户端实现
"""

from langchain.chat_models import ChatOpenAI
from config.prompt_manager import PromptManager
from llm.base_client import BaseLLMClient


class GPTClient(BaseLLMClient):
    """OpenAI GPT客户端"""
    
    def __init__(self, api_key: str, prompt_manager: PromptManager):
        super().__init__(prompt_manager, 'gpt')
        self.client = ChatOpenAI(
            openai_api_key=api_key,
            model=self.config['model'],
            temperature=self.config['temperature'],
            max_tokens=self.config['max_tokens']
        )
    
    async def _call_llm(self, prompt: str) -> str:
        """调用GPT API"""
        response = await self.client.apredict(prompt)
        return response 