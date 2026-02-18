import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Add parent directory to path to import spatiallm module
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestHello(unittest.TestCase):
    """Unit tests for hello.py module"""
    
    @patch('spatiallm.hello.OpenAI')
    @patch('spatiallm.hello.load_dotenv')
    def test_valid_response(self, mock_load_dotenv, mock_openai_class):
        """Test that hello.py handles a valid response correctly"""
        # Create a mock response object
        mock_response = Mock()
        mock_response.output_text = "Why don't scientists trust atoms? Because they make up everything!"
        
        # Create a mock client instance
        mock_client = Mock()
        mock_client.responses.create.return_value = mock_response
        
        # Configure the OpenAI class mock to return our mock client
        mock_openai_class.return_value = mock_client
        
        # Import and run the module
        import spatiallm.hello
        
        # Verify load_dotenv was called
        mock_load_dotenv.assert_called_once()
        
        # Verify OpenAI client was instantiated
        mock_openai_class.assert_called_once()
        
        # Verify the API call was made with correct parameters
        mock_client.responses.create.assert_called_once_with(
            model="gpt-5-mini",
            input="Tell me a one-liner joke",
        )
        
        # Verify the response has the expected output_text attribute
        self.assertIsNotNone(mock_response.output_text)
        self.assertIsInstance(mock_response.output_text, str)
        self.assertTrue(len(mock_response.output_text) > 0)


if __name__ == '__main__':
    unittest.main()
