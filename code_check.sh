    #!/bin/bash

    poetry run black . 
    poetry run flake8 .
    python3 -m pip install types-beautifulsoup4
    python3 -m pip install types-requests
    poetry run mypy packers_stats.py parse_schedule.py