#!/usr/bin/env python3
"""
Additional unit tests for Neural Protocol Scraper (Part 2)
"""

import unittest
import asyncio
import json
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from neural_protocol_simple import NeuralProtocolScraper


class TestNeuralProtocolScraperPart2(unittest.TestCase):
    """Additional test cases for Neural Protocol Scraper"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary config file
        self.config_data = {
            "neural_protocol": {
                "stealth_settings": {
                    "max_concurrent_sessions": 3,
                    "request_delay_range": [1, 3],
                    "proxy_rotation_interval": 60,
                    "user_agent_rotation_interval": 50,
                    "behavioral_randomization": True,
                    "anti_detection_level": 3
                },
                "proxy_configuration": {
                    "proxy_providers": ["test_proxies"],
                    "rotation_strategy": "round_robin",
                    "health_check_interval": 30,
                    "max_failures_before_rotation": 2
                },
                "browser_automation": {
                    "headless": True,
                    "window_size": [1280, 720],
                    "disable_images": False,
                    "disable_javascript": False,
                    "custom_flags": ["--test-flag"]
                },
                "extraction_rules": {
                    "linkedin_profile": {
                        "selectors": {
                            "name": "h1.test-name",
                            "title": ".test-title",
                            "company": ".test-company",
                            "location": ".test-location",
                            "connections": ".test-connections",
                            "about": ".test-about"
                        },
                        "dynamic_content": {
                            "scroll_to_load": True,
                            "click_show_more": True,
                            "wait_for_ajax": True
                        }
                    }
                },
                "neural_analysis": {
                    "profile_classification_model": "test_model",
                    "content_analysis_model": "test_analyzer",
                    "behavioral_prediction_model": "test_predictor",
                    "confidence_threshold": 0.7,
                    "retrain_interval_hours": 12
                },
                "data_quality": {
                    "minimum_completeness_score": 0.5,
                    "maximum_extraction_time": 120,
                    "data_validation_rules": {
                        "email_validation": True,
                        "phone_validation": True
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
        if hasattr(self, 'scraper') and hasattr(self.scraper, 'browser_pool'):
            for browser_info in self.scraper.browser_pool:
                try:
                    browser_info['browser'].quit()
                except:
                    pass

    async def test_get_available_browser_none_available(self):
        """Test getting browser when none are available"""
        mock_browser = Mock()
        self.scraper.browser_pool = [
            {"browser": mock_browser, "in_use": True, "created_at": "2023-01-01", "session_count": 1},
            {"browser": mock_browser, "in_use": True, "created_at": "2023-01-01", "session_count": 2}
        ]
        
        # Mock create_stealth_browser to return None
        with patch.object(self.scraper, 'create_stealth_browser', return_value=None):
            browser_info = await self.scraper.get_available_browser()
            self.assertIsNone(browser_info)

    def test_release_browser(self):
        """Test releasing browser back to pool"""
        mock_browser = Mock()
        browser_info = {
            "browser": mock_browser,
            "in_use": True,
            "created_at": "2023-01-01",
            "session_count": 10
        }
        
        # In simple version, release_browser just quits the browser
        self.scraper.release_browser(browser_info)
        
        # Verify browser quit was called
        mock_browser.quit.assert_called_once()

    def test_release_browser_high_session_count(self):
        """Test releasing browser with high session count (simple version just quits browser)"""
        mock_browser = Mock()
        browser_info = {
            "browser": mock_browser,
            "in_use": True,
            "created_at": "2023-01-01",
            "session_count": 60  # Above threshold
        }
        
        # In simple version, release_browser just quits the browser regardless of session count
        self.scraper.release_browser(browser_info)
        
        # Verify browser quit was called
        mock_browser.quit.assert_called_once()

    @patch('neural_protocol_simple.sqlite3.connect')
    def test_save_profile(self, mock_connect):
        """Test saving profile to database"""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        profile_data = {
            "profile_id": "test123",
            "source_url": "https://linkedin.com/in/test",
            "full_name": "John Doe",
            "title": "Software Engineer",
            "company": "Test Corp",
            "location": "Test City"
        }
        
        # In simple version, save_profile expects a dict, not a ScrapedProfile object
        self.scraper.save_profile(profile_data)
        
        mock_connect.assert_called_once_with(self.scraper.db_path)
        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('neural_protocol_simple.NeuralProtocolScraper.extract_linkedin_profile')
    @patch('neural_protocol_simple.NeuralProtocolScraper.save_profile')
    async def test_run_extraction_campaign(self, mock_save, mock_extract):
        """Test running extraction campaign"""
        mock_profile = Mock()
        mock_extract.return_value = mock_profile
        
        target_urls = [
            "https://linkedin.com/in/test1",
            "https://linkedin.com/in/test2",
            "https://linkedin.com/in/test3"
        ]
        
        await self.scraper.run_extraction_campaign(target_urls)
        
        self.assertEqual(mock_extract.call_count, 3)
        self.assertEqual(mock_save.call_count, 3)

    @patch('neural_protocol_simple.NeuralProtocolScraper.extract_linkedin_profile')
    async def test_run_extraction_campaign_no_profile(self, mock_extract):
        """Test running extraction campaign when no profile is extracted"""
        mock_extract.return_value = None
        
        target_urls = ["https://linkedin.com/in/test"]
        
        await self.scraper.run_extraction_campaign(target_urls)
        
        mock_extract.assert_called_once_with("https://linkedin.com/in/test")

    def test_apply_neural_analysis_neural_unavailable(self):
        """Test neural analysis when neural components are unavailable"""
        # Temporarily set NEURAL_AVAILABLE to False
        original_value = getattr(self.scraper, 'NEURAL_AVAILABLE', False)
        self.scraper.NEURAL_AVAILABLE = False
        
        profile_data = {
            "full_name": "John Doe",
            "title": "Engineer",
            "company": "Test Corp",
            "location": "Test City"
        }
        
        result = asyncio.run(self.scraper.apply_neural_analysis(profile_data))
        
        self.assertEqual(result, profile_data)
        self.scraper.NEURAL_AVAILABLE = original_value

    def test_config_access_safety(self):
        """Test that config access uses safe get methods"""
        # This should not raise KeyError even if config structure changes
        stealth_settings = self.scraper.config.get("neural_protocol", {}).get("stealth_settings", {})
        max_sessions = stealth_settings.get("max_concurrent_sessions", 5)
        
        self.assertEqual(max_sessions, 3)  # From our test config


if __name__ == '__main__':
    unittest.main()
