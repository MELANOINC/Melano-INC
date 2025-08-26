#!/usr/bin/env python3
"""
Unit tests for Neural Protocol Scraper
"""

import unittest
import asyncio
import json
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from neural_protocol_scraper import NeuralProtocolScraper, ScrapedProfile, ScrapingTarget, ProxyConfig


class TestNeuralProtocolScraper(unittest.TestCase):
    """Test cases for Neural Protocol Scraper"""

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

    def test_load_config_default(self):
        """Test loading default configuration"""
        scraper = NeuralProtocolScraper("non_existent_config.json")
        self.assertIsInstance(scraper.config, dict)
        self.assertIn("neural_protocol", scraper.config)

    def test_load_config_custom(self):
        """Test loading custom configuration"""
        self.assertEqual(self.scraper.config["neural_protocol"]["stealth_settings"]["max_concurrent_sessions"], 3)
        self.assertEqual(self.scraper.config["neural_protocol"]["stealth_settings"]["request_delay_range"], [1, 3])

    def test_calculate_completeness_score(self):
        """Test completeness score calculation"""
        # Test with complete data
        complete_profile = {
            "full_name": "John Doe",
            "title": "Software Engineer",
            "company": "Test Corp",
            "location": "Test City"
        }
        score = self.scraper.calculate_completeness_score(complete_profile)
        self.assertEqual(score, 1.0)
        
        # Test with partial data
        partial_profile = {
            "full_name": "John Doe",
            "title": "",
            "company": "Test Corp",
            "location": ""
        }
        score = self.scraper.calculate_completeness_score(partial_profile)
        self.assertEqual(score, 0.5)
        
        # Test with empty data
        empty_profile = {}
        score = self.scraper.calculate_completeness_score(empty_profile)
        self.assertEqual(score, 0.0)

    def test_calculate_confidence_score(self):
        """Test confidence score calculation"""
        profile_data = {
            "full_name": "John Doe",
            "title": "Senior Software Engineer",
            "company": "Test Corporation",
            "location": "San Francisco, CA",
            "connections_count": 500,
            "summary": "Experienced software engineer with 10+ years in the industry",
            "title": "Senior Software Engineer at Test Corporation"
        }
        
        score = self.scraper.calculate_confidence_score(profile_data)
        self.assertGreaterEqual(score, 0.7)
        self.assertLessEqual(score, 1.0)

    def test_calculate_lead_score(self):
        """Test lead score calculation"""
        # Test high-value lead
        high_value_profile = {
            "title": "Director of Engineering",
            "company": "Tech Company Inc",
            "connections_count": 300,
            "full_name": "John Director"
        }
        score = self.scraper.calculate_lead_score(high_value_profile)
        self.assertGreater(score, 0.5)
        
        # Test low-value lead
        low_value_profile = {
            "title": "Intern",
            "company": "",
            "connections_count": 50,
            "full_name": "Jane Intern"
        }
        score = self.scraper.calculate_lead_score(low_value_profile)
        self.assertLess(score, 0.5)

    def test_extract_number_from_text(self):
        """Test number extraction from text"""
        self.assertEqual(self.scraper.extract_number_from_text("500+ connections"), 500)
        self.assertEqual(self.scraper.extract_number_from_text("1,234 followers"), 1234)
        self.assertEqual(self.scraper.extract_number_from_text("no numbers here"), 0)
        self.assertEqual(self.scraper.extract_number_from_text(""), 0)

    @patch('neural_protocol_scraper.UserAgent')
    def test_initialize_user_agents_fake_available(self, mock_useragent):
        """Test user agent initialization with fake_useragent available"""
        mock_ua_instance = Mock()
        mock_ua_instance.random = "Mozilla/5.0 (Test) AppleWebKit/537.36"
        mock_useragent.return_value = mock_ua_instance
        
        # Temporarily set FAKE_USERAGENT_AVAILABLE to True
        original_value = getattr(self.scraper, 'FAKE_USERAGENT_AVAILABLE', False)
        self.scraper.FAKE_USERAGENT_AVAILABLE = True
        
        asyncio.run(self.scraper.initialize_user_agents())
        
        self.assertGreater(len(self.scraper.user_agents), 0)
        self.scraper.FAKE_USERAGENT_AVAILABLE = original_value

    def test_initialize_user_agents_fake_unavailable(self):
        """Test user agent initialization without fake_useragent"""
        # Temporarily set FAKE_USERAGENT_AVAILABLE to False
        original_value = getattr(self.scraper, 'FAKE_USERAGENT_AVAILABLE', False)
        self.scraper.FAKE_USERAGENT_AVAILABLE = False
        
        asyncio.run(self.scraper.initialize_user_agents())
        
        self.assertGreater(len(self.scraper.user_agents), 0)
        self.assertIn("Mozilla/5.0", self.scraper.user_agents[0])
        self.scraper.FAKE_USERAGENT_AVAILABLE = original_value

    @patch('neural_protocol_scraper.MLPClassifier')
    @patch('neural_protocol_scraper.TfidfVectorizer')
    def test_initialize_neural_models_available(self, mock_tfidf, mock_mlp):
        """Test neural models initialization when available"""
        # Temporarily set NEURAL_AVAILABLE to True
        original_value = getattr(self.scraper, 'NEURAL_AVAILABLE', False)
        self.scraper.NEURAL_AVAILABLE = True
        
        mock_mlp_instance = Mock()
        mock_tfidf_instance = Mock()
        mock_mlp.return_value = mock_mlp_instance
        mock_tfidf.return_value = mock_tfidf_instance
        
        asyncio.run(self.scraper.initialize_neural_models())
        
        self.assertIsNotNone(self.scraper.profile_classifier)
        self.assertIsNotNone(self.scraper.content_analyzer)
        self.scraper.NEURAL_AVAILABLE = original_value

    def test_initialize_neural_models_unavailable(self):
        """Test neural models initialization when unavailable"""
        # Temporarily set NEURAL_AVAILABLE to False
        original_value = getattr(self.scraper, 'NEURAL_AVAILABLE', False)
        self.scraper.NEURAL_AVAILABLE = False
        
        asyncio.run(self.scraper.initialize_neural_models())
        
        self.assertIsNone(self.scraper.profile_classifier)
        self.assertIsNone(self.scraper.content_analyzer)
        self.scraper.NEURAL_AVAILABLE = original_value

    @patch('neural_protocol_scraper.uc.Chrome')
    @patch('neural_protocol_scraper.webdriver.Chrome')
    def test_create_stealth_browser_undetected_available(self, mock_chrome, mock_uc_chrome):
        """Test stealth browser creation with undetected_chromedriver available"""
        # Temporarily set UNDETECTED_CHROME_AVAILABLE to True
        original_value = getattr(self.scraper, 'UNDETECTED_CHROME_AVAILABLE', False)
        self.scraper.UNDETECTED_CHROME_AVAILABLE = True
        
        mock_browser = Mock()
        mock_uc_chrome.return_value = mock_browser
        
        # Initialize user agents first
        self.scraper.user_agents = ["test-user-agent"]
        self.scraper.proxy_pool = [ProxyConfig(
            proxy_url="http://test:proxy@example.com:8080",
            proxy_type="http",
            country="US",
            speed_score=0.9,
            success_rate=0.95,
            is_active=True
        )]
        
        browser = asyncio.run(self.scraper.create_stealth_browser())
        
        self.assertIsNotNone(browser)
        mock_uc_chrome.assert_called_once()
        self.scraper.UNDETECTED_CHROME_AVAILABLE = original_value

    @patch('neural_protocol_scraper.webdriver.Chrome')
    def test_create_stealth_browser_undetected_unavailable(self, mock_chrome):
        """Test stealth browser creation without undetected_chromedriver"""
        # Temporarily set UNDETECTED_CHROME_AVAILABLE to False
        original_value = getattr(self.scraper, 'UNDETECTED_CHROME_AVAILABLE', False)
        self.scraper.UNDETECTED_CHROME_AVAILABLE = False
        
        mock_browser = Mock()
        mock_chrome.return_value = mock_browser
        
        # Initialize user agents first
        self.scraper.user_agents = ["test-user-agent"]
        self.scraper.proxy_pool = [ProxyConfig(
            proxy_url="http://test:proxy@example.com:8080",
            proxy_type="http",
            country="US",
            speed_score=0.9,
            success_rate=0.95,
            is_active=True
        )]
        
        browser = asyncio.run(self.scraper.create_stealth_browser())
