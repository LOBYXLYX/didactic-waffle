import colr
import time
import random

from client import Client
from _tomli import *
from kogama_scraper import Scraper, Info
from concurrent.futures import ThreadPoolExecutor
from typing import Union

R = colr.Colr().hex('#Fb0707')
B = '\33[94m'   # Blue
L = '\033[90m'  # Grey
G = '\033[92m'  # Green
W = '\033[0m'   # White
C = '\033[96m'  # Cyan
P = colr.Colr().hex('#b207f5')

class Console:
    def log(content: str, *args, mode=None, color=W) -> None:
        print(f'{color}{mode.upper()}{W} |', content, *args)

class Kogama:
    def __init__(self) -> None:
        self.client = Client()
        self.api = 'https://www.kogama.com'

    def _cen(self, sessionToken) -> str:
        return sessionToken[:30] + '**'

    def auth_account(self, username: str, password: str) -> tuple:
        session = self.client.Session()
        post_data = {
            'username': username,
            'password': password
        }
        session.headers['content-length'] = self.client._length(post_data)
        login = session.post(f'{self.api}/auth/login/', json=post_data)
        #print(username, login.cookies, login.text)

        if login.status_code == 200:
            Console.log(f'U: {username}', mode='authenticated', color=P)
            return login.cookies['session'], login.json()['data']['id']
        else:
            resp_e = login.json()['error']['__all__'][0]
            Console.log(f'U: {username} | E: {resp_e}', mode='failed', color=R)
            return None, None

    def send_request_friend(
        self,
        sessionToken,
        account_id: Union[str, int],
        profile_id: Union[str, int]
    ) -> None:
        session = self.client.Session(sessionToken)
        post_data = {
            'user_id': profile_id
        }
        send = session.post(f'{self.api}/user/{account_id}/friend', json=post_data)
        session.headers['content-length'] = self.client._length(post_data)

        if send.status_code in [200, 201]:
            Console.log(f'S: {self._cen(sessionToken)} | Profile: {profile_id}', mode='sent friend', color=G)
        else:
            resp_e = send.json()['error']['__all__'][0]
            Console.log(f'S: {self._cen(sessionToken)} | Profile: {profile_id} | E: {resp_e}', mode='failed', color=G)

    def give_game_like(
        self,
        sessionToken: str,
        game_id: Union[str, int]
    ) -> None:
        session = self.client.Session(sessionToken)
        like = session.post(f'{self.api}/game/{game_id}/like/')

        if like.status_code in [200, 201]:
            Console.log(f'S: {self._cen(sessionToken)} | Game: {game_id}', mode='liked game', color=G)
        else:
            resp_e = like.json()['error']['__all__'][0]
            Console.log(f'S: {self._cen(sessionToken)} | Game: {game_id} | E: {resp_e}', mode='failed', color=R)

    def game_session_play(self, game_id: Union[str, int]) -> None:
        session = self.client.Session()
        params = {
            'objectID': str(game_id),
            'profileID': '0',
            'lang': 'en_US',
            'type': 'play'
        }
        play = session.get(f'{self.api}/locator/session/', params=params)
        if play.status_code == 200:
            _token = play.json()['id']
            Console.log(f'T: {_token} | Game ID: {game_id}', mode='session', color=C)
        elif play.status_code == 429:
            Console.log('Ratelimited[429]', mode='failed', color=R)
            time.sleep(30)
        else:
            Console.log(f'E: {play.status_code}', mode='failed', color=R)
        
    def send_comment(
        self, 
        sessionToken: str, 
        game_id: Union[str, int],
        comment: str
    ) -> None:
        session = self.client.Session(sessionToken)
        post_data = {
            'comment': comment
        }
        session.headers['content-length'] = self.client._length(post_data)
        send = session.post(f'{self.api}/game/{game_id}/comment/', json=post_data)

        if send.status_code in [200, 201]:
            Console.log(f'S: {self._cen(sessionToken)} | Game: {game_id}', mode='sent message', color=G)
        else:
            resp_e = send.json()['error']['__all__'][0]
            Console.log(f'S: {self._cen(sessionToken)} | Game: {game_id} | E: {resp_e}', mode='failed', color=R)

    def send_noticie_comment(
        self,
        sessionToken: str,
        noticie_id: Union[str, int],
        comment: str
    ) -> None:
        session = self.client.Session(sessionToken)
        post_data = {
            'comment': comment
        }
        session.headers['content-length'] = self.client._length(post_data)
        send = session.post(f'{self.api}/api/news/{noticie_id}/comment/', json=post_data)

        if send.status_code in [200, 201]:
            Console.log(f'S: {self._cen(sessionToken)} | News: {noticie_id}', mode='sent message', color=G)
        else:
            resp_e = send.json()['error']['__all__'][0]
            Console.log(f'S: {self._cen(sessionToken)} | News: {noticie_id} | E: {resp_e}', mode='failed', color=R)

    def send_market_comment(
        self,
        sessionToken: str,
        product_id: str,
        comment: str
    ) -> None:
        session = self.client.Session(sessionToken)
        post_data = {
            'comment': comment
        }
        session.headers['content-length'] = self.client._length(post_data)
        send = session.post(f'{self.api}/model/market/{product_id}/comment/', json=post_data)

        if send.status_code in [200, 201]:
            Console.log(f'S: {self._cen(sessionToken)} | Product: {product_id}', mode='sent message', color=G)
        else:
            resp_e = send.json()['error']['__all__'][0]
            Console.log(f'S: {self._cen(sessionToken)} | Product: {product_id} | E: {resp_e}', mode='failed', color=R)

    def send_feed_comment(
        self,
        sessionToken: str,
        feed_id: Union[str, int],
        comment: str
    ) -> None:
        session = self.client.Session(sessionToken)
        post_data = {
            'comment': comment
        }
        session.headers['content-length'] = self.client._length(post_data)
        send = session.post(f'{self.api}/api/feed/{feed_id}/comment/', json=post_data)

        if send.status_code in [200, 201]:
            Console.log(f'S: {self._cen(sessionToken)} | Feed: {feed_id}', mode='sent message', color=G)
        else:
            resp_e = send.json()['error']['__all__'][0]
            Console.log(f'S: {self._cen(sessionToken)} | Feed: {feed_id} | E: {resp_e}', mode='failed', color=R)

