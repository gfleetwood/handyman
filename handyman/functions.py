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

plt.style.use('seaborn')
plt.rc('font', size=14)
plt.rc('figure', titlesize=18)
plt.rc('axes', labelsize=15)
plt.rc('axes', titlesize=18)

exclusion = lambda x,y: [j for i,j in enumerate(x) if i != y]

def keras_history(history, metric = "rmse"):

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

def lstm_reshape(df, num_features = 1):
    result = np.array(df).reshape((df.shape[0], df.shape[1], num_features))
    return(result)

def impute_scale_data(df):
    '''
    Role
    ----
    Imputes missing values with the median for numeric features and the mode for categorical ones, and then scales the numeric features
    by subtracting the mean and dividing by the standard deviation.
  
    Parameters
    ---------
    * df: A pandas dataframe
  
    Returns
    -------
    * df_imputed_scaled: A dataframe that has been imputed and scaled.
    '''
    
    imputer_num = Imputer(strategy = 'median') 
    df.loc[:, df.select_dtypes(exclude = ['object']).columns] = \
    imputer_num.fit_transform(df.select_dtypes(exclude = ['object']))  
    
    scaler = StandardScaler()
    df.loc[:, df.select_dtypes(exclude = ['object']).columns] = \
    scaler.fit_transform(df.select_dtypes(exclude = ['object']))
    
    for col in df.select_dtypes(include = ['object']).columns:
        df.loc[:, col] = df.loc[:, col].fillna(value = df.loc[:, col].value_counts().index[0])
        
    df_imputed_scaled = df
        
    return df_imputed_scaled
    
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

def data_diagnostics(df, num_cols, cat_cols):
    '''
    Role
    ----
    Takes a dataframe, and lists of its numeric and categorical variables. Returns a summary for each.
  
    Parameters
    ---------
    * df: A pandas dataframe
    * num_cols: A list of the numeric column names
    * cat_cols: A list of the categorical column names
  
    Returns
    -------
    * smry: A list containing: 1) num_summary: A pandas dataframe with a summary of the numeric variables, and 
    2) cat_summary: A pandas dataframe with a summary of the categorical variables
    '''

    # Numerical summary
    df_num = df[num_cols]
    num_summary = df_num.describe().T
    num_missingness_dtypes = pd.concat([df_num.isnull().sum(), df_num.dtypes], axis=1)
    num_missingness_dtypes.columns = ['null_values', 'data_type']
    num_summary_full = num_missingness_dtypes.join(num_summary, how='inner')

    # Categorical summary
    df_cat = df[cat_cols]
    cat_summary = pd.concat([df_cat.isnull().sum(), df_cat.dtypes], axis=1)
    cat_summary.columns = ['null_values', 'data_type']
    cat_summary['num_unique_values'] = [len(df_cat[col].value_counts()) for col in cat_cols]
    cat_summary['most_frequent_value'] = [
        df_cat[col].value_counts().reset_index().ix[0, 'index']
        for col in cat_cols
              ]
    cat_summary['most_frequent_value_ratio'] = [
        df_cat[col].value_counts(normalize = True).reset_index().ix[0, col]
        for col in cat_cols
              ]
    cat_summary['least_frequent_value'] = [
        df_cat[col].value_counts().reset_index().ix[len(df_cat[col].value_counts()) - 1, 'index']
        for col in cat_cols
              ]
    cat_summary['least_frequent_value_ratio'] = [
        df_cat[col].value_counts(normalize = True).reset_index().ix[len(df_cat[col].value_counts()) - 1, col]
        for col in cat_cols
              ]
    
    smry = [num_summary_full, cat_summary]

    return (smry)


def get_num_corr_plot(df, num_cols):
    '''
    Role
    ----
    Takes a dataframe and a list of its numeric columns and returns a plot of the correlation between variables.

    Parameters
    ---------
    * df: A pandas dataframe
    * num_cols: A list of the numeric column names

    Returns
    -------
    * df_num_correlations_plot: A heatmap plot of the correlation between the numeric variables.
    '''

    df_num = df[num_cols]
    df_num_correlations = df_num.corr().reset_index().melt(id_vars = ['index'],
                                                           value_vars = df_num.corr().columns)
    df_num_correlations = df_num_correlations.round({'value': 2})
    df_num_correlations_plot = (pn.ggplot(df_num_correlations, pn.aes('variable', 'index', fill='value'))
                                   + pn.geom_tile(pn.aes(width=.95, height=.95))
                                   + pn.geom_text(pn.aes(label='value'), size=10))

    return(df_num_correlations_plot)

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
    

