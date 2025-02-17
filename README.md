# Simple Website Change Detection

This repository contains a simple GitHub Action that runs weekly to check if specified websites or parts of websites have changed. If changes are detected, the GitHub Action fails, triggering a notification (you can configure the GitHub app to send notifications for failed actions).

The GitHub Action script is located at [.github/workflows/check_websites_weekly.yml](.github/workflows/check_websites_weekly.yml).

## Usage

To use this for your own purposes:

1. Fork this repository or copy the code.
2. Add your own websites and change conditions to `queries.py`.

## License

All code in this project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.