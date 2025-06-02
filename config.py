'''
Author: Ethan && ethan@hanlife02.com
Date: 2025-06-02 20:07:16
LastEditors: Ethan && ethan@hanlife02.com
LastEditTime: 2025-06-02 20:07:39
FilePath: /Social-Science-Quantitative-Methods/ethnic_conflict_analysis/config.py
Description: 

Copyright (c) 2025 by Ethan, All Rights Reserved. 
'''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration settings for the ethnic conflict analysis project.
"""

# File paths
DATA_PATH = "data/ethnic_conflict_data.csv"
OUTPUT_FIGURE_PATH = "output/figures/"
OUTPUT_RESULTS_PATH = "output/results/"

# Analysis parameters
LAG_YEARS = [1, 2, 3]  # Years to lag for future conflict analysis
EXCLUDED_THRESHOLD = 3  # Status_pwrrank <= this value is considered excluded

# Visualization settings
FIGURE_DPI = 300  # DPI for saved figures
FIGURE_FORMAT = "png"  # Format for saved figures