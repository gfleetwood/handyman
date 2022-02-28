from setuptools import setup, find_packages

setup(
  name = 'handyman',
  version = '0.1.0',
  description = 'Miscellaneous Data Science functions',
  long_description = "Miscellaneous Data Science functions",
  url = 'https://github.com/gfleetwood/handyman',
  author = 'gfleetwood',
  author_email = 'gfleetwood@protonmail.com',
  packages = find_packages(),
  license = 'MIT',
  zip_safe = False,
  entry_points = {'console_scripts': ['cmd = handyman.cmd:main']}
)
