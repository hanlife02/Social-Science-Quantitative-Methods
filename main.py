#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main entry point for ethnic conflict analysis.
This script analyzes whether politically excluded ethnic groups are more likely to engage in armed conflict
in subsequent years, and how factors like geographic concentration and governance experience moderate this relationship.
"""

import os
import sys
import pandas as pd
import warnings

# 导入配置和模块
from config import DATA_PATH, OUTPUT_FIGURE_PATH, OUTPUT_RESULTS_PATH

# 导入各个功能模块
from src.data_processing import load_and_preprocess_data
from src.descriptive_stats import generate_descriptive_stats
from src.visualization import create_visualizations, create_advanced_visualizations
from src.modeling import build_statistical_models
from src.interpretation import interpret_results, interpret_improved_results, answer_research_questions

def setup_directories():
    """Set up output directories"""
    os.makedirs(OUTPUT_FIGURE_PATH, exist_ok=True)
    os.makedirs(OUTPUT_RESULTS_PATH, exist_ok=True)

def main(file_path=None):
    """
    Main function to coordinate the entire analysis workflow with improved methods
    
    Parameters:
    file_path (str, optional): Path to the CSV file
    """
    # 忽略警告，使输出更清晰
    warnings.filterwarnings('ignore')
    
    # 设置目录
    setup_directories()
    
    # 使用默认路径如果未提供
    if file_path is None:
        file_path = DATA_PATH
    
    print("Loading and preprocessing data...")
    df = load_and_preprocess_data(file_path)
    print(f"Data loading complete, {len(df)} records loaded\n")
    
    print("Generating descriptive statistics...")
    desc_stats = generate_descriptive_stats(df)
    print("Descriptive statistics complete\n")
    
    print("Creating standard visualizations...")
    create_visualizations(df, OUTPUT_FIGURE_PATH)
    print("Standard visualizations created\n")
    
    print("Building improved statistical models...")
    model_results = build_statistical_models(df)
    print("Model building complete\n")
    
    print("Creating advanced visualizations...")
    create_advanced_visualizations(df, model_results, OUTPUT_FIGURE_PATH)
    print("Advanced visualizations created\n")
    
    print("Interpreting results with improved methods...")
    interpretation = interpret_improved_results(model_results, df, OUTPUT_RESULTS_PATH)
    print("Detailed interpretation complete\n")
    
    print("Answering research questions directly...")
    answers = answer_research_questions(model_results, df, OUTPUT_RESULTS_PATH)
    print("Research questions answered\n")
    
    # 输出结果
    print("=" * 80)
    print("Model Regression Results:")
    print(model_results['summary_table'])
    if 'future_summary_table' in model_results:
        print("\nFuture Conflict Model Results:")
        print(model_results['future_summary_table'])
    print("\n" + "=" * 80)
    print("Key Findings:")
    print(answers)
    print("\n" + "=" * 80)
    print("Analysis complete! Results saved to output directory.")
    print(f"- Visualizations: {OUTPUT_FIGURE_PATH}")
    print(f"- Detailed results: {OUTPUT_RESULTS_PATH}")

if __name__ == "__main__":
    # 检查是否提供了文件路径作为命令行参数
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        main(file_path)
    else:
        main()