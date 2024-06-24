# Download PGNs from Chess Life Magazine
Automates the process of downloading pgn files from the US Chess Federation Chess Life Magazine using selenium and webdriver

## Features
- Concurrently scrapes multiple pages to find download links
- Downloads files using Selenium with ChromeDriver
- Configurable download directory and browser options
- Logs errors to file for troubleshooting

## Requirements

- Python 3.x
- `requests`
- `beautifulsoup4`
- `selenium`
- ChromeDriver compatible with your Chrome version

## Installation

1. Install the required Python packages:

```bash
pip install requests beautifulsoup4 selenium
```

2. Download a compatible version of [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/)

3. Update `CHROME_PATH` to your Chrome executable.
4. Set `CHROME_DRIVER_PATH` to your ChromeDriver executable.
5. Optionaly set `DOWNLOAD_DIR`

## Usage

Run the script from the command line:

```bash
python clm.py
```

## Troubleshooting

- Ensure ChromeDriver is compatible with your installed version of Chrome.
- Check the `selenium.log` file for details on any errors encountered during execution.
- Verify that the configured download directory exists and is writable.

## TODO

- Fix issue with Chrome downloading files in wrong directory
