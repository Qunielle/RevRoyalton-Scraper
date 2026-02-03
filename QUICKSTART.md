# Quick Start Guide

## Getting Started in 5 Minutes

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Add Your Proxies

Choose one of these methods:

**Method A: Edit config.py**
```python
EXAMPLE_PROXIES = [
    'http://proxy1.example.com:8080',
    'http://user:pass@proxy2.example.com:8080',
]
```

**Method B: Create proxies.txt**
```
http://proxy1.example.com:8080
http://user:pass@proxy2.example.com:8080
```

### 3. Run Your First Scrape

```python
from scraper import PriceScraper
from proxy_rotator import ProxyRotator

# Load proxies
proxy_rotator = ProxyRotator()
proxy_rotator.load_proxies_from_file('proxies.txt')

# Create scraper
scraper = PriceScraper(proxy_rotator=proxy_rotator)

# Scrape a URL
result = scraper.scrape_price('https://example.com/product')
```

### 4. Test It

Run the example:
```bash
python example_usage.py
```

## Key Features

✅ **Rotating IP Addresses** - Automatically switches between proxies  
✅ **Retry Logic** - Retries failed requests with different IPs  
✅ **Random User Agents** - Looks like a real browser  
✅ **Smart Proxy Management** - Tracks and skips failed proxies  

## Where to Get Proxies

For production use, get proxies from:
- [Bright Data](https://brightdata.com/) - Enterprise grade
- [SmartProxy](https://smartproxy.com/) - Good value
- [Oxylabs](https://oxylabs.io/) - E-commerce focused

**Avoid free proxies** - they're slow and often blocked.

## Common Issues

**No proxies loaded?**
- Check your proxy format: `http://ip:port` or `http://user:pass@ip:port`
- Verify proxies.txt exists and has one proxy per line

**Requests failing?**
- Test your proxy manually first
- Try with more proxies (recommended: 5-10 minimum)
- Increase retry attempts in config.py

**Getting blocked anyway?**
- Use residential proxies instead of datacenter
- Increase delays between requests (2-5 seconds)
- Reduce request rate

## Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Check [example_proxy_services.py](example_proxy_services.py) for proxy service integrations
3. Customize scraper.py to parse actual price data from your target site

## Legal Notice

⚠️ Always respect:
- Website Terms of Service
- robots.txt files
- Rate limits
- Copyright and privacy laws

Use responsibly!
