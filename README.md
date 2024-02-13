# Swedish Equestrian Data Processing

## getOrgID.py
This Python script retrieves organization IDs from a specific API endpoint and saves them to a text file named organisation_ids.txt.

## Requirements
- Python 3.7 or higher
- Required Python libraries: httpx, asyncio

## Usage
Run the script by executing the following command:
`python getOrgID.py`
The script will retrieve organization IDs from the specified API endpoint and save them to a text file named organisation_ids.txt.

## mainAsyncTasks.py
This Python script performs asynchronous tasks to fetch organization information based on organization IDs obtained from the getOrgID.py script. It utilizes rate limiting to control the number of concurrent requests and caches fetched data to avoid redundant requests.
## Requirements
- Python 3.7 or higher
- Required Python libraries: httpx, asyncio, aiolimiter, openpyxl

## Usage
Run the script by executing the following command:
`python mainAsyncTasks.py`
The script will fetch organization information based on organization IDs obtained from the getOrgID.py script. It caches the fetched data, creates an Excel file (organisation_ids800.xlsx) containing organization information, and prints the time taken for execution.

## License
This project is licensed under the MIT License - see the LICENSE file for details.