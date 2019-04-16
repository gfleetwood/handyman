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

