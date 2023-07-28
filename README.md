# Deploy VueJS and Python Flask together
- Vuejs: Frontend
  - npm run build
  - npm run deploy-2-python
- Flask: Backend
  - pip install -r requirements.txt
  - flask --app index run or python index.py

# Setup server and software
- PostgreSQL (Default port: 5432 and It's not allowed to connect from outside, it's only allowed to connect from localhost
  - sudo apt update
  - sudo apt install postgresql postgresql-contrib
  - sudo systemctl status postgresql
  - Change password: sudo -u postgres psql
    - ALTER USER postgres WITH PASSWORD 'new_password';
    - \q
    - sudo systemctl restart postgresql
  - Use PGAdmin v4 to manage database and connect to server via SSH tunnel


```