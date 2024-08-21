#!/bin/bash

poetry run black . 
poetry run flake8 .
poetry run mypy .