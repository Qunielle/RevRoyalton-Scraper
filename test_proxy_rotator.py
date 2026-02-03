"""
Unit tests for the proxy rotator
"""
import unittest
from proxy_rotator import ProxyRotator


class TestProxyRotator(unittest.TestCase):
    """Test cases for ProxyRotator class"""
    
    def test_init_empty(self):
        """Test initialization with no proxies"""
        rotator = ProxyRotator()
        self.assertEqual(rotator.get_proxy_count(), 0)
        self.assertIsNone(rotator.get_next_proxy())
    
    def test_init_with_proxies(self):
        """Test initialization with proxy list"""
        proxies = ['http://proxy1:8080', 'http://proxy2:8080']
        rotator = ProxyRotator(proxies)
        self.assertEqual(rotator.get_proxy_count(), 2)
    
    def test_add_proxy(self):
        """Test adding a single proxy"""
        rotator = ProxyRotator()
        rotator.add_proxy('http://proxy1:8080')
        self.assertEqual(rotator.get_proxy_count(), 1)
    
    def test_add_duplicate_proxy(self):
        """Test that duplicate proxies are not added"""
        rotator = ProxyRotator()
        rotator.add_proxy('http://proxy1:8080')
        rotator.add_proxy('http://proxy1:8080')
        self.assertEqual(rotator.get_proxy_count(), 1)
    
    def test_add_multiple_proxies(self):
        """Test adding multiple proxies"""
        rotator = ProxyRotator()
        proxies = ['http://proxy1:8080', 'http://proxy2:8080', 'http://proxy3:8080']
        rotator.add_proxies(proxies)
        self.assertEqual(rotator.get_proxy_count(), 3)
    
    def test_get_next_proxy_rotation(self):
        """Test round-robin proxy rotation"""
        proxies = ['http://proxy1:8080', 'http://proxy2:8080']
        rotator = ProxyRotator(proxies)
        
        # First call should return first proxy
        proxy1 = rotator.get_next_proxy()
        self.assertEqual(proxy1['http'], 'http://proxy1:8080')
        
        # Second call should return second proxy
        proxy2 = rotator.get_next_proxy()
        self.assertEqual(proxy2['http'], 'http://proxy2:8080')
        
        # Third call should wrap around to first proxy
        proxy3 = rotator.get_next_proxy()
        self.assertEqual(proxy3['http'], 'http://proxy1:8080')
    
    def test_get_random_proxy(self):
        """Test random proxy selection"""
        proxies = ['http://proxy1:8080', 'http://proxy2:8080', 'http://proxy3:8080']
        rotator = ProxyRotator(proxies)
        
        # Get random proxy
        proxy = rotator.get_random_proxy()
        self.assertIn(proxy['http'], proxies)
    
    def test_mark_proxy_failed(self):
        """Test marking a proxy as failed"""
        proxies = ['http://proxy1:8080', 'http://proxy2:8080']
        rotator = ProxyRotator(proxies)
        
        # Mark first proxy as failed
        proxy1 = rotator.get_next_proxy()
        rotator.mark_proxy_failed(proxy1)
        
        # Available count should be 1
        self.assertEqual(rotator.get_available_proxy_count(), 1)
        
        # Next proxy should skip the failed one
        proxy2 = rotator.get_next_proxy()
        self.assertEqual(proxy2['http'], 'http://proxy2:8080')
    
    def test_failed_proxies_reset(self):
        """Test that failed proxies are reset when all fail"""
        proxies = ['http://proxy1:8080', 'http://proxy2:8080']
        rotator = ProxyRotator(proxies)
        
        # Mark both proxies as failed
        proxy1 = rotator.get_next_proxy()
        rotator.mark_proxy_failed(proxy1)
        proxy2 = rotator.get_next_proxy()
        rotator.mark_proxy_failed(proxy2)
        
        # All proxies should be available again
        self.assertEqual(rotator.get_available_proxy_count(), 0)
        
        # Getting next proxy should reset and return a proxy
        proxy = rotator.get_next_proxy()
        self.assertIsNotNone(proxy)
        self.assertIn(proxy['http'], proxies)
    
    def test_proxy_format(self):
        """Test that proxy is returned in correct format"""
        rotator = ProxyRotator(['http://proxy1:8080'])
        proxy = rotator.get_next_proxy()
        
        self.assertIsInstance(proxy, dict)
        self.assertIn('http', proxy)
        self.assertIn('https', proxy)
        self.assertEqual(proxy['http'], proxy['https'])


if __name__ == '__main__':
    unittest.main()
