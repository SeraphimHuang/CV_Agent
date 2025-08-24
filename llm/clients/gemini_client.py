from __future__ import annotations

"""
Google Gemini客户端新实现
使用 `google.genai.Client` 按官方示例调用 Gemini API。
"""

import asyncio
from google import genai

from config.prompt_manager import PromptManager
from llm.base_client import BaseLLMClient


class GeminiClient(BaseLLMClient):
    """Google Gemini客户端（基于 genai.Client）"""

    def __init__(self, api_key: str, prompt_manager: PromptManager):
        super().__init__(prompt_manager, "gemini")
        # 使用示例中的官方 Client，直接传入 API key
        self.client = genai.Client(api_key=api_key)
        self._use_client = True

    async def _call_llm(self, prompt: str) -> str:
        """调用 Gemini API 并返回文本"""
        print("🟡 Gemini API 调用开始...")
        response = await asyncio.to_thread(
            self.client.models.generate_content,
            model=self.config["model"],  # "gemini-2.5-flash"
            contents=prompt,
        )
        result_text = response.text
        print("🟡 Gemini API 调用完成")
        return result_text 