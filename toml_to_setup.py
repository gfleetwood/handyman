import toml
from jinja2 import Template
import os
from fire import Fire

def semantic_versioning(version: str, increment: str) -> str:
    
    version_list = version.split(".") 
    template = "{}.{}.{}"
    
    update = {
        "major": lambda x: template.format(int(x[0]) + 1, x[1], x[2]),
        "minor": lambda x: template.format(x[0], int(x[1]) + 1, x[2]),
        "patch": lambda x: template.format(x[0], x[1], int(x[2]) + 1)
    }
    
    result = update.get(increment)(version_list)
    
    return(result)

get_semantic_update = lambda key: key

setup_template = Template("""
from setuptools import setup

setup(
  name = {{name}},
  version = {{version}},
  description = {{description}},
  long_description = {{long_description}},
  url = {{url}},
  author = {{author}},
  author_email = {{author_email}},
  license = {{license}},
  packages = {{packages}},
  zip_safe = {{zip_safe}}
      )
""")

config = toml.load('setup.toml')
config["version"] = semantic_versioning(config.get("version"), Fire(get_semantic_update))

with open("setup.toml", "w") as f:
    f.write(toml.dumps(config))

with open("setup.py", "w") as f:
    f.write(setup_template.render(**config).strip())
