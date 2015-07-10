# Tests for SQLShare

## Steps to install

- Clone sqlshare-tests

`git clone https://github.com/uw-it-aca/sqlshare-tests`

- Make a virtualenv

`virtualenv sqlshare-tests`

`cd sqlshare-tests`

`source bin/activate`

- Install requirements (check requirements.txt for optional modules)

`pip install -r requirements.txt`

- Configure settings in sqlshare_settings.py

`$EDITOR sqlshare_settings.py`

- Run tests

`python sqlshare_tests.py`

- (Optional) Set env vars to avoid re-entering username and password

`export SQLSHARE_USERNAME=<sqlshare-username>`

`export SQLSHARE_PASSWORD=<sqlshare-password>`

You should probably delete the second line from your history file:

`$EDITOR $HISTFILE`


