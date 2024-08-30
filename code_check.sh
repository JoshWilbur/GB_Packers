    #!/bin/bash

    poetry run black . 
    poetry run flake8 .
    poetry run python -m pip install types-beautifulsoup4 types-requests
    poetry run mypy scrape_stats.py parse_schedule.py 
    poetry run pytest