'''
Author: Ethan && ethan@hanlife02.com
Date: 2025-06-02 20:07:16
LastEditors: Ethan && ethan@hanlife02.com
LastEditTime: 2025-06-02 20:07:59
FilePath: /Social-Science-Quantitative-Methods/ethnic_conflict_analysis/src/descriptive_stats.py
Description: 

Copyright (c) 2025 by Ethan, All Rights Reserved. 
'''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Descriptive statistics module for ethnic conflict analysis.
"""

import pandas as pd
import numpy as np

def generate_descriptive_stats(df):
    """
    Generate descriptive statistics tables and visualizations.
    
    Parameters:
    df (DataFrame): Preprocessed data
    
    Returns:
    dict: Containing descriptive statistics tables and charts
    """
    results = {}
    
    # Basic descriptive statistics
    desc_stats = df[['excluded', 'geo_concentrated', 'upgraded10', 'incidence_flag', 
                    'incidence_terr_flag', 'incidence_gov_flag', 'any_conflict',
                    'future_conflict_1yr', 'future_conflict_2yr', 'future_conflict_3yr']].describe()
    results['basic_stats'] = desc_stats
    
    # Percentage of excluded groups
    excluded_pct = df['excluded'].mean() * 100
    print(f"Percentage of excluded groups: {excluded_pct:.2f}%")
    
    # Conflict incidence rate by political status
    conflict_by_status = df.groupby('statusname')['any_conflict'].mean().sort_values(ascending=False)
    results['conflict_by_status'] = conflict_by_status
    
    # Future conflict incidence rate by political status (1 year ahead)
    future_conflict_by_status = df.groupby('statusname')['future_conflict_1yr'].mean().sort_values(ascending=False)
    results['future_conflict_by_status'] = future_conflict_by_status
    
    # Comparison of conflict between excluded and included groups
    conflict_by_exclusion = df.groupby('excluded')['any_conflict'].mean()
    results['conflict_by_exclusion'] = conflict_by_exclusion
    print("\nConflict incidence rate comparison between excluded and included groups:")
    print(f"Included groups (excluded=0): {conflict_by_exclusion[0]:.4f}")
    print(f"Excluded groups (excluded=1): {conflict_by_exclusion[1]:.4f}")
    
    # Comparison of future conflict between excluded and included groups
    future_conflict_by_exclusion = {}
    for lag_year in [1, 2, 3]:
        future_conflict = df.groupby('excluded')[f'future_conflict_{lag_year}yr'].mean()
        future_conflict_by_exclusion[lag_year] = future_conflict
        print(f"\nFuture conflict ({lag_year} year ahead) incidence rate comparison:")
        print(f"Included groups (excluded=0): {future_conflict[0]:.4f}")
        print(f"Excluded groups (excluded=1): {future_conflict[1]:.4f}")
    
    results['future_conflict_by_exclusion'] = future_conflict_by_exclusion
    
    # Cross tabulation: exclusion status and conflict incidence
    cross_tab = pd.crosstab(df['excluded'], df['any_conflict'], 
                           normalize='index', margins=True) * 100
    results['cross_tab'] = cross_tab
    
    # Cross tabulation: exclusion status and future conflict incidence
    future_cross_tab = pd.crosstab(df['excluded'], df['future_conflict_1yr'], 
                                  normalize='index', margins=True) * 100
    results['future_cross_tab'] = future_cross_tab
    
    return results