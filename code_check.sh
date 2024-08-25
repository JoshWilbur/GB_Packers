    #!/bin/bash

    poetry run black . 
    poetry run flake8 .
    poetry run mypy --install-types
    poetry run mypy scrape_stats.py parse_schedule.py