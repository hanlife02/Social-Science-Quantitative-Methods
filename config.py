#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration settings for the ethnic conflict analysis project.
"""

import os

# 确定当前脚本所在目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 文件路径
DATA_PATH = os.path.join(BASE_DIR, "data", "ethnic_conflict_data.csv")
OUTPUT_FIGURE_PATH = os.path.join(BASE_DIR, "output", "figures")
OUTPUT_RESULTS_PATH = os.path.join(BASE_DIR, "output", "results")

# 分析参数
LAG_YEARS = [1, 2, 3]  # 未来冲突分析的滞后年数
EXCLUDED_THRESHOLD = 3  # status_pwrrank <= 此值被视为排斥族群

# 可视化设置
FIGURE_DPI = 300  # 保存图像的DPI
FIGURE_FORMAT = "png"  # 保存图像的格式

# 是否使用稳健标准误
USE_ROBUST_SE = True

# 随机种子，确保结果可重复
RANDOM_SEED = 42