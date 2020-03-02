def auto_fe(X, tp = ['subtract', 'divide'], ap = ['mean', 'max', 'percent_true', 'last']):
    '''
    @description Automatic feature engineering with Feature Tools. See the Feature Tools docs for more 
    info on primitives and the corresonding options
    @param X A dataframe
    @param tp A list of trans_primitives
    @param ap A list of agg_primitives
    @return A dataframe with new features
    '''
    es = ft.EntitySet(id = "test")
    es = es.entity_from_dataframe(entity_id = 'd', dataframe = X, make_index = True, index = 'ind')
	
    fm, features = ft.dfs(entityset = es, target_entity = 'd', njobs = -1,
	                      trans_primitives = tp, agg_primitives = ap)
	                      
	# _, X_ft2 = ft.dfs(entityset = es, target_entity = 'd', max_depth = 2)

    return(features)

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

def get_rules(df, support):
    '''
    @description Get rules for Association Rules Mining
    @param df A dataframe
    @param support The support for the Association Rules
    @return A dataframe of rules
    '''    
    frequent_itemsets = apriori(df, min_support = support, use_colnames = True)
    rules = association_rules(frequent_itemsets, metric = "lift", min_threshold = 1)
    results = rules.loc[(rules['consequents'] == rules.consequents.unique()[0]),
                            ['antecedents', 'consequents', 'lift', 'confidence']] \
                   .sort_values(['lift', 'confidence'], ascending = [False, False])
    
    return(results)

def feature_selection_classif(X, y, fs_type = "mdl"):  
    '''
    @description A wrapper around some classification sklearn feature selection methods
    @param X Feature dataframe
    @param y The target
    @param type Use "mdl" for model based feature selection with The Random Forest Classifier and Recursive Feature Eliminination.
    Use "mic" for sklearn.feature_selection.mutual_info_classif, and use "f_classif" for sklearn.feature_selection.f_classif
    @return A dataframe with the selected features
    '''     
    if fs_type == "mic":
        fs_scores = sk_fs.mutual_info_classif(X, y)
        fs_cols = [x[0] for x in list(zip(X_train.columns, fs_scores)) if x[1] > 0]
    elif fs_type == "f_classif":
        fs_scores = sk_fs.f_classif(X_train, y_train)
        fs_cols = [x[0] for x in list(zip(X_train.columns, fs_scores[1])) if x[1] < .05]
    else:
        mdl = sk_fs.RFECV(sk_esb.RandomForestClassifier(), cv = 5, scoring = 'f1', n_jobs = -1)
        mdl.fit(X, y)
        fs_cols = X.columns[mdl.support_]

    X_fs = X.loc[:, fs_cols]
    
    return(X_fs)


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
    
def build_ensemble(model_list):
    '''
    @description A wrapper around building a model ensemble.
    @param model_list The list of models. The last model is the meta_classifier
    @return A dataframe with shap values
    '''    
    ensemble = mlx.classifier.StackingCVClassifier(classifiers = model_list[:-1],
                                                   use_probas = True, cv = 5, 
                                                   meta_classifier = model_list[-1])
    
    return(ensemble)

def plot_learning_curve(model, X, y):    
    '''
    @description A wrapper for plotting a learning curve
    @param model A trained model object
    @param X The feature dataframe
    @param y The target
    @return 
    '''
    folds = sk_ms.StratifiedKFold(5)
    sizes = np.linspace(0.3, 1.0, 10)

    viz = LearningCurve(model, cv = folds, train_sizes = sizes, scoring = 'accuracy', n_jobs = -1)
    viz.fit(X, y)
    viz.poof()
    
def custom_brier_score():
    '''
    @description A Brier score function
    @return The Brier score
    '''
    def proba_score_proxy(y_true, y_probs, class_idx, proxied_func, **kwargs):
        return proxied_func(y_true, y_probs[:, class_idx], **kwargs)

    custom_brier_scorer = sk_met.make_scorer(proba_score_proxy, greater_is_better = False, needs_proba = True, 
                             class_idx = 1, proxied_func = sk_met.brier_score_loss)
                             
    return(custom_brier_scorer)

    
def lstm_reshape(df, num_features = 1):
    '''
    @description A wrapper to reshape data for a keras LSTM model
    @param df The feature dataframe
    @return An array of the data in the required shape
    '''
    result = np.array(df).reshape((df.shape[0], df.shape[1], num_features))
    return(result)

def create_lstm_model(X, y, metric = ["accuracy"]):
    '''
    @description A wrapper to create a simple keras LSTM model
    @param X The feature dataframe
    @param y The target
    @param metric The metric of evaluation
    @return A list of the trained model and its training history
    '''
    mdl = Sequential() 

    mdl.add(LSTM(units = 64, return_sequences = False, input_shape = (X.shape[1], 1))) 
    mdl.add(Dropout(0.2))
    # mdl.add(LSTM(units = 64, return_sequences = True)) 
    # mdl.add(Dropout(0.2))
    # mdl.add(LSTM(units = 64, return_sequences = True)) 
    # mdl.add(Dropout(0.2))
    # mdl.add(LSTM(units = 64))  
    # mdl.add(Dropout(0.2))
    mdl.add(Dense(units = 1))

    mdl.compile(loss = "mean_squared_error", optimizer = "adam", metrics = metric)
    history = mdl.fit(X, y, epochs = 10, batch_size = 1, validation_split = 0.2, verbose = 0)
    
    return([mdl, history])

def lm_stats(X, y):
    '''
    @description A wrapper to create an OLS model with statsmodels
    @param X The feature dataframe
    @param y The target
    @return A trained OLS model
    '''
    X = sm.add_constant(X)
    mdl = sm.OLS(y, X).fit()

    return(mdl)

def keras_history(history, metric = "rmse"):
    '''
    @description A wrapper to plot a keras model's training history
    @param history An object produced by fitting a keras model
    @param metric The metric used to train the model
    @return A list of the trained model and its training history
    '''
    plt.plot(history.history[metric])
    plt.plot(history.history[('val_' + metric)])
    plt.title('model ' + metric)
    plt.ylabel(metric)
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc = 'upper left')
    plt.show()

    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.show()
    
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
    
def rf_feature_importance(df, model_rf):
    '''
    @description A wrapper for combining feature importances with their columns
    @param df A dataframe
    @param model_rf A trained sklearn Random Forest model 
    @return A sorted list of features and their importance
    '''
    fi = list(zip(df.columns, model_rf.feature_importances_))
    fi_sorted = sorted(fi, key = lambda x: -x[1])

    return(fi_sorted)
    
def get_coefficients(df, model):
    '''
    @description An implementation of the Kaiser-Harris Criterion
    @param df A dataframe used to train model
    @param model A sklearn model trained on df
    @return A dataframe of features and their coefficients
    '''
    df_coefficient = pd.DataFrame(sorted(list(zip(df.columns, model.coef_[0])), key = lambda x: -x[1]), 
                                  columns = ['feature', 'coefficient'])
    
    return(df_coefficient)
    

