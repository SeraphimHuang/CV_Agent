"""
LLM模块
统一的LLM客户端接口和管理
"""

from .manager import UnifiedLLMManager
from .clients import GeminiClient, GPTClient, ClaudeClient

__all__ = ['UnifiedLLMManager', 'GeminiClient', 'GPTClient', 'ClaudeClient', 'create_llm_manager']


def create_llm_manager(gemini_key: str, openai_key: str, anthropic_key: str) -> UnifiedLLMManager:
    """
    创建统一LLM管理器
    
    Args:
        gemini_key (str): Gemini API密钥
        openai_key (str): OpenAI API密钥
        anthropic_key (str): Anthropic API密钥
    
    Returns:
        UnifiedLLMManager: 统一LLM管理器实例
    """
    return UnifiedLLMManager(gemini_key, openai_key, anthropic_key) 