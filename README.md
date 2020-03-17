# Handyman

## Overview

handyman is a hodge-podge of useful Data Science functions. 

## Installation

Clone this repo, cd into it, and run: `python install setup.py`.

## Usage

See the [documentation](https://gfleetwood.github.io/handyman/) for examples.

## Building Documentation

Install pdoc3 with `pip install pdoc3`. In the root directory (where this README lives) run `pdoc --html handyman` which generates `html/handyman/*.html`. 
If you want to deploy these html files with GitHub pages further run `mv html/handyman/*.html html && rm -rf html/handyman && mv html docs`.
