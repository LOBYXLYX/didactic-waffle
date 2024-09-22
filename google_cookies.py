import time
import random
import hashlib

class CookieStatic:
    cookie = 'cookieName=someValue'
    referrer = 'https://www.kogama.com'

class GoogleCookies:
    def __init__(self, user_agent) -> None:
        self.hd = lambda: round(2147483647 * random.random())
        self._uastring = user_agent

    def _La(self, a: str) -> int:
        b = 1
        if a:
            for c in range(len(a) - 1, -1, -1):
                d = ord(a[c])
                b = (b << 6 & 268435455) + d + (d << 14)
                d = b & 266338304
                b = b ^ d >> 21 if d != 0 else b
        return b

    def _g_cookie(self) -> str:
        a = self._uastring + (CookieStatic.cookie) + (CookieStatic.referrer)
        b = len(a)
        c = len(a)
        while c > 0:
            a += str(c) + str(b)
            c -= 1
            b += 1
        return '.'.join(
            [str(self.hd() ^ self._La(a) & 2147483647), str(round(time.time()))]
        )
