# speakeasy
experimenting with collecting & exchanging audio snippets from anonymous phone calls

## Running this app locally
**1. Install OS level dependencies**
  - Python 3
  - MySQL

**2. Clone this repo**
  ```bash
  git clone https://github.com/buzzfeed-openlab/speakeasy.git
  cd speakeasy
  ```

**3. Install required python libraries**  

Optional but recommended: make a virtual environment using [virtualenv](https://virtualenv.readthedocs.io/en/latest/) and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html).

Notes:
- Instructions for setting up virtualenv [here](http://docs.python-guide.org/en/latest/dev/virtualenvs/).
- `mkvirtualenv` will automatically activate the `speakeasy` environment; to activate it in the future, just use `workon speakeasy`
- if the virtualenv you make isn't python 3 (check w/ `python --version`), use `mkvirtualenv speakeasy -p /path/to/your/python3` (find your python3 path with `which python3`)

```bash
mkvirtualenv rsf
```

Install requirements:
```bash
pip install -r requirements.txt
```


**4. Create a MySQL database**

```bash
mysql -u root
```
& then
```bash
create database story_collector;
```

If you're working locally, you're good to go. But if you're going to host this on a shared server you probably want to create a new user for this database so it isn't all `root`.

**5. Configure the app**

Two ways of doing this: (a) making a config file or (b) setting environment variables (for docker)

*Option A*:  
Copy the example secret config file
```bash
cp story_collector/app_config_secret.py.example story_collector/app_config_secret.py
```

Then, edit `story_collector/app_config_secret.py`. At a minimum, change `ADMIN_PASS`

*Option B*:  
see `story_collector/app_config.py` for the names of environment variables to set

**6. Run the app**

  ```bash
  python application.py
  ```

**7. Initialize the database**

  Visit the `/initialize` route (e.g. `localhost:5000/intialize`) & enter admin credentials (`ADMIN_USER` & `ADMIN_PASS`). This will create the story table & seed it with data.
