#!/bin/bash
gunicorn -w 2 'index:app' --access-logfile logs/access.log --error-logfile logs/error.log;