#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Model result interpretation module for ethnic conflict analysis.
"""

import numpy as np
import os
from config import OUTPUT_RESULTS_PATH

def ensure_output_dir():
    """Ensure output directory exists"""
    os.makedirs(OUTPUT_RESULTS_PATH, exist_ok=True)

def interpret_results(model_results):
    """
    Interpret model results and calculate marginal effects.
    
    Parameters:
    model_results (dict): Dictionary containing model results
    
    Returns:
    str: Results interpretation text
    """
    # Ensure output directory exists
    ensure_output_dir()
    
    # Current conflict models interpretation
    current_interpretation = interpret_current_conflict_models(model_results)
    
    # Future conflict models interpretation
    future_interpretation = interpret_future_conflict_models(model_results)
    
    # Combine interpretations
    interpretation = "# Ethnic Group Exclusion and Armed Conflict Analysis\n\n"
    interpretation += "## 1. Current Conflict Analysis\n\n"
    interpretation += current_interpretation
    interpretation += "\n\n## 2. Future Conflict Analysis\n\n"
    interpretation += future_interpretation
    
    # Save interpretation to file
    with open(os.path.join(OUTPUT_RESULTS_PATH, "model_interpretation.md"), "w") as f:
        f.write(interpretation)
    
    return interpretation

def interpret_current_conflict_models(model_results):
    """
    Interpret results for current conflict models.
    
    Parameters:
    model_results (dict): Dictionary containing model results
    
    Returns:
    str: Interpretation text for current conflict models
    """
    # Get coefficient and significance from base model
    base_model = model_results['model1']
    excluded_coef = base_model.params['excluded']
    excluded_pvalue = base_model.pvalues['excluded']
    
    # Calculate marginal effect for exclusion status
    # Convert coefficient to probability change
    marginal_effect = np.exp(excluded_coef) / (1 + np.exp(excluded_coef)) - 0.5
    
    # Interpret basic results
    interpretation = "### Current Conflict Models Interpretation\n\n"
    
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
    
    interpretation += f"1. Effect of exclusion on current conflict: coefficient is {excluded_coef:.4f}, {sig_status} (p={excluded_pvalue:.4f}), with a {direction} direction.\n"
    interpretation += f"   This means that {conclusion} in the same year.\n\n"
    
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
    
    return interpretation

def interpret_future_conflict_models(model_results):
    """
    Interpret results for future conflict models.
    
    Parameters:
    model_results (dict): Dictionary containing model results
    
    Returns:
    str: Interpretation text for future conflict models
    """
    # Get coefficient and significance from future base model
    base_model = model_results['model1f']
    excluded_coef = base_model.params['excluded']
    excluded_pvalue = base_model.pvalues['excluded']
    
    # Interpret basic results
    interpretation = "### Future Conflict Models Interpretation\n\n"
    
    if excluded_pvalue < 0.05:
        sig_status = "statistically significant"
        if excluded_coef > 0:
            direction = "positive"
            conclusion = "excluded groups are indeed more likely to engage in armed conflict in the following year"
        else:
            direction = "negative"
            conclusion = "excluded groups are actually less likely to engage in armed conflict in the following year"
    else:
        sig_status = "not significant"
        conclusion = "we cannot confirm a definite relationship between exclusion status and future armed conflict"
    
    interpretation += f"1. Effect of exclusion on future conflict: coefficient is {excluded_coef:.4f}, {sig_status} (p={excluded_pvalue:.4f}), with a {direction} direction.\n"
    interpretation += f"   This means that {conclusion}.\n\n"
    
    # Interpret interaction effects
    model3f = model_results['model3f']
    model4f = model_results['model4f']
    
    # Moderating effect of geographic concentration
    if 'excluded:geo_concentrated' in model3f.params:
        interaction_coef = model3f.params['excluded:geo_concentrated']
        interaction_pvalue = model3f.pvalues['excluded:geo_concentrated']
        
        if interaction_pvalue < 0.05:
            if interaction_coef > 0:
                conc_effect = "strengthens"
            else:
                conc_effect = "weakens"
            interpretation += f"2. Moderating effect of geographic concentration on future conflict: interaction coefficient is {interaction_coef:.4f}, statistically significant (p={interaction_pvalue:.4f}).\n"
            interpretation += f"   This indicates that geographic concentration {conc_effect} the effect of exclusion on future conflict.\n\n"
        else:
            interpretation += f"2. Moderating effect of geographic concentration on future conflict: interaction coefficient is {interaction_coef:.4f}, but not significant (p={interaction_pvalue:.4f}).\n"
            interpretation += "   We cannot confirm that geographic concentration moderates the exclusion-future conflict relationship.\n\n"
    
    # Moderating effect of prior governance experience
    if 'excluded:upgraded10' in model4f.params:
        interaction_coef = model4f.params['excluded:upgraded10']
        interaction_pvalue = model4f.pvalues['excluded:upgraded10']
        
        if interaction_pvalue < 0.05:
            if interaction_coef > 0:
                exp_effect = "strengthens"
            else:
                exp_effect = "weakens"
            interpretation += f"3. Moderating effect of prior governance experience on future conflict: interaction coefficient is {interaction_coef:.4f}, statistically significant (p={interaction_pvalue:.4f}).\n"
            interpretation += f"   This indicates that prior governance experience {exp_effect} the effect of exclusion on future conflict.\n\n"
        else:
            interpretation += f"3. Moderating effect of prior governance experience on future conflict: interaction coefficient is {interaction_coef:.4f}, but not significant (p={interaction_pvalue:.4f}).\n"
            interpretation += "   We cannot confirm that prior governance experience moderates the exclusion-future conflict relationship.\n\n"
    
    # Overall conclusion
    interpretation += "### Overall Conclusion on Future Conflict\n\n"
    interpretation += f"Based on the analysis of future conflict (one year ahead), {conclusion}."
    
    if 'excluded:geo_concentrated' in model3f.params and model3f.pvalues['excluded:geo_concentrated'] < 0.05:
        interpretation += f" Additionally, geographic concentration {conc_effect} this relationship."
    
    if 'excluded:upgraded10' in model4f.params and model4f.pvalues['excluded:upgraded10'] < 0.05:
        interpretation += f" Furthermore, prior governance experience {exp_effect} this relationship."
    
    return interpretation