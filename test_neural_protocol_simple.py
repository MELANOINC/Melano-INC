#!/usr/bin/env python3
"""
Unit tests for Neural Protocol Scraper Simple Version
"""

import unittest
import asyncio
import json
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from neural_protocol_simple import NeuralProtocolScraper


class TestNeuralProtocolScraperSimple(unittest.TestCase):
    """Test cases for Neural Protocol Scraper Simple Version"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary config file
        self.config_data = {
            "neural_protocol": {
                "stealth_settings": {
                    "max_concurrent_sessions": 3,
                    "request_delay_range": [1, 3]
                },
                "extraction_rules": {
                    "linkedin_profile": {
                        "selectors": {
                            "name": "h1.test-name",
                            "title": ".test-title",
                            "company": ".test-company",
                            "location": ".test-location"
                        }
                    }
                }
            }
        }
        
        # Create temporary config file
        self.temp_config = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(self.config_data, self.temp_config)
        self.temp_config.close()
        
        # Create scraper instance
        self.scraper = NeuralProtocolScraper(self.temp_config.name)
        
        # Mock the database initialization to avoid file operations
        self.scraper.init_database = Mock()
        self.scraper.logger = Mock()

    def tearDown(self):
        """Clean up test fixtures"""
        os.unlink(self.temp_config.name)

    def test_load_config_default(self):
        """Test loading default configuration"""
        scraper = NeuralProtocolScraper("non_existent_config.json")
        self.assertIsInstance(scraper.config, dict)
        self.assertIn("neural_protocol", scraper.config)

    def test_load_config_custom(self):
        """Test loading custom configuration"""
        self.assertEqual(self.scraper.config["neural_protocol"]["stealth_settings"]["max_concurrent_sessions"], 3)
        self.assertEqual(self.scraper.config["neural_protocol"]["stealth_settings"]["request_delay_range"], [1, 3])

    @patch('neural_protocol_simple.webdriver.Chrome')
    @patch('neural_protocol_simple.WebDriverWait')
    @patch('neural_protocol_simple.EC')
    def test_extract_linkedin_profile_success(self, mock_ec, mock_wait, mock_chrome):
        """Test successful LinkedIn profile extraction"""
        # Mock browser setup
        mock_browser = Mock()
        mock_chrome.return_value = mock_browser
        
        # Mock WebDriverWait
        mock_wait_instance = Mock()
        mock_wait.return_value = mock_wait_instance
        
        # Mock element finding
        mock_browser.find_element.side_effect = [
            Mock(text="John Doe"),  # name element
            Mock(text="Software Engineer"),  # title element
            Mock(text="Test Corp"),  # company element
            Mock(text="Test City")  # location element
        ]
        
        # Mock WebDriverWait until
        mock_wait_instance.until.return_value = Mock()
        
        # Run the test
        profile_url = "https://linkedin.com/in/test"
        result = asyncio.run(self.scraper.extract_linkedin_profile(profile_url))
        
        # Verify results
        self.assertIsNotNone(result)
        self.assertEqual(result["full_name"], "John Doe")
        self.assertEqual(result["title"], "Software Engineer")
        self.assertEqual(result["company"], "Test Corp")
        self.assertEqual(result["location"], "Test City")
        self.assertEqual(result["source_url"], profile_url)
        
        # Verify browser was used
        mock_browser.get.assert_called_once_with(profile_url)
        mock_browser.quit.assert_called_once()

    @patch('neural_protocol_simple.webdriver.Chrome')
    @patch('neural_protocol_simple.SELENIUM_AVAILABLE', False)
    def test_extract_linkedin_profile_selenium_unavailable(self, mock_chrome):
        """Test LinkedIn profile extraction when selenium is unavailable"""
        profile_url = "https://linkedin.com/in/test"
        result = asyncio.run(self.scraper.extract_linkedin_profile(profile_url))
        
        self.assertIsNone(result)
        mock_chrome.assert_not_called()

    @patch('neural_protocol_simple.webdriver.Chrome')
    def test_extract_linkedin_profile_exception(self, mock_chrome):
        """Test LinkedIn profile extraction with exception"""
        # Mock browser to raise exception during get()
        mock_browser = Mock()
        mock_browser.get.side_effect = Exception("Test error")
        mock_chrome.return_value = mock_browser
        
        profile_url = "https://linkedin.com/in/test"
        result = asyncio.run(self.scraper.extract_linkedin_profile(profile_url))
        
        self.assertIsNone(result)
        # Browser should be created but quit() may not be called if exception occurs early
        mock_chrome.assert_called_once()

    def test_save_profile(self):
        """Test profile saving"""
        profile_data = {
            "profile_id": "test123",
            "source_url": "https://linkedin.com/in/test",
            "full_name": "John Doe",
            "title": "Software Engineer",
            "company": "Test Corp",
            "location": "Test City"
        }
        
        # Mock sqlite3 connection
        with patch('neural_protocol_simple.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            
            self.scraper.save_profile(profile_data)
            
            # Verify database operations
            mock_connect.assert_called_once_with(self.scraper.db_path)
            mock_cursor.execute.assert_called_once()
            mock_conn.commit.assert_called_once()
            mock_conn.close.assert_called_once()

    async def test_apply_neural_analysis(self):
        """Test neural analysis application"""
        profile_data = {
            "full_name": "John Doe",
            "title": "Software Engineer",
            "company": "Test Corp"
        }
        
        result = await self.scraper.apply_neural_analysis(profile_data)
        
        self.assertIn("neural_analysis", result)
        self.assertEqual(result["neural_analysis"]["confidence_score"], 0.85)
        self.assertEqual(result["neural_analysis"]["data_completeness_score"], 0.7)
        self.assertIn("analysis_timestamp", result["neural_analysis"])

    def test_release_browser(self):
        """Test browser release"""
        mock_browser = Mock()
        browser_info = {"browser": mock_browser}
        
        self.scraper.release_browser(browser_info)
        
        mock_browser.quit.assert_called_once()

    def test_release_browser_no_browser(self):
        """Test browser release when no browser is present"""
        browser_info = {"other_key": "value"}
        
        # Should not raise an exception
        self.scraper.release_browser(browser_info)


if __name__ == "__main__":
    unittest.main()
