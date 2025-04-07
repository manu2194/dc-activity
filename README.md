# extract_events.py

This script extracts event data (date and events) from an HTML file and outputs it in JSON format.

## Prerequisites

-   Python 3.9+
-   `beautifulsoup4` library

## Installation

1.  Create a virtual environment:

    ```bash
    uv venv
    ```

2.  Activate the virtual environment:

    ```bash
    source .venv/bin/activate
    ```

3.  Install the required dependencies:

    ```bash
    uv pip install beautifulsoup4
    ```

## Usage

1.  Save the HTML content to a file named `sample.html`.
2.  Run the script in test mode:

    ```bash
    python extract_events.py --test
    ```

## Output

The script will output the event data in JSON format to the console.
