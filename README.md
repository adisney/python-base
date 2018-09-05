# PYTHON BASE
My base repo for python development with a focus on continuous TDD.

# Development

## Requirements
* python 3.6.4
* [pipenv](https://github.com/pypa/pipenv)
* Node.js
* bitgo-express

## Setup Instructions

Follow the below instructions to prepare your development environment. Once you are finished, [run the tests](#running-the-tests) to verify your setup.

### Python 3.6
If you need to install Python 3.6, execute the following:
```
sudo apt install -yq build-essential checkinstall git
sudo apt install -yq libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tar.xz
tar xf Python-3.6.0.tar.xz
cd Python-3.6.0/
./configure
sudo make altinstall
```
The above will install an executable named `python3.6` in a system directoy. Test that your installation was successful by running:
```
python3.6 --version
```

### Pipenv
This project depends on pipenv to manage python dependencies. To install pipenv and initialize the dev environment, execute:
```
python3.6 -m pip install pipenv
pipenv install --python 3.6
```
Ensure that your pipenv is properly initialized by running:
```
pipenv run python --version
```
You should see output similar to the output from `python3.6 --version`, indicating that the version of python the virtual environment is using is at least Python 3.6.

# Running the tests
Run the tests by executing the following command
```
./bin/tests
```

I practice continuous testing. As such, I have the tests run every time a python file changes on disk. To run the test suite continuously run the command
```
./bin/continuous_tests
```

This depends on the presence of the utility [entr](http://entrproject.org/) being present. If it is not found, the tests will be run a single time and exit.
