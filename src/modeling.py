#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Statistical modeling module for ethnic conflict analysis.
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from statsmodels.iolib.summary2 import summary_col

def build_statistical_models(df):
    """
    Build statistical models to analyze the relationship between exclusion and conflict.
    
    Parameters:
    df (DataFrame): Preprocessed data
    
    Returns:
    dict: Containing model results
    """
    results = {}
    
    # Current conflict models
    
    # Model 1: Base model - exclusion status only
    model1 = smf.logit('any_conflict ~ excluded', data=df)
    result1 = model1.fit(disp=0, method='bfgs')
    results['model1'] = result1
    
    # Model 2: Add control variables
    model2 = smf.logit('any_conflict ~ excluded + geo_concentrated + upgraded10', data=df)
    result2 = model2.fit(disp=0, method='bfgs')
    results['model2'] = result2
    
    # Model 3: Add interaction term - exclusion and geographic concentration
    model3 = smf.logit('any_conflict ~ excluded + geo_concentrated + upgraded10 + excluded:geo_concentrated', data=df)
    result3 = model3.fit(disp=0, method='bfgs')
    results['model3'] = result3
    
    # Model 4: Add interaction term - exclusion and prior governance experience
    model4 = smf.logit('any_conflict ~ excluded + geo_concentrated + upgraded10 + excluded:upgraded10', data=df)
    result4 = model4.fit(disp=0, method='bfgs')
    results['model4'] = result4
    
    # Model 5: Full model - all interaction terms
    model5 = smf.logit('any_conflict ~ excluded + geo_concentrated + upgraded10 + excluded:geo_concentrated + excluded:upgraded10', data=df)
    result5 = model5.fit(disp=0, method='bfgs')
    results['model5'] = result5
    
    # Create summary table for current conflict models
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
    
    results['current_conflict_summary'] = models_summary
    
    # Future conflict models (1 year ahead)
    
    # Model 1F: Base model - exclusion status only
    model1f = smf.logit('future_conflict_1yr ~ excluded', data=df)
    result1f = model1f.fit(disp=0, method='bfgs')
    results['model1f'] = result1f
    
    # Model 2F: Add control variables
    model2f = smf.logit('future_conflict_1yr ~ excluded + geo_concentrated + upgraded10', data=df)
    result2f = model2f.fit(disp=0, method='bfgs')
    results['model2f'] = result2f
    
    # Model 3F: Add interaction term - exclusion and geographic concentration
    model3f = smf.logit('future_conflict_1yr ~ excluded + geo_concentrated + upgraded10 + excluded:geo_concentrated', data=df)
    result3f = model3f.fit(disp=0, method='bfgs')
    results['model3f'] = result3f
    
    # Model 4F: Add interaction term - exclusion and prior governance experience
    model4f = smf.logit('future_conflict_1yr ~ excluded + geo_concentrated + upgraded10 + excluded:upgraded10', data=df)
    result4f = model4f.fit(disp=0, method='bfgs')
    results['model4f'] = result4f
    
    # Model 5F: Full model - all interaction terms
    model5f = smf.logit('future_conflict_1yr ~ excluded + geo_concentrated + upgraded10 + excluded:geo_concentrated + excluded:upgraded10', data=df)
    result5f = model5f.fit(disp=0, method='bfgs')
    results['model5f'] = result5f
    
    # Create summary table for future conflict models
    future_model_names = ['Model 1F', 'Model 2F', 'Model 3F', 'Model 4F', 'Model 5F']
    future_models_summary = summary_col(
        [result1f, result2f, result3f, result4f, result5f],
        model_names=future_model_names,
        stars=True,
        info_dict={
            'N': lambda x: "{0:d}".format(int(x.nobs)),
            'Log-Likelihood': lambda x: "{:.2f}".format(x.llf),
            'AIC': lambda x: "{:.2f}".format(x.aic),
            'Pseudo R²': lambda x: "{:.4f}".format(x.prsquared),
        }
    )
    
    results['future_conflict_summary'] = future_models_summary
    
    return results