def serialize_model(model, descr):
  
    '''
    Role
    ----
    Stores a fitted model's parameters and attributes in a dataframe.
  
    Parameters
    ---------
    * model: A fitted scikit-learn model.
    * descr: A text description of the model that the user wants to note.
  
    Returns
    -------
    * df: A dataframe with the model's type, the supplied description, the model's parameters,and its attributes.
    '''
    
    attrs = [i for i in dir(model) if i.endswith('_') and not i.endswith('__')]   
    attr_dict = {i: getattr(model, i) for i in attrs}    
    for k in attr_dict:
        if isinstance(attr_dict[k], np.ndarray):
            attr_dict[k] = attr_dict[k].tolist()
    attr_json = json.dumps(attr_dict)
    
    d = OrderedDict()
    d['model_type'] = [str(model).split('(')[0]]
    d['description'] = descr
    d['params'] = [json.dumps(model.get_params())]
    d['attrs'] = [attr_json]    
        
    df = pd.DataFrame(d)
    return df

def unserialize_model(df, model_revival, model_index = 0):
  
    '''
    Role
    ----
    Takes a dataframe produced by serialize_model and recreates the model object from a specified row.
  
    Parameters
    ---------
    * df: A dataframe of model info produced by serialize_model.
    * model_revival: An uninitialized model object of the type to be reconstructed.
    * model_index: Assuming df consists of multiple models, this is the index of the one to be recreated.
  
    Returns
    -------  
    * model_revival: The recreated model.
    '''
    
    params = json.loads(df.params[model_index])
    attributes = json.loads(df.attrs[model_index])
    model_revival.set_params(**params)
    for k in attributes:
        if isinstance(attributes[k], list):
            setattr(model_revival, k, np.array(attributes[k]))
        else:
            setattr(model_revival, k, attributes[k])
            
    return model_revival

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

def flatten_dict(y):  
    '''
    Role
    ----
    Flatten an arbitrarily nested dictionary.
    
    Parameters
    ---------
    * y: A dictionary
  
    Returns
    -------    
    * out: A flattened version of y. 
    '''
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out
    
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
    
def get_date_time():  
    '''
    Role
    ----
    Returns the system date and time as a string.
  
    Parameters
    ---------
    * None 
  
    Returns
    -------
    * * A list contains two elements as strings: 1) date, and 2) time.
    '''
    return str(datetime.datetime.now()).split(' ')
    
def ols_with_diagnostics(df, formula = 'sepal_length ~ sepal_width'):
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


def classification_status(y_train, y_pred, y_pred_proba, cv_scores):
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
    
## Borrowed from the pyjanitor

