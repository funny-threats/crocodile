"""
Utilities Module - Data Organization, Reporting, and UI
"""

import json
import os
from typing import List, Dict
from datetime import datetime
from collections import defaultdict
from colorama import Fore, Style

class DataOrganizer:
    """Organize and format extracted data"""
    
    def __init__(self, output_file: str = "results.txt"):
        self.output_file = output_file
        self.organized_data = {
            'vulnerable_urls': [],
            'database_files': [],
            'extracted_data': defaultdict(list),
            'summary': {}
        }
    
    def organize_vulnerable_urls(self, vulnerable_urls: List[Dict]):
        """Organize SQL injection vulnerable URLs"""
        self.organized_data['vulnerable_urls'] = vulnerable_urls
    
    def organize_database_files(self, database_files: List[Dict]):
        """Organize downloaded database files"""
        self.organized_data['database_files'] = database_files
        
        for db_file in database_files:
            for data_item in db_file.get('data', []):
                table_name = data_item.get('table', 'unknown')
                self.organized_data['extracted_data'][table_name].append(data_item)
    
    def generate_summary(self):
        """Generate summary statistics"""
        self.organized_data['summary'] = {
            'total_vulnerable_urls': len(self.organized_data['vulnerable_urls']),
            'total_database_files': len(self.organized_data['database_files']),
            'total_tables_found': len(self.organized_data['extracted_data']),
            'timestamp': datetime.now().isoformat()
        }
    
    def write_to_file(self):
        """Write organized data to output file"""
        self.generate_summary()
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            # Header
            f.write("=" * 80 + "\n")
            f.write("GOOGLE DORK SQL INJECTION SCAN RESULTS\n")
            f.write("=" * 80 + "\n\n")
            
            # Summary
            f.write("SUMMARY\n")
            f.write("-" * 80 + "\n")
            summary = self.organized_data['summary']
            f.write(f"Scan Date: {summary['timestamp']}\n")
            f.write(f"Total Vulnerable URLs: {summary['total_vulnerable_urls']}\n")
            f.write(f"Total Database Files: {summary['total_database_files']}\n")
            f.write(f"Total Tables Found: {summary['total_tables_found']}\n\n")
            
            # Vulnerable URLs
            if self.organized_data['vulnerable_urls']:
                f.write("SQL INJECTION VULNERABLE URLS\n")
                f.write("-" * 80 + "\n")
                for i, vuln in enumerate(self.organized_data['vulnerable_urls'], 1):
                    f.write(f"\n[{i}] {vuln.get('url', 'N/A')}\n")
                    f.write(f"    Vulnerable Parameter: {vuln.get('vulnerable_param', 'N/A')}\n")
                    f.write(f"    Payload: {vuln.get('payload', 'N/A')}\n")
                    f.write(f"    Status Code: {vuln.get('status_code', 'N/A')}\n")
                f.write("\n")
            
            # Database files
            if self.organized_data['database_files']:
                f.write("DOWNLOADED DATABASE FILES\n")
                f.write("-" * 80 + "\n")
                for i, db_file in enumerate(self.organized_data['database_files'], 1):
                    f.write(f"\n[{i}] URL: {db_file.get('url', 'N/A')}\n")
                    f.write(f"    File: {db_file.get('filepath', 'N/A')}\n")
                    f.write(f"    Data Items: {len(db_file.get('data', []))}\n")
                f.write("\n")
            
            # Extracted data
            if self.organized_data['extracted_data']:
                f.write("EXTRACTED DATA BY TABLE\n")
                f.write("-" * 80 + "\n")
                for table_name, data_items in self.organized_data['extracted_data'].items():
                    f.write(f"\nTable: {table_name}\n")
                    f.write(f"Items: {len(data_items)}\n")
                    for item in data_items[:5]:
                        f.write(f"  - Type: {item.get('type', 'N/A')}\n")
                        f.write(f"    Data: {item.get('data', '')[:100]}...\n")
                    if len(data_items) > 5:
                        f.write(f"  ... and {len(data_items) - 5} more items\n")
                f.write("\n")
            
            f.write("=" * 80 + "\n")
            f.write("END OF REPORT\n")
            f.write("=" * 80 + "\n")
    
    def write_json(self, json_file: str = "results.json"):
        """Write organized data to JSON file"""
        self.generate_summary()
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.organized_data, f, indent=2, default=str)


