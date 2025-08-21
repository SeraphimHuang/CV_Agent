"""
数据加载模块
负责读取职位描述Excel文件和个人经历JSON文件
"""

import pandas as pd
import json
from typing import List, Dict, Any


def load_positions(file_path: str) -> pd.DataFrame:
    """
    读取包含职位信息的Excel文件
    
    Excel文件包含列：job description、link、公司名字、岗位名、地点
    
    Args:
        file_path (str): Excel文件路径
        
    Returns:
        pd.DataFrame: 包含职位信息的DataFrame
    """
    df = pd.read_excel(file_path)
    print(f"成功加载 {len(df)} 个职位")
    return df


def load_experiences(file_path: str) -> List[Dict[str, Any]]:
    """
    读取包含个人经历的JSON文件
    
    Args:
        file_path (str): JSON文件路径
        
    Returns:
        List[Dict[str, Any]]: 包含个人经历的列表
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        experiences = json.load(file)
    
    print(f"成功加载 {len(experiences)} 个经历")
    return experiences


def get_position_info(position_row: pd.Series) -> Dict[str, str]:
    """
    从职位行中提取关键信息
    
    Args:
        position_row (pd.Series): 职位数据行
        
    Returns:
        Dict[str, str]: 包含职位关键信息的字典
    """
    return {
        'job_description': str(position_row['job description']),
        'company': str(position_row['公司名字']),
        'position': str(position_row['岗位名']),
        'location': str(position_row['地点']),
        'link': str(position_row['link'])
    }


if __name__ == "__main__":
    # 测试函数
    print("测试数据加载器...")
    
    # 测试加载示例数据
    positions = load_positions("positions_example.xlsx")
    print(f"职位列: {list(positions.columns)}")
    
    if len(positions) > 0:
        first_position = get_position_info(positions.iloc[0])
        print(f"第一个职位信息:")
        print(f"  公司: {first_position['company']}")
        print(f"  职位: {first_position['position']}")
        print(f"  地点: {first_position['location']}")
        print(f"  链接: {first_position['link']}")
        print(f"  职位描述长度: {len(first_position['job_description'])} 字符")
    
    experiences = load_experiences("experiences_example.json")
    print(f"第一个经历标题: {experiences[0]['title']}")
    
    print("数据加载器测试完成") 