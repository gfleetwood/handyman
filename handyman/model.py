import json
import datetime
import codecs
import numpy as np
import pandas as pd
import plotnine as pn
import sklearn.metrics as sk_mt
import statsmodels.formula.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import subprocess as sp
from io import StringIO
from collections import OrderedDict
from sklearn.metrics import roc_curve as rc
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import StandardScaler
from statsmodels.graphics.gofplots import ProbPlot
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import pyodbc
import statsmodels.api as sm

plt.style.use('seaborn')
plt.rc('font', size = 14)
plt.rc('figure', titlesize = 18)
plt.rc('axes', labelsize = 15)
plt.rc('axes', titlesize = 18)

def automl(X, y, other_params = {'key': 'value'}):

    '''
    Role
    ----
    A convenience function to show the feature importances produced by a Random Forest model in a nice format.
  
    Parameters
    ---------
    * df: The feature matrix passed to model_rf
    * model_rf: The Random Forest model constructed from df and the target.
  
    Returns
    -------    
    * fi_sorted: A sorted lists of feature names and their importance as per model_rf.
    '''
    
        mdl = TPOTClassifier(generations = 10, population_size = 50,
														 verbosity = 2, n_jobs = -1)
        mdl.fit(X_train_aug, y_train)
    
    return(mdl_generator)


def auto_fe(X, tp = ['subtract', 'divide'], ap = ['mean', 'max', 'percent_true', 'last']):

    '''
    Role
    ----
    A convenience function to show the feature importances produced by a Random Forest model in a nice format.
  
    Parameters
    ---------
    * df: The feature matrix passed to model_rf
    * model_rf: The Random Forest model constructed from df and the target.
  
    Returns
    -------    
    * fi_sorted: A sorted lists of feature names and their importance as per model_rf.
    '''

	es = ft.EntitySet(id = "test")
	es = es.entity_from_dataframe(entity_id = 'd', dataframe = X, 
																make_index = True, index = 'ind')
	
	fm, features = ft.dfs(entityset = es, target_entity = 'd', njobs = -1,
	                      trans_primitives = tp, agg_primitives = ap)
	                      
	# _, X_ft2 = ft.dfs(entityset = es, target_entity = 'd', max_depth = 2)

	return(features)

