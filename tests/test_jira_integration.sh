#!/bin/bash
# Manual integration test for JIRA check hook

set -e

WORKING_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${WORKING_DIR}/.."

echo "=== JIRA Check Hook Integration Test ==="
echo ""

# Test 1: Direct script execution
echo "Test 1: Direct script execution with valid JIRA ticket"
echo "PROJ-123 Test commit" | ${PROJECT_ROOT}/pre_commit_hooks/jira-check.sh
echo ""

# Test 2: Test with invalid message
echo "Test 2: Direct script execution without JIRA ticket (should fail)"
if echo "Invalid commit message" | ${PROJECT_ROOT}/pre_commit_hooks/jira-check.sh 2>/dev/null; then
  echo "ERROR: Should have failed!"
  exit 1
else
  echo "✓ Correctly rejected commit without JIRA ticket"
fi
echo ""

# Test 3: Test as commit-msg hook simulation
echo "Test 3: Simulate commit-msg hook"
TEMP_MSG_FILE=$(mktemp)
echo "TEST-456 Add feature" > "$TEMP_MSG_FILE"
${PROJECT_ROOT}/pre_commit_hooks/jira-check.sh "$TEMP_MSG_FILE"
rm "$TEMP_MSG_FILE"
echo ""

# Test 4: Test custom pattern
echo "Test 4: Test with custom pattern"
export JIRA_PATTERN="[A-Z]{3}-[0-9]{4}"
echo "ABC-1234 Custom pattern test" | ${PROJECT_ROOT}/pre_commit_hooks/jira-check.sh
unset JIRA_PATTERN
echo ""

echo "=== All integration tests passed! ==="
