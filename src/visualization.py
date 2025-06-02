#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data visualization module for ethnic conflict analysis.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

def ensure_output_dir(output_path):
    """Ensure output directory exists"""
    os.makedirs(output_path, exist_ok=True)

def save_figure(filepath, dpi=300):
    """Save figure with standard settings"""
    plt.savefig(filepath, dpi=dpi, bbox_inches='tight')
    print(f"Figure saved: {filepath}")

def create_visualizations(df, output_path='output/figures/'):
    """
    Create data visualizations with English titles and labels
    
    Parameters:
    df (DataFrame): Preprocessed data
    output_path (str): Path to save figures
    """
    # 确保输出目录存在
    ensure_output_dir(output_path)
    
    # 设置绘图风格
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
    save_figure(os.path.join(output_path, 'conflict_by_political_status.png'))
    plt.close()
    
    # Figure 2: Relationship between exclusion, geographic concentration and conflict
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
        save_figure(os.path.join(output_path, 'exclusion_concentration_conflict.png'))
        plt.close()
    
    # Figure 3: Relationship between exclusion, geographic concentration and future conflict
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
        save_figure(os.path.join(output_path, 'exclusion_concentration_future_conflict.png'))
        plt.close()
    
    # Figure 4: Relationship between exclusion, prior governance experience and conflict
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
        save_figure(os.path.join(output_path, 'exclusion_experience_conflict.png'))
        plt.close()
    
    # Figure 5: Relationship between exclusion, prior governance experience and future conflict
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
        save_figure(os.path.join(output_path, 'exclusion_experience_future_conflict.png'))
        plt.close()
    
    # Figure 6: Time trends
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
        save_figure(os.path.join(output_path, 'conflict_time_trend.png'))
        plt.close()

# 添加高级可视化函数
def create_advanced_visualizations(df, model_results, output_path='output/figures/'):
    """
    创建高级数据可视化以更好地理解模型结果
    
    参数:
    df (DataFrame): 预处理后的数据
    model_results (dict): 包含模型结果的字典
    output_path (str): 图表保存路径
    """
    # 确保输出目录存在
    ensure_output_dir(output_path)
    
    # 设置绘图风格
    sns.set_style("whitegrid")
    plt.rcParams.update({'font.size': 12})
    
    # 1. 预测概率图 - 展示排斥、地理聚集和冲突的关系
    try:
        plt.figure(figsize=(12, 8))
        
        # 生成预测数据点
        X_new = pd.DataFrame({
            'excluded': [0, 0, 1, 1],
            'geo_concentrated': [0, 1, 0, 1],
            'upgraded10': [0, 0, 0, 0]  # 固定为无执政经验
        })
        
        # 使用模型5预测概率
        model5 = model_results['model5']
        X_new['predicted_prob'] = model5.predict(X_new)
        
        # 创建分组条形图
        ax = sns.barplot(x='excluded', y='predicted_prob', hue='geo_concentrated',
                         data=X_new, palette=['lightblue', 'darkblue'])
        
        # 添加数据标签
        for i, p in enumerate(ax.patches):
            height = p.get_height()
            ax.text(p.get_x() + p.get_width()/2., height + 0.005,
                   f'{height:.3f}', ha="center", fontsize=10)
        
        plt.title('Predicted Probability of Conflict by Exclusion and Geographic Concentration', 
                  fontsize=14, pad=20)
        plt.xticks([0, 1], ['Included Groups', 'Excluded Groups'])
        plt.xlabel('Group Exclusion Status', fontsize=12)
        plt.ylabel('Predicted Probability of Conflict', fontsize=12)
        plt.legend(title='Geographic Concentration', labels=['Dispersed', 'Concentrated'])
        plt.tight_layout()
        save_figure(os.path.join(output_path, 'predicted_probability_plot.png'))
        plt.close()
    except Exception as e:
        print(f"无法创建预测概率图: {e}")
    
    # 2. 时间趋势的深入分析
    try:
        # 按年份、排斥状态和地理聚集度分析冲突趋势
        time_trend = df.groupby(['year', 'excluded', 'geo_concentrated'])['any_conflict'].mean().reset_index()
        
        plt.figure(figsize=(16, 8))
        
        # 创建时间趋势图，区分排斥状态和地理聚集度
        for excluded in [0, 1]:
            for geo in [0, 1]:
                subset = time_trend[(time_trend['excluded']==excluded) & 
                                    (time_trend['geo_concentrated']==geo)]
                
                if not subset.empty:
                    # 设置标签和样式
                    excluded_label = 'Excluded' if excluded == 1 else 'Included'
                    geo_label = 'Concentrated' if geo == 1 else 'Dispersed'
                    linestyle = '-' if geo == 1 else '--'
                    color = 'darkred' if excluded == 1 else 'darkblue'
                    
                    plt.plot(subset['year'], subset['any_conflict'], 
                            label=f"{excluded_label}, {geo_label}",
                            linestyle=linestyle, linewidth=2, marker='o' if geo == 1 else 's',
                            markersize=4, color=color, alpha=0.7 if geo == 0 else 1.0)
        
        plt.title('Conflict Trends by Exclusion Status and Geographic Concentration', fontsize=16, pad=20)
        plt.xlabel('Year', fontsize=14)
        plt.ylabel('Conflict Incidence Rate', fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.legend(title='Group Characteristics', fontsize=12)
        plt.tight_layout()
        save_figure(os.path.join(output_path, 'detailed_time_trend.png'))
        plt.close()
    except Exception as e:
        print(f"无法创建详细时间趋势图: {e}")
    
    # 3. ROC曲线比较图
    try:
        from sklearn.metrics import roc_curve, auc
        
        plt.figure(figsize=(10, 8))
        
        # 颜色和标签
        colors = ['blue', 'green', 'red', 'purple', 'orange']
        models = ['model1', 'model2', 'model3', 'model4', 'model5']
        labels = ['Base Model', 'Control Variables', 'Geo Interaction', 
                 'Experience Interaction', 'Full Model']
        
        for i, model_name in enumerate(models):
            if model_name in model_results:
                model = model_results[model_name]
                
                # 计算预测概率
                y_pred = model.predict(df)
                y_true = df['any_conflict']
                
                # 计算ROC曲线
                fpr, tpr, _ = roc_curve(y_true, y_pred)
                roc_auc = auc(fpr, tpr)
                
                # 绘制ROC曲线
                plt.plot(fpr, tpr, color=colors[i], lw=2,
                        label=f'{labels[i]} (AUC = {roc_auc:.3f})')
        
        # 绘制对角线
        plt.plot([0, 1], [0, 1], 'k--', lw=2)
        
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curves for Different Models')
        plt.legend(loc="lower right")
        
        plt.tight_layout()
        save_figure(os.path.join(output_path, 'roc_comparison.png'))
        plt.close()
    except Exception as e:
        print(f"无法创建ROC比较图: {e}")