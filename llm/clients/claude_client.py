"""
Anthropic Claude客户端实现
"""

from langchain.chat_models import ChatAnthropic
from config.prompt_manager import PromptManager
from llm.base_client import BaseLLMClient


class ClaudeClient(BaseLLMClient):
    """Anthropic Claude客户端"""
    
    def __init__(self, api_key: str, prompt_manager: PromptManager):
        super().__init__(prompt_manager, 'claude')
        self.client = ChatAnthropic(
            anthropic_api_key=api_key,
            model=self.config['model'],
            temperature=self.config['temperature'],
            max_tokens=self.config['max_tokens']
        )
    
    async def _call_llm(self, prompt: str) -> str:
        """调用Claude API"""
        response = await self.client.apredict(prompt)
        return response 