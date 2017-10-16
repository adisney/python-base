# PYTHON BASE
My base repo for python development with a focus on continuous TDD

## Setup
I reccommend using [virtualenv](https://virtualenv.pypa.io/en/stable/) and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/). To use this repo most effectively, execute the following.

```
git clone git@github.com:adisney/python_base.git
mv python_base your_project_name
cd your_project_name
mkvirtualenv your_project_name
pip install -r requirements.txt
```

## Running tests
There is an executable file in `bin/ `that runs the python tests in the `test/` dir every time you save a file either in `src/` or `test/`. The bash utility [entr](http://entrproject.org/) is needed for this script to execute properly.

The test runner I am using called [green](https://github.com/CleanCut/green) and is compatible with tests written in unittest. This should work with both Python 2.7 and python 3. I have not tested with versions of python earlier than 2.7.

To run your tests continuously, simply execute the following:

```
./bin/tests
```