def ols_with_diagnostics(df, formula = 'sepal_length ~ sepal_width'):

    '''
    Role
    ----
    A convenience function to show the feature importances produced by a Random Forest model in a nice format.
  
    Parameters
    ---------
    * df: The feature matrix passed to model_rf
    * model_rf: The Random Forest model constructed from df and the target.
  
    Returns
    -------    
    * fi_sorted: A sorted lists of feature names and their importance as per model_rf.
    '''
    
    # https://medium.com/@emredjan/emulating-r-regression-plots-in-python-43741952c034
    
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
    Role
    ----
    A convenience function to show the feature importances produced by a Random Forest model in a nice format.
  
    Parameters
    ---------
    * df: The feature matrix passed to model_rf
    * model_rf: The Random Forest model constructed from df and the target.
  
    Returns
    -------    
    * fi_sorted: A sorted lists of feature names and their importance as per model_rf.
    '''
    
    frequent_itemsets = apriori(df, min_support = support, use_colnames = True)
    rules = association_rules(frequent_itemsets, metric = "lift", min_threshold = 1)
    results = rules.loc[(rules['consequents'] == rules.consequents.unique()[0]),
                            ['antecedents', 'consequents', 'lift', 'confidence']] \
                   .sort_values(['lift', 'confidence'], ascending = [False, False])
    
    return(results)

def classification_status(y_train, y_pred, y_pred_proba, cv_scores):
    '''
    Role
    ----
    A convenience function to show the feature importances produced by a Random Forest model in a nice format.
  
    Parameters
    ---------
    * df: The feature matrix passed to model_rf
    * model_rf: The Random Forest model constructed from df and the target.
  
    Returns
    -------    
    * fi_sorted: A sorted lists of feature names and their importance as per model_rf.
    '''
    
    print('classification report: ')
    print('\n')
    print(sk_met.classification_report(y_train, y_pred))
    print('\n')
    print('cv scores: mean - {:0.2f} & std - {:0.2f} '.format(np.mean(cv_scores), np.std(cv_scores)))
    print('\n')
    print('confusion matrix: ')
    print('\n')
    print(sk_met.confusion_matrix(y_train, y_pred))
    print('\n')
    print('auc-roc: ')
    print('\n')
    fpr, tpr, _ = sk_met.roc_curve(y_train, y_pred_proba[:, 1])
    auc = sk_met.roc_auc_score(y_train, y_pred)
    plt.plot(fpr, tpr, label = "auc=" + str(np.round(auc, 2)))
    plt.legend(loc = 4)
    plt.show()
    print('\n')
    print("brier score: ", sk_met.brier_score_loss(y_train, y_pred)) # lower is better

def feature_selection_classif(X, y, fs_type = "mdl"):  

    '''
    Role
    ----
    A convenience function to show the feature importances produced by a Random Forest model in a nice format.
  
    Parameters
    ---------
    * df: The feature matrix passed to model_rf
    * model_rf: The Random Forest model constructed from df and the target.
  
    Returns
    -------    
    * fi_sorted: A sorted lists of feature names and their importance as per model_rf.
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
    Role
    ----
    A convenience function to show the feature importances produced by a Random Forest model in a nice format.
  
    Parameters
    ---------
    * df: The feature matrix passed to model_rf
    * model_rf: The Random Forest model constructed from df and the target.
  
    Returns
    -------    
    * fi_sorted: A sorted lists of feature names and their importance as per model_rf.
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
    Role
    ----
    A convenience function to show the feature importances produced by a Random Forest model in a nice format.
  
    Parameters
    ---------
    * df: The feature matrix passed to model_rf
    * model_rf: The Random Forest model constructed from df and the target.
  
    Returns
    -------    
    * fi_sorted: A sorted lists of feature names and their importance as per model_rf.
    '''
    cv_scores = sk_ms.cross_val_score(model, X, y, cv = cv, n_jobs = -1)
    return(cv_scores.mean(), cv_scores.std())
    
def build_ensemble(model_list):

    '''
    Role
    ----
    A convenience function to show the feature importances produced by a Random Forest model in a nice format.
  
    Parameters
    ---------
    * df: The feature matrix passed to model_rf
    * model_rf: The Random Forest model constructed from df and the target.
  
    Returns
    -------    
    * fi_sorted: A sorted lists of feature names and their importance as per model_rf.
    '''
    
    ensemble = mlx.classifier.StackingCVClassifier(classifiers = model_list[:-1],
                                              use_probas = True, cv = 5, 
                                              meta_classifier = model_list[-1])
    
    return(ensemble)

def get_baselines(X, y, ml_type = 'classification'):

    '''
    Role
    ----
    A convenience function to show the feature importances produced by a Random Forest model in a nice format.
  
    Parameters
    ---------
    * df: The feature matrix passed to model_rf
    * model_rf: The Random Forest model constructed from df and the target.
  
    Returns
    -------    
    * fi_sorted: A sorted lists of feature names and their importance as per model_rf.
    '''
    
    ml_dict = {'classification': [sk_lm.LogisticRegression()], 'regression':  [sk_lm.LinearRegression()]}
    mdl = ml_dict[ml_type]
    cv_scores = sk_ms.cross_val_score(mdl, X.values, y.values, cv = 5, n_jobs = -1)
    
    target_baseline = [y.value_counts(normalize = True).to_dict() if type = "classification" else y.mean()]

    return("Naive Baseline: ", target_baseline, 
           "Model Baseline (mu & sigma): ", cv_scores.mean(), cv_scores.std())

def plot_learning_curve(model, X, y):    

    '''
    Role
    ----
    A convenience function to show the feature importances produced by a Random Forest model in a nice format.
  
    Parameters
    ---------
    * df: The feature matrix passed to model_rf
    * model_rf: The Random Forest model constructed from df and the target.
  
    Returns
    -------    
    * fi_sorted: A sorted lists of feature names and their importance as per model_rf.
    '''

    folds = sk_ms.StratifiedKFold(5)
    sizes = np.linspace(0.3, 1.0, 10)

    viz = LearningCurve(model, cv = folds, train_sizes = sizes, scoring = 'accuracy', n_jobs = -1)
    viz.fit(X, y)
    viz.poof()

def custom_metrics(y_true, y_pred, metrics_dict = {'accuracy': 0, 'recall': 0, 'precision': 0, 'f1': 0}):

    '''
    Role
    ----
    A convenience function to show the feature importances produced by a Random Forest model in a nice format.
  
    Parameters
    ---------
    * df: The feature matrix passed to model_rf
    * model_rf: The Random Forest model constructed from df and the target.
  
    Returns
    -------    
    * fi_sorted: A sorted lists of feature names and their importance as per model_rf.
    '''
    
    metrics_dict['accuracy'] = sk_met.accuracy_score(y_true, y_pred)
    metrics_dict['f1'] = sk_met.f1_score(y_true, y_pred)
    metrics_dict['recall'] = sk_met.recall_score(y_true, y_pred)
    metrics_dict['precision'] = sk_met.precision_score(y_true, y_pred)
        
    return metrics_dict

def custom_metrics_cv(clf, X, y, metrics_dict = {'accuracy': [], 'recall': [], 'precision': [], 'f1': []}):

    '''
    Role
    ----
    A convenience function to show the feature importances produced by a Random Forest model in a nice format.
  
    Parameters
    ---------
    * df: The feature matrix passed to model_rf
    * model_rf: The Random Forest model constructed from df and the target.
  
    Returns
    -------    
    * fi_sorted: A sorted lists of feature names and their importance as per model_rf.
    '''
    
    for metric in metrics_dict.keys():
        cv_scores = sk_ms.cross_val_score(clf, X.values, y.values, scoring = 'f1', cv = 5, n_jobs = -1)
        metrics_dict[metric] = [cv_scores.mean(), cv_scores.std()]
        
    return metrics_dict

def proba_score_proxy(y_true, y_probs, class_idx, proxied_func, **kwargs):
    '''
    Role
    ----
    A convenience function to show the feature importances produced by a Random Forest model in a nice format.
  
    Parameters
    ---------
    * df: The feature matrix passed to model_rf
    * model_rf: The Random Forest model constructed from df and the target.
  
    Returns
    -------    
    * fi_sorted: A sorted lists of feature names and their importance as per model_rf.
    '''
    return proxied_func(y_true, y_probs[:, class_idx], **kwargs)
    
def custom_brier_score():
    custom_brier_scorer = sk_met.make_scorer(proba_score_proxy, greater_is_better = False, needs_proba = True, 
                             class_idx = 1, proxied_func = sk_met.brier_score_loss)
                             
    return(custom_brier_scorer)

    
def lstm_reshape(df, num_features = 1):
    '''
    Role
    ----
    A convenience function to show the feature importances produced by a Random Forest model in a nice format.
  
    Parameters
    ---------
    * df: The feature matrix passed to model_rf
    * model_rf: The Random Forest model constructed from df and the target.
  
    Returns
    -------    
    * fi_sorted: A sorted lists of feature names and their importance as per model_rf.
    '''
    result = np.array(df).reshape((df.shape[0], df.shape[1], num_features))
    return(result)

def create_lstm_model(X, y, metric = ["accuracy"]):
    '''
    Role
    ----
    A convenience function to show the feature importances produced by a Random Forest model in a nice format.
  
    Parameters
    ---------
    * df: The feature matrix passed to model_rf
    * model_rf: The Random Forest model constructed from df and the target.
  
    Returns
    -------    
    * fi_sorted: A sorted lists of feature names and their importance as per model_rf.
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
    Role
    ----
    A convenience function to show the feature importances produced by a Random Forest model in a nice format.
  
    Parameters
    ---------
    * df: The feature matrix passed to model_rf
    * model_rf: The Random Forest model constructed from df and the target.
  
    Returns
    -------    
    * fi_sorted: A sorted lists of feature names and their importance as per model_rf.
    '''

  X = sm.add_constant(X) # adding a constant
  mdl = sm.OLS(y, X).fit()
  return(mdl)

def keras_history(history, metric = "rmse"):
    '''
    Role
    ----
    A convenience function to show the feature importances produced by a Random Forest model in a nice format.
  
    Parameters
    ---------
    * df: The feature matrix passed to model_rf
    * model_rf: The Random Forest model constructed from df and the target.
  
    Returns
    -------    
    * fi_sorted: A sorted lists of feature names and their importance as per model_rf.
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
    Role
    ----
    Implement's Younden's J Statistic for finding an optimal threshold for a binary classification model.
  
    Parameters
    ---------
    * y: The true labels
    * y_hat_probs: The probabilities of the positive class
  
    Returns
    ------- 
    * youden_j: A recommended threshold for the model.
    '''
    
    fpr, tpr, thresholds = rc(y, y_hat_probs, pos_label = 1)
    j_scores = tpr - fpr
    j_ordered = sorted(zip(j_scores,thresholds))
    youden_j = j_ordered[-1][1]
    
    return youden_j

def classification_metrics(y_actual, y_predicted):

    '''
    Role
    ----
    Generates a set of classification scores for a model's predictions.

    Parameters
    ---------
    * y_actual: The correct labels for the data.
    * y_predicted: The predicted labels produced by a model.

    Returns
    -------
    * metrics_dict: A dictionary with the accuracy, roc-auc, and f1 scores for the model's predictions.
    '''
    
    metrics_dict = OrderedDict()
    metrics_dict['accuracy'] = sum(y_actual == y_predicted)/float(len(y_actual))
    metrics_dict['roc_auc'] = sk_mt.roc_auc_score(y_actual, y_predicted)
    metrics_dict['f1_score'] = sk_mt.f1_score(y_actual, y_predicted)

    return(metrics_dict)
    
def kaiser_harris_criterion(df):
    '''
    Role
    ----
    Implement's the Kaiser-Harris criterion for suggesting an optimal number of dimensions for Principal Component Analysis.
  
    Parameters
    ---------
    * df: A pandas dataframe.
  
    Returns
    -------
    * dim_rec: The recommended dimensional space to project the original data into.
    '''
    
    cov_mat = np.cov(df.T)
    e_vals, _ = np.linalg.eig(cov_mat)
    dim_rec = len(e_vals[e_vals > 1])
    return(dim_rec)
    
def rf_feature_importance(df, model_rf):
    '''
    Role
    ----
    A convenience function to show the feature importances produced by a Random Forest model in a nice format.
  
    Parameters
    ---------
    * df: The feature matrix passed to model_rf
    * model_rf: The Random Forest model constructed from df and the target.
  
    Returns
    -------    
    * fi_sorted: A sorted lists of feature names and their importance as per model_rf.
    '''

    fi = list(zip(df.columns, model_rf.feature_importances_))
    fi_sorted = sorted(fi, key = lambda x: -x[1])
    return fi_sorted
    
def get_coefficients(df, model):
    '''
    Role
    ----
    A convenience function to match the coefficients of a model to the features they correspond to.
  
    Parameters
    ---------
    * df: A pandas dataframe of features used in model.
    * model: A fitted scikit-learn model.
  
    Returns
    -------    
    * df_coefficient: A dataframe of features and their coefficients.
    '''
    df_coefficient = pd.DataFrame(sorted(list(zip(df.columns, model.coef_[0])), key = lambda x: -x[1]), 
                                  columns = ['feature', 'coefficient'])
    
    return df_coefficient
    

