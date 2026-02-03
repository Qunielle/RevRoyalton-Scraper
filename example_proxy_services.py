"""
Example: How to use the scraper with real proxy services
"""
from scraper import PriceScraper
from proxy_rotator import ProxyRotator


def example_with_bright_data():
    """
    Example using Bright Data (formerly Luminati) proxy service
    
    Bright Data provides residential and datacenter proxies.
    Format: http://username-session-{random}:password@proxy-server:port
    """
    print("Example: Using Bright Data Proxies")
    print("-" * 60)
    
    # Bright Data proxy format (replace with your credentials)
    proxy_rotator = ProxyRotator()
    
    # For rotating sessions, use different session IDs
    for i in range(5):
        proxy = f'http://username-session-{i}:password@zproxy.lum-superproxy.io:22225'
        proxy_rotator.add_proxy(proxy)
    
    scraper = PriceScraper(proxy_rotator=proxy_rotator)
    print(f"Loaded {proxy_rotator.get_proxy_count()} Bright Data proxies\n")


def example_with_smartproxy():
    """
    Example using SmartProxy service
    
    SmartProxy provides residential and datacenter proxies.
    Format: http://username:password@gate.smartproxy.com:port
    """
    print("Example: Using SmartProxy")
    print("-" * 60)
    
    # SmartProxy format (replace with your credentials)
    proxy = 'http://username:password@gate.smartproxy.com:7000'
    
    proxy_rotator = ProxyRotator([proxy])
    scraper = PriceScraper(proxy_rotator=proxy_rotator)
    print(f"Loaded {proxy_rotator.get_proxy_count()} SmartProxy proxies\n")


def example_with_oxylabs():
    """
    Example using Oxylabs proxy service
    
    Oxylabs provides residential and datacenter proxies.
    Format: http://username:password@pr.oxylabs.io:7777
    """
    print("Example: Using Oxylabs")
    print("-" * 60)
    
    # Oxylabs format (replace with your credentials)
    proxy = 'http://username:password@pr.oxylabs.io:7777'
    
    proxy_rotator = ProxyRotator([proxy])
    scraper = PriceScraper(proxy_rotator=proxy_rotator)
    print(f"Loaded {proxy_rotator.get_proxy_count()} Oxylabs proxies\n")


def example_with_proxy_file():
    """
    Example using proxies from a file
    
    Create a proxies.txt file with one proxy per line:
    http://proxy1.example.com:8080
    http://user:pass@proxy2.example.com:8080
    http://proxy3.example.com:8080
    """
    print("Example: Loading Proxies from File")
    print("-" * 60)
    
    proxy_rotator = ProxyRotator()
    proxy_rotator.load_proxies_from_file('proxies.txt')
    
    scraper = PriceScraper(proxy_rotator=proxy_rotator)
    print(f"Loaded {proxy_rotator.get_proxy_count()} proxies from file\n")


def example_scraping_expedia():
    """
    Example: Scraping hotel prices from Expedia
    
    Note: This is a conceptual example. You need to:
    1. Add proper HTML parsing with BeautifulSoup
    2. Respect Expedia's Terms of Service
    3. Use appropriate request delays
    """
    print("Example: Scraping Expedia (Conceptual)")
    print("-" * 60)
    
    # Set up proxies (use your actual proxy service)
    proxy_rotator = ProxyRotator()
    # proxy_rotator.add_proxy('http://your-proxy:8080')
    
    scraper = PriceScraper(
        proxy_rotator=proxy_rotator,
        use_random_proxy=True,
        retry_attempts=3
    )
    
    # Example URL (this is just a placeholder)
    url = "https://www.expedia.com/Hotel-Search?..."
    
    print(f"Would scrape: {url}")
    print("\nTo implement actual scraping:")
    print("1. Use scraper.fetch_page(url) to get the HTML")
    print("2. Parse with BeautifulSoup to extract price data")
    print("3. Handle pagination and multiple listings")
    print("4. Store results in a database or file")
    print("\nImportant: Always check robots.txt and Terms of Service!")


def example_best_practices():
    """
    Example: Best practices for avoiding detection
    """
    print("\nBest Practices for Web Scraping")
    print("=" * 60)
    
    practices = [
        "1. Use residential proxies (better than datacenter)",
        "2. Rotate proxies frequently (every request or every few requests)",
        "3. Add random delays between requests (1-3 seconds minimum)",
        "4. Use realistic user agents (scraper does this automatically)",
        "5. Respect robots.txt and rate limits",
        "6. Handle cookies and sessions properly",
        "7. Monitor success/failure rates",
        "8. Use quality proxy services, not free proxies",
        "9. Spread requests across different IP ranges",
        "10. Check website Terms of Service first"
    ]
    
    for practice in practices:
        print(f"  {practice}")
    
    print("\nProxy Recommendations:")
    print("  - Bright Data: Enterprise-grade, expensive but reliable")
    print("  - SmartProxy: Good balance of price and quality")
    print("  - Oxylabs: High quality, good for e-commerce")
    print("  - Avoid: Free proxy lists (unreliable, often blocked)")


if __name__ == "__main__":
    # Show examples (these won't actually scrape without real proxies)
    example_with_bright_data()
    example_with_smartproxy()
    example_with_oxylabs()
    example_with_proxy_file()
    example_scraping_expedia()
    example_best_practices()
