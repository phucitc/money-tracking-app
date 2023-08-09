#!/bin/bash
rm -rf my_app/home/vuejs_webapp;
cd ./webapp;
rm -rf dist;
npm run build;
npm run deploy-2-python;