#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Statistical modeling module for ethnic conflict analysis.
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from statsmodels.iolib.summary2 import summary_col
import os
import warnings

def build_statistical_models(df):
    """
    构建统计模型分析排斥与冲突的关系
    
    参数:
    df (DataFrame): 预处理后的数据
    
    返回:
    dict: 包含模型结果
    """
    warnings.filterwarnings('ignore')
    results = {}
    
    # 1. 使用不同优化方法和设置来解决收敛问题
    optimization_methods = {
        'bfgs': {'method': 'bfgs', 'maxiter': 1000},
        'newton': {'method': 'newton', 'maxiter': 1000},
        'lbfgs': {'method': 'lbfgs', 'maxiter': 1000}
    }
    
    # 找到最佳优化方法
    formula = 'any_conflict ~ excluded + geo_concentrated + upgraded10 + excluded:geo_concentrated + excluded:upgraded10'
    best_method = 'bfgs'  # 默认方法
    best_convergence = False
    best_result = None
    
    for method_name, method_params in optimization_methods.items():
        try:
            model = smf.logit(formula, data=df)
            result = model.fit(**method_params, disp=0)
            mle_retvals = getattr(result, 'mle_retvals', None)
            converged = mle_retvals.get('converged', False) if mle_retvals else False
            
            if converged:
                best_method = method_name
                best_convergence = True
                best_result = result
                break
            elif best_result is None:
                best_method = method_name
                best_result = result
        except Exception as e:
            continue
    
    print(f"使用的优化方法: {best_method}, 收敛状态: {best_convergence}")
    
    # 2. 构建标准模型但使用最佳优化方法
    # 模型1：基础模型 - 仅包含排斥状态
    model1 = smf.logit('any_conflict ~ excluded', data=df)
    result1 = model1.fit(**optimization_methods[best_method], disp=0)
    results['model1'] = result1
    
    # 模型2：加入控制变量
    model2 = smf.logit('any_conflict ~ excluded + geo_concentrated + upgraded10', data=df)
    result2 = model2.fit(**optimization_methods[best_method], disp=0)
    results['model2'] = result2
    
    # 模型3：加入交互项 - 排斥与族群聚集度
    model3 = smf.logit('any_conflict ~ excluded + geo_concentrated + upgraded10 + excluded:geo_concentrated', data=df)
    result3 = model3.fit(**optimization_methods[best_method], disp=0)
    results['model3'] = result3
    
    # 模型4：加入交互项 - 排斥与执政经验
    model4 = smf.logit('any_conflict ~ excluded + geo_concentrated + upgraded10 + excluded:upgraded10', data=df)
    result4 = model4.fit(**optimization_methods[best_method], disp=0)
    results['model4'] = result4
    
    # 模型5：完整模型 - 包含所有交互项
    model5 = smf.logit('any_conflict ~ excluded + geo_concentrated + upgraded10 + excluded:geo_concentrated + excluded:upgraded10', data=df)
    result5 = model5.fit(**optimization_methods[best_method], disp=0)
    results['model5'] = result5
    
    # 3. 使用更稳健的标准误
    # 为模型5添加稳健标准误
    try:
        cov_type = 'HC0'  # 使用White标准误
        robust_result5 = model5.fit(**optimization_methods[best_method], disp=0, cov_type=cov_type)
        results['robust_model5'] = robust_result5
        print("成功计算稳健标准误")
    except Exception as e:
        print(f"无法计算稳健标准误，使用常规标准误: {e}")
    
    # 4. 尝试使用混合效应模型(如果有族群和年份面板数据)
    try:
        from linearmodels.panel import PanelOLS
        
        # 设置面板数据
        panel_df = df.copy()
        panel_df['entity'] = panel_df['gwgroupid']
        panel_df['time'] = panel_df['year']
        panel_df = panel_df.set_index(['entity', 'time'])
        
        # 构建固定效应模型
        formula = 'any_conflict ~ 1 + excluded + geo_concentrated + excluded:geo_concentrated + EntityEffects + TimeEffects'
        mod = PanelOLS.from_formula(formula, data=panel_df)
        panel_results = mod.fit(cov_type='clustered', cluster_entity=True)
        results['panel_model'] = panel_results
        print("成功构建面板数据模型")
    except Exception as e:
        print(f"无法构建面板数据模型，回退到常规模型: {e}")
    
    # 5. 创建汇总表格
    model_names = ['Model 1', 'Model 2', 'Model 3', 'Model 4', 'Model 5']
    models_summary = summary_col(
        [result1, result2, result3, result4, result5],
        model_names=model_names,
        stars=True,
        info_dict={
            'N': lambda x: "{0:d}".format(int(x.nobs)),
            'Log-Likelihood': lambda x: "{:.2f}".format(x.llf),
            'AIC': lambda x: "{:.2f}".format(x.aic),
            'Pseudo R²': lambda x: "{:.4f}".format(x.prsquared),
        }
    )
    
    results['summary_table'] = models_summary
    
    # 6. 添加边际效应分析
    for model_name, model_result in [('model1', result1), ('model5', result5)]:
        try:
            # 计算平均边际效应
            margins = model_result.get_margeff(at='overall', method='dydx')
            results[f'{model_name}_margins'] = margins
            print(f"成功计算{model_name}的边际效应")
        except Exception as e:
            print(f"无法为{model_name}计算边际效应: {e}")
    
    # 7. 计算未来冲突的模型
    try:
        # 基础模型 - 排斥对未来冲突的影响
        model1f = smf.logit('future_conflict_1yr ~ excluded', data=df)
        result1f = model1f.fit(**optimization_methods[best_method], disp=0)
        results['model1f'] = result1f
        
        # 完整模型 - 包含交互项
        model5f = smf.logit('future_conflict_1yr ~ excluded + geo_concentrated + upgraded10 + excluded:geo_concentrated + excluded:upgraded10', data=df)
        result5f = model5f.fit(**optimization_methods[best_method], disp=0)
        results['model5f'] = result5f
        
        # 创建未来冲突汇总表
        future_model_names = ['Future Model 1', 'Future Model 5']
        future_models_summary = summary_col(
            [result1f, result5f],
            model_names=future_model_names,
            stars=True,
            info_dict={
                'N': lambda x: "{0:d}".format(int(x.nobs)),
                'Log-Likelihood': lambda x: "{:.2f}".format(x.llf),
                'AIC': lambda x: "{:.2f}".format(x.aic),
                'Pseudo R²': lambda x: "{:.4f}".format(x.prsquared),
            }
        )
        results['future_summary_table'] = future_models_summary
        print("成功构建未来冲突模型")
    except Exception as e:
        print(f"构建未来冲突模型时出错: {e}")
    
    return results

# 为了保持向后兼容，保留原函数名但使用新实现
build_improved_statistical_models = build_statistical_models