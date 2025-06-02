#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Model result interpretation module for ethnic conflict analysis.
"""

import numpy as np
import os
from scipy import stats

def ensure_output_dir(output_path):
    """Ensure output directory exists"""
    os.makedirs(output_path, exist_ok=True)

def interpret_results(model_results, output_path='output/results/'):
    """
    Interpret model results and calculate marginal effects
    
    Parameters:
    model_results (dict): Dictionary containing model results
    output_path (str): Path to save result files
    
    Returns:
    str: Results interpretation text
    """
    # Ensure output directory exists
    ensure_output_dir(output_path)
    
    # Get coefficient and significance from base model
    base_model = model_results['model1']
    excluded_coef = base_model.params['excluded']
    excluded_pvalue = base_model.pvalues['excluded']
    
    # Calculate marginal effect for exclusion status
    # Convert coefficient to probability change
    marginal_effect = np.exp(excluded_coef) / (1 + np.exp(excluded_coef)) - 0.5
    
    # Interpret basic results
    interpretation = "## Model Results Interpretation\n\n"
    
    if excluded_pvalue < 0.05:
        sig_status = "statistically significant"
        if excluded_coef > 0:
            direction = "positive"
            conclusion = "excluded groups are indeed more likely to engage in armed conflict"
        else:
            direction = "negative"
            conclusion = "excluded groups are actually less likely to engage in armed conflict"
    else:
        sig_status = "not significant"
        conclusion = "we cannot confirm a definite relationship between exclusion status and armed conflict"
    
    interpretation += f"1. Effect of exclusion on conflict: coefficient is {excluded_coef:.4f}, {sig_status} (p={excluded_pvalue:.4f}), with a {direction} direction.\n"
    interpretation += f"   This means that {conclusion}.\n\n"
    
    # Interpret interaction effects
    model3 = model_results['model3']
    model4 = model_results['model4']
    
    # Moderating effect of geographic concentration
    if 'excluded:geo_concentrated' in model3.params:
        interaction_coef = model3.params['excluded:geo_concentrated']
        interaction_pvalue = model3.pvalues['excluded:geo_concentrated']
        
        if interaction_pvalue < 0.05:
            if interaction_coef > 0:
                conc_effect = "strengthens"
            else:
                conc_effect = "weakens"
            interpretation += f"2. Moderating effect of geographic concentration: interaction coefficient is {interaction_coef:.4f}, statistically significant (p={interaction_pvalue:.4f}).\n"
            interpretation += f"   This indicates that geographic concentration {conc_effect} the effect of exclusion on conflict.\n\n"
        else:
            interpretation += f"2. Moderating effect of geographic concentration: interaction coefficient is {interaction_coef:.4f}, but not significant (p={interaction_pvalue:.4f}).\n"
            interpretation += "   We cannot confirm that geographic concentration moderates the exclusion-conflict relationship.\n\n"
    
    # Moderating effect of prior governance experience
    if 'excluded:upgraded10' in model4.params:
        interaction_coef = model4.params['excluded:upgraded10']
        interaction_pvalue = model4.pvalues['excluded:upgraded10']
        
        if interaction_pvalue < 0.05:
            if interaction_coef > 0:
                exp_effect = "strengthens"
            else:
                exp_effect = "weakens"
            interpretation += f"3. Moderating effect of prior governance experience: interaction coefficient is {interaction_coef:.4f}, statistically significant (p={interaction_pvalue:.4f}).\n"
            interpretation += f"   This indicates that prior governance experience {exp_effect} the effect of exclusion on conflict.\n\n"
        else:
            interpretation += f"3. Moderating effect of prior governance experience: interaction coefficient is {interaction_coef:.4f}, but not significant (p={interaction_pvalue:.4f}).\n"
            interpretation += "   We cannot confirm that prior governance experience moderates the exclusion-conflict relationship.\n\n"
    
    # Overall conclusion
    interpretation += "## Overall Conclusion\n\n"
    interpretation += f"Based on the above analysis, {conclusion}."
    
    if 'excluded:geo_concentrated' in model3.params and model3.pvalues['excluded:geo_concentrated'] < 0.05:
        interpretation += f" Additionally, geographic concentration {conc_effect} this relationship."
    
    if 'excluded:upgraded10' in model4.params and model4.pvalues['excluded:upgraded10'] < 0.05:
        interpretation += f" Furthermore, prior governance experience {exp_effect} this relationship."
    
    # Save interpretation to file
    with open(os.path.join(output_path, 'model_interpretation.md'), 'w') as f:
        f.write(interpretation)

    return interpretation

# 添加更精确的解释函数
def interpret_improved_results(model_results, df, output_path='output/results/'):
    """
    更精确地解释模型结果，包括边际效应和交互作用
    
    参数:
    model_results (dict): 包含模型结果的字典
    df (DataFrame): 原始数据框
    output_path (str): 结果保存路径
    
    返回:
    str: 结果解释文本
    """
    # 确保输出目录存在
    ensure_output_dir(output_path)
    
    # 开始解释
    interpretation = "# 族群政治排斥与武装冲突的关系：详细分析\n\n"
    
    # 1. 描述性统计摘要
    interpretation += "## 1. 描述性统计\n\n"
    
    # 计算比率并格式化
    excluded_pct = df['excluded'].mean() * 100
    conflict_by_exclusion = df.groupby('excluded')['any_conflict'].mean()
    ratio = conflict_by_exclusion[1] / conflict_by_exclusion[0] if conflict_by_exclusion[0] > 0 else float('inf')
    
    interpretation += f"- **排除族群比例**: {excluded_pct:.2f}%\n"
    interpretation += f"- **包容族群冲突率**: {conflict_by_exclusion[0]:.4f}\n"
    interpretation += f"- **排斥族群冲突率**: {conflict_by_exclusion[1]:.4f}\n"
    interpretation += f"- **比率**: 排斥族群的冲突率是包容族群的 {ratio:.2f} 倍\n\n"
    
    # 按地理聚集度和排斥状态分析
    cross_tab = df.groupby(['excluded', 'geo_concentrated'])['any_conflict'].mean().reset_index()
    cross_tab_pivot = cross_tab.pivot(index='excluded', columns='geo_concentrated', values='any_conflict')
    
    interpretation += "### 地理聚集度与排斥状态的交叉分析\n\n"
    interpretation += "| 族群类型 | 地理分散 | 地理聚集 |\n"
    interpretation += "|---------|---------|--------|\n"
    
    if not cross_tab_pivot.empty and 0 in cross_tab_pivot.columns and 1 in cross_tab_pivot.columns:
        interpretation += f"| 包容族群 | {cross_tab_pivot.loc[0, 0]:.4f} | {cross_tab_pivot.loc[0, 1]:.4f} |\n"
        interpretation += f"| 排斥族群 | {cross_tab_pivot.loc[1, 0]:.4f} | {cross_tab_pivot.loc[1, 1]:.4f} |\n\n"
        
        dispersed_effect = cross_tab_pivot.loc[1, 0] - cross_tab_pivot.loc[0, 0]
        concentrated_effect = cross_tab_pivot.loc[1, 1] - cross_tab_pivot.loc[0, 1]
        
        interpretation += f"- 对地理分散族群，排斥增加了 {dispersed_effect:.4f} 的冲突概率\n"
        interpretation += f"- 对地理聚集族群，排斥增加了 {concentrated_effect:.4f} 的冲突概率\n"
        interpretation += f"- 排斥效应的差异: {abs(dispersed_effect - concentrated_effect):.4f}\n\n"
    
    # 2. 基础模型解释
    interpretation += "## 2. 基础模型结果\n\n"
    
    if 'model1' in model_results:
        base_model = model_results['model1']
        excluded_coef = base_model.params['excluded']
        excluded_pvalue = base_model.pvalues['excluded']
        
        interpretation += f"- **排斥系数**: {excluded_coef:.4f} ({'+' if excluded_coef > 0 else ''}{excluded_coef:.4f})\n"
        interpretation += f"- **p值**: {excluded_pvalue:.4f}\n"
        interpretation += f"- **显著性**: {'***' if excluded_pvalue < 0.01 else '**' if excluded_pvalue < 0.05 else '*' if excluded_pvalue < 0.1 else '不显著'}\n"
        
        # 转换为概率变化
        excluded_odds = np.exp(excluded_coef)
        prob_change = (excluded_odds / (1 + excluded_odds)) - 0.5
        
        interpretation += f"- **优势比**: {excluded_odds:.4f}，表明排斥族群发生冲突的几率是包容族群的 {excluded_odds:.2f} 倍\n"
        interpretation += f"- **边际效应**: {prob_change:.4f}\n\n"
    
    # 3. 完整模型解释
    interpretation += "## 3. 完整模型结果\n\n"
    
    if 'model5' in model_results:
        full_model = model_results['model5']
        
        # 提取所有系数和p值
        coef_table = "| 变量 | 系数 | 标准误 | p值 | 显著性 |\n"
        coef_table += "|------|------|--------|-----|--------|\n"
        
        for var, coef in full_model.params.items():
            if var == 'Intercept':
                continue
            p_val = full_model.pvalues[var]
            std_err = full_model.bse[var]
            stars = '***' if p_val < 0.01 else '**' if p_val < 0.05 else '*' if p_val < 0.1 else ''
            coef_table += f"| {var} | {coef:.4f} | {std_err:.4f} | {p_val:.4f} | {stars} |\n"
        
        interpretation += coef_table + "\n"
    
    # 4. 交互效应的详细解释
    interpretation += "## 4. 交互效应分析\n\n"
    
    if 'model5' in model_results:
        full_model = model_results['model5']
        
        # 地理聚集度的交互效应
        geo_coef = full_model.params.get('geo_concentrated', 0)
        excluded_coef = full_model.params.get('excluded', 0)
        interaction_coef = full_model.params.get('excluded:geo_concentrated', 0)
        
        interpretation += "### 地理聚集度的调节作用\n\n"
        interpretation += f"- **地理聚集基础效应**: {geo_coef:.4f}\n"
        interpretation += f"- **排斥基础效应**: {excluded_coef:.4f}\n"
        interpretation += f"- **交互效应**: {interaction_coef:.4f}\n\n"
        
        # 计算不同条件下的总效应
        interpretation += "#### 不同条件下的总效应\n\n"
        interpretation += "| 族群类型 | 地理分散 | 地理聚集 | 差异 |\n"
        interpretation += "|---------|---------|--------|------|\n"
        interpretation += f"| 包容族群 | 0 | {geo_coef:.4f} | {geo_coef:.4f} |\n"
        interpretation += f"| 排斥族群 | {excluded_coef:.4f} | {excluded_coef + geo_coef + interaction_coef:.4f} | {geo_coef + interaction_coef:.4f} |\n"
        interpretation += f"| 排斥的边际效应 | {excluded_coef:.4f} | {excluded_coef + interaction_coef:.4f} | {interaction_coef:.4f} |\n\n"
        
        # 解释交互效应的含义
        if interaction_coef > 0:
            interpretation += "这表明地理聚集**增强**了排斥对冲突的影响，即地理聚集的排斥族群与地理分散的排斥族群相比，冲突概率的增加更为明显。\n\n"
        else:
            interpretation += "这表明地理聚集**减弱**了排斥对冲突的影响，即地理聚集的排斥族群与地理分散的排斥族群相比，冲突概率的增加较小。\n\n"
        
    # 5. 未来冲突分析
    interpretation += "## 5. 未来冲突分析\n\n"
    
    if 'model1f' in model_results:
        future_model = model_results['model1f']
        future_excluded_coef = future_model.params['excluded']
        future_excluded_pvalue = future_model.pvalues['excluded']
        
        interpretation += f"- **排斥对未来冲突的系数**: {future_excluded_coef:.4f}\n"
        interpretation += f"- **p值**: {future_excluded_pvalue:.4f}\n"
        interpretation += f"- **显著性**: {'***' if future_excluded_pvalue < 0.01 else '**' if future_excluded_pvalue < 0.05 else '*' if future_excluded_pvalue < 0.1 else '不显著'}\n\n"
        
        # 对比当前和未来影响
        if 'model1' in model_results:
            current_coef = model_results['model1'].params['excluded']
            interpretation += f"- **当前vs未来比较**: 排斥对当前冲突的系数为{current_coef:.4f}，对未来冲突的系数为{future_excluded_coef:.4f}\n"
            
            if abs(current_coef) > abs(future_excluded_coef):
                interpretation += "  这表明排斥对当前冲突的影响比对未来冲突更强。\n\n"
            else:
                interpretation += "  这表明排斥对未来冲突的影响与对当前冲突相当或更强。\n\n"
    
    # 6. 主要发现总结
    interpretation += "## 6. 主要发现总结\n\n"
    
    # 根据模型结果确定主要发现
    if 'model1' in model_results:
        base_model = model_results['model1']
        excluded_coef = base_model.params['excluded']
        excluded_pvalue = base_model.pvalues['excluded']
        
        if excluded_coef > 0 and excluded_pvalue < 0.05:
            interpretation += "1. **排斥显著增加冲突风险**: 被政治排斥的族群确实更容易参与武装冲突，这一效应在统计上高度显著。\n\n"
        else:
            interpretation += "1. **排斥与冲突的关系不确定**: 研究未能确定排斥状态与武装冲突之间存在稳健的统计关系。\n\n"
    
    if 'model5' in model_results:
        full_model = model_results['model5']
        if 'excluded:geo_concentrated' in full_model.params:
            interaction_coef = full_model.params['excluded:geo_concentrated'] 
            interaction_pvalue = full_model.pvalues['excluded:geo_concentrated']
            
            if abs(interaction_coef) > 0 and interaction_pvalue < 0.05:
                if interaction_coef > 0:
                    interpretation += "2. **地理聚集度强化排斥效应**: 研究发现地理聚集显著增强了排斥对冲突的影响。\n\n"
                else:
                    interpretation += "2. **地理聚集度减弱排斥效应**: 研究发现地理聚集显著减弱了排斥对冲突的影响。\n\n"
            else:
                interpretation += "2. **地理聚集度的调节作用不显著**: 研究未发现地理聚集对排斥-冲突关系有显著的调节作用。\n\n"
    
    # 7. 研究问题的直接回答
    interpretation += "## 7. 研究问题的直接回答\n\n"
    interpretation += "### 问题：被排斥的族群是否更容易在之后某一年参与武装冲突？\n\n"
    
    if 'model1f' in model_results:
        future_model = model_results['model1f']
        future_excluded_coef = future_model.params['excluded']
        future_excluded_pvalue = future_model.pvalues['excluded']
        
        if future_excluded_coef > 0 and future_excluded_pvalue < 0.05:
            interpretation += "**答案：是的**\n\n"
            interpretation += "研究结果表明，被政治排斥的族群确实更容易在之后参与武装冲突。这一发现具有统计显著性，"
            interpretation += f"系数为{future_excluded_coef:.4f}，p值为{future_excluded_pvalue:.4f}。\n\n"
            
            # 添加描述性证据
            future_conflict_by_exclusion = df.groupby('excluded')['future_conflict_1yr'].mean()
            interpretation += f"描述性统计显示，排斥族群在未来一年的冲突发生率为{future_conflict_by_exclusion[1]:.4f}，"
            interpretation += f"而包容族群为{future_conflict_by_exclusion[0]:.4f}，前者是后者的{future_conflict_by_exclusion[1]/future_conflict_by_exclusion[0]:.2f}倍。\n\n"
        elif future_excluded_pvalue < 0.05:
            interpretation += "**答案：否，相反**\n\n"
            interpretation += "研究结果表明，被政治排斥的族群反而不太容易在之后参与武装冲突。这与我们的假设相反。\n\n"
        else:
            interpretation += "**答案：无法确定**\n\n"
            interpretation += "研究未能找到被排斥族群更容易在之后参与武装冲突的显著证据。\n\n"
    
    # 保存到文件
    with open(os.path.join(output_path, 'improved_interpretation.md'), 'w') as f:
        f.write(interpretation)
    
    # 同时生成中文和英文版本
    with open(os.path.join(output_path, 'interpretation_chinese.md'), 'w') as f:
        f.write(interpretation)
    
    # 为了保持与原来的interpretation.md兼容
    with open(os.path.join(output_path, 'model_interpretation.md'), 'w') as f:
        f.write(interpretation)
    
    return interpretation

# 直接回答研究问题的函数
def answer_research_questions(model_results, df, output_path='output/results/'):
    """
    直接回答研究问题，使结果更加明确
    
    参数:
    model_results (dict): 包含模型结果的字典
    df (DataFrame): 原始数据框
    output_path (str): 结果保存路径
    
    返回:
    str: 研究问题回答
    """
    # 确保输出目录存在
    ensure_output_dir(output_path)
    
    answers = "# 研究问题的明确回答\n\n"
    
    # 问题1: 排斥族群是否更容易参与冲突
    if 'model1f' in model_results:
        future_model = model_results['model1f']
        future_excluded_coef = future_model.params['excluded']
        future_excluded_pvalue = future_model.pvalues['excluded']
        significant = future_excluded_pvalue < 0.05
        
        answers += "## 问题1: 被排斥的族群是否更容易在之后某一年参与武装冲突?\n\n"
        
        if significant and future_excluded_coef > 0:
            answers += "**答案: 是的**\n\n"
            answers += f"被排斥的族群确实更容易在之后某一年参与武装冲突。模型结果显示，排斥变量的系数为 {future_excluded_coef:.4f}，"
            answers += f"在p<{future_excluded_pvalue:.4f}水平上显著为正。这表明，控制其他因素后，排斥族群参与武装冲突的概率显著高于非排斥族群。\n\n"
            
            # 添加具体数值
            future_conflict_by_exclusion = df.groupby('excluded')['future_conflict_1yr'].mean()
            if 0 in future_conflict_by_exclusion.index and 1 in future_conflict_by_exclusion.index and future_conflict_by_exclusion[0] > 0:
                ratio = future_conflict_by_exclusion[1] / future_conflict_by_exclusion[0]
                
                answers += f"具体而言，排斥族群的未来冲突发生率为{future_conflict_by_exclusion[1]:.4f}，而非排斥族群为{future_conflict_by_exclusion[0]:.4f}，"
                answers += f"前者是后者的{ratio:.2f}倍。\n\n"
            
        elif significant and future_excluded_coef < 0:
            answers += "**答案: 否，相反**\n\n"
            answers += f"研究结果表明，被排斥的族群反而不太容易在之后参与武装冲突。模型显示排斥变量的系数为{future_excluded_coef:.4f}，"
            answers += f"在p<{future_excluded_pvalue:.4f}水平上显著为负。这与初始假设相反。\n\n"
        else:
            answers += "**答案: 证据不足**\n\n"
            answers += "研究未能找到被排斥族群更容易在之后参与武装冲突的显著证据。"
    
    # 问题2: 地理聚集度如何影响这种关系
    if 'model5f' in model_results:
        full_model = model_results['model5f']
        if 'excluded:geo_concentrated' in full_model.params:
            interaction_coef = full_model.params['excluded:geo_concentrated']
            interaction_pvalue = full_model.pvalues['excluded:geo_concentrated']
            
            answers += "## 问题2: 地理聚集度如何影响排斥与冲突的关系?\n\n"
            
            if interaction_pvalue < 0.05:
                if interaction_coef > 0:
                    answers += "**答案: 地理聚集增强了关系**\n\n"
                    answers += f"研究发现，地理聚集显著增强了排斥族群参与未来武装冲突的可能性。交互项系数为{interaction_coef:.4f}，"
                    answers += f"在p<{interaction_pvalue:.4f}水平上显著为正。这表明，对于地理上聚集的排斥族群，在未来参与冲突的可能性进一步增加。\n\n"
                    
                    # 添加描述性统计证据
                    cross_tab = df.groupby(['excluded', 'geo_concentrated'])['future_conflict_1yr'].mean()
                    if (0,0) in cross_tab.index and (0,1) in cross_tab.index and (1,0) in cross_tab.index and (1,1) in cross_tab.index:
                        dispersed_diff = cross_tab[1,0] - cross_tab[0,0]
                        concentrated_diff = cross_tab[1,1] - cross_tab[0,1]
                        
                        answers += "描述性统计显示:\n\n"
                        answers += f"- 对于地理分散族群，排斥增加了{dispersed_diff:.4f}的未来冲突概率\n"
                        answers += f"- 对于地理聚集族群，排斥增加了{concentrated_diff:.4f}的未来冲突概率\n"
                        answers += f"- 地理聚集确实增强了排斥效应，差异为{concentrated_diff-dispersed_diff:.4f}\n\n"
                    
                else:
                    answers += "**答案: 地理聚集减弱了关系**\n\n"
                    answers += f"研究发现，地理聚集显著减弱了排斥族群参与未来武装冲突的可能性。交互项系数为{interaction_coef:.4f}，"
                    answers += f"在p<{interaction_pvalue:.4f}水平上显著为负。这表明，地理聚集可能减轻了排斥对未来冲突的促进作用。\n\n"
            else:
                answers += "**答案: 无显著影响**\n\n"
                answers += "研究未发现地理聚集度对排斥与未来冲突之间关系有显著的调节作用。"
    
    # 问题3: 执政经验如何影响这种关系
    if 'model5f' in model_results:
        full_model = model_results['model5f']
        if 'excluded:upgraded10' in full_model.params:
            interaction_coef = full_model.params['excluded:upgraded10']
            interaction_pvalue = full_model.pvalues['excluded:upgraded10']
            
            answers += "## 问题3: 执政经验如何影响排斥与冲突的关系?\n\n"
            
            if interaction_pvalue < 0.05:
                if interaction_coef > 0:
                    answers += "**答案: 执政经验增强了关系**\n\n"
                    answers += f"研究发现，过去的执政经验显著增强了排斥族群参与未来武装冲突的可能性。交互项系数为{interaction_coef:.4f}，"
                    answers += f"在p<{interaction_pvalue:.4f}水平上显著为正。\n\n"
                else:
                    answers += "**答案: 执政经验减弱了关系**\n\n"
                    answers += f"研究发现，过去的执政经验显著减弱了排斥族群参与未来武装冲突的可能性。交互项系数为{interaction_coef:.4f}，"
                    answers += f"在p<{interaction_pvalue:.4f}水平上显著为负。这可能表明，有执政经验的族群即使被排斥，也比没有执政经验的排斥族群更不倾向于使用武力。\n\n"
            else:
                answers += "**答案: 无显著影响**\n\n"
                answers += "研究未发现执政经验对排斥与未来冲突之间关系有显著的调节作用。"
    
    # 保存到文件
    with open(os.path.join(output_path, 'research_questions_answers.md'), 'w') as f:
        f.write(answers)
    
    return answers