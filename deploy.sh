#!/bin/bash
cd ./webapp;
npm run build;
npm run deploy-2-python;
cd ..;
gunicorn -w 2 'index:app' --access-logfile access.log --error-logfile error.log -b;