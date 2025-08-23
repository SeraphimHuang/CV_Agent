"""
将结构化的experiences.json 转为供LLM prompt使用的半结构化库字符串
"""

from typing import List, Dict

MAX_BULLETS = 6


def _truncate_bullets(bullets: List[str], max_len: int = MAX_BULLETS) -> List[str]:
    """保留前 max_len 条 bullet"""
    return bullets[:max_len]


def format_single_experience(exp: Dict) -> str:
    """根据type格式化单条经历"""
    t = exp.get("type", "unknown").lower()
    lines = []
    if t == "internship":
        header = f"[INTERNSHIP] {exp.get('company', '')} – {exp.get('role', '')}"
        if project := exp.get("project"):
            header += f"\nProject: {project}"
        tech = ", ".join(exp.get("tech_stack", []))
        if tech:
            header += f"\nTech: {tech}"
        lines.append(header)
    elif t == "project":
        header = f"[PROJECT] {exp.get('title')}"
        tech = ", ".join(exp.get("tech_stack", []))
        if tech:
            header += f"\nTech: {tech}"
        lines.append(header)
    elif t == "publication":
        title = exp.get("title")
        venue = exp.get("venue", "")
        year = exp.get("year", "")
        header = f"[PUBLICATION] {title} ({venue} {year})"
        lines.append(header)
    else:
        lines.append(f"[UNKNOWN] {exp.get('title', '')}")

    bullets = _truncate_bullets(exp.get("bullet_points", []))
    for bp in bullets:
        lines.append(f"• {bp}")
    lines.append("")  # 空行分隔
    return "\n".join(lines)


def format_experiences_library(experiences: List[Dict]) -> str:
    """将整个经历列表格式化为字符串"""
    blocks = [format_single_experience(exp) for exp in experiences]
    library = "\n".join(blocks)
    return f"==== 经历库 ====""\n" + library + "\n==== 结束====" 