# un-decided
experimenting with collecting audio snippets from phone calls - starting with people who feel conflicted about election 2016

## Setup
1. **Install OS level dependencies**
  - Python 3
  - MySQL
2. **Clone this repo & install app requirements**

  ```bash
  git clone https://github.com/buzzfeed-openlab/un-decided.git
  cd un-decided
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

4. **Create your own `app_config.py` file**

  ```bash
  cp story_collector/app_config.py.example story_collector/app_config.py
  ```
  change the settings (e.g. db info) in `app_config.py` as appropriate

5. **Initialize the database**
  
  ```bash
  python init_db.py
  ```
6. **Run the app**
  
  ```bash
  python app.py
  ```
