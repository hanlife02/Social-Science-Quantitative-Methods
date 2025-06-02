'''
Author: Ethan && ethan@hanlife02.com
Date: 2025-06-02 20:07:16
LastEditors: Ethan && ethan@hanlife02.com
LastEditTime: 2025-06-02 20:08:30
FilePath: /Social-Science-Quantitative-Methods/ethnic_conflict_analysis/main.py
Description: 

Copyright (c) 2025 by Ethan, All Rights Reserved. 
'''
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
from config import DATA_PATH, OUTPUT_FIGURE_PATH, OUTPUT_RESULTS_PATH

# Import modules
from src.data_processing import load_and_preprocess_data
from src.descriptive_stats import generate_descriptive_stats
from src.visualization import create_visualizations
from output.figures.modeling import build_statistical_models
from src.interpretation import interpret_results

def setup_directories():
    """Set up output directories"""
    os.makedirs(OUTPUT_FIGURE_PATH, exist_ok=True)
    os.makedirs(OUTPUT_RESULTS_PATH, exist_ok=True)

def main(file_path=None):
    """
    Main function to coordinate the entire analysis workflow.
    
    Parameters:
    file_path (str, optional): Path to the CSV file. Defaults to None, which will use the path from config.
    """
    # Set up directories
    setup_directories()
    
    # Use default path if not provided
    if file_path is None:
        file_path = DATA_PATH
    
    print("Loading and preprocessing data...")
    df = load_and_preprocess_data(file_path)
    print(f"Data loading complete, {len(df)} records loaded\n")
    
    print("Generating descriptive statistics...")
    desc_stats = generate_descriptive_stats(df)
    print("Descriptive statistics complete\n")
    
    print("Creating visualizations...")
    create_visualizations(df)
    print("Visualizations created\n")
    
    print("Building statistical models...")
    model_results = build_statistical_models(df)
    print("Model building complete\n")
    
    print("Interpreting results...")
    interpretation = interpret_results(model_results)
    print("Results interpretation complete\n")
    
    # Output results
    print("=" * 80)
    print("Model Regression Results (Current Conflict):")
    print(model_results['current_conflict_summary'])
    print("\nModel Regression Results (Future Conflict):")
    print(model_results['future_conflict_summary'])
    print("\n" + "=" * 80)
    print("Summary of findings saved to output/results/model_interpretation.md")

if __name__ == "__main__":
    # Check if file path is provided as command line argument
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        main(file_path)
    else:
        main()