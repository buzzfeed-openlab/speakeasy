# speakeasy
experimenting with collecting & exchanging audio snippets from anonymous phone calls

## Running this app locally
1. **Install OS level dependencies**
  - Python 3
  - MySQL
  
2. **Clone this repo**
  ```bash
  git clone https://github.com/buzzfeed-openlab/speakeasy.git
  cd speakeasy
  ```
  
3. **Create a virtualenv (optional) & install app requirements**  
 
  ```bash
  virtualenv -p /usr/bin/python3 speakeasy
  source speakeasy/bin/activate
  pip install -r requirements.txt
  ```
  Note: If you're not excited about [virtual environments](http://docs.python-guide.org/en/latest/dev/virtualenvs/), you can also just install the requirements directly. 

3. **Create a MySQL database**

  ```bash
  mysql -u root -p
  ```
  & then
  ```
  create database story_collector;
  ```
  
  If you're working locally, you're good to go. But if you're going to host this on a shared server you probably want to create a new user for this database so it isn't all `root`.

4. **Configure the app**
  Two ways of doing this: (a) making a config file or (b) setting environment variables (for docker)
  
  *Option A*:  
  Copy the example secret config file
  ```bash
  cp story_collector/app_config_secret.py.example story_collector/app_config_secret.py
  ```
  
  Then, edit `story_collector/app_config_secret.py`. At a minimum, change `ADMIN_PASS`
  
  *Option B*:  
  see `story_collector/app_config.py` for the names of environment variables to set

5. **Initialize the database**
  
  ```bash
  python init_db.py
  ```

6. **Run the app**
  
  ```bash
  python app.py
  ```
  

