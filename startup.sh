#!/bin/bash
pip install --no-cache-dir --force-reinstall moviepy
gunicorn app:app
