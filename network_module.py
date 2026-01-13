"""
Network Module - Proxy Management and Google Search
Handles proxy scraping, validation, rotation, and Google search automation
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import random
from typing import List, Dict, Optional
from urllib.parse import quote_plus
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from colorama import Fore, Style

class ProxyManager:
    """Aggressive proxy scraper and manager with multiple sources"""
    
    def __init__(self, max_proxies=50):
        self.ua = UserAgent()
        self.proxies = []
        self.user_proxies = []
        self.max_proxies = max_proxies
        self.validated_proxies = []
        
        # Expanded proxy sources
        self.proxy_sources = [
            "https://www.free-proxy-list.net/",
            "https://www.sslproxies.org/",
            "https://www.us-proxy.org/",
            "https://www.proxy-list.download/HTTP",
            "https://www.proxy-list.download/HTTPS",
            "https://www.proxy-list.download/SOCKS4",
            "https://www.proxy-list.download/SOCKS5",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
        ]
        
        # API sources
        self.api_sources = [
            "https://api.proxyscrape.com/v2/?request=get&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
            "https://api.proxyscrape.com/v2/?request=get&protocol=https&timeout=10000&country=all&ssl=all&anonymity=all",
            "https://api.proxyscrape.com/v2/?request=get&protocol=socks4&timeout=10000&country=all",
            "https://api.proxyscrape.com/v2/?request=get&protocol=socks5&timeout=10000&country=all",
            "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=http%2Chttps",
        ]
    
    def get_headers(self):
        """Generate random headers"""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    def load_user_proxies(self, filepath: str):
        """Load proxies from user-provided file (format: ip:port)"""
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if ':' in line:
                            ip, port = line.split(':')
                            self.user_proxies.append({
                                'ip': ip.strip(),
                                'port': port.strip(),
                                'protocol': 'http',
                                'source': 'user_provided'
                            })
            print(f"{Fore.GREEN}[+] Loaded {len(self.user_proxies)} user proxies{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.YELLOW}[!] Error loading user proxies: {e}{Style.RESET_ALL}")
    
    def scrape_html_source(self, url: str) -> List[Dict]:
        """Scrape proxies from HTML table sources"""
        proxies = []
        try:
            response = requests.get(url, headers=self.get_headers(), timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            table = soup.find('table')
            if table:
                rows = table.find_all('tr')[1:]
                for row in rows[:self.max_proxies]:
                    cols = row.find_all('td')
                    if len(cols) >= 2:
                        ip = cols[0].text.strip()
                        port = cols[1].text.strip()
                        protocol = 'https' if len(cols) > 6 and 'yes' in cols[6].text.lower() else 'http'
                        proxies.append({
                            'ip': ip,
                            'port': port,
                            'protocol': protocol,
                            'source': url
                        })
        except Exception as e:
            pass
        return proxies
    
    def scrape_text_source(self, url: str) -> List[Dict]:
        """Scrape proxies from raw text sources"""
        proxies = []
        try:
            response = requests.get(url, headers=self.get_headers(), timeout=10)
            if response.status_code == 200:
                lines = response.text.strip().split('\n')
                for line in lines[:self.max_proxies]:
                    line = line.strip()
                    if ':' in line and not line.startswith('#'):
                        parts = line.split(':')
                        if len(parts) >= 2:
                            ip = parts[0].strip()
                            port = parts[1].strip()
                            protocol = 'https' if 'https' in url.lower() or 'socks' in url.lower() else 'http'
                            proxies.append({
                                'ip': ip,
                                'port': port,
                                'protocol': protocol,
                                'source': url
                            })
        except Exception as e:
            pass
        return proxies
    
    def scrape_api_source(self, url: str) -> List[Dict]:
        """Scrape proxies from API sources"""
        proxies = []
        try:
            response = requests.get(url, headers=self.get_headers(), timeout=10)
            if response.status_code == 200:
                if 'geonode' in url:
                    data = response.json()
                    for proxy in data.get('data', [])[:self.max_proxies]:
                        proxies.append({
                            'ip': proxy.get('ip'),
                            'port': str(proxy.get('port')),
                            'protocol': proxy.get('protocols', ['http'])[0],
                            'source': 'geonode'
                        })
                else:
                    lines = response.text.strip().split('\n')
                    for line in lines[:self.max_proxies]:
                        if ':' in line:
                            ip, port = line.strip().split(':')
                            protocol = 'https' if 'https' in url or 'socks' in url else 'http'
                            proxies.append({
                                'ip': ip,
                                'port': port,
                                'protocol': protocol,
                                'source': url
                            })
        except Exception as e:
            pass
        return proxies
    
    def scrape_all_sources(self):
        """Aggressively scrape all proxy sources"""
        all_proxies = []
        
        # Add user proxies first
        all_proxies.extend(self.user_proxies)
        
        with tqdm(total=len(self.proxy_sources) + len(self.api_sources), 
                 desc="Scraping proxies", unit="source", ncols=80) as pbar:
            
            # Scrape HTML/text sources
            for url in self.proxy_sources:
                if 'github' in url or 'raw' in url:
                    proxies = self.scrape_text_source(url)
                else:
                    proxies = self.scrape_html_source(url)
                all_proxies.extend(proxies)
                pbar.update(1)
                time.sleep(0.5)
            
            # Scrape API sources
            for url in self.api_sources:
                proxies = self.scrape_api_source(url)
                all_proxies.extend(proxies)
                pbar.update(1)
                time.sleep(0.5)
        
        # Remove duplicates
        unique_proxies = []
        seen = set()
        for proxy in all_proxies:
            key = (proxy['ip'], proxy['port'])
            if key not in seen:
                seen.add(key)
                unique_proxies.append(proxy)
        
        print(f"{Fore.GREEN}[+] Scraped {len(unique_proxies)} unique proxies{Style.RESET_ALL}")
        
        # Validate proxies
        self.validate_proxies(unique_proxies[:self.max_proxies * 3])
    
    def validate_proxy(self, proxy: Dict) -> Optional[Dict]:
        """Validate a single proxy"""
        try:
            proxy_url = f"{proxy['protocol']}://{proxy['ip']}:{proxy['port']}"
            proxies = {'http': proxy_url, 'https': proxy_url}
            
            response = requests.get(
                "http://httpbin.org/ip",
                proxies=proxies,
                timeout=5,
                headers={'User-Agent': self.ua.random}
            )
            
            if response.status_code == 200:
                proxy['validated'] = True
                proxy['response_time'] = response.elapsed.total_seconds()
                return proxy
        except:
            pass
        return None
    
    def validate_proxies(self, proxies: List[Dict], max_workers=30):
        """Validate proxies concurrently"""
        print(f"{Fore.CYAN}[*] Validating {len(proxies)} proxies...{Style.RESET_ALL}")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_proxy = {executor.submit(self.validate_proxy, proxy): proxy for proxy in proxies}
            
            for future in tqdm(as_completed(future_to_proxy), total=len(proxies), 
                             desc="Validating", unit="proxy", ncols=80):
                result = future.result()
                if result:
                    self.validated_proxies.append(result)
                    if len(self.validated_proxies) >= self.max_proxies:
                        break
        
        self.validated_proxies.sort(key=lambda x: x.get('response_time', 999))
        self.proxies = self.validated_proxies
        print(f"{Fore.GREEN}[+] Validated {len(self.validated_proxies)} working proxies{Style.RESET_ALL}")
    
    def get_proxy(self) -> Optional[Dict]:
        """Get next available proxy"""
        if self.proxies:
            return random.choice(self.proxies[:10])  # Use top 10 fastest
        return None
    
    def has_proxies(self) -> bool:
        """Check if proxies are available"""
        return len(self.proxies) > 0
    
    def get_proxy_count(self) -> int:
        """Get total proxy count"""
        return len(self.proxies)


class GoogleSearcher:
    """Enhanced Google search with rate limit bypass"""
    
    def __init__(self, proxy_manager: Optional[ProxyManager] = None, threads=10):
        self.proxy_manager = proxy_manager
        self.ua = UserAgent()
        self.threads = threads
        self.results = []
        self.search_engines = [
            "https://www.google.com/search?q={}",
            "https://www.bing.com/search?q={}",
            "https://duckduckgo.com/?q={}",
        ]
    
    def get_headers(self):
        """Generate realistic browser headers"""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
        }
    
    def search_google(self, query: str, num_results: int = 10) -> List[Dict]:
        """Search Google with rate limit bypass"""
        results = []
        max_retries = 3
        
        for retry in range(max_retries):
            try:
                # Get proxy if available
                proxy = self.proxy_manager.get_proxy() if self.proxy_manager else None
                proxies = {}
                if proxy:
                    proxy_url = f"{proxy['protocol']}://{proxy['ip']}:{proxy['port']}"
                    proxies = {'http': proxy_url, 'https': proxy_url}
                
                # Randomize search engine
                search_url = random.choice(self.search_engines).format(quote_plus(query))
                
                session = requests.Session()
                response = session.get(
                    search_url,
                    headers=self.get_headers(),
                    proxies=proxies,
                    timeout=10
                )
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Parse based on search engine
                    if 'google' in search_url:
                        search_results = soup.find_all('div', class_='g')
                    elif 'bing' in search_url:
                        search_results = soup.find_all('li', class_='b_algo')
                    else:
                        search_results = soup.find_all('div', class_='result')
                    
                    for result in search_results[:num_results]:
                        try:
                            link_elem = result.find('a')
                            url = link_elem.get('href') if link_elem else None
                            
                            if url and url.startswith('http'):
                                title_elem = result.find('h3')
                                title = title_elem.text if title_elem else "No title"
                                
                                results.append({
                                    'title': title,
                                    'url': url,
                                    'query': query
                                })
                        except:
                            continue
                    
                    # Success, break retry loop
                    break
                    
                elif response.status_code == 429:
                    # Rate limited, wait and retry
                    wait_time = (retry + 1) * 5
                    time.sleep(wait_time)
                else:
                    time.sleep(2)
                    
            except Exception as e:
                if retry < max_retries - 1:
                    time.sleep(random.uniform(2, 5))
                continue
        
        # Random delay between searches
        time.sleep(random.uniform(1, 3))
        return results
    
    def search_multiple_dorks(self, dorks: List[str]) -> List[Dict]:
        """Search multiple dorks with threading"""
        all_results = []
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            future_to_dork = {executor.submit(self.search_google, dork): dork for dork in dorks}
            
            for future in tqdm(as_completed(future_to_dork), total=len(dorks),
                             desc="Searching", unit="dork", ncols=80):
                try:
                    results = future.result()
                    all_results.extend(results)
                except:
                    continue
        
        return all_results
