"""
数据加载模块
负责读取职位描述Excel文件和个人经历JSON文件
支持多sheet和日期范围筛选
"""

import pandas as pd
import json
from typing import List, Dict, Any
from datetime import datetime


def load_config(config_path: str) -> dict:
    """
    加载配置文件
    
    Args:
        config_path (str): 配置文件路径
        
    Returns:
        dict: 配置信息
    """
    with open(config_path, 'r', encoding='utf-8') as file:
        config = json.load(file)
    
    print(f"加载配置: Excel文件={config['excel_file']}, Sheet={config['sheet_name']}")
    return config


def load_positions(config: dict) -> pd.DataFrame:
    """
    根据配置读取包含职位信息的Excel文件
    
    支持指定sheet和日期范围筛选
    
    Args:
        config (dict): 配置信息，包含excel_file、sheet_name、date_filter
        
    Returns:
        pd.DataFrame: 包含职位信息的DataFrame
    """
    # 读取指定sheet
    df = pd.read_excel(config['excel_file'], sheet_name=config['sheet_name'])
    print(f"从sheet '{config['sheet_name']}' 加载 {len(df)} 行数据")
    
    # 日期筛选
    if 'date_filter' in config:
        date_config = config['date_filter']
        date_column = date_config['column']
        
        if date_column not in df.columns:
            print(f"警告: 未找到日期列 '{date_column}'，跳过日期筛选")
        else:
            # 转换日期列为datetime格式
            df[date_column] = pd.to_datetime(df[date_column])
            
            start_date = pd.to_datetime(date_config['start_date'])
            end_date = pd.to_datetime(date_config['end_date'])
            
            # 筛选日期范围
            original_len = len(df)
            df = df[(df[date_column] >= start_date) & (df[date_column] <= end_date)]
            filtered_len = len(df)
            
            print(f"日期筛选 ({date_config['start_date']} 到 {date_config['end_date']}): {original_len} -> {filtered_len} 行")

    # 仅保留 status 为 None 的职位
    if 'status' in df.columns:
        before_status_len = len(df)
        df = df[df['status'].isna()]
        after_status_len = len(df)
        print(f"状态筛选 (status == None): {before_status_len} -> {after_status_len} 行")
    else:
        print("警告: 未找到 'status' 列，跳过状态筛选")
    
    print(f"最终加载 {len(df)} 个职位")
    return df


def load_positions_simple(file_path: str) -> pd.DataFrame:
    """
    简单读取Excel文件（保持向后兼容）
    
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
    
    # 测试简单加载（向后兼容）
    print("\n=== 测试简单加载 ===")
    positions = load_positions_simple("positions_example.xlsx")
    print(f"职位列: {list(positions.columns)}")
    
    if len(positions) > 0:
        first_position = get_position_info(positions.iloc[0])
        print(f"第一个职位: {first_position['company']} - {first_position['position']}")
    
    # 测试经历加载
    print("\n=== 测试经历加载 ===")
    experiences = load_experiences("experiences_example.json")
    print(f"第一个经历: {experiences[0]['title']}")
    
    print("\n数据加载器测试完成") 