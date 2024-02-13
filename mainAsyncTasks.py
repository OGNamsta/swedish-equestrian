import asyncio
import json
import time
from time import perf_counter
from aiolimiter import AsyncLimiter
import httpx
import openpyxl


async def log_request(request):
    print(f"Sending request {request.method} {request.url}")


async def log_response(response):
    request = response.request
    print(f"Received response {request.method} {request.url} - {response.status_code}")

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9,en-GB;q=0.8,de;q=0.7,es;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'JSESSIONID=E50A86FF82618645F36545577A720B6A; SiteVisionLTM=\\u0021Ne3x/UrprIoGuyjenlzEFn0oniVgyoHPK8BPTNfMfknyA8c9rDEWl+6jVOErFlxhlqrcG6qAf2s=; _tpc_persistance_cookie=\\u0021OXNO6bD5gkaRUewjYrUrzaw5qWx0afofgVizxRWL0cq3rrSg1oUaHy+Q6vYip92V45/ZmGAkp+LXsXw=; BBN019d87b7=01e09e29e61dfe299d3782b3c6bdc2dbfd367e6a5b81dc00c9cadb493a0fd5ccd7b032bb721730a1c80f620d2213cdf08eb88b4c0b; sv-cookie-consent=.c3YtaW50ZXJuYWwtc3Ytd2ViLWFuYWx5dGljcyxzdi1pbnRlcm5hbC1tdG1fY29va2llX2NvbnNlbnQ=; BBNeec01410053=0827476505ab20004d38ba40432c7da2cb2ec5a4abd7a85845bb667c00f74cf68007dfd8607e309408015fb0e011300060ad08bfc3cd118c91072caf4878cd2307715e2509b017245e6613f418b18d8e25a45601bdb82e74873273f734629e2f',
    'DNT': '1',
    'Pragma': 'no-cache',
    'Referer': 'https://ridsport.se/om-oss/organisation/foreningar',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

cache_name = "organisation_cache800"
file_name = "organisation_ids800"
urls_id = "8"


async def fetch_organisation_info(organisation_id, cache, limiter):
    # Check if the data is already in the cache
    if organisation_id in cache:
        print(f"Fetching organization {organisation_id} from cache")
        return cache[organisation_id]
    # 10 works for 50 organizations
    # Trying 5 for 100 organizations
    # semaphore = asyncio.Semaphore(5)  # Adjust the number based on trial and error

    async with httpx.AsyncClient(event_hooks={'request': [log_request], 'response': [log_response]}, timeout=300.0, headers=headers) as client:
        async with limiter:
            r = await client.get(f'https://ridsport.se/appresource/4.3cb87ac0181add8e8cf3750/12.bf1aab51875678c7738f16d/organisation?organisationId={organisation_id}&svAjaxReqParam=ajax')
            content_type = r.headers.get('Content-Type', '').lower()
            if r.status_code == 200:
                if 'application/json' in content_type:
                    try:
                        result = r.content.decode('utf-8')
                        organisation_data = json.loads(result).get('organisation', {})
                        if organisation_data:
                            results.append(organisation_data)
                            # Cache the fetched data
                            cache[organisation_id] = organisation_data
                            # Save the cache to a JSON file
                            with open(f'caches/{cache_name}.json', 'w') as json_file:
                                json.dump(cache, json_file)
                        else:
                            print(f"No 'organisation' key in the response for organization {organisation_id}")
                    except Exception as e:
                        print(f"Error decoding JSON for organization {organisation_id}: {e}")
                else:
                    print(f"Received error response for organization {organisation_id}: {r.status_code}")
                return


async def main():
    # Create a cache to avoid fetching the same organization info multiple times
    cache = {}
    # Read organisation IDs from the text file
    with open(f"fileSplitting/url_files/urls_{urls_id}.txt", "r") as file:
        organisation_ids = [line.strip() for line in file]

    rate_limit = AsyncLimiter(10, 1)
    tasks = []
    index = 1
    for org_id in organisation_ids:
        # Inside your scraping loop
        retries = 3  # Adjust the number of retries as needed
        for _ in range(retries):
            try:
                # Check if we can create a new task based on the rate limiter
                async with rate_limit:
                    # Make your request here
                    task = asyncio.create_task(fetch_organisation_info(org_id, cache, rate_limit))
                    tasks.append(task)
                    # print the org id and the number.
                    print(f"Fetching organization {org_id} ({index}/{len(organisation_ids)})")
                    index += 1  # Increment index counter
                    # If successful, break the loop
                    break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(5)  # Adjust the sleep duration as needed

    await asyncio.gather(*tasks)
    # await asyncio.sleep(5)

    # Create Excel file
    wb = openpyxl.Workbook()
    ws = wb.active
    print("Creating Excel file...")

    headings = [
        "Organisation Full Name",
        "Association Code",
        "Mobile Number",
        "Phone",
        "Email Address",
        "Website",
        "Address",
        "Postal Code",
        "Postal Place",
        "Sport Name",
        "Regional District Org Name",
    ]
    # Write header row
    ws.append(headings)

    # Write data to rows
    for org_data in results:
        org_info = org_data  # No need to access 'organisation' key again

        row_data = [
            org_info.get('Organisation_name', {}).get('full_name', 'N/A'),
            org_info.get('code', 'N/A'),
            org_info.get('Telephone_number', {}).get('mobile_number', 'N/A'),
            org_info.get('Telephone_number', {}).get('phone_1', 'N/A'),
            org_info.get('Electronic_address', {}).get('email', 'N/A'),
            org_info.get('Electronic_address', {}).get('homepage', 'N/A'),
            org_info.get('Postal_address', {}).get('street_address', 'N/A'),
            org_info.get('Postal_address', {}).get('postal_code', 'N/A'),
            org_info.get('Postal_address', {}).get('postal_place', 'N/A'),
            org_info.get('Sport_registration', [{}])[0].get('Sport', {}).get('name', 'N/A'),
            org_info.get('Belonging', {}).get('Regional_district', {}).get('Organisation_name', {}).get('full_name', 'N/A'),
        ]
        ws.append(row_data)

    # Save the workbook to a file
    wb.save(f"toCompile/{file_name}.xlsx")
    print(f"Saving workbook {file_name}.xlsx")

if __name__ == "__main__":
    results = []
    start = perf_counter()
    asyncio.run(main())
    end = perf_counter()
    print(f"Time taken: {end-start:.2f}s")
    # print(results)
    print(f"Data written to {file_name}.xlsx")
