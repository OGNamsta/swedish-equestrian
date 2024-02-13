import httpx
import asyncio


async def fetch_data():
    url = 'https://ridsport.se/appresource/4.3cb87ac0181add8e8cf3750/12.bf1aab51875678c7738f16d/search'
    params = {
        'query': '',
        'district': '',
        'municipality': '',
        'subSport': '',
        'svAjaxReqParam': 'ajax',
    }

    cookies = {
        'JSESSIONID': 'E50A86FF82618645F36545577A720B6A',
        'SiteVisionLTM': '!Ne3x/UrprIoGuyjenlzEFn0oniVgyoHPK8BPTNfMfknyA8c9rDEWl+6jVOErFlxhlqrcG6qAf2s=',
        '_tpc_persistance_cookie': '!OXNO6bD5gkaRUewjYrUrzaw5qWx0afofgVizxRWL0cq3rrSg1oUaHy+Q6vYip92V45/ZmGAkp+LXsXw=',
        'BBN019d87b7': '01e09e29e61dfe299d3782b3c6bdc2dbfd367e6a5b81dc00c9cadb493a0fd5ccd7b032bb721730a1c80f620d2213cdf08eb88b4c0b',
        'sv-cookie-consent': '.c3YtaW50ZXJuYWwtc3Ytd2ViLWFuYWx5dGljcyxzdi1pbnRlcm5hbC1tdG1fY29va2llX2NvbnNlbnQ=',
        'BBNeec01410053': '0827476505ab20009f6b5fbcb5e077b37329e35d8899c52c3ce63b056a214459f7f6e24809a1b6ca0888fce1191130001eb63d70f26b43bd8faa2f9a44d3573a105d6224037cceba0fac7b0384c8ad52bb27314fb8420c21e0f0f4048e7c765f',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9,en-GB;q=0.8,de;q=0.7,es;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
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

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, cookies=cookies, headers=headers)
        data = response.json()

        # Extracting organization IDs
        organization_ids = [org['id'] for org in data.get('organisations', [])]

        return organization_ids


async def main():
    organization_ids = await fetch_data()
    print("Organization IDs:", organization_ids)
    # Save organization IDs to file
    with open('organisation_ids.txt', 'w') as f:
        for org_id in organization_ids:
            f.write(f'{org_id}\n')

if __name__ == "__main__":
    asyncio.run(main())
