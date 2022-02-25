import os
import requests

class SteamApi():

    USER_AGENT = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4400.8 Safari/537.36'
    }

    def __init__(self):
        pass

    @classmethod
    def GetNewsForApp(self, appid: int, count: int = 5, maxlenght: int = 300):
        """Получение опубликованных новостей о приложение или игре (от новых к более старым)
        https://developer.valvesoftware.com/wiki/Steam_Web_API#GetNewsForApp_(v0002)

        Args:
            appid (int): AppId приложения или игры. Можно узнать на странице игры
            count (int, optional): Количество новостей, которые будут отображены. По умолчанию - 5.
            maxlenght (int, optional): Максимальная длина каждой новости. По умолчанию - 300.

        Raises:
            AttributeError: Missing attributes

        Returns:
            Успех - json
            Ошибка - 'invalid appid'
            Ошибка - 'retry later'

        Json Output: {
            'appid': 730,
            'newsitems': [
                {
                    'gid': '4246335198897543166',
                    'title': 'Counter-Strike: Global Offensive update for 18 February 2022',
                    'url': 'https://steamstore-a.akamaihd.net/news/externalpost/SteamDB/4246335198897543166',
                    'is_external_url': True,
                    author': 'SteamDB',
                    'contents': '<a href="https://steamdb.info/patchnotes/8233299/?utm_source=Steam&utm_medium=Steam&utm_campaign=SteamRSS"> Read patchnotes on SteamDB...</a>',
                    'feedlabel': 'SteamDB',
                    'date': 1645224721,
                    'feedname': 'SteamDB',
                    'feed_type': 0,
                    'appid': 730
                }
            ],
            'count': 1248
        }
        """
        if appid:
            try:
                url = f"http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid={appid}&count={count}&maxlength={maxlenght}&format=json"
                res = requests.get(url, headers = self.USER_AGENT)
                try:
                    json = res.json()['appnews']
                    return json
                except:
                    return 'invalid appid'
            except:
                return 'retry later'
        else:
            raise AttributeError('Missing attributes')

    def Test_GetNewsForApp(self):
        print('\n----------------GetNewsForApp--------------------')
        try:
            logger.info(SteamApi.GetNewsForApp())
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetNewsForApp(-730))
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetNewsForApp(730, -10))
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetNewsForApp(730, 1))
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetNewsForApp(730, 2, 1000))
        except Exception as err:
            logger.error(err)

    @classmethod
    def GetGlobalAchievementPercentagesForApp(self, appid: int):
        """Получение всех достижений и процента пользователей, у которых они имеются в заданной игре
        https://developer.valvesoftware.com/wiki/Steam_Web_API#GetGlobalAchievementPercentagesForApp_(v0002)

        Args:
            appid (int): AppId приложения или игры. Можно узнать на странице игры

        Raises:
            AttributeError: Missing attributes

        Returns:
            Успех - json
            Ошибка - 'invalid appid'
            Ошибка - 'retry later'

        Json Output: [
            {
                "name": "GIVE_DAMAGE_LOW",
                "percent": 66.9000015258789
            },
            ...
            {
                "name": "KILL_ENEMY_LAST_BULLET",
                "percent": 55
            },
            {
                "name": "DAMAGE_NO_KILL",
                "percent": 53.5
            },
            ...
        ]
        """
        if appid:
            try:
                url = f"http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid={appid}&format=json"
                res = requests.get(url, headers = self.USER_AGENT)
                try:
                    json = res.json()['achievementpercentages']['achievements']
                    return json
                except:
                    return 'invalid appid'
            except:
                return 'retry later'
        else:
            raise AttributeError('Missing attributes')

    def Test_GetGlobalAchievementPercentagesForApp(self):
        print('\n------GetGlobalAchievementPercentagesForApp------')
        try:
            logger.info(SteamApi.GetGlobalAchievementPercentagesForApp())
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetGlobalAchievementPercentagesForApp(11111111111))
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetGlobalAchievementPercentagesForApp(730)[0])
        except Exception as err:
            logger.error(err)

    @classmethod
    def GetPlayerSummaries(self, api_key: str, steamid64: str):
        """Получение основной информации о стим аккаунте пользователя
        https://developer.valvesoftware.com/wiki/Steam_Web_API#GetPlayerSummaries_(v0002)

        Args:
            api_key (str): API_KEY с сайта https://steamcommunity.com/dev/apikey
            steamid64 (str): steamid64 пользователя, о котором хотим узнать информацию

        Raises:
            AttributeError: Missing attributes
            AttributeError: You have entered a non-existent ApiKey or Steamid

        Returns:
            Успех - json
            Ошибка - 'invalid steamid'
            Ошибка - 'retry later'

        Json Output (no activity): {
                'steamid': '76561198808376430',
                'communityvisibilitystate': 3,
                'profilestate': 1,
                'personaname': 'Toil',
                'commentpermission': 1,
                'profileurl': 'https://steamcommunity.com/id/ToilOfficial/',
                'avatar': 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/b2/b2b1caed0c91418bffd250fad099d839505dc8fd.jpg',
                'avatarmedium': 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/b2/b2b1caed0c91418bffd250fad099d839505dc8fd_medium.jpg',
                'avatarfull': 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/b2/b2b1caed0c91418bffd250fad099d839505dc8fd_full.jpg',
                'avatarhash': 'b2b1caed0c91418bffd250fad099d839505dc8fd',
                'lastlogoff': 1645312560,
                'personastate': 1,
                'realname': 'Илья',
                'primaryclanid': '103582791429521408',
                'timecreated': 1516713427,
                'personastateflags': 0,
                'loccountrycode': 'RU',
                'locstatecode': '86'
            }

        Json Output (playing a game): {
                'steamid': '76561198808376430',
                'communityvisibilitystate': 3,
                'profilestate': 1,
                'personaname': 'Toil',
                'commentpermission': 1,
                'profileurl': 'https://steamcommunity.com/id/ToilOfficial/',
                'avatar': 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/b2/b2b1caed0c91418bffd250fad099d839505dc8fd.jpg',
                'avatarmedium': 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/b2/b2b1caed0c91418bffd250fad099d839505dc8fd_medium.jpg',
                'avatarfull': 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/b2/b2b1caed0c91418bffd250fad099d839505dc8fd_full.jpg',
                'avatarhash': 'b2b1caed0c91418bffd250fad099d839505dc8fd',
                'lastlogoff': 1645312560,
                'personastate': 1,
                'realname': 'Илья',
                'primaryclanid': '103582791429521408',
                'timecreated': 1516713427,
                'personastateflags': 0,
                'gameextrainfo': 'Counter-Strike: Global Offensive',
                'gameid': '730'
                'loccountrycode': 'RU',
                'locstatecode': '86'
            }
        """
        if all((api_key, steamid64)):
            if len(api_key) == 32 and len(steamid64) == 17:
                try:
                    url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steamid64}&format=json"
                    res = requests.get(url, headers = self.USER_AGENT)
                    try:
                        json = res.json()['response']['players'][0]
                        return json
                    except:
                        return 'invalid steamid'
                except:
                    return 'retry later'
            else:
                raise AttributeError('You have entered a non-existent ApiKey or Steamid')
        else:
            raise AttributeError('Missing attributes')

    def Test_GetPlayerSummaries(self):
        print('\n----------------GetPlayerSummaries---------------')
        try:
            logger.info(SteamApi.GetPlayerSummaries())
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetPlayerSummaries(os.environ.get('STEAM_WEB_APIKEY'), "test"))
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetPlayerSummaries(os.environ.get('STEAM_WEB_APIKEY'), "99999999999999999"))
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetPlayerSummaries(os.environ.get('STEAM_WEB_APIKEY'), "76561198808376430"))
        except Exception as err:
            logger.error(err)


    @classmethod
    def GetFriendList(self, api_key: str, steamid64: str):
        """Получение информации о друзьях определенного пользователя
        https://developer.valvesoftware.com/wiki/Steam_Web_API#GetFriendList_(v0001)

        Args:
            api_key (str): API_KEY с сайта https://steamcommunity.com/dev/apikey
            steamid64 (str): steamid64 пользователя, о котором хотим узнать информацию

        Raises:
            AttributeError: Missing attributes
            AttributeError: You have entered a non-existent ApiKey or Steamid

        Returns:
            Успех - json
            Ошибка - 'invalid steamid or private profile'
            Ошибка - 'retry later'

        Json Output: [
            {
                'steamid': '76561197990537496',
                'relationship': 'friend',
                'friend_since': 1642958015
            },
            {
                'steamid': '76561197995549484',
                'relationship': 'friend',
                'friend_since': 1577648817
            },
            ...
        ]
        """
        if all((api_key, steamid64)):
            if len(api_key) == 32 and len(steamid64) == 17:
                try:
                    url = f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={api_key}&steamid={steamid64}&relationship=friend&format=json"
                    res = requests.get(url, headers = self.USER_AGENT)
                    try:
                        json = res.json()['friendslist']['friends']
                        return json
                    except:
                        return 'invalid steamid or private profile'
                except:
                    return 'retry later'
            else:
                raise AttributeError('You have entered a non-existent ApiKey or Steamid')
        else:
            raise AttributeError('Missing attributes')

    def Test_GetFriendList(self):
        print('\n-------------------GetFriendList-----------------')
        try:
            logger.info(SteamApi.GetFriendList())
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetFriendList(os.environ.get('STEAM_WEB_APIKEY'), "test"))
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetFriendList(os.environ.get('STEAM_WEB_APIKEY'), "99999999999999999"))
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetFriendList(os.environ.get('STEAM_WEB_APIKEY'), "76561198808376430")[0])
        except Exception as err:
            logger.error(err)

    @classmethod
    def GetPlayerAchievements(self, api_key: str, steamid64: str, appid: int):
        """Получение всех достижений и того, получены они пользователем или нет в заданной игре
        https://developer.valvesoftware.com/wiki/Steam_Web_API#GetPlayerAchievements_(v0001)

        Args:
            api_key (str): API_KEY с сайта https://steamcommunity.com/dev/apikey
            steamid64 (str): steamid64 пользователя, о котором хотим узнать информацию
            appid (int): AppId приложения или игры. Можно узнать на странице игры

        Raises:
            AttributeError: Missing attributes

        Returns:
            Успех - json
            Ошибка (приватный профиль) - json
            Ошибка - 'invalid steamid'
            Ошибка - 'retry later'

        Json Output (Success): {
            'steamID': '76561198808376430',
            'gameName': 'Counter-Strike: Global Offensive',
            'achievements': [
                {
                    'apiname': 'WIN_BOMB_PLANT',
                    'achieved': 1,
                    'unlocktime': 1551212377
                },
                {
                    'apiname': 'BOMB_PLANT_LOW',
                    'achieved': 0,
                    'unlocktime': 0
                },
                ...
            ],
            'success': True
        }

        Json Output (Private profile): {
            'error': 'Profile is not public',
            'success': False
        }

        Json Output (invalid appid): {
            'error': 'Requested app has no stats',
            'success': False
        }
        """
        if all((api_key, steamid64, appid)):
            try:
                url = f"http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={appid}&key={api_key}&steamid={steamid64}&format=json"
                res = requests.get(url, headers = self.USER_AGENT)
                try:
                    json = res.json()['playerstats']
                    return json
                except:
                    return 'invalid steamid'
            except:
                return 'retry later'
        else:
            raise AttributeError('Missing attributes')

    def Test_GetPlayerAchievements(self):
        print('\n-------------------GetPlayerAchievements-----------------')
        try:
            logger.info(SteamApi.GetPlayerAchievements())
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetPlayerAchievements(os.environ.get('STEAM_WEB_APIKEY'), "test"))
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetPlayerAchievements(os.environ.get('STEAM_WEB_APIKEY'), "test", -1))
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetPlayerAchievements(os.environ.get('STEAM_WEB_APIKEY'), "test", 730))
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetPlayerAchievements(os.environ.get('STEAM_WEB_APIKEY'), "99999999999999999", -1))
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetPlayerAchievements(os.environ.get('STEAM_WEB_APIKEY'), "99999999999999999", 730))
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetPlayerAchievements(os.environ.get('STEAM_WEB_APIKEY'), "76561198808376430", -1))
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetPlayerAchievements(os.environ.get('STEAM_WEB_APIKEY'), "76561198808376430", 730)['achievements'][0])
        except Exception as err:
            logger.error(err)

    @classmethod
    def GetUserStatsForGame(self, api_key: str, steamid64: str, appid: int):
        """Получение статистики пользователя в заданной игре
        https://developer.valvesoftware.com/wiki/Steam_Web_API#GetUserStatsForGame_(v0002)

        Args:
            api_key (str): API_KEY с сайта https://steamcommunity.com/dev/apikey
            steamid64 (str): steamid64 пользователя, о котором хотим узнать информацию
            appid (int): AppId приложения или игры. Можно узнать на странице игры

        Raises:
            AttributeError: Missing attributes

        Returns:
            Успех - json
            Ошибка - 'invalid steamid or private profile'
            Ошибка - 'retry later'

        Json Output (Success): {
            'steamID': '76561198808376430',
            'gameName': 'ValveTestApp260',
            'stats': [
                {
                    'name': 'total_kills',
                    'value': 89044
                },
                {
                    'name': 'total_deaths',
                    'value': 82887
                },
                ...
            ]
        }
        """
        if all((api_key, steamid64, appid)):
            try:
                url = f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={appid}&key={api_key}&steamid={steamid64}&format=json"
                res = requests.get(url, headers = self.USER_AGENT)
                try:
                    json = res.json()['playerstats']
                    return json
                except:
                    return 'invalid steamid or private profile'
            except:
                return 'retry later'
        else:
            raise AttributeError('Missing attributes')

    def Test_GetUserStatsForGame(self):
        print('\n--------------------GetUserStatsForGame------------------')
        try:
            logger.info(SteamApi.GetUserStatsForGame())
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetUserStatsForGame(os.environ.get('STEAM_WEB_APIKEY'), "test", 730))
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetUserStatsForGame(os.environ.get('STEAM_WEB_APIKEY'), "99999999999999999", 730))
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetUserStatsForGame(os.environ.get('STEAM_WEB_APIKEY'), "76561198808376430", 730)['stats'][0])
        except Exception as err:
            logger.error(err)

    @classmethod
    def GetOwnedGames(self, api_key: str, steamid64: str, include_appinfo: bool = True, include_played_free_games: bool = False):
        """Получение всех игр, которыми владеет пользователь
        https://developer.valvesoftware.com/wiki/Steam_Web_API#GetOwnedGames_(v0001)

        Args:
            api_key (str): API_KEY с сайта https://steamcommunity.com/dev/apikey
            steamid64 (str): steamid64 пользователя, о котором хотим узнать информацию
            include_appinfo (bool, optional): Включать ли название игры и ссылку на логотип игры в конечный вывод? (Если False, то возвращается только appid и наигранное время). По умолчанию - True
            include_played_free_games (bool, optional): Включать ли бесплатные игры в конечный вывод? (Если False, то возвращаются только платные игры, а любые бесплатные игры будут проигнорированы). По умолчанию - False

        Raises:
            AttributeError: Missing attributes

        Returns:
            Успех - json
            Ошибка - 'invalid steamid or private profile'
            Ошибка - 'retry later'

        Json Output (Success):{
            'game_count':	1109
            'games': [
                {
                    'appid': 10,
                    'name': 'Counter-Strike',
                    'playtime_forever': 192,
                    'img_icon_url': '6b0312cda02f5f777efa2f3318c307ff9acafbb5',
                    'img_logo_url': 'af890f848dd606ac2fd4415de3c3f5e7a66fcb9f',
                    'playtime_windows_forever': 151,
                    'playtime_mac_forever': 0,
                    'playtime_linux_forever': 0
                },
                ...
            ]
        }

        """
        if all((api_key, steamid64)):
            try:
                url = f" http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steamid64}&include_appinfo={include_appinfo}&include_played_free_games={include_played_free_games}&format=json"
                res = requests.get(url, headers = self.USER_AGENT)
                try:
                    json = res.json()['response']
                    return json
                except:
                    return 'invalid steamid or private profile'
            except:
                return 'retry later'
        else:
            raise AttributeError('Missing attributes')

    def Test_GetOwnedGames(self):
        print('\n-----------------------GetOwnedGames---------------------')
        try:
            logger.info(SteamApi.GetOwnedGames())
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetOwnedGames(os.environ.get('STEAM_WEB_APIKEY'), "test"))
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetOwnedGames(os.environ.get('STEAM_WEB_APIKEY'), "99999999999999999"))
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetOwnedGames(os.environ.get('STEAM_WEB_APIKEY'), "76561198808376430")['games'][0])
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetOwnedGames(os.environ.get('STEAM_WEB_APIKEY'), "76561198808376430", True, True)['games'][0])
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetOwnedGames(os.environ.get('STEAM_WEB_APIKEY'), "76561198808376430", False, True)['games'][0])
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetOwnedGames(os.environ.get('STEAM_WEB_APIKEY'), "76561198808376430", False, False)['games'][0])
        except Exception as err:
            logger.error(err)

    @classmethod
    def GetRecentlyPlayedGames(self, api_key: str, steamid64: str, count: int = 10):
        """Получение всех игр, которыми владеет пользователь
        https://developer.valvesoftware.com/wiki/Steam_Web_API#GetRecentlyPlayedGames_(v0001)

        Args:
            api_key (str): API_KEY с сайта https://steamcommunity.com/dev/apikey
            steamid64 (str): steamid64 пользователя, о котором хотим узнать информацию
            count (int, optional): Количество отображаемых игр. По умолчанию - 10

        Raises:
            AttributeError: Missing attributes

        Returns:
            Успех - json
            Ошибка - 'invalid steamid or private profile'
            Ошибка - 'retry later'

        Json Output (Success): {
            'game_count': 199,
            'games': [
                {
                    'appid': 10,
                    'name': 'Counter-Strike',
                    'playtime_forever': 192,
                    'img_icon_url': '6b0312cda02f5f777efa2f3318c307ff9acafbb5',
                    'img_logo_url': 'af890f848dd606ac2fd4415de3c3f5e7a66fcb9f',
                    'playtime_windows_forever': 151,
                    'playtime_mac_forever': 0,
                    'playtime_linux_forever': 0
                },
                ...
            ]
        }
        """
        if all((api_key, steamid64)):
            try:
                url = f"http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={api_key}&steamid={steamid64}&count={count}&format=json"
                res = requests.get(url, headers = self.USER_AGENT)
                try:
                    json = res.json()['response']
                    return json
                except:
                    return 'invalid steamid or private profile'
            except:
                return 'retry later'
        else:
            raise AttributeError('Missing attributes')

    def Test_GetRecentlyPlayedGames(self):
        print('\n------------------GetRecentlyPlayedGames-----------------')
        try:
            logger.info(SteamApi.GetRecentlyPlayedGames())
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetRecentlyPlayedGames(os.environ.get('STEAM_WEB_APIKEY'), "test"))
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetRecentlyPlayedGames(os.environ.get('STEAM_WEB_APIKEY'), "99999999999999999"))
        except Exception as err:
            logger.error(err)
        try:
            logger.info(SteamApi.GetRecentlyPlayedGames(os.environ.get('STEAM_WEB_APIKEY'), "76561198808376430", 3))
        except Exception as err:
            logger.error(err)

if __name__ == '__main__':
    # Get env and import logger
    from dotenv import load_dotenv
    from loguru import logger
    load_dotenv(dotenv_path = os.path.join(os.path.dirname(__file__), '../', '.env'))

    # Test GetNewsForApp
    SteamApi = SteamApi()
    SteamApi.Test_GetNewsForApp()

    # Test GetGlobalAchievementPercentagesForApp
    SteamApi.Test_GetGlobalAchievementPercentagesForApp()

    # Test GetPlayerSummaries
    SteamApi.Test_GetPlayerSummaries()

    # Test GetFriendList
    SteamApi.Test_GetFriendList()

    # Test GetPlayerAchievements
    SteamApi.Test_GetPlayerAchievements()

    # Test GetUserStatsForGame
    SteamApi.Test_GetUserStatsForGame()

    # Test GetOwnedGames
    SteamApi.Test_GetOwnedGames()

    # Test GetRecentlyPlayedGames
    SteamApi.Test_GetRecentlyPlayedGames()