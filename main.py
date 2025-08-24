"""
简历优化主程序
整合所有功能模块，提供完整的JD分析和简历优化工作流
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Dict, List, Any

from data_loader import load_config, load_positions, load_experiences, get_position_info
from llm.manager import UnifiedLLMManager
from report_generator import create_markdown_report


class ResumeOptimizer:
    """简历优化器主类"""
    
    def __init__(self):
        self.llm_manager = None
        self.positions_data = None
        self.experiences_data = None
        self.analysis_results = []
    
    def check_environment(self) -> bool:
        """检查环境变量和必要文件"""
        print("🔍 检查运行环境...")
        
        # 检查API密钥
        required_keys = ['GEMINI_API_KEY', 'OPENAI_API_KEY', 'ANTHROPIC_API_KEY']
        missing_keys = []
        
        for key in required_keys:
            if not os.getenv(key):
                missing_keys.append(key)
        
        if missing_keys:
            print(f"❌ 缺少API密钥: {', '.join(missing_keys)}")
            print("请确保 .env 文件包含所有必要的API密钥")
            return False
        
        print("✅ API密钥检查通过")
        return True
    
    def load_data(self, config_path: str = "config_example.json", experience_path: str = "experiences_example.json") -> bool:
        """加载数据文件"""
        print("📂 加载数据文件...")
        
        try:
            # 加载配置
            config = load_config(config_path)
            print(f"✅ 配置文件加载成功: {config_path}")
            
            # 加载职位数据
            self.positions_data = load_positions(config)
            print(f"✅ 职位数据加载成功: {len(self.positions_data)} 个职位")
            
            # 加载经历数据
            self.experiences_data = load_experiences(experience_path)
            print(f"✅ 经历数据加载成功: {len(self.experiences_data)} 个经历")
            
            return True
            
        except FileNotFoundError as e:
            print(f"❌ 文件未找到: {e}")
            return False
        except Exception as e:
            print(f"❌ 数据加载失败: {e}")
            return False
    
    def initialize_llm_manager(self) -> bool:
        """初始化LLM管理器"""
        print("🤖 初始化LLM管理器...")
        
        try:
            self.llm_manager = UnifiedLLMManager(
                os.getenv('GEMINI_API_KEY'),
                os.getenv('OPENAI_API_KEY'),
                os.getenv('ANTHROPIC_API_KEY')
            )
            print("✅ LLM管理器初始化成功")
            return True
        except Exception as e:
            print(f"❌ LLM管理器初始化失败: {e}")
            return False
    
    async def analyze_single_position(self, position_data: Dict[str, Any]) -> Dict[str, Any]:
        """分析单个职位"""
        position_info = get_position_info(position_data)
        jd_text = position_info['job_description']
        
        print(f"  🔍 分析: {position_info['company']} - {position_info['position']}")
        
        # 步骤1: 仅使用 Gemini 进行初步筛选
        try:
            gemini_result = await self.llm_manager.gemini.screen_jd(jd_text)
            print("    ✅ Gemini 筛选完成")
        except Exception as e:
            print(f"    ❌ Gemini 筛选失败: {e}")
            return {
                "position_info": position_info,
                "screening_results": {"gemini": {"error": str(e)}},
                "ranking_results": {},
                "error": f"筛选失败: {str(e)}"
            }

        # 如果 Gemini 判断不合适则直接拒绝
        if gemini_result.get("citizenship_required", False) or gemini_result.get("senior_level_required", False):
            print("    🚫 职位不合适 (Gemini 判断有身份或高级要求)")
            return {
                "position_info": position_info,
                "screening_results": {"gemini": gemini_result},
                "ranking_results": {},
                "rejected": True,
                "rejection_reasons": ["gemini"]
            }

        # 记录筛选结果，仅包含 Gemini
        screening_results = {"gemini": gemini_result}
        
        # 步骤2: 经历排名
        try:
            ranking_results = await self.llm_manager.rank_experiences_all(jd_text, self.experiences_data)
            print("    ✅ 排名完成")

            # 打印各LLM排名摘要
            for llm_name, res in ranking_results.items():
                print(f"    📝 {llm_name} 排名结果:")
                ranked = res.get("ranked_experiences")
                if ranked:
                    for item in ranked:
                        rid = item.get("id", "?")
                        rank = item.get("rank", "?")
                        justification = item.get("justification", "")[:60]
                        print(f"      #{rank} -> {rid} : {justification}...")
                else:
                    print(f"      ⚠️  无排名数据: {res.get('error', 'unknown')}")
        except Exception as e:
            print(f"    ❌ 排名失败: {e}")
            ranking_results = {"error": f"排名失败: {str(e)}"}
        
        return {
            "position_info": position_info,
            "screening_results": screening_results,
            "ranking_results": ranking_results,
            "rejected": False
        }
    
    async def analyze_all_positions(self) -> List[Dict[str, Any]]:
        """分析所有职位"""
        print(f"🚀 开始分析 {len(self.positions_data)} 个职位...")
        
        self.analysis_results = []
        
        for i, position_data in enumerate(self.positions_data.iterrows(), 1):
            print(f"\n📋 处理职位 {i}/{len(self.positions_data)}")
            
            # 获取行数据
            _, row_data = position_data
            position_dict = row_data.to_dict()
            
            # 分析单个职位
            result = await self.analyze_single_position(position_dict)
            self.analysis_results.append(result)
            
            # 简短的间隔，避免API限制
            await asyncio.sleep(0.1)
        
        return self.analysis_results
    
    def generate_report(self, output_path: str = "resume_analysis_report.md") -> bool:
        """生成分析报告"""
        print(f"📝 生成分析报告...")
        
        try:
            create_markdown_report(self.analysis_results, self.experiences_data, output_path)
            return True
        except Exception as e:
            print(f"❌ 报告生成失败: {e}")
            return False
    
    def print_summary(self):
        """打印分析总结"""
        if not self.analysis_results:
            print("⚠️ 没有分析结果")
            return
        
        total = len(self.analysis_results)
        suitable = sum(1 for r in self.analysis_results if not r.get("rejected", False))
        rejected = total - suitable
        
        print("\n" + "="*50)
        print("📊 分析总结")
        print("="*50)
        print(f"📋 总职位数: {total}")
        print(f"✅ 推荐投递: {suitable} 个")
        print(f"🚫 不推荐投递: {rejected} 个")
        print(f"📈 推荐率: {suitable/total*100:.1f}%")
        print("="*50)
    
    async def run(self, config_path: str = "config_example.json", 
                  output_path: str = "resume_analysis_report.md") -> bool:
        """运行完整的分析流程"""
        print("🚀 启动简历优化分析...")
        print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)
        
        # 检查环境
        if not self.check_environment():
            return False
        
        # 加载数据
        if not self.load_data():
            return False
        
        # 初始化LLM管理器
        if not self.initialize_llm_manager():
            return False
        
        # 分析所有职位
        try:
            await self.analyze_all_positions()
        except KeyboardInterrupt:
            print("\n⚠️ 用户中断分析")
            return False
        except Exception as e:
            print(f"\n❌ 分析过程出错: {e}")
            return False
        
        # 生成报告
        if not self.generate_report(output_path):
            return False
        
        # 打印总结
        self.print_summary()
        
        print(f"\n⏰ 完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🎉 分析完成！")
        
        return True


async def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="简历优化分析工具")
    parser.add_argument("--config", "-c", default="config_example.json", 
                       help="配置文件路径 (默认: config_example.json)")
    parser.add_argument("--output", "-o", default="resume_analysis_report.md", 
                       help="输出报告路径 (默认: resume_analysis_report.md)")
    
    args = parser.parse_args()
    
    # 创建优化器实例
    optimizer = ResumeOptimizer()
    
    # 运行分析
    success = await optimizer.run(args.config, args.output)
    
    if success:
        print(f"\n✅ 报告已保存到: {args.output}")
    else:
        print("\n❌ 分析失败")
        exit(1)


if __name__ == "__main__":
    # 加载环境变量
    from dotenv import load_dotenv
    load_dotenv()
    
    # 运行主程序
    asyncio.run(main()) 