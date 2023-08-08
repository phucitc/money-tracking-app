#!/bin/bash
gunicorn -w 2 'index:app'