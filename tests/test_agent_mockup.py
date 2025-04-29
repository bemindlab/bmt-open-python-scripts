#!/usr/bin/env python3
"""Test module for mockup.py."""

import os
import sys
from unittest import TestCase, mock
import pytest
from unittest.mock import patch, MagicMock

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.agents.mockup import MockupAgent
from scripts.git.commit_summary import CommitInfo


class TestMockupAgent(TestCase):
    """Test class for MockupAgent."""

    def setUp(self):
        """Set up test environment."""
        self.agent = MockupAgent()
        self.test_commit = CommitInfo(
            hash="abc123",
            author="John Doe",
            date="2024-04-29",
            message="Test commit message",
        )

    @mock.patch("scripts.agents.mockup.get_current_commit")
    def test_get_commit_info_first_call(self, mock_get_current_commit):
        """Test get_commit_info when called for the first time."""
        mock_get_current_commit.return_value = self.test_commit
        
        # First call should fetch commit info
        commit_info = self.agent.get_commit_info()
        
        self.assertEqual(commit_info.hash, self.test_commit.hash)
        self.assertEqual(commit_info.author, self.test_commit.author)
        self.assertEqual(commit_info.date, self.test_commit.date)
        self.assertEqual(commit_info.message, self.test_commit.message)
        
        # Verify get_current_commit was called once
        mock_get_current_commit.assert_called_once()

    @mock.patch("scripts.agents.mockup.get_current_commit")
    def test_get_commit_info_cached(self, mock_get_current_commit):
        """Test get_commit_info uses cached value on subsequent calls."""
        mock_get_current_commit.return_value = self.test_commit
        
        # First call
        self.agent.get_commit_info()
        # Second call should use cached value
        self.agent.get_commit_info()
        
        # Verify get_current_commit was called only once
        mock_get_current_commit.assert_called_once()

    @mock.patch("scripts.agents.mockup.get_current_commit")
    def test_generate_mockup(self, mock_get_current_commit):
        """Test generate_mockup returns correct structure."""
        mock_get_current_commit.return_value = self.test_commit
        
        mockup_data = self.agent.generate_mockup()
        
        # Check structure and values
        self.assertIsInstance(mockup_data, dict)
        self.assertIn("commit", mockup_data)
        self.assertIn("files", mockup_data)
        self.assertIn("summary", mockup_data)
        
        # Check commit data
        commit_data = mockup_data["commit"]
        self.assertEqual(commit_data["hash"], self.test_commit.hash)
        self.assertEqual(commit_data["author"], self.test_commit.author)
        self.assertEqual(commit_data["date"], self.test_commit.date)
        self.assertEqual(commit_data["message"], self.test_commit.message)
        
        # Check files and summary
        self.assertEqual(mockup_data["files"], [])
        self.assertEqual(mockup_data["summary"], "")

@pytest.fixture
def mockup_agent():
    """Create a MockupAgent instance for testing."""
    return MockupAgent()

@pytest.fixture
def mock_commit_info():
    """Create mock commit information."""
    return CommitInfo(
        hash="abc123",
        author="Test Author",
        date="2024-01-01",
        message="Test commit message"
    )

def test_get_commit_info(mockup_agent, mock_commit_info):
    """Test getting commit information."""
    with patch('scripts.agents.mockup.get_current_commit', return_value=mock_commit_info):
        result = mockup_agent.get_commit_info()
        assert result.hash == mock_commit_info.hash
        assert result.author == mock_commit_info.author
        assert result.date == mock_commit_info.date
        assert result.message == mock_commit_info.message

def test_get_commit_info_cached(mockup_agent, mock_commit_info):
    """Test that commit info is cached."""
    with patch('scripts.agents.mockup.get_current_commit', return_value=mock_commit_info) as mock_get_commit:
        # First call should get from git
        result1 = mockup_agent.get_commit_info()
        assert result1.hash == mock_commit_info.hash
        assert mock_get_commit.call_count == 1

        # Second call should use cached value
        result2 = mockup_agent.get_commit_info()
        assert result2.hash == mock_commit_info.hash
        assert mock_get_commit.call_count == 1  # Should not call again

def test_generate_mockup(mockup_agent, mock_commit_info):
    """Test generating mockup data."""
    with patch('scripts.agents.mockup.get_current_commit', return_value=mock_commit_info):
        mockup_data = mockup_agent.generate_mockup()
        assert isinstance(mockup_data, dict)
        assert 'commit' in mockup_data
        commit_data = mockup_data['commit']
        assert commit_data['hash'] == mock_commit_info.hash
        assert commit_data['author'] == mock_commit_info.author
        assert commit_data['date'] == mock_commit_info.date
        assert commit_data['message'] == mock_commit_info.message 