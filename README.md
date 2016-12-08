# speakeasy
experimenting with collecting & exchanging audio snippets from anonymous phone calls

## Running this app locally
1. **Install OS level dependencies**
  - Python 3
  - MySQL
2. **Clone this repo & install app requirements**

  ```bash
  git clone https://github.com/buzzfeed-openlab/speakeasy.git
  cd speakeasy
  pip install -r requirements.txt
  ```
3. **Create a MySQL database**

  ```bash
  mysql -u root -p
  ```
  & then
  ```
  create database story_collector
  ```

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
