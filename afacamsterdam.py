import requests
import json

page_size = 10
current_page = 0
date_from = '01-04-2022'
date_to = '02-04-2022'

def switch_on_http_debug():
    """Switches on http debugging"""
    import logging
    from http.client import HTTPConnection  # py3

    log = logging.getLogger('urllib3')
    log.setLevel(logging.DEBUG)

    # logging from urllib3 to console
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    log.addHandler(ch)

    # print statements from `http.client.HTTPConnection` to console/stdout
    HTTPConnection.debuglevel = 1

def get_cases(page, date_from, date_to):
    """Gets the next page of cases (server-side hard-coded to a pagesize of 10)"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # Already added when you pass json=
        # 'Content-Type': 'application/json',
        'Origin': 'https://www.verlorenofgevonden.nl',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }
    
    params = {
        'q': 'fietsendepot amsterdam',
        'org': '',
        'date_from': date_from,
        'date_to': date_to,
        'from': str(page),
        'site': 'nl',
        'timestamp': '1648891632604',
    }
    
    json_data = {
        'subcategories': [
            'herenfiets',
        ],
        'colors': [],
        'cities': [],
    }

    response = requests.post('https://verlorenofgevonden.nl/scripts//ez.php', headers=headers, params=params, json=json_data)
    data = response.json()
    #print(json.dumps(data, indent=4, sort_keys=True))
    return data['hits']['hits']


def process_cases(cases):
    """Print case info to stdout"""
    for hit in cases:
        case = hit['_source']
        print('')
        print(f"Registratienummer: {case['ObjectNumber']}")
        print(f"Image: https://www.verlorenofgevonden.nl/assets/image/{case['ObjectId']}")
        print(f"Description:\n{case['Description']}")


#switch_on_http_debug()
cases = get_cases(current_page, date_from, date_to)
while cases:
    process_cases(cases)
    current_page += page_size
    cases = get_cases(current_page, date_from, date_to)

