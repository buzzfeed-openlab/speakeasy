# un-decided
experimenting with collecting audio snippets from phone calls - starting with people who feel conflicted about election 2016

## Running this app locally
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

4. **Set environment variables if appropriate**

  see `story_collector/app_config.py`

5. **Initialize the database**
  
  ```bash
  python init_db.py
  ```

6. **Run the app**
  
  ```bash
  python app.py
  ```
