#!/usr/bin/env python3
"""Test module for commit-summary.py."""

import os
import subprocess
import sys
import tempfile
from unittest import TestCase, mock

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.git.commit_summary import (
    CommitInfo,
    generate_prompt,
    get_changed_files,
    get_current_commit,
    has_commits,
    is_git_repository,
    save_summary,
)


class TestCommitSummary(TestCase):
    """Test class for commit-summary.py."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir)

    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_dir)
        # Clean up temp directory
        for root, dirs, files in os.walk(self.temp_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.temp_dir)

    @mock.patch("subprocess.check_output")
    def test_is_git_repository_true(self, mock_check_output):
        """Test is_git_repository when in a git repository."""
        mock_check_output.return_value = b"true"
        self.assertTrue(is_git_repository())

    @mock.patch("subprocess.check_output")
    def test_is_git_repository_false(self, mock_check_output):
        """Test is_git_repository when not in a git repository."""
        mock_check_output.side_effect = subprocess.CalledProcessError(1, "git")
        self.assertFalse(is_git_repository())

    @mock.patch("subprocess.check_output")
    def test_has_commits_true(self, mock_check_output):
        """Test has_commits when repository has commits."""
        mock_check_output.return_value = b"abc123"
        self.assertTrue(has_commits())

    @mock.patch("subprocess.check_output")
    def test_has_commits_false(self, mock_check_output):
        """Test has_commits when repository has no commits."""
        mock_check_output.side_effect = subprocess.CalledProcessError(1, "git")
        self.assertFalse(has_commits())

    @mock.patch("scripts.git.commit_summary.is_git_repository")
    @mock.patch("scripts.git.commit_summary.has_commits")
    @mock.patch("subprocess.check_output")
    def test_get_current_commit(self, mock_check_output, mock_has_commits, mock_is_repo):
        """Test get_current_commit."""
        mock_is_repo.return_value = True
        mock_has_commits.return_value = True
        mock_check_output.side_effect = [
            b"abc123",  # rev-parse HEAD
            b"John Doe",  # log -1 --pretty=format:%an
            b"2024-04-29",  # log -1 --pretty=format:%ad
            b"Test commit message",  # log -1 --pretty=format:%B
        ]

        commit_info = get_current_commit()
        self.assertIsInstance(commit_info, CommitInfo)
        self.assertEqual(commit_info.hash, "abc123")
        self.assertEqual(commit_info.author, "John Doe")
        self.assertEqual(commit_info.date, "2024-04-29")
        self.assertEqual(commit_info.message, "Test commit message")

    @mock.patch("subprocess.check_output")
    def test_get_changed_files(self, mock_check_output):
        """Test get_changed_files."""
        mock_check_output.return_value = b"file1.py\nfile2.py"
        changed_files = get_changed_files()
        self.assertEqual(changed_files, ["file1.py", "file2.py"])

    def test_generate_prompt(self):
        """Test generate_prompt."""
        commit_info = CommitInfo(
            hash="abc123",
            author="John Doe",
            date="2024-04-29",
            message="Test commit message",
        )
        changed_files = ["file1.py", "file2.py"]
        prompt = generate_prompt(commit_info, changed_files)

        self.assertIn("abc123", prompt)
        self.assertIn("John Doe", prompt)
        self.assertIn("2024-04-29", prompt)
        self.assertIn("Test commit message", prompt)
        self.assertIn("file1.py", prompt)
        self.assertIn("file2.py", prompt)

    def test_save_summary(self):
        """Test save_summary."""
        commit_info = CommitInfo(
            hash="abc123",
            author="John Doe",
            date="2024-04-29",
            message="Test commit message",
        )
        changed_files = ["file1.py", "file2.py"]
        summary = "Test summary"

        filepath = save_summary(summary, commit_info, changed_files)
        self.assertTrue(os.path.exists(filepath))

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("abc123", content)
            self.assertIn("John Doe", content)
            self.assertIn("2024-04-29", content)
            self.assertIn("Test commit message", content)
            self.assertIn("Test summary", content)
            self.assertIn("file1.py", content)
            self.assertIn("file2.py", content) 