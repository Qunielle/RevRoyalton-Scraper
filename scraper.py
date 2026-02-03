"""
Main scraper module with rotating IP address support
"""
import requests
import time
import random
from typing import Optional, Dict, Any
from fake_useragent import UserAgent
from proxy_rotator import ProxyRotator


class PriceScraper:
    """
    Web scraper with rotating IP addresses and user agents to avoid blocking.
    """
    
    def __init__(self, proxy_rotator: Optional[ProxyRotator] = None, 
                 use_random_proxy: bool = True,
                 retry_attempts: int = 3):
        """
        Initialize the price scraper.
        
        Args:
            proxy_rotator: ProxyRotator instance for IP rotation
            use_random_proxy: If True, use random proxy selection; if False, use round-robin
            retry_attempts: Number of retry attempts for failed requests
        """
        self.proxy_rotator = proxy_rotator or ProxyRotator()
        self.use_random_proxy = use_random_proxy
        self.retry_attempts = retry_attempts
        self.ua = UserAgent()
        self.session = requests.Session()
        
    def _get_headers(self) -> Dict[str, str]:
        """Generate random headers to mimic real browser."""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    
    def _get_proxy(self) -> Optional[Dict[str, str]]:
        """Get next proxy based on rotation strategy."""
        if self.use_random_proxy:
            return self.proxy_rotator.get_random_proxy()
        else:
            return self.proxy_rotator.get_next_proxy()
    
    def _handle_proxy_failure(self, proxy: Optional[Dict[str, str]], 
                             error_type: str, error: Exception, 
                             attempt: int):
        """
        Handle proxy failure by marking it as failed and logging details.
        
        Args:
            proxy: The proxy that failed
            error_type: Type of error (e.g., 'Proxy', 'Timeout')
            error: The exception that occurred
            attempt: Current attempt number
        """
        proxy_info = proxy['http'] if proxy else 'No proxy'
        print(f"{error_type} error on attempt {attempt + 1} with {proxy_info}: {error}")
        if proxy:
            self.proxy_rotator.mark_proxy_failed(proxy)
    
    def fetch_page(self, url: str, delay: float = 1.0) -> Optional[requests.Response]:
        """
        Fetch a page with rotating IP addresses and retry logic.
        
        Args:
            url: URL to fetch
            delay: Delay between requests in seconds (default: 1.0)
            
        Returns:
            Response object if successful, None otherwise
        """
        proxy = None  # Initialize proxy variable for exception handlers
        
        for attempt in range(self.retry_attempts):
            try:
                # Add random delay to appear more human-like
                if attempt > 0:
                    time.sleep(delay + random.uniform(0, 1))
                
                # Get proxy and headers
                proxy = self._get_proxy()
                headers = self._get_headers()
                
                # Log proxy being used (for debugging)
                proxy_info = proxy['http'] if proxy else 'No proxy'
                print(f"Attempt {attempt + 1}/{self.retry_attempts} - Using proxy: {proxy_info}")
                
                # Make request
                response = self.session.get(
                    url,
                    headers=headers,
                    proxies=proxy,
                    timeout=30,
                    allow_redirects=True
                )
                
                # Check if request was successful
                if response.status_code == 200:
                    print(f"Successfully fetched: {url}")
                    return response
                elif response.status_code == 403 or response.status_code == 429:
                    proxy_info = proxy['http'] if proxy else 'No proxy'
                    print(f"Blocked (status {response.status_code}) on attempt {attempt + 1} with {proxy_info}, rotating...")
                    if proxy:
                        self.proxy_rotator.mark_proxy_failed(proxy)
                    time.sleep(delay * 2)
                else:
                    print(f"Unexpected status code {response.status_code} on attempt {attempt + 1}")
                    
            except requests.exceptions.ProxyError as e:
                self._handle_proxy_failure(proxy, 'Proxy', e, attempt)
            except requests.exceptions.Timeout as e:
                self._handle_proxy_failure(proxy, 'Timeout', e, attempt)
            except requests.exceptions.RequestException as e:
                proxy_info = proxy['http'] if proxy else 'No proxy'
                print(f"Request error on attempt {attempt + 1} with {proxy_info}: {e}")
            except Exception as e:
                proxy_info = proxy['http'] if proxy else 'No proxy'
                print(f"Unexpected error on attempt {attempt + 1} with {proxy_info}: {e}")
        
        print(f"Failed to fetch after {self.retry_attempts} attempts: {url}")
        return None
    
    def scrape_price(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape price information from a URL.
        
        Args:
            url: URL to scrape
            
        Returns:
            Dictionary with scraped data or None if failed
        """
        response = self.fetch_page(url)
        
        if not response:
            return None
        
        # Basic structure for scraped data
        # In real implementation, you would parse the HTML to extract specific price data
        return {
            'url': url,
            'status_code': response.status_code,
            'content_length': len(response.content),
            'timestamp': time.time(),
            # Add your custom parsing logic here
            # 'price': parse_price(response),
            # 'title': parse_title(response),
            # etc.
        }
