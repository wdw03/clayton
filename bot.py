from aiohttp import (
    ClientResponseError,
    ClientSession,
    ClientTimeout
)
from colorama import *
from datetime import datetime
from fake_useragent import FakeUserAgent
import asyncio, json, re, os, random, pytz

wib = pytz.timezone('Asia/Jakarta')

class Clayton:
    def __init__(self) -> None:
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Host': 'tonclayton.fun',
            'Origin': 'https://tonclayton.fun',
            'Pragma': 'no-cache',
            'Referer': 'https://tonclayton.fun/?tgWebAppStartParam=1493482017',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': FakeUserAgent().random
        }
        self.base_url = "https://tonclayton.fun"
        self.api_base_id = None

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(f"""
{Fore.GREEN + Style.BRIGHT}
███████  █████  ██    ██  █████  ███    ██ 
██      ██   ██ ██    ██ ██   ██ ████   ██ 
███████ ███████ ██    ██ ███████ ██ ██  ██ 
     ██ ██   ██  ██  ██  ██   ██ ██  ██ ██ 
███████ ██   ██   ████   ██   ██ ██   ████ 
{Style.RESET_ALL}

{Fore.CYAN + Style.BRIGHT}[1]{Style.RESET_ALL} Add Query
{Fore.CYAN + Style.BRIGHT}[2]{Style.RESET_ALL} Reset Query  
{Fore.CYAN + Style.BRIGHT}[3]{Style.RESET_ALL} Start Bot
        """)

        choice = input(f"{Fore.YELLOW + Style.BRIGHT}Select Option:{Style.RESET_ALL} ")

        if choice == "1":
            query = input(f"{Fore.YELLOW + Style.BRIGHT}Enter Query:{Style.RESET_ALL} ")
            with open("query.txt", "w") as f:
                f.write(query)
            print(f"{Fore.GREEN + Style.BRIGHT}Query saved successfully!{Style.RESET_ALL}")
            input("Press Enter to continue...")
            self.clear_terminal()
            self.welcome()

        elif choice == "2":
            with open("query.txt", "w") as f:
                f.write("")
            print(f"{Fore.GREEN + Style.BRIGHT}Query reset successfully!{Style.RESET_ALL}")
            input("Press Enter to continue...")
            self.clear_terminal() 
            self.welcome()

        elif choice == "3":
            self.clear_terminal()
            print(f"""
{Fore.GREEN + Style.BRIGHT}Auto Claim {Fore.BLUE + Style.BRIGHT}Clayton - BOT
{Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """)
            
        else:
            print(f"{Fore.RED + Style.BRIGHT}Invalid option!{Style.RESET_ALL}")
            input("Press Enter to continue...")
            self.clear_terminal()
            self.welcome()

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    async def find_latest_js_file(self):
        async with ClientSession(timeout=ClientTimeout(total=20)) as session:
            async with session.get(self.base_url) as response:
                response.raise_for_status()
                html = await response.text()
                match = re.search(r'\/assets\/index-[^"]+\.js', html)
                return match.group(0).split('/')[-1] if match else None

    async def fetch_api_base_id(self, retries=5, delay=3):
        for attempt in range(retries):
            js_file = await self.find_latest_js_file()
            if js_file:
                try:
                    async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                        async with session.get(f"{self.base_url}/assets/{js_file}") as response:
                            response.raise_for_status()
                            js_content = await response.text()
                            match = re.findall(r'(\w+)\s*=\s*"([^"]+)"', js_content)
                            if match:
                                for _, api_base_id in match:
                                    if api_base_id.startswith("aT83M535"):
                                        return api_base_id
                            return None
                except (Exception, ClientResponseError) as e:
                    if attempt < retries - 1:
                        await asyncio.sleep(delay)
            else:
                if attempt < retries - 1:
                    await asyncio.sleep(delay)
        return None
    
    async def user_authorization(self, query: str, retries=5):
        url = f'{self.base_url}/api/{self.api_base_id}/user/authorization'
        headers = {
            **self.headers,
            'Content-Length': '0',
            'Init-Data': query,
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
    
    async def save_user(self, query: str, retries=5):
        url = f'{self.base_url}/api/{self.api_base_id}/user/save-user'
        headers = {
            **self.headers,
            'Content-Length': '0',
            'Init-Data': query,
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
                
    async def daily_claim(self, query: str, retries=5):
        url = f'{self.base_url}/api/{self.api_base_id}/user/daily-claim'
        headers = {
            **self.headers,
            'Content-Length': '0',
            'Init-Data': query,
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
    
    async def all_tasks(self, query: str, type: str, retries=5):
        url = f'{self.base_url}/api/{self.api_base_id}/tasks/{type}'
        headers = {
            **self.headers,
            'Init-Data': query,
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.get(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
        
    async def start_tasks(self, query: str, task_id: int, retries=5):
        url = f'{self.base_url}/api/{self.api_base_id}/tasks/complete'
        data = json.dumps({'task_id': task_id})
        headers = {
            **self.headers,
            'Content-Length': str(len(data)),
            'Init-Data': query,
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
        
    async def claim_tasks(self, query: str, task_id: int, retries=5):
        url = f'{self.base_url}/api/{self.api_base_id}/tasks/claim'
        data = json.dumps({'task_id': task_id})
        headers = {
            **self.headers,
            'Init-Data': query,
            'Content-Type': 'application/json'
        }
        headers = {
            **self.headers,
            'Content-Length': str(len(data)),
            'Init-Data': query,
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
        
    async def check_tasks(self, query: str, task_id: int, retries=5):
        url = f'{self.base_url}/api/{self.api_base_id}/tasks/check'
        data = json.dumps({'task_id': task_id})
        headers = {
            **self.headers,
            'Content-Length': str(len(data)),
            'Init-Data': query,
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
        
    async def user_achievements(self, query: str, retries=5):
        url = f'{self.base_url}/api/{self.api_base_id}/user/achievements/get'
        headers = {
            **self.headers,
            'Content-Length': '0',
            'Init-Data': query,
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
        
    async def claim_achievements(self, query: str, type: str, level: int, retries=5):
        url = f'{self.base_url}/api/{self.api_base_id}/user/achievements/claim/{type}/{level}'
        headers = {
            **self.headers,
            'Content-Length': '0',
            'Init-Data': query,
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None

    async def claywheel_info(self, query: str, retries=5):
        url = f'{self.base_url}/api/{self.api_base_id}/spin/info'
        headers = {
            **self.headers,
            'Init-Data': query,
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.get(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None

    async def perform_claywheel(self, query: str, retries=5):
        url = f'{self.base_url}/api/{self.api_base_id}/spin/perform'
        data = json.dumps({'multiplier':3})
        headers = {
            **self.headers,
            'Content-Length': str(len(data)),
            'Init-Data': query,
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
                
    async def start_game1024(self, query: str, retries=5):
        url = f'{self.base_url}/api/{self.api_base_id}/game/start'
        headers = {
            **self.headers,
            'Content-Length': '0',
            'Init-Data': query,
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None

    async def save_tile(self, query: str, session_id: str, tile: int, retries=5):
        url = f'{self.base_url}/api/{self.api_base_id}/game/save-tile'
        data = json.dumps({'session_id':session_id, 'maxTile':tile})
        headers = {
            **self.headers,
            'Content-Length': str(len(data)),
            'Init-Data': query,
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None

    async def over_tile(self, query: str, session_id: str, tile: int, retries=5):
        url = f'{self.base_url}/api/{self.api_base_id}/game/over'
        data = json.dumps({'session_id':session_id, 'multiplier':1, 'maxTile':tile})
        headers = {
            **self.headers,
            'Content-Length': str(len(data)),
            'Init-Data': query,
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
                
    async def start_clayball(self, query: str, retries=5):
        url = f'{self.base_url}/api/clay/start-game'
        data = {}
        headers = {
            **self.headers,
            'Content-Length': str(len(data)),
            'Init-Data': query,
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers, json=data) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
                
    async def end_clayball(self, query: str, score: int, retries=5):
        url = f'{self.base_url}/api/clay/end-game'
        data = json.dumps({'score':score})
        headers = {
            **self.headers,
            'Content-Length': str(len(data)),
            'Init-Data': query,
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
                
    async def start_gamestack(self, query: str, retries=5):
        url = f'{self.base_url}/api/{self.api_base_id}/stack/st-game'
        headers = {
            **self.headers,
            'Content-Length': '0',
            'Init-Data': query,
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None

    async def upadate_stack(self, query: str, score: int, retries=5):
        url = f'{self.base_url}/api/{self.api_base_id}/stack/update-game'
        data = json.dumps({'score':score})
        headers = {
            **self.headers,
            'Content-Length': str(len(data)),
            'Init-Data': query,
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None

    async def end_stack(self, query: str, score: int, retries=5):
        url = f'{self.base_url}/api/{self.api_base_id}/stack/en-game'
        data = json.dumps({'score':score, 'multiplier':1})
        headers = {
            **self.headers,
            'Content-Length': str(len(data)),
            'Init-Data': query,
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
                
    async def process_query(self, query: str):
        user = await self.user_authorization(query)
        if not user:
            self.log(
                f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                f"{Fore.RED + Style.BRIGHT} Query ID May Invalid {Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT}or{Style.RESET_ALL}"
                f"{Fore.YELLOW + Style.BRIGHT} Clayton Server Down {Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
            )
            return
        
        if user:
            await self.save_user(query)
            self.log(
                f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {user['user']['first_name']} {Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT}] [ Balance{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {user['user']['tokens']} $CLAY {Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT}] [ Ticket{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {user['user']['daily_attempts']} {Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT}] [ Streak{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {user['dailyReward']['current_day']} day {Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
            )
            await asyncio.sleep(1)

            daily = user['dailyReward']['can_claim_today']
            if daily:
                claim = await self.daily_claim(query)
                if claim and claim['message'] == 'Daily reward claimed successfully':
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Check-In{Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT} Is Claimed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}] [ Balance{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {claim['tokens']} $CLAY {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} Ticket {claim['daily_attempts']} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                else:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Check-In{Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT} Isn't Claimed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )
            else:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Check-In{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} Is Already Claimed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                )
            await asyncio.sleep(1)

            for type in ['super-tasks', 'partner-tasks', 'default-tasks', 'daily-tasks']:
                tasks = await self.all_tasks(query, type)
                if tasks:
                    completed = False
                    for task in tasks:
                        task_id = task['task_id']
                        is_completed = task['is_completed']
                        is_claimed = task['is_claimed']
                        requires_check = task['task']['requires_check']

                        if task and not is_completed and not is_claimed:
                            if not requires_check:
                                start = await self.start_tasks(query, task_id)
                                if start and start['message'] == 'Task completed':
                                    self.log(
                                        f"{Fore.MAGENTA + Style.BRIGHT}[ Tasks{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} {task['task']['title']} {Style.RESET_ALL}"
                                        f"{Fore.GREEN + Style.BRIGHT}Is Started{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                    )
                                    await asyncio.sleep(1)

                                    claim = await self.claim_tasks(query, task_id)
                                    if claim and claim['message'] == 'Reward claimed':
                                        self.log(
                                            f"{Fore.MAGENTA + Style.BRIGHT}[ Tasks{Style.RESET_ALL}"
                                            f"{Fore.WHITE + Style.BRIGHT} {task['task']['title']} {Style.RESET_ALL}"
                                            f"{Fore.GREEN + Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                            f"{Fore.MAGENTA + Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                            f"{Fore.WHITE + Style.BRIGHT} {claim['reward_tokens']} $CLAY {Style.RESET_ALL}"
                                            f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                            f"{Fore.WHITE + Style.BRIGHT} {claim['game_attempts']} Ticket {Style.RESET_ALL}"
                                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                        )
                                    else:
                                        self.log(
                                            f"{Fore.MAGENTA + Style.BRIGHT}[ Tasks{Style.RESET_ALL}"
                                            f"{Fore.WHITE + Style.BRIGHT} {task['task']['title']} {Style.RESET_ALL}"
                                            f"{Fore.RED + Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                                            f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                        )
                                    await asyncio.sleep(1)

                                else:
                                    self.log(
                                        f"{Fore.MAGENTA + Style.BRIGHT}[ Tasks{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} {task['task']['title']} {Style.RESET_ALL}"
                                        f"{Fore.RED + Style.BRIGHT}Isn't Started{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                    )
                                await asyncio.sleep(1)

                            else:
                                check = await self.check_tasks(query, task_id)
                                if check and check['message'] == 'Task completed':
                                    self.log(
                                        f"{Fore.MAGENTA + Style.BRIGHT}[ Tasks{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} {task['task']['title']} {Style.RESET_ALL}"
                                        f"{Fore.GREEN + Style.BRIGHT}Is Checked{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                    )
                                    await asyncio.sleep(1)

                                    claim = await self.claim_tasks(query, task_id)
                                    if claim and claim['message'] == 'Reward claimed':
                                        self.log(
                                            f"{Fore.MAGENTA + Style.BRIGHT}[ Tasks{Style.RESET_ALL}"
                                            f"{Fore.WHITE + Style.BRIGHT} {task['task']['title']} {Style.RESET_ALL}"
                                            f"{Fore.GREEN + Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                            f"{Fore.MAGENTA + Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                            f"{Fore.WHITE + Style.BRIGHT} {claim['reward_tokens']} $CLAY {Style.RESET_ALL}"
                                            f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                            f"{Fore.WHITE + Style.BRIGHT} {claim['game_attempts']} Ticket {Style.RESET_ALL}"
                                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                        )
                                    else:
                                        self.log(
                                            f"{Fore.MAGENTA + Style.BRIGHT}[ Tasks{Style.RESET_ALL}"
                                            f"{Fore.WHITE + Style.BRIGHT} {task['task']['title']} {Style.RESET_ALL}"
                                            f"{Fore.RED + Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                                            f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                        )
                                    await asyncio.sleep(1)

                                else:
                                    self.log(
                                        f"{Fore.MAGENTA + Style.BRIGHT}[ Tasks{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} {task['task']['title']} {Style.RESET_ALL}"
                                        f"{Fore.RED + Style.BRIGHT}Isn't Checked{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                    )
                                await asyncio.sleep(1)

                        elif task and is_completed and not is_claimed:
                            claim = await self.claim_tasks(query, task_id)
                            if claim and claim['message'] == 'Reward claimed':
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Tasks{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {task['task']['title']} {Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {claim['reward_tokens']} $CLAY {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {claim['game_attempts']} Ticket {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                            else:
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Tasks{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {task['task']['title']} {Style.RESET_ALL}"
                                    f"{Fore.RED + Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                )
                            await asyncio.sleep(1)

                        else:
                            completed = True

                    if completed:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Tasks{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {type} {Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT}Is Completed{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                        )
                    await asyncio.sleep(1)
                        
                else:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Tasks{Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                await asyncio.sleep(1)

            user_achievements = await self.user_achievements(query)
            if user_achievements:
                for type, achievements in user_achievements.items():
                    if type in ["friends", "games", "stars"]:
                        completed = False
                        for achievement in achievements:
                            level = str(achievement['level'])
                            is_completed = achievement['is_completed']
                            is_rewarded = achievement['is_rewarded']

                            if achievement and is_completed and not is_rewarded:
                                claim = await self.claim_achievements(query, type, level)
                                if claim and claim['reward']:
                                    self.log(
                                        f"{Fore.MAGENTA + Style.BRIGHT}[ Achievements{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} {type} {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} Level {level} {Style.RESET_ALL}"
                                        f"{Fore.GREEN + Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT} ][ Reward{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} {claim['reward']} $CLAY {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                    )
                                else:
                                    self.log(
                                        f"{Fore.MAGENTA + Style.BRIGHT}[ Achievements{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} {type} {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} Level {level} {Style.RESET_ALL}"
                                        f"{Fore.RED + Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                    )
                                await asyncio.sleep(1)

                            else:
                                completed = True

                        if completed:
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Achievements{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} {type} {Style.RESET_ALL}"
                                f"{Fore.GREEN + Style.BRIGHT}Is Completed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                            )
                        await asyncio.sleep(1)

            else:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Achievements{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                )
            await asyncio.sleep(1)

            user = await self.user_authorization(query)
            ticket = user['user']['daily_attempts']
            if ticket is not None and ticket > 0:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Play Game{Style.RESET_ALL}"
                    f"{Fore.GREEN + Style.BRIGHT} Is Prepared {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}] [ Ticket{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {ticket} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                )
                await asyncio.sleep(1)

                if ticket >= 2:
                    claywheel = await self.claywheel_info(query)
                    if claywheel:
                        free_spin = claywheel['free_spins']
                        if free_spin and free_spin > 0:
                            perform = await self.perform_claywheel(query)
                            if perform:
                                ticket -= 2
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Game Claywheel{Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT} Is Started {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {perform['win']} $CLAY {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}] [ Ticket{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {ticket} Left {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                            else:
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Game Claywheel{Style.RESET_ALL}"
                                    f"{Fore.RED + Style.BRIGHT} Isn't Started {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                            await asyncio.sleep(3)
                            
                        else:
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Game Claywheel{Style.RESET_ALL}"
                                f"{Fore.YELLOW + Style.BRIGHT} No Available Attempts {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                    else:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Game Claywheel{Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                else:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Game Claywheel{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Isn't Started {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}] [ Reason{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} Tickets Not Enough {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )

                if ticket <= 0:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Play Game{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} No Ticket Remaining {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                    return

                start = await self.start_game1024(query)
                if start and start['message'] == 'Game started successfully':
                    ticket -= 1
                    session_id = start['session_id']
                    tile = 2
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Game 1024{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} ID {session_id} {Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT}Is Started{Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT} ] [ Ticket{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {ticket} Left {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                    await asyncio.sleep(1)
                    
                    save = await self.save_tile(query, session_id, tile)
                    if save and save['message'] == 'MaxTile saved successfully':
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Game 1024{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} ID {session_id} {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}] [ Status{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {tile} Tiles {Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT}Is Saved{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                        )

                        for remaining in range(150, 0, -1):
                            print(
                                f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                                f"{Fore.YELLOW + Style.BRIGHT} {remaining} {Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT}Seconds to Complete Game{Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}   ",
                                end="\r",
                                flush=True
                            )
                            await asyncio.sleep(1)

                        over = await self.over_tile(query, session_id, tile)
                        if over:
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Game 1024{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} ID {session_id} {Style.RESET_ALL}"
                                f"{Fore.GREEN + Style.BRIGHT}Is Completed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} {over['earn']} $CLAY {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} {over['xp_earned']} XP {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Game 1024{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} ID {session_id} {Style.RESET_ALL}"
                                f"{Fore.RED + Style.BRIGHT}Isn't Completed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                            )
                    else:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Game 1024{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} ID {session_id} {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}] [ Status{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {tile} Tiles {Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT}Isn't Saved{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                        )
                else:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Game 1024{Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT} Isn't Started {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                await asyncio.sleep(3)

                while ticket > 0:
                    if ticket <= 0:
                        break

                    start = await self.start_clayball(query)
                    if start:
                        session_id = start['session_id']
                        ticket = start['attempts']
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Game Clayball{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} ID {session_id} {Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT}Is Started{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} ] [ Ticket{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {ticket} Left {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                        await asyncio.sleep(1)

                        for remaining in range(150, 0, -1):
                            print(
                                f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                                f"{Fore.YELLOW + Style.BRIGHT} {remaining} {Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT}Seconds to Complete Game{Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}   ",
                                end="\r",
                                flush=True
                            )
                            await asyncio.sleep(1)

                        score = 250
                        end = await self.end_clayball(query, score)
                        if end:
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Game Clayball{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} ID {session_id} {Style.RESET_ALL}"
                                f"{Fore.GREEN + Style.BRIGHT}Is Completed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} {end['reward']} $CLAY {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Game Clayball{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} ID {session_id} {Style.RESET_ALL}"
                                f"{Fore.RED + Style.BRIGHT}Isn't Completed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}              "
                            )
                    else:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Game Clayball{Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT} Isn't Started {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                    await asyncio.sleep(3)

                    if ticket <= 0:
                        break

                    game_stack = await self.start_gamestack(query)
                    if game_stack:
                        session_id = game_stack['session_id']
                        ticket -= 1
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Game Stack{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} ID {session_id} {Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT}Is Started{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} ] [ Ticket{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {ticket} Left {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                        )

                        score = 10
                        while True:
                            if score == 100:
                                break

                            update = await self.upadate_stack(query, score)
                            if update and update['message'] == 'Score updated successfully':
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Game Stack{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} ID {session_id} {Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT}Is Success to Update{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} ] [ Score{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {score} Remaining {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                            else:
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Game Stack{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} ID {session_id} {Style.RESET_ALL}"
                                    f"{Fore.RED + Style.BRIGHT}Isn't Success to Update{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                )
                            await asyncio.sleep(1)

                            score += 10

                        if score == 100:
                            end = await self.end_stack(query, score)
                            if end:
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Game Stack{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} ID {session_id} {Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT}Is Completed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {end['earn']} $CLAY {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {end['xp_earned']} XP {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                            else:
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Game Stack{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} ID {session_id} {Style.RESET_ALL}"
                                    f"{Fore.RED + Style.BRIGHT}Isn't Completed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                )

                    else:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Game Stack{Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT} Isn't Started {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                    await asyncio.sleep(3)

                if ticket == 0:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Play Game{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} No Ticket Remaining {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                    
            else:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Play Game{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} No Ticket Remaining {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                )

    async def main(self):
        try:
            with open('query.txt', 'r') as file:
                queries = [line.strip() for line in file if line.strip()]

            while True:
                print(f"{Fore.YELLOW + Style.BRIGHT}Looking For API Base ID...{Style.RESET_ALL}")

                self.api_base_id = await self.fetch_api_base_id()
                if not self.api_base_id:
                    self.log(
                        f"{Fore.RED + Style.BRIGHT}API Base ID Not Found. {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}Clayton Server May Down{Style.RESET_ALL}"
                    )
                    for remaining in range(60, 0, -1):
                        print(
                            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT} {remaining} {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}to Try Again...{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}   ",
                            end="\r",
                            flush=True
                        )
                        await asyncio.sleep(1)

                    continue

                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)

                for query in queries:
                    query = query.strip()
                    if query:
                        await self.process_query(query)
                        self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)
                        seconds = random.randint(5, 15)
                        while seconds > 0:
                            formatted_time = self.format_seconds(seconds)
                            print(
                                f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                                f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}",
                                end="\r"
                            )
                            await asyncio.sleep(1)
                            seconds -= 1

                seconds = 21600
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}",
                        end="\r"
                    )
                    await asyncio.sleep(1)
                    seconds -= 1

        except FileNotFoundError:
            self.log(f"{Fore.RED}File 'query.txt' tidak ditemukan.{Style.RESET_ALL}")
            return
        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        bot = Clayton()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] Clayton - BOT{Style.RESET_ALL}",                                       
        )
