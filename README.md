# RevRoyalton-Scraper

A Python web scraper with rotating IP address support to avoid being blocked when scraping price data from websites like Expedia.

## Features

- **Rotating IP Addresses**: Automatically rotates through a pool of proxy servers to avoid IP-based blocking
- **Random User Agents**: Generates random browser user agents to appear more like a real user
- **Retry Logic**: Automatically retries failed requests with different proxies
- **Flexible Proxy Management**: Supports round-robin and random proxy selection strategies
- **Failed Proxy Handling**: Temporarily marks failed proxies and rotates to working ones

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Qunielle/RevRoyalton-Scraper.git
cd RevRoyalton-Scraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Setting Up Proxies

You have three options to configure proxies:

#### Option 1: Edit config.py
Add your proxy list directly in `config.py`:
```python
EXAMPLE_PROXIES = [
    'http://proxy1.example.com:8080',
    'http://proxy2.example.com:8080',
    'http://user:pass@proxy3.example.com:8080',
]
```

#### Option 2: Use a proxies.txt file
Create a `proxies.txt` file with one proxy per line:
```
http://proxy1.example.com:8080
http://proxy2.example.com:8080
http://user:pass@proxy3.example.com:8080
```

#### Option 3: Add proxies programmatically
```python
from proxy_rotator import ProxyRotator

proxy_rotator = ProxyRotator()
proxy_rotator.add_proxy('http://proxy1.example.com:8080')
proxy_rotator.add_proxy('http://user:pass@proxy2.example.com:8080')
```

### Getting Proxies

You can obtain proxy servers from various services:
- [Bright Data](https://brightdata.com/) (formerly Luminati)
- [SmartProxy](https://smartproxy.com/)
- [ProxyMesh](https://proxymesh.com/)
- [Oxylabs](https://oxylabs.io/)
- Free proxy lists (less reliable): [free-proxy-list.net](https://free-proxy-list.net/)

## Usage

### Basic Example

```python
from scraper import PriceScraper
from proxy_rotator import ProxyRotator

# Initialize proxy rotator
proxy_rotator = ProxyRotator()
proxy_rotator.add_proxy('http://proxy1.example.com:8080')
proxy_rotator.add_proxy('http://proxy2.example.com:8080')

# Initialize scraper
scraper = PriceScraper(proxy_rotator=proxy_rotator)

# Scrape a URL
result = scraper.scrape_price('https://example.com/product')
if result:
    print(f"Successfully scraped: {result['url']}")
```

### Running the Example

Run the included example script:
```bash
python example_usage.py
```

### Advanced Usage

#### Custom Retry Attempts and Delay
```python
scraper = PriceScraper(
    proxy_rotator=proxy_rotator,
    use_random_proxy=True,  # Use random proxy selection
    retry_attempts=5        # Retry up to 5 times
)

result = scraper.fetch_page('https://example.com', delay=2.0)
```

#### Load Proxies from File
```python
proxy_rotator = ProxyRotator()
proxy_rotator.load_proxies_from_file('proxies.txt')

scraper = PriceScraper(proxy_rotator=proxy_rotator)
```

## Components

### ProxyRotator (`proxy_rotator.py`)
Manages a pool of proxies and handles rotation logic:
- `add_proxy(proxy)`: Add a single proxy
- `add_proxies(proxies)`: Add multiple proxies
- `load_proxies_from_file(filepath)`: Load proxies from file
- `get_next_proxy()`: Get next proxy in round-robin fashion
- `get_random_proxy()`: Get a random proxy
- `mark_proxy_failed(proxy_dict)`: Mark a proxy as temporarily failed

### PriceScraper (`scraper.py`)
Main scraper class with IP rotation:
- `fetch_page(url, delay)`: Fetch a page with retry logic
- `scrape_price(url)`: Scrape price data from a URL
- Automatic header rotation
- Proxy failure handling
- Configurable retry attempts

## Configuration Options

Edit `config.py` to customize:
- `RETRY_ATTEMPTS`: Number of retry attempts (default: 3)
- `REQUEST_DELAY`: Delay between requests in seconds (default: 1.0)
- `USE_RANDOM_PROXY`: Use random vs round-robin proxy selection (default: True)

## How It Works

1. **Proxy Rotation**: The scraper maintains a pool of proxy servers and rotates through them for each request
2. **User Agent Spoofing**: Each request uses a different, realistic user agent string
3. **Automatic Retry**: If a request fails or returns a blocking status code (403, 429), the scraper automatically tries again with a different proxy
4. **Failed Proxy Management**: Proxies that fail are temporarily marked as failed and skipped in rotation
5. **Random Delays**: Adds random delays between requests to appear more human-like

## Avoiding Detection

To maximize your chances of not being blocked:

1. **Use High-Quality Proxies**: Residential proxies work better than datacenter proxies
2. **Rotate User Agents**: The scraper does this automatically
3. **Add Delays**: Use appropriate delays between requests (1-3 seconds minimum)
4. **Respect robots.txt**: Check the site's robots.txt file
5. **Limit Request Rate**: Don't scrape too aggressively
6. **Handle Cookies**: The scraper uses a session to maintain cookies

## Legal and Ethical Considerations

⚠️ **Important**: Web scraping may have legal and ethical implications:
- Always check and respect the website's Terms of Service
- Review and follow the site's `robots.txt` file
- Don't overload the target server with too many requests
- Some websites explicitly prohibit scraping
- Be aware of copyright and data protection laws in your jurisdiction

Use this tool responsibly and ethically.

## License

This project is provided as-is for educational purposes.

## Contributing

Feel free to open issues or submit pull requests for improvements.