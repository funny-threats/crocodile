# Google Dork SQL Injection Scanner 🔍

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Proxies](https://img.shields.io/badge/Proxy%20Sources-15+-green.svg)]()

An advanced automated penetration testing tool for bug bounty hunting with aggressive proxy scraping from 15+ sources, enhanced Google search with rate limit bypass, and comprehensive SQL injection detection using 100+ payloads.

## ⚠️ Legal Disclaimer

**This tool is intended for legitimate bug bounty programs and authorized penetration testing only.**

- Only use on systems you own or have explicit written permission to test
- Unauthorized access to computer systems is illegal
- Users are solely responsible for their actions and compliance with applicable laws

## ✨ Key Features

### 🔄 Advanced Proxy Management
- **15+ Proxy Sources**: Aggressive scraping from multiple free proxy websites and APIs
- **User Proxy Support**: Add your own proxies via `proxies.txt` file (ip:port format)
- **Smart Validation**: Concurrent proxy validation with response time tracking
- **Auto-Rotation**: Intelligent proxy rotation for reliability
- **Speed Optimization**: Uses fastest proxies first

### 🔎 Enhanced Google Search
- **Rate Limit Bypass**: Smart delays and proxy rotation to avoid detection
- **Multi-Engine Support**: Google, Bing, DuckDuckGo search fallback
- **Concurrent Searching**: Multi-threaded dork searching for speed
- **Random User-Agents**: Mimics real browser traffic

### 💉 Comprehensive SQL Injection Detection
- **100+ Payloads**: Organized into 12 categories
  - Basic injection vectors
  - Union-based attacks
  - Boolean-based blind injection
  - Time-based blind injection
  - Error-based extraction
  - Stacked queries
  - Database-specific (MySQL, MSSQL, PostgreSQL, Oracle)
  - WAF bypass techniques
  - Encoded payloads
- **Aggressive Mode**: Tests all payload types for maximum coverage
- **Multi-threaded Testing**: Fast concurrent URL testing
- **Smart Detection**: Pattern-based SQL error detection

### 💾 Database Extraction
- **Automatic Detection**: Identifies database files in search results
- **File Parsing**: Extracts data from SQL files
- **Structured Output**: Organized by tables and data types

### 📊 Professional Reporting
- **Detailed Reports**: Human-readable text format
- **JSON Export**: Machine-readable structured data
- **Statistics**: Comprehensive scan metrics
- **Color-Coded UI**: Professional terminal interface

## 📋 Requirements

- Python 3.7 or higher
- Internet connection
- (Optional) Virtual environment

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/Googledorky.git
cd Googledorky

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Basic scan
python main.py --dorks dorks.txt

# Aggressive mode with all payloads
python main.py --dorks dorks.txt --aggressive

# With user proxies
python main.py --dorks dorks.txt --user-proxies proxies.txt

# Maximum performance
python main.py --dorks dorks.txt --aggressive --max-proxies 100 --threads 20
```

## 📖 Detailed Usage

### Command Line Arguments

```
--dorks, -d          Path to dorks file (default: dorks.txt)
--max-proxies, -p    Maximum proxies to scrape (default: 50)
--user-proxies, -u   Path to user proxies file (format: ip:port)
--no-proxy           Run without proxies (not recommended)
--output, -o         Output file (default: results.txt)
--aggressive, -a     Use all 100+ SQL injection payloads
--max-urls           Limit URLs to test (default: unlimited)
--threads, -t        Number of threads (default: 10)
```

### Examples

**1. Quick Test with Limited URLs**
```bash
python main.py --dorks dorks.txt --max-urls 50
```

**2. Aggressive Scan with Custom Proxies**
```bash
python main.py --dorks dorks.txt --aggressive --user-proxies my_proxies.txt --max-proxies 100
```

**3. Fast Multi-threaded Scan**
```bash
python main.py --dorks dorks.txt --threads 20 --max-proxies 80
```

**4. Comprehensive Bug Bounty Scan**
```bash
python main.py --dorks dorks.txt --aggressive --max-proxies 100 --threads 20 --output bounty_results.txt
```

## 📁 File Structure

```
Googledorky/
├── main.py                  # Central access point
├── network_module.py        # Proxy management & Google search
├── scanner_module.py        # SQL injection & database scanning
├── payload_module.py        # SQL injection payloads
├── utils_module.py          # Utilities, reporting, UI
├── dorks.txt               # Google dorks (customizable)
├── proxies.txt             # User proxies (optional, ip:port format)
├── requirements.txt        # Python dependencies
├── results.txt             # Scan results (auto-generated)
├── results.json            # JSON results (auto-generated)
└── downloads/              # Downloaded database files
```

## 🔧 Configuration Files

### dorks.txt
Add your Google dorks, one per line. Lines starting with `#` are comments.

```
# SQL Injection vulnerable parameters
inurl:index.php?id=
inurl:page.php?id=
inurl:product.php?id=

# Database files
filetype:sql
filetype:db
intitle:index.of database
```

### proxies.txt (Optional)
Add your own proxies in `ip:port` format, one per line.

```
# HTTP Proxies
123.45.67.89:8080
98.76.54.32:3128
# More proxies...
```

## 🌐 Proxy Sources

The tool automatically scrapes from **15+ sources**:

1. free-proxy-list.net
2. sslproxies.org
3. us-proxy.org
4. proxy-list.download (HTTP, HTTPS, SOCKS4, SOCKS5)
5. GitHub proxy lists (TheSpeedX, ShiftyTR, monosans)
6. ProxyScrape API (HTTP, HTTPS, SOCKS4, SOCKS5)
7. GeoNode API
8. User-provided proxies (proxies.txt)

## 💉 SQL Injection Payloads

**Standard Mode**: ~15 basic payloads for fast testing

**Aggressive Mode**: 100+ comprehensive payloads including:
- 12 Basic injection vectors
- 10 Union-based attacks
- 10 Boolean-based blind injection
- 10 Time-based blind injection
- 9 Error-based extraction
- 7 Stacked queries
- 6 MySQL-specific payloads
- 6 MSSQL-specific payloads
- 5 PostgreSQL-specific payloads
- 4 Oracle-specific payloads
- 14 WAF bypass techniques
- 5 Encoded payloads

## 📊 Output Format

### results.txt (Human-Readable)
```
================================================================================
GOOGLE DORK SQL INJECTION SCAN RESULTS
================================================================================

SUMMARY
--------------------------------------------------------------------------------
Scan Date: 2025-01-13T12:00:00
Total Vulnerable URLs: 15
Total Database Files: 3
Total Tables Found: 8

SQL INJECTION VULNERABLE URLS
--------------------------------------------------------------------------------

[1] http://example.com/page.php?id=1
    Vulnerable Parameter: id
    Payload: ' OR '1'='1
    Status Code: 200
...
```

### results.json (Machine-Readable)
```json
{
  "vulnerable_urls": [
    {
      "url": "http://example.com/page.php?id=1",
      "vulnerable_param": "id",
      "payload": "' OR '1'='1",
      "status_code": 200
    }
  ],
  "database_files": [...],
  "summary": {...}
}
```

## ⚡ Performance Optimization

### Speed Tips
1. **Increase threads**: `--threads 20` (higher = faster, more resource intensive)
2. **More proxies**: `--max-proxies 100` (better reliability)
3. **Limit URLs**: `--max-urls 100` (for testing)
4. **Use fast proxies**: Add premium proxies to `proxies.txt`

### Rate Limit Bypass
- Smart delays between requests (1-3 seconds)
- Proxy rotation on each request
- Random user-agent rotation
- Multiple search engine fallback
- Request pattern randomization

## 🛡️ Detection Patterns

The tool detects SQL injection vulnerabilities by identifying these error patterns:

- MySQL errors
- PostgreSQL errors
- MSSQL errors
- Oracle errors
- ODBC errors
- SQLite errors
- Generic SQL syntax errors

## 📈 Typical Workflow

1. **Proxy Collection**: Scrapes and validates proxies from 15+ sources
2. **Google Searching**: Searches with dork queries using proxies
3. **URL Extraction**: Extracts unique URLs from search results
4. **Vulnerability Testing**: Tests URLs with SQL injection payloads
5. **Database Extraction**: Downloads and parses database files found
6. **Report Generation**: Creates detailed text and JSON reports

## 🔍 Troubleshooting

**No proxies found:**
- Check internet connection
- Proxy sources may be temporarily down
- Add your own proxies to `proxies.txt`

**Rate limited by Google:**
- Tool includes smart delays
- Increase `--max-proxies` for more rotation
- Add working proxies to `proxies.txt`

**No results found:**
- Verify dork syntax in `dorks.txt`
- Try different dork combinations
- Some dorks may not return results

**Slow scanning:**
- Increase threads: `--threads 20`
- Increase proxies: `--max-proxies 100`
- Use premium proxies in `proxies.txt`

## 📚 Advanced Tips

### Custom Payload Testing
Edit `payload_module.py` to add custom SQL injection payloads:

```python
'custom': [
    "your custom payload 1",
    "your custom payload 2",
]
```

### Proxy Quality
For best results, add high-quality proxies to `proxies.txt`:
- Premium proxy services
- Private proxies
- VPN endpoints
- Your own proxy servers

### Dork Optimization
Create targeted dorks for specific technologies:
```
# WordPress sites
inurl:/wp-content/ inurl:id=
# PHP applications
inurl:.php?id= site:.com
# Specific countries
inurl:page.php?id= site:.uk
```

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional proxy sources
- Enhanced SQL detection patterns
- More database file formats
- Improved WAF bypass techniques
- Additional search engines
- Better error handling

## ⚖️ Ethical Usage

This tool is designed for:
- ✅ Authorized penetration testing
- ✅ Bug bounty programs
- ✅ Security research
- ✅ Educational purposes

Never use for:
- ❌ Unauthorized system access
- ❌ Malicious activities
- ❌ Privacy violations
- ❌ Illegal activities

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Built for the bug bounty and security research community
- Inspired by OWASP testing methodologies
- Thanks to all proxy list maintainers

## 📞 Support

- **Issues**: Open an issue on GitHub
- **Questions**: Check existing issues first
- **Security**: Report vulnerabilities privately

## 🔄 Version History

**v2.0 - Enhanced Edition**
- 15+ proxy sources
- User proxy support (proxies.txt)
- Rate limit bypass mechanisms
- Multi-threaded operations
- 100+ SQL injection payloads
- Enhanced error detection
- Professional UI

**v1.0 - Initial Release**
- Basic proxy scraping
- Google dork searching
- SQL injection detection
- Database extraction

---

**Remember**: Always get proper authorization before testing any system. Happy (legal) hunting! 🐛💰