if __name__ == '__main__':
    scr = Scraper()
    kog = Kogama()

    ALL_GAME_PRODUCTS_IDS = {'games': [], 'products': [], 'news': []}
    ALL_OWNERS_IDS = {'owners': [], 'feeds': []} #!!!!!
    RECIENT_GAMES_IDS = [] # for like game and add pplay

    PLAYERS_COUNT = 0
    GAMES_COUNT = 0
    TOTAL_FEEDS = 0
    PLAY_AMOUNT_PER_ACCOUNT = get_config('config')['play_per_account']

    comment = input('Comment: ')
    amount = int(input('Comment Amount: '))
    max_pages = int(input('Max Pages (example: 1-10): '))
    give_likes_option = input('Give Like to Games (y/n): ').lower() == 'y'
    give_game_play_option = input('Give Games Play [Joiner] (y/n): ').lower() == 'y'
    send_request_friend = input('Send Request Friend (y/n): ').lower() == 'y'

    def _total_feeds_profiles(feeds, id, count) -> int:
        for feed in feeds[id]:
            count += 1

    def spamThread(
        username: str, 
        password: str, 
        game_products_ids: list[Union[str, int]], 
        owners_ids: list[int],
        recient_games: list[int]
    ) -> None:
        try:
            sessionToken, account_id = kog.auth_account(username, password) 

            for objects_data in game_products_ids.items(), owners_ids.items():
                objects_data = dict(objects_data)

                for object, data in objects_data.items():
                    if len(data) != 0:
                        object_id = random.choice(data)

                        if object == 'products':
                            kog.send_market_comment(sessionToken, object_id, comment)
                        elif object == 'games':
                            kog.send_comment(sessionToken, object_id, comment)
                        elif object == 'feeds':
                            kog.send_feed_comment(sessionToken, object_id, comment)
                        elif object == 'news':
                            kog.send_noticie_comment(sessionToken, object_id, comment)

                        elif send_request_friend == True and object == 'owners':
                            kog.send_request_friend(sessionToken, account_id, object_id)

            if len(recient_games) != 0:
                for recient_id in recient_games:
                    if give_likes_option == False and give_game_play_option == False:
                        break

                    if give_likes_option:
                        kog.give_game_like(sessionToken, recient_id)

                    if give_game_play_option:
                        for i in range(PLAY_AMOUNT_PER_ACCOUNT):
                            kog.game_session_play(recient_id)

            if 'session' in kog.client.cookie_dict:
                del kog.client.cookie_dict['session']
        except Exception as e:
            if 'session' in kog.client.cookie_dict:
                del kog.client.cookie_dict['session']
            #print(e.with_traceback())
            print(e)

    print('Getting KoGaMa Information....')
    for _type in ['new', 'playing', 'calendar-weekly']:
        scr.get_categories(pages=[page for page in range(max_pages)], cate_type=_type)

    for data in Info.categories_list.values():
        for _data in data:
            GAMES_COUNT += 1
            print(f'fetched main games:{G}', GAMES_COUNT, W, end='\r')
            ALL_OWNERS_IDS['owners'].append(_data['owner_id'])
            ALL_GAME_PRODUCTS_IDS['games'].append(_data['game_id'])
            
            if _data['is_recient']:
                RECIENT_GAMES_IDS.append(_data['game_id'])

    print()

    scr.get_noticies()
    for new_id in Info.new_noticies:
        players = scr.get_noticies_comments(new_id)
        ALL_GAME_PRODUCTS_IDS['news'].append(new_id)

    for profile_id in Info.noticies_comments:
        PLAYERS_COUNT += 1
        scr.get_profile_feeds(profile_id) # Info.profiles_feed
        
        for feed_id in Info.profiles_feed[profile_id]:
            ALL_OWNERS_IDS['feeds'].append(feed_id)

        print(
            f'Fetched players: {G}{PLAYERS_COUNT}{W}', 
            f'id: {L}{profile_id}{W}',
            f'| Fetched feeds: {G}{len(Info.profiles_feed[profile_id])}{W}', 
            f'on: {L}{profile_id}{W}', 
            f'| Total feeds: {G}{len(ALL_OWNERS_IDS["feeds"])}{W}', 
            end='\r'
        )
        ALL_OWNERS_IDS['owners'].append(profile_id)
        scr.get_profile_games(profile_id)

    for game_id in Info.profiles_list:
        ALL_GAME_PRODUCTS_IDS['games'].append(game_id)

    print()

    print('Fetching KoGaMa MarketPlace....')
    for m_type in ['avatar', 'model']:
        scr.get_popular_markets(category=m_type, pages=[page for page in range(max_pages)])

    for product_id, data in Info.marketplace_products.items():
        ALL_GAME_PRODUCTS_IDS['products'].append(product_id)
        ALL_OWNERS_IDS['owners'].append(data['owner_id'])

    print('Starting Thread....')

    print(ALL_GAME_PRODUCTS_IDS)
    print(ALL_OWNERS_IDS)

    accounts = open('accounts.txt', 'r').read().strip().splitlines()
    max_threads = get_config('config')['max_threads']


    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        for account in accounts:
            for i in range(amount):
                if not ':' in account:
                    continue

                username, password = account.split(':')
                executor.submit(
                    spamThread, 
                    username, 
                    password, 
                    ALL_GAME_PRODUCTS_IDS, 
                    ALL_OWNERS_IDS,
                    RECIENT_GAMES_IDS
                )
