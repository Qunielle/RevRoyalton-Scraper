"""
Proxy Manager for rotating IP addresses
"""
import random
from typing import List, Optional, Dict


class ProxyRotator:
    """
    Manages a pool of proxies and rotates through them to avoid IP blocking.
    """
    
    def __init__(self, proxies: Optional[List[str]] = None):
        """
        Initialize the ProxyRotator with a list of proxy addresses.
        
        Args:
            proxies: List of proxy URLs in format 'http://ip:port' or 'http://user:pass@ip:port'
        """
        self.proxies = proxies or []
        self.current_index = 0
        self.failed_proxies = set()
        
    def add_proxy(self, proxy: str):
        """Add a single proxy to the pool."""
        if proxy and proxy not in self.proxies:
            self.proxies.append(proxy)
    
    def add_proxies(self, proxies: List[str]):
        """Add multiple proxies to the pool."""
        for proxy in proxies:
            self.add_proxy(proxy)
    
    def load_proxies_from_file(self, filepath: str):
        """
        Load proxies from a file (one proxy per line).
        
        Args:
            filepath: Path to file containing proxy addresses
        """
        try:
            with open(filepath, 'r') as f:
                proxies = [line.strip() for line in f if line.strip()]
                self.add_proxies(proxies)
        except FileNotFoundError:
            print(f"Proxy file not found: {filepath}")
    
    def get_next_proxy(self) -> Optional[Dict[str, str]]:
        """
        Get the next proxy in rotation.
        
        Returns:
            Dictionary with 'http' and 'https' proxy URLs, or None if no proxies available
        """
        if not self.proxies:
            return None
        
        available_proxies = [p for p in self.proxies if p not in self.failed_proxies]
        
        if not available_proxies:
            # Reset failed proxies if all have failed
            self.failed_proxies.clear()
            available_proxies = self.proxies
        
        # Round-robin selection
        proxy = available_proxies[self.current_index % len(available_proxies)]
        self.current_index = (self.current_index + 1) % len(available_proxies)
        
        return {
            'http': proxy,
            'https': proxy
        }
    
    def get_random_proxy(self) -> Optional[Dict[str, str]]:
        """
        Get a random proxy from the pool.
        
        Returns:
            Dictionary with 'http' and 'https' proxy URLs, or None if no proxies available
        """
        if not self.proxies:
            return None
        
        available_proxies = [p for p in self.proxies if p not in self.failed_proxies]
        
        if not available_proxies:
            self.failed_proxies.clear()
            available_proxies = self.proxies
        
        proxy = random.choice(available_proxies)
        
        return {
            'http': proxy,
            'https': proxy
        }
    
    def mark_proxy_failed(self, proxy_dict: Dict[str, str]):
        """
        Mark a proxy as failed so it won't be used temporarily.
        
        Args:
            proxy_dict: The proxy dictionary returned by get_next_proxy or get_random_proxy
        """
        if proxy_dict and 'http' in proxy_dict:
            self.failed_proxies.add(proxy_dict['http'])
    
    def get_proxy_count(self) -> int:
        """Get the total number of proxies in the pool."""
        return len(self.proxies)
    
    def get_available_proxy_count(self) -> int:
        """Get the number of available (not failed) proxies."""
        return len([p for p in self.proxies if p not in self.failed_proxies])
