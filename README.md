## Overview

An untested hodge podge of different Data Science functions I kept re-writing. Everything is version 0.0001 right now. 

## Installation

Developed with Python 3.5. It's only on PyPi because I wanted to test out how to deploy a package.

`pip install handyman`

## Usage

Here are the functions in handyman.

* data_diagnostics: Leverages pandas to return an expanded summary of the categorical and numeric columns of a dataframe.

* get_num_corr_plot: Takes a dataframe and returns a plot of the correlation between numeric variables.

model serialization: serialize_model() stores a fitted models parameters and attributes in a dataframe while unserialize_model() takes a dataframe produced by serialize_model and recreates the model object from a specified row. The majority of the model serialization code comes from this [post](https://nbviewer.jupyter.org/github/rasbt/python-machine-learning-book/blob/master/code/bonus/scikit-model-to-json.ipynb).

* flatten nested dictionary: flatten_dict() is a more robust version of pandas.io.json.json_normalize(). The code is from [here](https://towardsdatascience.com/flattening-json-objects-in-python-f5343c794b10)
