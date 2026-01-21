#!/bin/bash
#set -eu

WORKING_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# shellcheck source=/dev/null
source "${WORKING_DIR}/../scripts/step-0-color.sh"

echo -e "${green}Running JIRA check tests${NC}"

JIRA_CHECK_SCRIPT="${WORKING_DIR}/../pre_commit_hooks/jira-check.sh"
TEST_FAILED=0

# Test 1: Valid JIRA ticket
echo -e "${cyan}Test 1: Valid JIRA ticket${NC}"
echo "TEST-123 Add new feature" > /tmp/test_commit_msg_1.txt
if ${JIRA_CHECK_SCRIPT} --commit-msg-file /tmp/test_commit_msg_1.txt; then
  echo -e "${green}✓ Test 1 passed${NC}"
else
  echo -e "${red}✗ Test 1 failed${NC}"
  TEST_FAILED=1
fi

# Test 2: No JIRA ticket (should fail)
echo -e "${cyan}Test 2: No JIRA ticket (should fail)${NC}"
echo "No JIRA ticket here" > /tmp/test_commit_msg_2.txt
if ! ${JIRA_CHECK_SCRIPT} --commit-msg-file /tmp/test_commit_msg_2.txt; then
  echo -e "${green}✓ Test 2 passed (correctly rejected)${NC}"
else
  echo -e "${red}✗ Test 2 failed (should have been rejected)${NC}"
  TEST_FAILED=1
fi

# Test 3: JIRA ticket with brackets
echo -e "${cyan}Test 3: JIRA ticket with brackets${NC}"
echo "[PROJ-456] Fix critical bug" > /tmp/test_commit_msg_3.txt
if ${JIRA_CHECK_SCRIPT} --commit-msg-file /tmp/test_commit_msg_3.txt; then
  echo -e "${green}✓ Test 3 passed${NC}"
else
  echo -e "${red}✗ Test 3 failed${NC}"
  TEST_FAILED=1
fi

# Test 4: Merge commit (should be skipped)
echo -e "${cyan}Test 4: Merge commit (should be skipped)${NC}"
echo "Merge branch 'feature' into main" > /tmp/test_commit_msg_4.txt
if ${JIRA_CHECK_SCRIPT} --commit-msg-file /tmp/test_commit_msg_4.txt; then
  echo -e "${green}✓ Test 4 passed (merge commit skipped)${NC}"
else
  echo -e "${red}✗ Test 4 failed${NC}"
  TEST_FAILED=1
fi

# Test 5: Revert commit (should be skipped)
echo -e "${cyan}Test 5: Revert commit (should be skipped)${NC}"
echo "Revert \"Add broken feature\"" > /tmp/test_commit_msg_5.txt
if ${JIRA_CHECK_SCRIPT} --commit-msg-file /tmp/test_commit_msg_5.txt; then
  echo -e "${green}✓ Test 5 passed (revert commit skipped)${NC}"
else
  echo -e "${red}✗ Test 5 failed${NC}"
  TEST_FAILED=1
fi

# Test 6: Long project key
echo -e "${cyan}Test 6: Long project key${NC}"
echo "LONGPROJ-999 Update documentation" > /tmp/test_commit_msg_6.txt
if ${JIRA_CHECK_SCRIPT} --commit-msg-file /tmp/test_commit_msg_6.txt; then
  echo -e "${green}✓ Test 6 passed${NC}"
else
  echo -e "${red}✗ Test 6 failed${NC}"
  TEST_FAILED=1
fi

# Test 7: JIRA ticket in middle of message
echo -e "${cyan}Test 7: JIRA ticket in middle of message${NC}"
echo "Fix bug related to TASK-789 and improve performance" > /tmp/test_commit_msg_7.txt
if ${JIRA_CHECK_SCRIPT} --commit-msg-file /tmp/test_commit_msg_7.txt; then
  echo -e "${green}✓ Test 7 passed${NC}"
else
  echo -e "${red}✗ Test 7 failed${NC}"
  TEST_FAILED=1
fi

# Clean up test files
rm -f /tmp/test_commit_msg_*.txt

if [ $TEST_FAILED -eq 0 ]; then
  echo -e "${green}All JIRA check tests passed!${NC}"
  exit 0
else
  echo -e "${red}Some JIRA check tests failed!${NC}"
  exit 1
fi
