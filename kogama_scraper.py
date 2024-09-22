from client import Client

WHITELISTED_IDS = [
    11027852,
    10538394,
    21305165, # azukaritas
    10510020
]

class Info:
    new_noticies = []
    categories_list = {
        'new': [],
        'calendar-weekly': [],
        'playing': []
    }
    profiles_list = {}
    noticies_comments = []
    marketplace_products = {}
    profiles_feed = {}

class Scraper:
    def __init__(self) -> None:
        self.api = 'https://www.kogama.com'
        self.session = Client().Session()

    def get_noticies(self, pages=[1]) -> None:
        """
        API: https://www.kogama.com/api/news/<id>/
        """
        for page in pages:
            news = self.session.get(
                f'{self.api}/api/news/',
                params={
                    'page': page,
                    'count': 4,
                    'order': 'desc'
                }
            )
            for new in news.json()['data']:
                if not new['id'] in WHITELISTED_IDS:
                    Info.new_noticies.append(new['id'])

    def get_noticies_comments(self, id) -> None:
        """
        https://www.kogama.com/api/news/<id>/comment/
        Request Payload:
         {
            'comment': message
         }
        """
        comments = self.session.get(
            f'https://www.kogama.com/api/news/{id}/comment/',
            params={'count': 24}
        )
        for comment in comments.json()['data']:
            if not comment['profile_id'] in WHITELISTED_IDS:
                Info.noticies_comments.append(comment['profile_id'])

    def get_categories(self, pages=[1], cate_type='new') -> None:
        """
        API: https://www.kogama.com/game/<id>/comment/
        Request Payload:
         {
            'comment': message
         }

        Categories: new, playing, calendar-weekly
        """
        for page in pages:
            category = self.session.get(
                f'{self.api}/game/category/{cate_type}/',
                params={
                    'page': page,
                    'count': 24
                }
            )
            for cate in category.json()['data']:
                if (cate['id'], cate['owners'][0]['id']) not in WHITELISTED_IDS:
                    Info.categories_list[cate_type].append({
                        'game_id': cate['id'],
                        'owner_id': cate['owners'][0]['id'],
                        'is_recient': True if cate_type == 'new' else False
                    })

    def get_popular_markets(self, category='avatar', pages=[1]) -> None:
        """
        API: https://www.kogama.com/model/market/<id>/comment/
        Request Payload:
         {
            'comment': message
         }
        """
        for page in pages:
            markets = self.session.get(
                f'{self.api}/model/market/',
                params={
                    'page': page,
                    'count': 24,
                    'order': 'undefined',
                    'category': category,
                    'popular': 1
                }
            )
            for market in markets.json()['data']:
                if (market['product_id'], market['author_profile_id']) not in WHITELISTED_IDS:
                    Info.marketplace_products.update({
                        market['product_id']: {
                            'owner_id': market['author_profile_id']
                        }
                    })

    def get_profile_games(self, id) -> None:
        """
        API: https://www.kogama.com/game/<id>/comment/
        Request Payload:
         {
            'comment': message
         }
        """
        game_ids = []
        games = self.session.get(
            f'{self.api}/user/{id}/game/',
            params={'count': 24}
        )
        for game in games.json()['data']:
            #print(game['owners'][0]['username'], game['id'])
            if not game['id'] in WHITELISTED_IDS:
                game_ids.append(game['id'])

        Info.profiles_list.update({id: game_ids})

    def get_profile_feeds(self, id, pages=[1]) -> None:
        """
        API: https://www.kogama.com/api/feed/<id>/comment/
        Request Playload:
         {
            'comment': comment
         }
        """
        if not id in WHITELISTED_IDS:
            Info.profiles_feed[id] = []

        for page in pages:
            feeds = self.session.get(
                f'{self.api}/api/feed/{id}/',
                params={
                    'page': page,
                    'count': 12
                }
            )

            for feed in feeds.json()['data']:
                if not feed['id'] in WHITELISTED_IDS:
                    Info.profiles_feed[id].append(feed['id'])

#sc = Scraper()
#sc.get_profile_feeds(id=4, pages=[1, 2])
#
#print(Info.profiles_feed)
