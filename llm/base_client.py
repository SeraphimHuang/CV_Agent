"""
LLM客户端基类
定义通用接口和重试机制
"""

import json
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, List, Any

from config.prompt_manager import PromptManager
from utils.json_fixer import JSONFixer


class BaseLLMClient(ABC):
    """LLM客户端基类"""
    
    def __init__(self, prompt_manager: PromptManager, llm_name: str):
        self.prompt_manager = prompt_manager
        self.llm_name = llm_name
        self.config = prompt_manager.get_llm_config(llm_name)
        self.retry_config = prompt_manager.get_retry_config()
        self.json_fixer = JSONFixer()
    
    @abstractmethod
    async def _call_llm(self, prompt: str) -> str:
        """调用LLM API"""
        pass
    
    async def _call_with_retry(self, prompt: str) -> str:
        """带重试机制的LLM调用"""
        max_retries = self.retry_config['max_retries']
        retry_delay = self.retry_config['retry_delay']
        
        for attempt in range(max_retries + 1):
            try:
                response = await self._call_llm(prompt)
                
                # 尝试修复和解析JSON
                fixed_response = self.json_fixer.fix_json(response)
                json.loads(fixed_response)  # 验证JSON格式
                
                return fixed_response
                
            except json.JSONDecodeError as e:
                print(f"{self.llm_name} JSON解析错误 (尝试 {attempt + 1}/{max_retries + 1}): {e}")
                if attempt < max_retries:
                    await asyncio.sleep(retry_delay)
                    continue
                else:
                    raise Exception(f"{self.llm_name} JSON解析失败，已重试{max_retries}次")
                    
            except Exception as e:
                print(f"{self.llm_name} API调用错误 (尝试 {attempt + 1}/{max_retries + 1}): {e}")
                if attempt < max_retries:
                    await asyncio.sleep(retry_delay)
                    continue
                else:
                    raise Exception(f"{self.llm_name} API调用失败，已重试{max_retries}次: {str(e)}")
    
    async def screen_jd(self, jd_text: str) -> Dict[str, Any]:
        """筛选职位描述"""
        try:
            prompt = self.prompt_manager.get_prompt('screen_jd', self.llm_name, jd_text=jd_text)
            response = await self._call_with_retry(prompt)
            return json.loads(response)
        except Exception as e:
            return {
                "citizenship_required": False,
                "senior_level_required": False,
                "reason": f"{self.llm_name}调用失败: {str(e)}"
            }
    
    async def rank_experiences(self, jd_text: str, experiences: List[Dict[str, Any]]) -> Dict[str, Any]:
        """对经历进行排名"""
        try:
            experiences_text = json.dumps(experiences, ensure_ascii=False, indent=2)
            prompt = self.prompt_manager.get_prompt(
                'rank_experiences', 
                self.llm_name, 
                jd_text=jd_text, 
                experiences_text=experiences_text
            )
            response = await self._call_with_retry(prompt)
            return json.loads(response)
        except Exception as e:
            return {
                "match_percentage": 0,
                "ranked_experiences": [],
                "error": f"{self.llm_name}调用失败: {str(e)}"
            } 