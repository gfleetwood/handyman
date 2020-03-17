def adverserial_validation(X1, X2):
    """
    Get the top resulting cricle from the hough circle transform
    """

    df_av = pd.concat([X2.assign(test=1), X1.assign(test=0)], axis=0)
    mdl_av = sk_lm.LogisticRegression()
    training_scores_av = sk_ms.cross_val_score(
        mdl_av,
        df_av.drop(['test'], axis=1),
        df_av.test.values,
        cv = 5,
        scoring='roc_auc'
        )
        
    results = (training_scores_av.mean(), training_scores.std())

    return(results)

def subset_by_iqr(df, column, whisker_width = 1.5):
    """
    Get the top resulting cricle from the hough circle transform
    """

    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1

    mask = (
        df[column] >= q1 -
        whisker_width *
        iqr) & (
        df[column] <= q3 +
        whisker_width *
        iqr)

    return df.loc[mask]

def get_exp_shap_vals(mdl, X, y):
    """
    fplot = shap.force_plot(explainer.expected_value, shap_vals[45,:], X_train.iloc[45,:], link = 'logit')
    """

    mdl.fit(X.values, y.values)
    explainer = shap.TreeExplainer(test, model_output = "probability")
    shap_values = explainer.shap_values(X.values)

    return((explainer, shap_values))

def date_decomposition(df, col):
    """
    Get the top resulting cricle from the hough circle transform
    """

    result = df.assign(
        hour = lambda x: x[col].dt.hour,
        day = lambda x: x[col].dt.day,
        month = lambda x: x[col].dt.month,
        year = lambda x: x[col].dt.year
    )

    return(result)
