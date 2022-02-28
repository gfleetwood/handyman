def ols_with_diagnostics(df, formula = 'sepal_length ~ sepal_width'):
    '''
    @description OLS with diagnostics. Source: https://medium.com/@emredjan/emulating-r-regression-plots-in-python-43741952c034
    @param df A dataframe
    @param formula The regression to perform as a formula, eg. sepal_length ~ sepal_width
    @return A confirmation message
    '''        
    model_fit = sm.ols(formula, data = df).fit()

    # fitted values (need a constant term for intercept)
    model_fitted_y = model_fit.fittedvalues

    # model residuals
    model_residuals = model_fit.resid

    # normalized residuals
    model_norm_residuals = model_fit.get_influence().resid_studentized_internal

    # absolute squared normalized residuals
    model_norm_residuals_abs_sqrt = np.sqrt(np.abs(model_norm_residuals))

    # absolute residuals
    model_abs_resid = np.abs(model_residuals)

    # leverage, from statsmodels internals
    model_leverage = model_fit.get_influence().hat_matrix_diag

    # cook's distance, from statsmodels internals
    model_cooks = model_fit.get_influence().cooks_distance[0]
    
    plot_lm_1 = plt.figure(1)
    plot_lm_1.set_figheight(8)
    plot_lm_1.set_figwidth(12)

    plot_lm_1.axes[0] = sns.residplot(model_fitted_y, 'sepal_length', data=df, 
                              lowess=True, 
                              scatter_kws={'alpha': 0.5}, 
                              line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8})

    plot_lm_1.axes[0].set_title('Residuals vs Fitted')
    plot_lm_1.axes[0].set_xlabel('Fitted values')
    plot_lm_1.axes[0].set_ylabel('Residuals')

    # annotations
    abs_resid = model_abs_resid.sort_values(ascending=False)
    abs_resid_top_3 = abs_resid[:3]

    for i in abs_resid_top_3.index:
        plot_lm_1.axes[0].annotate(i, 
                                   xy=(model_fitted_y[i], 
                                       model_residuals[i]));
        
    QQ = ProbPlot(model_norm_residuals)
    plot_lm_2 = QQ.qqplot(line='45', alpha=0.5, color='#4C72B0', lw=1)

    plot_lm_2.set_figheight(8)
    plot_lm_2.set_figwidth(12)

    plot_lm_2.axes[0].set_title('Normal Q-Q')
    plot_lm_2.axes[0].set_xlabel('Theoretical Quantiles')
    plot_lm_2.axes[0].set_ylabel('Standardized Residuals');

    # annotations
    abs_norm_resid = np.flip(np.argsort(np.abs(model_norm_residuals)), 0)
    abs_norm_resid_top_3 = abs_norm_resid[:3]

    for r, i in enumerate(abs_norm_resid_top_3):
        plot_lm_2.axes[0].annotate(i, 
                                   xy=(np.flip(QQ.theoretical_quantiles, 0)[r],
                                       model_norm_residuals[i]));
        
    plot_lm_3 = plt.figure(3)
    plot_lm_3.set_figheight(8)
    plot_lm_3.set_figwidth(12)

    plt.scatter(model_fitted_y, model_norm_residuals_abs_sqrt, alpha=0.5)
    sns.regplot(model_fitted_y, model_norm_residuals_abs_sqrt, 
                scatter=False, 
                ci=False, 
                lowess=True,
                line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8})

    plot_lm_3.axes[0].set_title('Scale-Location')
    plot_lm_3.axes[0].set_xlabel('Fitted values')
    plot_lm_3.axes[0].set_ylabel('$\sqrt{|Standardized Residuals|}$');

    # annotations
    abs_sq_norm_resid = np.flip(np.argsort(model_norm_residuals_abs_sqrt), 0)
    abs_sq_norm_resid_top_3 = abs_sq_norm_resid[:3]

    for i in abs_norm_resid_top_3:
        plot_lm_3.axes[0].annotate(i, 
                                   xy=(model_fitted_y[i], 
                                       model_norm_residuals_abs_sqrt[i]));
        
    plot_lm_4 = plt.figure(4)
    plot_lm_4.set_figheight(8)
    plot_lm_4.set_figwidth(12)

    plt.scatter(model_leverage, model_norm_residuals, alpha=0.5)
    sns.regplot(model_leverage, model_norm_residuals, 
                scatter=False, 
                ci=False, 
                lowess=True,
                line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8})

    plot_lm_4.axes[0].set_xlim(0, 0.20)
    plot_lm_4.axes[0].set_ylim(-3, 5)
    plot_lm_4.axes[0].set_title('Residuals vs Leverage')
    plot_lm_4.axes[0].set_xlabel('Leverage')
    plot_lm_4.axes[0].set_ylabel('Standardized Residuals')

    # annotations
    leverage_top_3 = np.flip(np.argsort(model_cooks), 0)[:3]

    for i in leverage_top_3:
        plot_lm_4.axes[0].annotate(i, 
                                   xy=(model_leverage[i], 
                                       model_norm_residuals[i]))

    # shenanigans for cook's distance contours
    def graph(formula, x_range, label=None):
        x = x_range
        y = formula(x)
        plt.plot(x, y, label=label, lw=1, ls='--', color='red')

    p = len(model_fit.params) # number of model parameters

    graph(lambda x: np.sqrt((0.5 * p * (1 - x)) / x), 
          np.linspace(0.001, 0.200, 50), 
          'Cook\'s distance') # 0.5 line
    graph(lambda x: np.sqrt((1 * p * (1 - x)) / x), 
          np.linspace(0.001, 0.200, 50)) # 1 line
    plt.legend(loc='upper right');
    
    return('Done')

