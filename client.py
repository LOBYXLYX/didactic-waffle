import json
import requests
import random
from google_cookies import GoogleCookies
from requests.cookies import RequestsCookieJar

class Client(GoogleCookies):
    def __init__(self, language='en_US'):
        self.language = language

        self.domain = 'www.kogama.com'
        self.session = requests.Session()
        self.cookie_dict = {
            '_pp': 'WINDOWS',
            'm': '0',
            '_kref': 'kogama',
            'is_american': 'true',
            'is_european': 'true',
            'language': random.choice(['en_US', 'es_ES']) # self.language
        }
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        super().__init__(user_agent=self.user_agent)

    def _get_proxies(self) -> list[str]:
        with open('proxies.txt', 'r') as file:
            proxies = file.read().strip().splitlines()
        return proxies

    def _build_proxy_payload(self) -> dict[str, str]:
        proxy = random.choice(self._get_proxies())
        return {
            'http': proxy,
            'https': proxy
        }

    def _create_cookie_g(self) -> str:
        return 'GA1.2.' + self._g_cookie()

    def _build_cookies(self, sessionToken=None) -> requests.cookies:
        cookiejar = RequestsCookieJar()

        if sessionToken is not None:
            self.cookie_dict['session'] = sessionToken

        self.cookie_dict['_ga'] = self._create_cookie_g()
        self.cookie_dict['_gid'] = self._create_cookie_g()

        for cookie_name, value in self.cookie_dict.items():
            cookiejar.set(name=cookie_name, value=value, domain=self.domain)
        return cookiejar

    def _length(self, payload) -> str:
        return str(len(json.dumps(payload)))

    def Session(self, sessionToken=None) -> requests.Session:
        session = requests.Session()

        if len(self._get_proxies()) > 1:
            session.proxies = self._build_proxy_payload()

        session.cookies = self._build_cookies(sessionToken)
        session.headers = {
            'accept': 'application/json,text/plain,*/*',
            'accept-encoding': 'gzip,deflate,br',
            'accept-language': 'en-US,en;q=0.9,es-US;q=0.8,es;q=0.7',
            'cache-control': 'no-cache',
            'connection': 'keep-alive',
            'host': 'www.kogama.com',
            'user-agent': self.user_agent,
            'pragma': 'no-cache',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin'
        }
        return session
