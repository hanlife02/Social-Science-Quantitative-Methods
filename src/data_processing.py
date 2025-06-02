'''
Author: Ethan && ethan@hanlife02.com
Date: 2025-06-02 20:07:16
LastEditors: Ethan && ethan@hanlife02.com
LastEditTime: 2025-06-02 20:07:49
FilePath: /Social-Science-Quantitative-Methods/ethnic_conflict_analysis/src/data_processing.py
Description: 

Copyright (c) 2025 by Ethan, All Rights Reserved. 
'''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data loading and preprocessing module for ethnic conflict analysis.
"""

import pandas as pd
import numpy as np
import os

def load_and_preprocess_data(file_path):
    """
    Load CSV data and preprocess it for analysis.
    
    Parameters:
    file_path (str): Path to the CSV file
    
    Returns:
    DataFrame: Preprocessed data
    """
    # Read data
    df = pd.read_csv(file_path)
    
    # Check for missing values
    missing_values = df.isnull().sum()
    print("Missing value statistics:")
    print(missing_values)
    
    # Create exclusion indicator based on political status
    # status_pwrrank: 1-3 indicates exclusion, 4-7 indicates inclusion
    df['excluded'] = (df['status_pwrrank'] <= 3).astype(int)
    
    # Create comprehensive conflict indicator from different conflict levels
    df['any_conflict'] = (
        (df['incidence_flag'] == 1) | 
        (df['incidence_terr_flag'] == 1) | 
        (df['incidence_gov_flag'] == 1)
    ).astype(int)
    
    # Create group-country-year unique identifier for panel data analysis
    df['group_country_id'] = df['gwgroupid'].astype(str) + "_" + df['countries_gwid'].astype(str)
    
    # Ensure correct data types
    numeric_cols = ['year', 'status_pwrrank', 'upgraded10', 'geo_concentrated', 
                    'incidence_flag', 'incidence_terr_flag', 'incidence_gov_flag']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Create lagged variables for analyzing the effect of exclusion on future conflicts
    # Sort by group-country and year
    grouped = df.sort_values(['group_country_id', 'year'])
    
    # Create future conflict variables for each group-country combination
    for lag_year in [1, 2, 3]:
        df[f'future_conflict_{lag_year}yr'] = grouped.groupby('group_country_id')['any_conflict'].shift(-lag_year)
        
        # Fill missing values
        df[f'future_conflict_{lag_year}yr'] = df[f'future_conflict_{lag_year}yr'].fillna(0)
        
        # Ensure correct data type
        df[f'future_conflict_{lag_year}yr'] = df[f'future_conflict_{lag_year}yr'].astype(int)
    
    return df