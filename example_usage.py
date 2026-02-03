"""
Example usage of the price scraper with rotating IP addresses
"""
from scraper import PriceScraper
from proxy_rotator import ProxyRotator
import config


def main():
    """
    Example: Scrape with rotating proxies
    """
    print("=" * 60)
    print("Price Scraper with Rotating IP Addresses")
    print("=" * 60)
    
    # Option 1: Initialize with proxy list from config
    proxy_rotator = ProxyRotator(config.EXAMPLE_PROXIES)
    
    # Option 2: Load proxies from a file (one proxy per line)
    # proxy_rotator = ProxyRotator()
    # proxy_rotator.load_proxies_from_file('proxies.txt')
    
    # Option 3: Add proxies manually
    # proxy_rotator = ProxyRotator()
    # proxy_rotator.add_proxy('http://proxy1.example.com:8080')
    # proxy_rotator.add_proxy('http://user:pass@proxy2.example.com:8080')
    
    print(f"\nTotal proxies loaded: {proxy_rotator.get_proxy_count()}")
    
    # Initialize scraper with proxy rotation
    scraper = PriceScraper(
        proxy_rotator=proxy_rotator,
        use_random_proxy=config.USE_RANDOM_PROXY,
        retry_attempts=config.RETRY_ATTEMPTS
    )
    
    # Example: Scrape a test URL
    test_url = "https://httpbin.org/ip"  # This URL returns your IP address
    print(f"\nTesting with URL: {test_url}")
    print("-" * 60)
    
    result = scraper.scrape_price(test_url)
    
    if result:
        print("\nScrape successful!")
        print(f"URL: {result['url']}")
        print(f"Status: {result['status_code']}")
        print(f"Content length: {result['content_length']} bytes")
    else:
        print("\nScrape failed!")
    
    # Example: Scrape multiple URLs
    if config.EXAMPLE_URLS:
        print("\n" + "=" * 60)
        print("Scraping multiple URLs")
        print("=" * 60)
        
        for url in config.EXAMPLE_URLS:
            print(f"\nScraping: {url}")
            result = scraper.scrape_price(url)
            if result:
                print(f"✓ Success")
            else:
                print(f"✗ Failed")
    
    print("\n" + "=" * 60)
    print("Scraping completed")
    print("=" * 60)


def demo_without_proxies():
    """
    Example: Scrape without proxies (direct connection)
    """
    print("\nDemo: Scraping without proxies")
    print("-" * 60)
    
    scraper = PriceScraper()  # No proxy rotator
    test_url = "https://httpbin.org/headers"
    
    result = scraper.scrape_price(test_url)
    if result:
        print("✓ Scrape successful (no proxy)")
    else:
        print("✗ Scrape failed")


if __name__ == "__main__":
    # Run main example
    main()
    
    # Uncomment to test without proxies
    # demo_without_proxies()