def clean_names(df):

    def convert(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    df = df.rename(
        columns = lambda x: x.replace(" ", "_")
        .replace("/", "_")
        .replace(":", "_")
        .replace("'", "")
        .replace("’", "")
        .replace(",", "_")
        .replace("?", "_")
        .replace("-", "_")
        .replace("(", "_")
        .replace(")", "_")
        .replace(".", "_")
    )\
    .rename(columns= lambda x: convert(x))\
    .rename(columns = lambda x: re.sub("_+", "_", x))
    return df
    
    
def get_types_na_count(df):
  result = pd.concat([df.dtypes, df.isnull().sum()], axis = 1)
  result.columns = ["type", "na_count"]
  return(result)

def get_rules(df):
    
    frequent_itemsets = apriori(df, min_support = 0.07, use_colnames = True)
    rules = association_rules(frequent_itemsets, metric = "lift", min_threshold = 1)
    results = rules.loc[(rules['consequents'] == rules.consequents.unique()[0]),
                            ['antecedents', 'consequents', 'lift', 'confidence']] \
                   .sort_values(['lift', 'confidence'], ascending = [False, False])
    
    return(results)

def classification_status(y_train, y_pred, y_pred_proba, cv_scores):
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
    
def read_csv_sample(fpath, nrows, seed = 8, header = "-r"):
    
    sample = sp.getoutput('subsample -s {seed} -n {nrows} {fpath} {header}'\
                          .format(seed = seed, nrows = nrows, fpath = fpath, header = header))
    
    # Remove the first line which is metadata
    sample_cleaned = StringIO(sample[(sample.find("\n") + 1):])
    
    df = pd.read_csv(sample_cleaned, sep = ",")
    
    return(df)

def feature_selection_classif(X, y, fs_type = "mdl"):   
    
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
    
def auto_fe(df, agg = None, tran = None):
    
    aggs = ['mean', 'max', 'percent_true', 'last']
    tran = ['subtract', 'divide']
    
    es = ft.EntitySet(id = "test")
    es = es.entity_from_dataframe(entity_id = 'd', dataframe = df, make_index = True, index = 'ind')

    fm, X_ft1 = ft.dfs(entityset = es, target_entity = 'd', agg_primitives = aggs, trans_primitives = tran)

    _, X_ft2 = ft.dfs(entityset = es, target_entity = 'd', max_depth = 2)
    
    return(X_ft1)
    
 
def mdl_cv(model, X, y, cv = 5):
    cv_scores = sk_ms.cross_val_score(model, X, y, cv = cv, n_jobs = -1)
    return(cv_scores.mean(), cv_scores.std())
    
def build_ensemble(model_list):
    
    ensemble = mlx.classifier.StackingCVClassifier(classifiers = model_list[:-1],
                                              use_probas = True, cv = 5, 
                                              meta_classifier = model_list[-1])
    
    return(ensemble)

def get_model_baselines(X, y, ml_type = 'classification'):
    
    ml_dict = {'classification': sk_lm.LogisticRegression(), 'regression':  sk_lm.LinearRegression()}
    mdl = ml_dict[ml_type]
    cv_scores = sk_ms.cross_val_score(mdl, X.values, y.values, cv = 5, n_jobs = -1)

    return("Naive Baseline: ", y.value_counts(normalize = True).to_dict(), 
           "Model Baseline (mu & sigma): ", cv_scores.mean(), cv_scores.std())

def plot_learning_curve(model, X, y):    

    folds = sk_ms.StratifiedKFold(5)
    sizes = np.linspace(0.3, 1.0, 10)

    viz = LearningCurve(model, cv = folds, train_sizes = sizes, scoring = 'accuracy', n_jobs = -1)
    viz.fit(X, y)
    viz.poof()

def custom_metrics(y_true, y_pred, metrics_dict = {'accuracy': 0, 'recall': 0, 'precision': 0, 'f1': 0}):
    
    metrics_dict['accuracy'] = sk_met.accuracy_score(y_true, y_pred)
    metrics_dict['f1'] = sk_met.f1_score(y_true, y_pred)
    metrics_dict['recall'] = sk_met.recall_score(y_true, y_pred)
    metrics_dict['precision'] = sk_met.precision_score(y_true, y_pred)
        
    return metrics_dict

def custom_metrics_cv(clf, X, y, metrics_dict = {'accuracy': [], 'recall': [], 'precision': [], 'f1': []}):
    
    for metric in metrics_dict.keys():
        cv_scores = sk_ms.cross_val_score(clf, X.values, y.values, scoring = 'f1', cv = 5, n_jobs = -1)
        metrics_dict[metric] = [cv_scores.mean(), cv_scores.std()]
        
    return metrics_dict
    
custom_brier_scorer = sk_met.make_scorer(proba_score_proxy, greater_is_better = False, needs_proba = True, 
                             class_idx = 1, proxied_func = sk_met.brier_score_loss)

def proba_score_proxy(y_true, y_probs, class_idx, proxied_func, **kwargs):
    return proxied_func(y_true, y_probs[:, class_idx], **kwargs)
    
def lstm_reshape(df, num_features = 1):
    result = np.array(df).reshape((df.shape[0], df.shape[1], num_features))
    return(result)

def create_lstm_model(X, y, metric = ["accuracy"]):

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
    
 def get_data(server, un, pwd, driver, db, query):
    """Connects to database and gets the data outlined by query as a dataframe."""
    
    con = pyodbc.connect('DRIVER=' + driver +
                     ';PORT=1433;' 'SERVER=' + server +
                     ';PORT=1443;' 'DATABASE=' + db +
                     ';UID=' + un + ';PWD=' + pwd)
                     
    cursor = con.cursor()
    cursor.execute(query)
    cols = [column[0] for column in cursor.description]
    data = [list(row) for row in cursor.fetchall()]
    df = pd.DataFrame(data = data, columns = cols)

    cursor.close()
    con.close()
    return(df)

def set_data(server, un, pwd, driver, db, query, data):
    """Connects to database and gets the data outlined by query as a dataframe."""
    con = pyodbc.connect('DRIVER=' + DRIVER +
                     ';PORT=1433;' 'SERVER=' + SERVER +
                     ';PORT=1443;' 'DATABASE=' + DB +
                     ';UID=' + USERNAME + ';PWD=' + PASSWORD)
    cursor = con.cursor()
    
    #query ex: "insert into reference.{tbname}({c1}, {c2}, depth) values (%d, %d, %d)"
    for val in data:
        cursor.execute(insertion_query)
        CXN.commit()

    cursor.close()
    con.close()
    return 'Write Done'
