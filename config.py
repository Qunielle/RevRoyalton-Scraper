"""
Example configuration for the scraper
"""

# Example proxy list (replace with your actual proxy servers)
# You can get proxies from services like:
# - ProxyMesh (https://proxymesh.com/)
# - Bright Data (https://brightdata.com/)
# - SmartProxy (https://smartproxy.com/)
# - Free proxy lists (less reliable): https://free-proxy-list.net/

EXAMPLE_PROXIES = [
    # Format: 'http://ip:port' or 'http://username:password@ip:port'
    # 'http://proxy1.example.com:8080',
    # 'http://proxy2.example.com:8080',
    # 'http://user:pass@proxy3.example.com:8080',
]

# Scraper settings
RETRY_ATTEMPTS = 3
REQUEST_DELAY = 1.0  # seconds between requests
USE_RANDOM_PROXY = True  # True for random selection, False for round-robin

# Example sites to scrape (for testing purposes)
EXAMPLE_URLS = [
    # 'https://www.expedia.com/...',
    # Add your target URLs here
]