# UI Functions
def print_banner():
    """Print main banner"""
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║  {Fore.YELLOW}╔═╗╔═╗╔═╗╔═╗╔╦╗╔═╗╦ ╦╔═╗╔═╗╦═╗╔═╗╔╦╗  {Fore.CYAN}╔═╗╔═╗╔═╗╦ ╦╔═╗╔═╗╦═╗╔═╗╔╦╗  ║
║  {Fore.YELLOW}║  ╠═╝╠═╝║ ╦║║║║ ║║║║║╣ ║╣ ╠╦╝╠═╣ ║   {Fore.CYAN}╚═╗║  ║ ║║║║║╣ ║ ╦╠╦╝╠═╣ ║   ║
║  {Fore.YELLOW}╚═╝╩  ╩  ╚═╝╩ ╩╚═╝╚╩╝╚═╝╚═╝╩╚═╩ ╩ ╩   {Fore.CYAN}╚═╝╚═╝╚═╝╚╩╝╚═╝╚═╝╩╚═╩ ╩ ╩   ║
║                                                                          ║
║  {Fore.RED}╔═╗╔═╗╦  ╔═╗╔═╗╦═╗╔═╗╔═╗╔═╗╔═╗╦═╗╔═╗╔╦╗╔═╗╦═╗  {Fore.CYAN}║
║  {Fore.RED}║╣ ║ ╦║  ╠═╝║ ║╠╦╝║╣ ║ ╦║ ╦║ ╦╠╦╝╠═╣ ║ ║╣ ╠╦╝  {Fore.CYAN}║
║  {Fore.RED}╚═╝╚═╝╩═╝╩  ╚═╝╩╚═╚═╝╚═╝╚═╝╚═╝╩╚═╩ ╩ ╩ ╚═╝╩╚═  {Fore.CYAN}║
║                                                                          ║
║  {Fore.GREEN}Automated SQL Injection Scanner for Bug Bounty Hunting{Fore.CYAN}                  ║
║  {Fore.WHITE}Version 2.0 | Enhanced Proxy Scraping | Rate Limit Bypass{Fore.CYAN}              ║
╚══════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)

def print_section_header(text: str, color=Fore.CYAN):
    """Print section header"""
    width = 80
    print(f"\n{color}{'═' * width}{Style.RESET_ALL}")
    print(f"{color}{text.center(width)}{Style.RESET_ALL}")
    print(f"{color}{'═' * width}{Style.RESET_ALL}\n")

def print_status(message: str, status_type: str = "info"):
    """Print status message with icon"""
    icons = {
        "info": f"{Fore.CYAN}[*]{Style.RESET_ALL}",
        "success": f"{Fore.GREEN}[+]{Style.RESET_ALL}",
        "warning": f"{Fore.YELLOW}[!]{Style.RESET_ALL}",
        "error": f"{Fore.RED}[!]{Style.RESET_ALL}",
        "vuln": f"{Fore.RED}[VULN]{Style.RESET_ALL}",
    }
    icon = icons.get(status_type, icons["info"])
    print(f"{icon} {message}")

def print_stats(stats: dict):
    """Print statistics"""
    print(f"\n{Fore.CYAN}{'─' * 80}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}📊 SCAN STATISTICS{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'─' * 80}{Style.RESET_ALL}")
    
    for key, value in stats.items():
        formatted_key = key.replace('_', ' ').title()
        print(f"  {Fore.WHITE}{formatted_key:.<30}{Style.RESET_ALL} {Fore.GREEN}{value}{Style.RESET_ALL}")
    
    print(f"{Fore.CYAN}{'─' * 80}{Style.RESET_ALL}\n")
