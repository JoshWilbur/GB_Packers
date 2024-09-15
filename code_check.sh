    #!/bin/bash

    poetry run black .
    poetry run flake8 .
    poetry run python -m pip install types-beautifulsoup4 types-requests
    poetry run mypy .
    poetry run pytest
