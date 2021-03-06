def serialize_model(model, descr = ""):

    '''
    @description Saves a model's parameters. 
    Source: https://nbviewer.jupyter.org/github/rasbt/python-machine-learning-book/blob/master/code/bonus/scikit-model-to-json.ipynb

    @param model A sklearn model object

    @param descr Notes on the model

    @return A dataframe containing the model's parameters
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
    @description Constructs a model from its serialization produced by serialize_model. 
    Source: https://nbviewer.jupyter.org/github/rasbt/python-machine-learning-book/blob/master/code/bonus/scikit-model-to-json.ipynb

    @param df A dataframe of model parameters produced by serialize_model

    @param model_revival A sklearn model object of the model to be unserialized

    @param model_index The row of the model to be unserialized

    @return A dataframe of columns types and NA counts for them
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

