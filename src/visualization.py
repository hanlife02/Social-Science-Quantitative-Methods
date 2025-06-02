#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data visualization module for ethnic conflict analysis.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from config import OUTPUT_FIGURE_PATH, FIGURE_DPI, FIGURE_FORMAT

def ensure_output_dir():
    """Ensure output directory exists"""
    os.makedirs(OUTPUT_FIGURE_PATH, exist_ok=True)

def save_figure(filename):
    """Save figure with standard settings"""
    filepath = os.path.join(OUTPUT_FIGURE_PATH, f"{filename}.{FIGURE_FORMAT}")
    plt.savefig(filepath, dpi=FIGURE_DPI, bbox_inches='tight')
    print(f"Figure saved: {filepath}")

def create_visualizations(df):
    """
    Create data visualizations with English titles and labels.
    
    Parameters:
    df (DataFrame): Preprocessed data
    """
    # Ensure output directory exists
    ensure_output_dir()
    
    # Set plot style
    sns.set_style("whitegrid")
    
    # Figure 1: Conflict incidence rate by political status
    plt.figure(figsize=(12, 6))
    status_conflict = df.groupby('statusname')['any_conflict'].mean().sort_values(ascending=True)
    ax = status_conflict.plot(kind='barh', color=sns.color_palette("viridis", 7))
    plt.title('Conflict Incidence Rate by Political Status', fontsize=14)
    plt.xlabel('Conflict Incidence Rate', fontsize=12)
    plt.ylabel('Political Status', fontsize=12)
    for i, v in enumerate(status_conflict):
        ax.text(v + 0.01, i, f'{v:.3f}', va='center')
    plt.tight_layout()
    save_figure('conflict_by_political_status')
    plt.close()
    
    # Figure 2: Future conflict incidence rate by political status (1 year ahead)
    plt.figure(figsize=(12, 6))
    future_status_conflict = df.groupby('statusname')['future_conflict_1yr'].mean().sort_values(ascending=True)
    ax = future_status_conflict.plot(kind='barh', color=sns.color_palette("viridis", 7))
    plt.title('Future Conflict Incidence Rate by Political Status (1 Year Ahead)', fontsize=14)
    plt.xlabel('Future Conflict Incidence Rate', fontsize=12)
    plt.ylabel('Political Status', fontsize=12)
    for i, v in enumerate(future_status_conflict):
        ax.text(v + 0.01, i, f'{v:.3f}', va='center')
    plt.tight_layout()
    save_figure('future_conflict_by_political_status')
    plt.close()
    
    # Figure 3: Relationship between exclusion, geographic concentration and conflict
    plt.figure(figsize=(10, 6))
    grouped_data = df.groupby(['excluded', 'geo_concentrated'])['any_conflict'].mean().reset_index()
    grouped_data = grouped_data.pivot(index='excluded', columns='geo_concentrated', values='any_conflict')
    
    if 0 in grouped_data.columns and 1 in grouped_data.columns:
        grouped_data.columns = ['Dispersed Groups', 'Concentrated Groups']
        ax = grouped_data.plot(kind='bar', color=['lightblue', 'darkblue'])
        plt.title('Relationship between Exclusion, Geographic Concentration and Conflict', fontsize=14)
        plt.xlabel('Group Exclusion Status', fontsize=12)
        plt.ylabel('Conflict Incidence Rate', fontsize=12)
        plt.xticks([0, 1], ['Included Groups', 'Excluded Groups'], rotation=0)
        plt.legend(title='Geographic Concentration')
        
        # Add value labels
        for container in ax.containers:
            ax.bar_label(container, fmt='%.3f')
            
        plt.tight_layout()
        save_figure('exclusion_concentration_conflict')
        plt.close()
    
    # Figure 4: Relationship between exclusion, geographic concentration and future conflict
    plt.figure(figsize=(10, 6))
    grouped_data = df.groupby(['excluded', 'geo_concentrated'])['future_conflict_1yr'].mean().reset_index()
    grouped_data = grouped_data.pivot(index='excluded', columns='geo_concentrated', values='future_conflict_1yr')
    
    if 0 in grouped_data.columns and 1 in grouped_data.columns:
        grouped_data.columns = ['Dispersed Groups', 'Concentrated Groups']
        ax = grouped_data.plot(kind='bar', color=['lightblue', 'darkblue'])
        plt.title('Relationship between Exclusion, Geographic Concentration and Future Conflict', fontsize=14)
        plt.xlabel('Group Exclusion Status', fontsize=12)
        plt.ylabel('Future Conflict Incidence Rate (1 Year Ahead)', fontsize=12)
        plt.xticks([0, 1], ['Included Groups', 'Excluded Groups'], rotation=0)
        plt.legend(title='Geographic Concentration')
        
        # Add value labels
        for container in ax.containers:
            ax.bar_label(container, fmt='%.3f')
            
        plt.tight_layout()
        save_figure('exclusion_concentration_future_conflict')
        plt.close()
    
    # Figure 5: Relationship between exclusion, prior governance experience and conflict
    plt.figure(figsize=(10, 6))
    grouped_data = df.groupby(['excluded', 'upgraded10'])['any_conflict'].mean().reset_index()
    grouped_data = grouped_data.pivot(index='excluded', columns='upgraded10', values='any_conflict')
    
    if 0 in grouped_data.columns and 1 in grouped_data.columns:
        grouped_data.columns = ['No Prior Experience', 'Prior Experience']
        ax = grouped_data.plot(kind='bar', color=['lightgreen', 'darkgreen'])
        plt.title('Relationship between Exclusion, Prior Governance Experience and Conflict', fontsize=14)
        plt.xlabel('Group Exclusion Status', fontsize=12)
        plt.ylabel('Conflict Incidence Rate', fontsize=12)
        plt.xticks([0, 1], ['Included Groups', 'Excluded Groups'], rotation=0)
        plt.legend(title='Prior Governance Experience')
        
        # Add value labels
        for container in ax.containers:
            ax.bar_label(container, fmt='%.3f')
            
        plt.tight_layout()
        save_figure('exclusion_experience_conflict')
        plt.close()
    
    # Figure 6: Relationship between exclusion, prior governance experience and future conflict
    plt.figure(figsize=(10, 6))
    grouped_data = df.groupby(['excluded', 'upgraded10'])['future_conflict_1yr'].mean().reset_index()
    grouped_data = grouped_data.pivot(index='excluded', columns='upgraded10', values='future_conflict_1yr')
    
    if 0 in grouped_data.columns and 1 in grouped_data.columns:
        grouped_data.columns = ['No Prior Experience', 'Prior Experience']
        ax = grouped_data.plot(kind='bar', color=['lightgreen', 'darkgreen'])
        plt.title('Relationship between Exclusion, Prior Governance Experience and Future Conflict', fontsize=14)
        plt.xlabel('Group Exclusion Status', fontsize=12)
        plt.ylabel('Future Conflict Incidence Rate (1 Year Ahead)', fontsize=12)
        plt.xticks([0, 1], ['Included Groups', 'Excluded Groups'], rotation=0)
        plt.legend(title='Prior Governance Experience')
        
        # Add value labels
        for container in ax.containers:
            ax.bar_label(container, fmt='%.3f')
            
        plt.tight_layout()
        save_figure('exclusion_experience_future_conflict')
        plt.close()
    
    # Figure 7: Time trends
    plt.figure(figsize=(14, 7))
    time_trend = df.groupby(['year', 'excluded'])['any_conflict'].mean().reset_index()
    time_trend_pivot = time_trend.pivot(index='year', columns='excluded', values='any_conflict')
    if 0 in time_trend_pivot.columns and 1 in time_trend_pivot.columns:
        time_trend_pivot.columns = ['Included Groups', 'Excluded Groups']
        ax = time_trend_pivot.plot(marker='o')
        plt.title('Time Trend of Conflict Incidence by Group Exclusion Status', fontsize=14)
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Conflict Incidence Rate', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        save_figure('conflict_time_trend')
        plt.close()