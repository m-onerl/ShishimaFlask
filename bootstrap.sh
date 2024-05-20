# create our project directory and move to it
mkdir cashman-flask-project && cd cashman-flask-project

# use pipenv to create a Python 3 (--three) virtualenv for our project
pipenv --three

# install flask a dependency on our project
pipenv install flask