def get_shap_values(model, X, y):
    '''
    @description A wrapper around some classification sklearn feature selection methods
    @param model A trained model
    @param X The feature dataframe
    @param y The target
    @return A dataframe with shap values
    '''
    model.fit(X, y)
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(model)

    # shap.summary_plot(shap_values, X_train) # all records explained
    # shap.summary_plot(shap_values, X_train, plot_type = "bar") # shap mae for features across all records

    df_shap = pd.DataFrame(list(zip(np.mean(shap_values, axis = 0), X.columns)),
                           columns = ['shap_mean', 'feature'])
    df_shap = df_shap[['feature', 'shap_mean']]
    df_shap['shap_mean_abs'] = np.absolute(df_shap['shap_mean'])
    df_shap.sort_values(['shap_mean_abs'], ascending = False, inplace = True)
    
    return(df_shap)    
 
def mdl_cv(model, X, y, cv = 5):
    '''
    @description A wrapper around using cross validation for model selection
    @param model A sklearn model object
    @param X The feature dataframe
    @param y The target
    @param cv The number of folds. Defaults to 5.
    @return A dataframe with shap values
    '''
    cv_scores = sk_ms.cross_val_score(model, X, y, cv = cv, n_jobs = -1)

    return(cv_scores.mean(), cv_scores.std())

def lm_stats(X, y):

    X = sm.add_constant(X)
    mdl = sm.OLS(y, X).fit()

    return(mdl)
    
def cutoff_youdens_j(y, y_hat_probs):
    '''
    @description Implements the Youden's J cutoff for the optimal classification threshold
    @param y The target
    @param y_hat_probs The generated model probabilities for the target
    @return A threshold to be used as a cutoff in binary classification
    '''    
    fpr, tpr, thresholds = rc(y, y_hat_probs, pos_label = 1)
    j_scores = tpr - fpr
    j_ordered = sorted(zip(j_scores,thresholds))
    youden_j = j_ordered[-1][1]
    
    return(youden_j)

def kaiser_harris_criterion(df):
    '''
    @description An implementation of the Kaiser-Harris Criterion
    @param df A dataframe
    @return The recommendation for how many Principal Components to use in PCA
    '''    
    cov_mat = np.cov(df.T)
    e_vals, _ = np.linalg.eig(cov_mat)
    dim_rec = len(e_vals[e_vals > 1])

    return(dim_rec)
 

