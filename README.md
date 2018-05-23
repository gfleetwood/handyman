## Overview

An untested hodge podge of different Data Science functions I kept re-writing. Everything is version 0.0001 right now. 

## Installation

Developed with Python 3.5. The package is on PyPi but I haven't updated it in a while. To get the latest version clone this repo, cd into it, and run:

`python install setup.py`

## Usage

Here are some of the functions in handyman.

* `data_diagnostics`: Leverages pandas to return an expanded summary of the categorical and numeric columns of a dataframe.

* `get_num_corr_plot`: Takes a dataframe and returns a plot of the correlation between numeric variables.

* `serialize_model()`: Stores a fitted models parameters and attributes in a dataframe. [1]

* `unserialize_model()`: Takes a dataframe produced by serialize_model and recreates the model object from a specified row. [1]

* `flatten_dict()`: A more robust version of pandas.io.json.json_normalize(). [2]

## To Do

Add docs.

[1]: The majority of the model serialization code comes from this [post](https://nbviewer.jupyter.org/github/rasbt/python-machine-learning-book/blob/master/code/bonus/scikit-model-to-json.ipynb).

[2]: The code is from [here](https://towardsdatascience.com/flattening-json-objects-in-python-f5343c794b10)
