# Midterm Assignment
### Note: heat map and Brute Force plot generated do not appear in terminal,
### but they will display when ran in pycharm/ Visual Studio

### The three html charts will save to your folder. 
# Setup for developement:

- Setup a python 3.x venv (usually in `.venv`)
  - You can run `./scripts/create-venv.sh` to generate one
- `pip3 install --upgrade pip`
- Install dev requirements `pip3 install -r requirements.dev.txt`
- Install requirements `pip3 install -r requirements.txt`
- `pre-commit install`

## Update versions

`pip-compile --output-file=requirements.dev.txt requirements.dev.in --upgrade`

# Run `pre-commit` locally.

`pre-commit run --all-files`

```
 Clone repo: git clone -b Midterm https://github.com/bwilder95/FrenchStewart.git
```

Note: Make sure you are in an empty directory, otherwise type '''mkdir newdir'''

Go into the directory where the repo is cloned: '''cd newdir'''

Enter into the FrenchStewart directory: '''cd FrenchStewart'''

Run script: '''./scripts/run-Midterm.sh'''

Note: If you are unable to run script, try typing '''chmod +x ./scripts/run-Midterm.sh'''
and then '''./scripts/run-Midterm.sh'''


