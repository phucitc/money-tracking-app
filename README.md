# Deploy VueJS and Python Flask together
- Vuejs: Frontend
  - Must be nodejs >= 16
  - npm run build
  - npm run deploy-2-python
- Flask: Backend
  - pip install -r requirements.txt
  - Start app local
    - flask --app index run or python index.py
  - Start app on Production
    - gunicorn -w 4 'index:app' (gunicorn is only enabled on production mode and run in Ubuntu)

# Setup server and software
- PostgreSQL (Default port: 5432 and It's not allowed to connect from outside, it's only allowed to connect from localhost
  - sudo apt update
  - sudo apt install postgresql postgresql-contrib
  - sudo apt-get install python-psycopg2
  - sudo apt-get install libpq-dev
  - sudo systemctl status postgresql
  - Change password: sudo -u postgres psql
    - ALTER USER postgres WITH PASSWORD 'new_password';
    - \q
    - sudo systemctl restart postgresql
  - Use PGAdmin v4 to manage database and connect to server via SSH tunnel
  - Install python3:
    - sudo apt update
    - sudo apt install python3
    - sudo apt install python3-pip
    - echo "alias python=python3" >> ~/.bashrc
    - source ~/.bashrc
  - Install Virtualenv:
    - sudo apt update
    - sudo apt install python3-venv
    - python3 -m venv env
    - source env/bin/activate


```