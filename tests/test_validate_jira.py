#!/usr/bin/env python3
"""
Tests for validate_jira module.
"""
import os
import sys
import tempfile
import unittest

# Add hooks directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'hooks'))

from validate_jira import extract_jira_ticket, is_special_commit, validate_commit_message


class TestValidateJira(unittest.TestCase):
    """Test cases for JIRA validation."""
    
    def test_extract_jira_ticket_valid(self):
        """Test extracting valid JIRA tickets."""
        self.assertEqual(extract_jira_ticket("TEST-123 Add feature"), "TEST-123")
        self.assertEqual(extract_jira_ticket("[PROJ-456] Fix bug"), "PROJ-456")
        self.assertEqual(extract_jira_ticket("ABC-789: Update docs"), "ABC-789")
        self.assertEqual(extract_jira_ticket("Fix TASK-111 issue"), "TASK-111")
    
    def test_extract_jira_ticket_invalid(self):
        """Test messages without JIRA tickets."""
        self.assertIsNone(extract_jira_ticket("Add feature"))
        self.assertIsNone(extract_jira_ticket("Fix bug"))
        self.assertIsNone(extract_jira_ticket("A-123 too short"))  # Project key too short
        # Note: TOOLONGKEY-123 would match if pattern allows up to 10 chars
    
    def test_extract_jira_ticket_custom_pattern(self):
        """Test custom JIRA patterns."""
        pattern = r'[A-Z]{3}-[0-9]{4}'
        self.assertEqual(extract_jira_ticket("ABC-1234 test", pattern), "ABC-1234")
        self.assertIsNone(extract_jira_ticket("AB-123 test", pattern))  # Too short
    
    def test_is_special_commit_merge(self):
        """Test merge commit detection."""
        self.assertTrue(is_special_commit("Merge branch 'feature' into main"))
        self.assertTrue(is_special_commit("Merge pull request #123"))
        self.assertFalse(is_special_commit("TEST-123 Add feature"))
    
    def test_is_special_commit_revert(self):
        """Test revert commit detection."""
        self.assertTrue(is_special_commit("Revert \"Add broken feature\""))
        self.assertFalse(is_special_commit("TEST-123 Revert changes"))  # Not a revert commit
    
    def test_is_special_commit_fixup(self):
        """Test fixup and squash commit detection."""
        self.assertTrue(is_special_commit("fixup! TEST-123 Add feature"))
        self.assertTrue(is_special_commit("squash! Fix bug"))
        self.assertFalse(is_special_commit("TEST-123 Fix and squash"))
    
    def test_validate_commit_message_valid(self):
        """Test validation with valid commit messages."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("TEST-123 Add new feature")
            f.flush()
            
            try:
                result = validate_commit_message(f.name)
                self.assertTrue(result)
            finally:
                os.unlink(f.name)
    
    def test_validate_commit_message_invalid(self):
        """Test validation with invalid commit messages."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Add new feature without ticket")
            f.flush()
            
            try:
                result = validate_commit_message(f.name)
                self.assertFalse(result)
            finally:
                os.unlink(f.name)
    
    def test_validate_commit_message_merge(self):
        """Test validation skips merge commits."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Merge branch 'feature' into main")
            f.flush()
            
            try:
                result = validate_commit_message(f.name)
                self.assertTrue(result)  # Should pass (skip validation)
            finally:
                os.unlink(f.name)
    
    def test_validate_commit_message_empty(self):
        """Test validation with empty commit message."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("")
            f.flush()
            
            try:
                result = validate_commit_message(f.name)
                self.assertFalse(result)
            finally:
                os.unlink(f.name)


if __name__ == '__main__':
    unittest.main()
