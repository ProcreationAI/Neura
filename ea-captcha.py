import requests
from bs4 import BeautifulSoup

session = requests.Session()

#action GET_TIMESTAMP_HMAC
#sitekey 6LewzIEhAAAAAE-bf5ypbqFl5rhvTQUECKDA0T7n

session.headers = {
    'Host': 'exchange.art',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'es-ES,es;q=0.9',
}

""" res = session.get("https://exchange.art/editions/AXHjBjooeNEYmFmzy9wNRPsAr91fCCGCBvQ7JS5NfCre")

print(res.status_code) """


session.headers = {
    'Host': 'www.google.com',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'iframe',
    'referer': 'https://exchange.art/',
    'accept-language': 'es-ES,es;q=0.9',
}

params = {
    'ar': '1',
    'k': '6LewzIEhAAAAAE-bf5ypbqFl5rhvTQUECKDA0T7n',
    'co': 'aHR0cHM6Ly9leGNoYW5nZS5hcnQ6NDQz',
    'hl': 'es',
    'v': '3TZgZIog-UsaFDv31vC4L9R_',
    'size': 'invisible',
    'cb': 'nvr0tqwk7asv',
}

response = session.get('https://www.google.com/recaptcha/enterprise/anchor', params=params)


soup = BeautifulSoup(response.text, "lxml")

token = soup.find("input", {"id": "recaptcha-token"}).get("value")

print(token)



