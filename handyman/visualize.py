import plotnine as pn

def get_num_corr_plot(df, num_cols):
    '''
    @description Takes a dataframe and a list of its numeric columns and returns a plot of the correlation between variables.
    @param df A dataframe
    @param num_cols: A list of the numeric column names
    @return A heatmap plot of the correlation between the numeric variables.
    '''
    df_num = df[num_cols]
    df_num_correlations = df_num.corr().reset_index().melt(id_vars = ['index'],
                                                           value_vars = df_num.corr().columns)
    df_num_correlations = df_num_correlations.round({'value': 2})
    df_num_correlations_plot = (pn.ggplot(df_num_correlations, pn.aes('variable', 'index', fill='value'))
                                   + pn.geom_tile(pn.aes(width=.95, height=.95))
                                   + pn.geom_text(pn.aes(label='value'), size=10))

    return(df_num_correlations_plot)
