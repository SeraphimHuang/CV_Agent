"""
Markdown报告生成器
将LLM分析结果生成格式化的Markdown报告
"""

from typing import Dict, List, Any
from datetime import datetime


class MarkdownReportGenerator:
    """Markdown格式报告生成器"""
    
    def __init__(self):
        self.report_content = []
    
    def _add_line(self, line: str = ""):
        """添加一行内容到报告"""
        self.report_content.append(line)
    
    def _add_header(self, text: str, level: int = 1):
        """添加标题"""
        prefix = "#" * level
        self._add_line(f"{prefix} {text}")
        self._add_line()
    
    def _add_quote(self, text: str):
        """添加引用块"""
        self._add_line(f"> {text}")
        self._add_line()
    
    def _add_list_item(self, text: str, level: int = 0):
        """添加列表项"""
        indent = "  " * level
        self._add_line(f"{indent}- {text}")
    
    def _add_ordered_item(self, text: str, number: int):
        """添加有序列表项"""
        self._add_line(f"{number}. {text}")
    
    def _format_llm_results(self, llm_results: Dict[str, Dict[str, Any]], result_type: str) -> str:
        """格式化LLM结果为可读文本"""
        formatted_results = []
        
        for llm_name, result in llm_results.items():
            if result_type == "screening":
                citizenship = "有身份要求" if result.get("citizenship_required") else "无身份要求"
                senior_level = "要求高级别" if result.get("senior_level_required") else "不要求高级别"
                reason = result.get("reason", "无")
                formatted_results.append(f"**{llm_name.upper()}**: {citizenship}, {senior_level} - {reason}")
            
            elif result_type == "ranking":
                match_percentage = result.get("match_percentage", 0)
                error = result.get("error")
                if error:
                    formatted_results.append(f"**{llm_name.upper()}**: ❌ 调用失败 - {error}")
                else:
                    formatted_results.append(f"**{llm_name.upper()}**: 匹配度 {match_percentage}%")
        
        return formatted_results
    
    def _should_reject_position(self, screening_results: Dict[str, Dict[str, Any]]) -> tuple[bool, List[str]]:
        """
        判断是否应该拒绝该职位（>=2个LLM认为不合适）
        
        Returns:
            tuple: (是否拒绝, 拒绝原因列表)
        """
        rejection_count = 0
        rejection_reasons = []
        
        for llm_name, result in screening_results.items():
            citizenship_required = result.get("citizenship_required", False)
            senior_level_required = result.get("senior_level_required", False)
            
            if citizenship_required or senior_level_required:
                rejection_count += 1
                reasons = []
                if citizenship_required:
                    reasons.append("有身份要求")
                if senior_level_required:
                    reasons.append("要求高级别经验")
                rejection_reasons.append(f"{llm_name}: {', '.join(reasons)}")
        
        should_reject = rejection_count >= 2
        return should_reject, rejection_reasons
    
    def _aggregate_experience_rankings(self, ranking_results: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        聚合三个LLM的经历排名结果
        
        Returns:
            List[Dict]: 按总分排序的经历列表
        """
        experience_scores = {}
        
        # 收集所有LLM的排名
        for llm_name, result in ranking_results.items():
            if "error" in result:
                continue  # 跳过失败的LLM
                
            ranked_experiences = result.get("ranked_experiences", [])
            for exp in ranked_experiences:
                exp_id = exp.get("id")
                rank = exp.get("rank", 999)
                justification = exp.get("justification", "")
                
                if exp_id not in experience_scores:
                    experience_scores[exp_id] = {
                        "id": exp_id,
                        "total_score": 0,
                        "llm_rankings": {},
                        "count": 0
                    }
                
                experience_scores[exp_id]["total_score"] += rank
                experience_scores[exp_id]["llm_rankings"][llm_name] = {
                    "rank": rank,
                    "justification": justification
                }
                experience_scores[exp_id]["count"] += 1
        
        # 补齐缺失LLM评分：未出现的按5分计
        num_llms = len(ranking_results)
        for exp_data in experience_scores.values():
            missing = num_llms - exp_data["count"]
            if missing > 0:
                exp_data["total_score"] += missing * 5

        # 按总分排序（分数越低越好）
        sorted_experiences = sorted(
            experience_scores.values(),
            key=lambda x: x["total_score"]
        )
        
        # 返回所有出现过的经历，已按总分排序
        return sorted_experiences[:6]
    
    def generate_report(self, analysis_results: List[Dict[str, Any]], experiences_data: List[Dict[str, Any]]) -> str:
        """
        生成完整的Markdown报告
        
        Args:
            analysis_results: 所有职位的分析结果
            experiences_data: 经历数据（用于显示经历标题）
            
        Returns:
            str: Markdown格式的报告内容
        """
        self.report_content = []  # 重置报告内容
        
        # 报告标题和生成信息
        self._add_header("简历优化分析报告", 1)
        self._add_line(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self._add_line(f"**分析职位数量**: {len(analysis_results)}")
        self._add_line(f"**使用LLM**: Gemini 2.5, GPT-5-mini Claude-4-Sonnet")
        self._add_line()
        
        # 我们仅使用经历ID，不再依赖 title 字段
        
        # 统计信息
        suitable_count = 0
        rejected_count = 0
        
        for i, position_result in enumerate(analysis_results, 1):
            position_info = position_result["position_info"]
            screening_results = position_result["screening_results"]
            ranking_results = position_result.get("ranking_results", {})
            
            # 职位标题
            self._add_header(f"职位 {i}: {position_info['company']} - {position_info['position']}", 2)
            
            # 基本信息
            self._add_line("**基本信息**:")
            self._add_list_item(f"**公司**: {position_info['company']}")
            self._add_list_item(f"**职位**: {position_info['position']}")
            self._add_list_item(f"**地点**: {position_info['location']}")
            self._add_list_item(f"**链接**: {position_info['link']}")
            self._add_line()
            
            # 筛选结果
            should_reject, rejection_reasons = self._should_reject_position(screening_results)
            
            if should_reject:
                rejected_count += 1
                self._add_header("🚫 筛选结果：不推荐投递", 3)
                self._add_quote("❌ **该职位不符合投递条件，建议跳过**")
                
                self._add_line("**拒绝原因**:")
                for reason in rejection_reasons:
                    self._add_list_item(reason)
                self._add_line()
                
                self._add_line("**各LLM详细分析**:")
                llm_formatted = self._format_llm_results(screening_results, "screening")
                for result_line in llm_formatted:
                    self._add_list_item(result_line)
                self._add_line()
                
            else:
                suitable_count += 1
                self._add_header("✅ 筛选结果：推荐投递", 3)
                self._add_quote("✅ **该职位符合投递条件，建议准备申请材料**")
                
                # 筛选详情
                self._add_line("**各LLM筛选结果**:")
                llm_formatted = self._format_llm_results(screening_results, "screening")
                for result_line in llm_formatted:
                    self._add_list_item(result_line)
                self._add_line()
                
                # 如果有排名结果，显示推荐经历
                if ranking_results:
                    self._add_header("📝 推荐经历 Top ", 3)
                    
                    # 聚合排名结果
                    top_experiences = self._aggregate_experience_rankings(ranking_results)
                    
                    if top_experiences:
                        for rank, exp_data in enumerate(top_experiences, 1):
                            exp_id = exp_data["id"]
                            total_score = exp_data["total_score"]
                            
                            self._add_ordered_item(f"**{exp_id}** (总分: {total_score})", rank)
                            
                            # 显示各LLM的评价
                            for llm_name, ranking_info in exp_data["llm_rankings"].items():
                                llm_rank = ranking_info["rank"]
                                justification = ranking_info["justification"]
                                self._add_list_item(f"**{llm_name}** (排名{llm_rank}): {justification}", 1)
                            
                            self._add_line()
                    else:
                        self._add_quote("⚠️ 无法获取有效的经历排名结果")
                
                # LLM匹配度信息
                self._add_line("**各LLM匹配度评估**:")
                ranking_formatted = self._format_llm_results(ranking_results, "ranking")
                for result_line in ranking_formatted:
                    self._add_list_item(result_line)
                self._add_line()
            
            # 分隔线
            self._add_line("---")
            self._add_line()
        
        # 报告总结
        self._add_header("📊 分析总结", 2)
        self._add_list_item(f"**总职位数**: {len(analysis_results)}")
        self._add_list_item(f"**推荐投递**: {suitable_count} 个")
        self._add_list_item(f"**不推荐投递**: {rejected_count} 个")
        self._add_list_item(f"**推荐率**: {suitable_count/len(analysis_results)*100:.1f}%")
        
        return "\n".join(self.report_content)


def create_markdown_report(analysis_results: List[Dict[str, Any]], 
                          experiences_data: List[Dict[str, Any]], 
                          output_path: str) -> None:
    """
    创建Markdown格式的分析报告
    
    Args:
        analysis_results: 所有职位的分析结果
        experiences_data: 经历数据
        output_path: 输出文件路径
    """
    generator = MarkdownReportGenerator()
    report_content = generator.generate_report(analysis_results, experiences_data)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"✅ Markdown报告已生成: {output_path}")