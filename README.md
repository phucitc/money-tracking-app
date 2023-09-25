# Deploy VueJS and Python Flask together
- Vuejs: Frontend
  - Must be nodejs >= 16
  - npm install
  - npm run dev
  - npm run build
  - npm run deploy-2-python
- Flask: Backend
  - pip install -r requirements.txt
  - Start app local
    - flask --app index run or python index.py
  - Start app on Production
    - chmod u+x deploy.sh
    - pm2 startOrReload ecosystem.config.js
    - gunicorn -w 4 'index:app' (gunicorn is only enabled on production mode and run in Ubuntu)
  - Important: Please create folders:
    - storage/qrcode

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

# Setup Gunicorn as a service
This is command to test Gunicorn
- gunicorn -w 2 'index:app';

sudo nano /etc/systemd/system/zipit.service

Content config
```
[Unit]
Description=Gunicorn instance to serve zipit
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/root/all-my-app/money-tracking-app
Environment="PATH=/root/all-my-app/money-tracking-app/env/bin"
ExecStart=/root/all-my-app/money-tracking-app/env/bin/gunicorn -c /root/all-my-app/money-tracking-app/gunicorn_config.py index:app

[Install]
WantedBy=multi-user.target

```
Then run command:
```
sudo systemctl daemon-reload
sudo systemctl start zipit
sudo systemctl restart zipit

sudo systemctl enable zipit
sudo systemctl status zipit
sudo systemctl stop zipit
```
- Note: Please remember create config file `gunicorn_config.py`

# VueJS Knowledge
```sh
In Vue.js, lifecycle hooks are methods that are automatically called at different stages of a component's lifecycle. These hooks provide developers with the ability to execute code at specific points in a component's lifecycle. Here's a description of all the available lifecycle hooks in Vue.js:

beforeCreate: This hook is called before the instance is created. Data and events have not been set up yet.

created: The instance has been created. Data observation, computed properties, and methods are set up. However, the DOM is not yet available for interaction.

beforeMount: This hook is called before the component is mounted to the DOM. Useful for setting up things that need to be done before the component renders.

mounted: The component is now mounted to the DOM. This is where you can interact with the DOM or perform actions that require the DOM's presence.

beforeUpdate: Called before the component is updated, but not for the initial render. It's triggered when data changes and the component is about to re-render.

updated: The component has been updated due to a data change. You can perform actions that need to respond to the updated DOM or component state.

beforeUnmount (Vue 3 Composition API): Called before the component is unmounted and destroyed. It's an equivalent of beforeDestroy in the Options API.

unmounted (Vue 3 Composition API): Called when the component is unmounted and destroyed. An equivalent of destroyed in the Options API.

errorCaptured: A hook for capturing errors thrown by child components.

activated (Vue Router): Called when a component is activated as part of a route navigation.

deactivated (Vue Router): Called when a component is deactivated as part of a route navigation.

renderTracked (Vue 3 Composition API): Called when a property on the component is accessed during rendering.

renderTriggered (Vue 3 Composition API): Called when a reactive dependency used in the render function changes.

These lifecycle hooks provide control over the component's behavior and interaction with the application's lifecycle. It's important to use them appropriately based on the needs of your component and application. Keep in mind that with Vue 3 and the Composition API, there are some changes and additional hooks.
```