# Recipe App

## Exercise 1

### Step One

Install Python with Windows installer as well as VSCdoe and create virtual environment.

`mkvirtualenv cf-python-base`

![Step 1](./Exercise%201.1/Step%201.PNG)

### Step 2

Set up an IPython shell and enter it

`pip install ipython`

`ipython`

![Step 2](./Exercise%201.1/Step%202.PNG)

### Step 3

Export a requirements file

`pip freeze > requirements.txt`

![Step 3](./Exercise%201.1/Step%203.PNG)

### Step 4

Import the requirements file into a new environment

`mkvirtualenv cf-python-copy`

`pip install -r requirements.txt`

![Step 4](./Exercise%201.1/Step%204.PNG)

### Step 5

Create and run [add.py script](./Exercise%201.1/add.py)

`python add.py`

![Step 5](./Exercise%201.1/Step%205.PNG)