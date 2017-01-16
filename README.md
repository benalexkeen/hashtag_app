## Hashtag Application

This application has been tested using python 2.7 and python 3.5 on Mac OS X and Ubuntu 16.04.

It is recommended to install this application from inside a virtual environment.
For instructions on creating a virtual environment, see the docs [here](https://virtualenv.pypa.io/en/stable/installation/).

### Installation

From this directory:
  * `pip install -r requirements.txt`
  * `python install_nltk_requirements.py`

### Serving

To serve the application:
  * `python hashtag_app.py`
  * Open http://localhost:5000/ in your preferred browser.

### Testing

To run the unit tests:
  * `export NLTK_DATA=./nltk_data/` 
  * `nosetests -v tests.py`
