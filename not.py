import sys
import json
import time
import requests
from datetime import datetime
from colorama import init, Fore, Style
from urllib.parse import unquote
import cloudscraper
import os
import pyrogram
from pyrogram import Client
from fake_useragent import UserAgent
from pyrogram.raw.functions.messages import RequestAppWebView
from pyrogram.raw.types import InputBotAppShortName
import random


init(autoreset=True)


PROXY_TYPE = "socks5"  # http/socks5
USE_PROXY = False  # True/False
API_ID = 11111111  # апи
API_HASH = 'gfdfgdfgdfgdfgdfgdf'
REF = '382695384'  # рефка для запуска бота
SQUAD = -1001943111151  # айди канала сквала
SQUAD2 = "cmVmPTY5MjIxMjcwODk="  # рефка сквада

# Включите нужные таски убрав #
TASKS_LIST = [
    "x:notcoin",
    "x:notpixel",
    #"invite3frens",
    "paint20pixels",
    #"premium",
    "joinSquad",
    #"spendStars",
    "channel:notpixel_channel",
    "channel:notcoin"
    #"leagueBonusSilver"
    #"leagueBonusGold"
    #"leagueBonusPlatinum"
    ]


class Data:
    def __init__(self, token):
        self.init_data = token

class PixelTod:
    def __init__(self):
        self.scraper = cloudscraper.create_scraper()
        self.DEFAULT_COUNTDOWN = 300  # Интервал между повтором скрипта, 300 сек дефолт
        self.INTERVAL_DELAY = 10  # Интервал между каждым аккаунтом, 10 секунды дефолт
        self.base_headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Content-Type': 'application/json',
            'Origin': 'https://app.notpx.app',
            'Referer': 'https://app.notpx.app/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Ch-Ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128", "Microsoft Edge WebView2";v="128"',
            'Sec-Ch-Ua-mobile': '?0',
            'Sec-Ch-Ua-platform': '"Android"',
            "User-Agent": UserAgent(os='android').random
        }
        self.ref = REF
        self.proxy = None
        self.peer = 'notpixel'
        self.name = "app"
        self.squad_prox = None
        self.account_squad = None

    def data_parsing(self, data):
        return {key: value for key, value in (i.split('=') for i in unquote(data).split('&'))}

    def main(self):
        action = int(input(f'{Fore.LIGHTBLUE_EX}Выберите действие:\n{Fore.LIGHTWHITE_EX}1. Начать фарм\n{Fore.LIGHTWHITE_EX}2. Создать сессию\n>'))

        if not os.path.exists('sessions'):
            os.mkdir('sessions')

        if action == 2:
            self.create_sessions()

        if action == 1:
            sessions = self.pars_sessions()
            accounts = self.check_valid_sessions(sessions)

            if not accounts:
                raise ValueError(f"{Fore.LIGHTRED_EX}Нет валидных сессий")

            while True:
                for idx, account in enumerate(accounts):
                    self.log(f'{Fore.LIGHTYELLOW_EX}Аккаунт {idx+1}: {Fore.LIGHTWHITE_EX}{account}')

                    if USE_PROXY:
                        proxy_dict = {}
                        with open('proxy.txt', 'r') as file:
                            proxy_list = [i.strip().split() for i in file.readlines() if len(i.strip().split()) == 2]
                            for prox, name in proxy_list:
                                proxy_dict[name] = prox
                        proxy = proxy_dict[account]
                        proxy_client = {
                            "scheme": PROXY_TYPE,
                            "hostname": proxy.split(':')[0],
                            "port": int(proxy.split(':')[1]),
                            "username": proxy.split(':')[2],
                            "password": proxy.split(':')[3],
                        }
                        prox = proxy_client
                        self.proxy = f"{PROXY_TYPE}://{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}"
                    else:
                        prox = None
                    self.squad_prox = prox
                    self.account_squad = account
                    data = self.get_tg_web_data(account, prox, ref=self.ref, peer=self.peer, name=self.name)
                    new_data = Data(data)
                    self.process_account(new_data)

                    print('-' * 50)
                    self.countdown(self.INTERVAL_DELAY)
                self.countdown(self.DEFAULT_COUNTDOWN)



    def process_account(self, data):
        self.get_me(data)
        self.claim_hourly_reward(data)
        self.paint_pixel(data)
        self.task(data)
        self.buy_upgrades(data)

    def pars_sessions(self):
        sessions = []
        for file in os.listdir('sessions/'):
            if file.endswith(".session"):
                sessions.append(file.replace(".session", ""))

        self.log(f"{Fore.LIGHTYELLOW_EX}Найдено сессий: {Fore.LIGHTWHITE_EX}{len(sessions)}!")
        return sessions
    def create_sessions(self):
        while True:
            session_name = input(F'{Fore.LIGHTBLUE_EX}Введите название сессии (для выхода нажмите Enter)\n')
            if not session_name:
                return

            if USE_PROXY:
                proxy_dict = {}
                with open('proxy.txt', 'r') as file:
                    proxy_list = [i.strip().split() for i in file.readlines() if len(i.strip().split()) == 2]
                    for prox, name in proxy_list:
                        proxy_dict[name] = prox

                if session_name in proxy_dict:
                    proxy = proxy_dict[session_name]
                    proxy_client = {
                        "scheme": PROXY_TYPE,
                        "hostname": proxy.split(':')[0],
                        "port": int(proxy.split(':')[1]),
                        "username": proxy.split(':')[2],
                        "password": proxy.split(':')[3],
                    }

                    with pyrogram.Client(
                        api_id=API_ID,
                        api_hash=API_HASH,
                        name=session_name,
                        workdir="sessions/",
                        proxy=proxy_client
                    ) as session:
                        user_data = session.get_me()
                    self.log(f'{Fore.LIGHTYELLOW_EX}Добавлена сессия +{user_data.phone_number} @{user_data.username} PROXY {proxy.split(":")[0]}')
                else:

                    with pyrogram.Client(
                        api_id=API_ID,
                        api_hash=API_HASH,
                        name=session_name,
                        workdir="sessions/"
                    ) as session:


                        user_data = session.get_me()

                    self.log(f'{Fore.LIGHTYELLOW_EX}Добавлена сессия +{user_data.phone_number} @{user_data.username} PROXY : NONE')
            else:

                with pyrogram.Client(
                        api_id=API_ID,
                        api_hash=API_HASH,
                        name=session_name,
                        workdir="sessions/"
                ) as session:

                    user_data = session.get_me()

                self.log(f'{Fore.LIGHTYELLOW_EX}Добавлена сессия +{user_data.phone_number} @{user_data.username} PROXY : NONE')

    def check_valid_sessions(self, sessions: list):
        self.log(f"{Fore.LIGHTYELLOW_EX}Проверяю сессии на валидность!")
        valid_sessions = []
        if USE_PROXY:
            proxy_dict = {}
            with open('proxy.txt', 'r') as file:
                proxy_list = [i.strip().split() for i in file.readlines() if len(i.strip().split()) == 2]
                for prox, name in proxy_list:
                    proxy_dict[name] = prox
            for session in sessions:
                try:
                    if session in proxy_dict:
                        proxy = proxy_dict[session]
                        proxy_client = {
                            "scheme": PROXY_TYPE,
                            "hostname": proxy.split(':')[0],
                            "port": int(proxy.split(':')[1]),
                            "username": proxy.split(':')[2],
                            "password": proxy.split(':')[3],
                        }
                        client = Client(name=session, api_id=API_ID, api_hash=API_HASH, workdir="sessions/",
                                        proxy=proxy_client)

                        if client.connect():
                            valid_sessions.append(session)
                        else:
                            self.log(f"{Fore.LIGHTRED_EX}{session}.session is invalid")

                        client.disconnect()
                    else:
                        client = Client(name=session, api_id=API_ID, api_hash=API_HASH, workdir="sessions/")

                        if client.connect():
                            valid_sessions.append(session)
                        else:
                            self.log(f"{Fore.LIGHTRED_EX}{session}.session is invalid")
                        client.disconnect()
                except:
                    self.log(f"{Fore.LIGHTRED_EX}{session}.session is invalid")
            self.log(f"{Fore.LIGHTYELLOW_EX}Валидных сессий: {Fore.LIGHTWHITE_EX}{len(valid_sessions)}; {Fore.LIGHTYELLOW_EX}Невалидных: {Fore.LIGHTWHITE_EX}{len(sessions) - len(valid_sessions)}")

        else:
            for session in sessions:
                try:
                    client = Client(name=session, api_id=API_ID, api_hash=API_HASH, workdir="sessions/")

                    if client.connect():
                        valid_sessions.append(session)
                    else:
                        self.log(f"{session}.session is invalid")
                    client.disconnect()
                except:
                    self.log(f"{Fore.LIGHTRED_EX}{session}.session is invalid")
            self.log(f"{Fore.LIGHTYELLOW_EX}Валидных сессий: {Fore.LIGHTWHITE_EX}{len(valid_sessions)}; {Fore.LIGHTYELLOW_EX}Невалидных: {Fore.LIGHTWHITE_EX}{len(sessions) - len(valid_sessions)}")
        return valid_sessions

    def get_tg_web_data(self, account, prox, ref: str, peer: str, name: str):
        auth_url = None
        if USE_PROXY:
            client = Client(name=account, api_id=API_ID, api_hash=API_HASH, workdir="sessions/", proxy=prox)
        else:
            client = Client(name=account, api_id=API_ID, api_hash=API_HASH, workdir="sessions/")
        client.connect()

        try:
            bot = client.resolve_peer(peer)
            app = InputBotAppShortName(bot_id=bot, short_name=f"{name}")
            web_view = client.invoke(RequestAppWebView(
                    peer=bot,
                    app=app,
                    platform='android',
                    write_allowed=True,
                    start_param=ref
                ))
            auth_url = web_view.url
            json.loads((unquote(string=unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])))[5:].split('&chat_instance')[0])

            client.join_chat('notpixel_channel')
            client.join_chat('notcoin')




        except Exception as err:
            self.log(f"{err}")
        client.disconnect()
        return unquote(auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])



    def countdown(self, t):
        while t:
            one, two = divmod(t, 3600)
            three, four = divmod(two, 60)
            print(f"{Fore.LIGHTWHITE_EX}Ожидание до {one:02}:{three:02}:{four:02} ", flush=True, end="\r")
            t -= 1
            time.sleep(1)
        print("                          ", flush=True, end="\r")

    def api_call(self, url, data=None, headers=None, method='GET'):
        while True:
            try:
                if hasattr(self, 'proxy'):
                    proxy_dict = {
                        "http": self.proxy,
                        "https": self.proxy,
                    }
                else:
                    proxy_dict = None
                if method == 'GET':
                    res = self.scraper.get(url, headers=headers, proxies=proxy_dict)
                elif method == 'POST':
                    res = self.scraper.post(url, headers=headers, data=data, proxies=proxy_dict)
                else:
                    raise ValueError(f'Не поддерживаемый метод: {method}')
                if res.status_code == 401:
                    self.log(f'{Fore.LIGHTRED_EX}{res.text}')
                return res
            except (
            requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout,
            requests.exceptions.Timeout):
                self.log(f'{Fore.LIGHTRED_EX}Ошибка подключения соединения!')

                time.sleep(3)

    def get_me(self, data: Data):
        url = "https://notpx.app/api/v1/users/me"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"initData {data.init_data}"
        res = self.api_call(url, headers=headers)
        if res.status_code == 200 or res.status_code == 201:
            response_data = res.json()
            self.log(f"{Fore.LIGHTYELLOW_EX}Аккаунт: {Fore.LIGHTWHITE_EX}{response_data['firstName']}")
            self.log(f"{Fore.LIGHTYELLOW_EX}Баланс: {Fore.LIGHTWHITE_EX}{response_data['balance']}")
            squad = response_data['squad']

            if squad['id'] is None:

                tg_web_data = self.get_tg_web_data(account=self.account_squad, prox=self.squad_prox, peer="notgames_bot", ref=SQUAD2, name="squads")

                bearer_token = None
                custom_headers = {
                    "Accept": "*/*",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate, br, zstd",
                    "Referer": "https://webapp.notcoin.tg/",
                    "content-type": "application/json",
                    "Origin": "https://webapp.notcoin.tg",
                    "Connection": "keep-alive",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-site",
                    "Priority": "u=4",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
                }
                try:
                    login_url = "https://api.notcoin.tg/auth/login"
                    custom_headers["Host"] = "api.notcoin.tg"
                    custom_headers["bypass-tunnel-reminder"] = "x"

                    custom_headers['Content-Length'] = str(len(tg_web_data) + 18)
                    custom_headers['x-auth-token'] = "Bearer null"
                    r = {"webAppData": f"{tg_web_data}"}

                    login_req = self.api_call(login_url, headers=custom_headers, data=json.dumps(r), method='POST')

                    if login_req.status_code == 200 or login_req.status_code == 201:
                        login_data = login_req.json()
                        bearer_token = login_data.get("data", {}).get("accessToken", None)
                        time.sleep(3)
                        if not bearer_token:
                            raise Exception
                except Exception as error:
                    self.log(f"{Fore.LIGHTRED_EX}Ошибка логина сквада: {error}")
                custom_headers["Content-Length"] = "26"
                custom_headers["x-auth-token"] = f"Bearer {bearer_token}"

                try:
                    join_url = "https://api.notcoin.tg/squads/absolateA/join"
                    b = {"chatId": SQUAD}
                    login_req = self.api_call(join_url, headers=custom_headers, data=json.dumps(b), method='POST')
                    if login_req.status_code == 200 or login_req.status_code == 201:
                        self.log(f"{Fore.LIGHTYELLOW_EX}Вступил в сквад")

                except Exception as error:
                    self.log(f"{Fore.LIGHTRED_EX}Ошибка вступления в сквад: {error}")
            time.sleep(3)



    def hourly_reward_stats(self, data: Data) -> bool:
        url = "https://notpx.app/api/v1/mining/status"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"initData {data.init_data}"
        res = self.api_call(url, headers=headers)
        if res.status_code == 200 or res.status_code == 201:
            response_data = res.json()
            if response_data["fromStart"] > 3600:
                return True


    def claim_hourly_reward(self, data: Data):
        if self.hourly_reward_stats(data):
            url = "https://notpx.app/api/v1/mining/claim"
            headers = self.base_headers.copy()
            headers["Authorization"] = f"initData {data.init_data}"
            res = self.api_call(url, headers=headers)
            if res.status_code == 200 or res.status_code == 201:
                self.log(f"{Fore.LIGHTYELLOW_EX}Забрал ревард")
            else:
                self.log(f"{Fore.LIGHTRED_EX}Ошибка {res.text}")


    def position_to_coordinates(self, position, width=1000):
        x = (position - 1) % width
        y = (position - 1) // width
        return x, y


    def paint_pixel(self, data: Data):
        url = "https://notpx.app/api/v1/mining/status"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"initData {data.init_data}"
        res = self.api_call(url, headers=headers)

        if res.status_code == 200 or res.status_code == 201:
            response_data = res.json()
            num = response_data['charges']
            for _ in range(num):
                time.sleep(3)
                color = random.choice(["#e46e6e", "#FFD635", "#7EED56", "#00CCC0", "#51E9F4", "#94B3FF", "#E4ABFF", "#FF99AA", "#FFB470", "#FFFFFF"])
                pixel_id = random.randint(1, 1000000)
                datat = {
                    "pixelId": pixel_id,
                    "newColor": color
                }
                url = "https://notpx.app/api/v1/repaint/start"
                headers = self.base_headers.copy()
                headers["Authorization"] = f"initData {data.init_data}"
                res = self.api_call(url, headers=headers, data=json.dumps(datat), method='POST')
                if res.status_code == 200 or res.status_code == 201:
                    self.log(
                        f"{Fore.LIGHTYELLOW_EX}Нарисовал {Fore.LIGHTWHITE_EX}{self.position_to_coordinates(pixel_id)} {Fore.LIGHTYELLOW_EX}Цвет {Fore.LIGHTWHITE_EX}{color}")
                else:
                    self.log(f"{Fore.LIGHTRED_EX}Не могу нарисавать ")
                    break



    def buy_upgrades(self, data: Data):
        url = "https://notpx.app/api/v1/mining/status"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"initData {data.init_data}"
        res = self.api_call(url, headers=headers)

        if res.status_code == 200 or res.status_code == 201:
            response_data = res.json()
            boost = response_data["boosts"]


            time.sleep(3)
            if boost["paintReward"] < 7:
                url1 = "https://notpx.app/api/v1/mining/boost/check/paintReward"
                headers1 = self.base_headers.copy()
                headers1["Authorization"] = f"initData {data.init_data}"
                res1 = self.api_call(url1, headers=headers1)
                if res1.status_code == 200 or res1.status_code == 201:
                    response_data1 = res1.json()
                    if response_data1["paintReward"]:
                        self.log(f"{Fore.LIGHTYELLOW_EX}Купил улучшение {Fore.LIGHTWHITE_EX}Paint Reward")


            time.sleep(3)
            if boost["reChargeSpeed"] < 11:
                url2 = "https://notpx.app/api/v1/mining/boost/check/reChargeSpeed"
                headers2 = self.base_headers.copy()
                headers2["Authorization"] = f"initData {data.init_data}"
                res2 = self.api_call(url2, headers=headers2)
                if res2.status_code == 200 or res2.status_code == 201:
                    response_data2 = res2.json()
                    if response_data2["reChargeSpeed"]:
                        self.log(f"{Fore.LIGHTYELLOW_EX}Купил улучшение {Fore.LIGHTWHITE_EX}Recharging Speed")



            time.sleep(3)
            if boost["energyLimit"] < 6:
                url3 = "https://notpx.app/api/v1/mining/boost/check/energyLimit"
                headers3 = self.base_headers.copy()
                headers3["Authorization"] = f"initData {data.init_data}"
                res3 = self.api_call(url3, headers=headers3)
                if res3.status_code == 200 or res3.status_code == 201:
                    response_data3 = res3.json()
                    if response_data3["energyLimit"]:
                        self.log(f"{Fore.LIGHTYELLOW_EX}Купил улучшение {Fore.LIGHTWHITE_EX}Energy Limit")


    def task(self, data: Data):
        url = "https://notpx.app/api/v1/mining/status"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"initData {data.init_data}"
        res = self.api_call(url, headers=headers)

        if res.status_code == 200 or res.status_code == 201:
            response_data = res.json()
            tasks = response_data["tasks"].keys()
            repaints = response_data['repaintsTotal']

            for task in TASKS_LIST:
                if task not in tasks:
                    if task == 'paint20pixels':
                        if repaints < 20:
                            continue
                    if "channel" in task:
                        entity, name = task.split(':')
                        taskk = f"{entity}?name={name}"
                        url2 = f'https://notpx.app/api/v1/mining/task/check/{taskk}'
                    else:
                        url2 = f'https://notpx.app/api/v1/mining/task/check/{task}'
                    time.sleep(3)

                    headers1 = self.base_headers.copy()
                    headers1["Authorization"] = f"initData {data.init_data}"
                    res1 = self.api_call(url2, headers=headers1)
                    if res1.status_code == 200 or res1.status_code == 201:
                        response_data1 = res1.json()
                        status = response_data1[task]
                        if status:
                            self.log(f"{Fore.LIGHTYELLOW_EX}Выполнил задание: {Fore.LIGHTWHITE_EX}{task}")



    def log(self, message):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{Fore.LIGHTBLACK_EX}[{now}]{Style.RESET_ALL} {message}")



if __name__ == "__main__":
    try:
        app = PixelTod()
        app.main()
    except KeyboardInterrupt:
        sys.exit()
