#!/usr/bin/env bash
#set -xv

set -o errexit
set -o pipefail
set -o nounset

DEBUG=${DEBUG:=0}
[[ $DEBUG -eq 1 ]] && set -o xtrace

WORKING_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# shellcheck source=./pre_commit_hooks/step-0-color.sh
source "${WORKING_DIR}/step-0-color.sh"

# You can test it with
# pre_commit_hooks/jira-check.sh --commit-msg-file .git/COMMIT_EDITMSG
# echo "TEST-123 Fix bug" > /tmp/test_commit_msg.txt && pre_commit_hooks/jira-check.sh --commit-msg-file /tmp/test_commit_msg.txt

usage() {
  echo "Usage: $0 [--commit-msg-file <path>] [--pattern <pattern>] [--help]" 1>&2
  echo "  --commit-msg-file: Path to commit message file (default: read from stdin or first file argument)" 1>&2
  echo "  --pattern: JIRA ticket pattern (default: [A-Z]{2,10}-[0-9]+)" 1>&2
  echo "  --help: Show this help message" 1>&2
  exit 1
}

# Default JIRA pattern: PROJECT-123 format (2-10 uppercase letters, dash, numbers)
# Use a simple if statement to avoid brace expansion issues
if [[ -z "${JIRA_PATTERN:-}" ]]; then
  JIRA_PATTERN='[A-Z]{2,10}-[0-9]+'
fi
COMMIT_MSG_FILE=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --commit-msg-file)
      COMMIT_MSG_FILE="$2"
      shift 2
      ;;
    --pattern)
      JIRA_PATTERN="$2"
      shift 2
      ;;
    --help|-h)
      usage
      ;;
    *)
      # If no flag specified, treat as commit message file
      if [[ -z "$COMMIT_MSG_FILE" ]] && [[ -f "$1" ]]; then
        COMMIT_MSG_FILE="$1"
      fi
      shift
      ;;
  esac
done

# Read commit message from file or stdin
if [[ -n "$COMMIT_MSG_FILE" ]] && [[ -f "$COMMIT_MSG_FILE" ]]; then
  COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")
elif [[ ! -t 0 ]]; then
  # Read from stdin if available
  COMMIT_MSG=$(cat)
else
  echo -e "${red}Error: No commit message provided${NC}" 1>&2
  usage
fi

# Skip empty commit messages
if [[ -z "$COMMIT_MSG" ]]; then
  echo -e "${yellow}Warning: Empty commit message, skipping JIRA check${NC}"
  exit 0
fi

# Skip merge commits
if echo "$COMMIT_MSG" | grep -q "^Merge branch"; then
  echo -e "${green}Merge commit detected, skipping JIRA check${NC}"
  exit 0
fi

# Skip revert commits
if echo "$COMMIT_MSG" | grep -q "^Revert"; then
  echo -e "${green}Revert commit detected, skipping JIRA check${NC}"
  exit 0
fi

# Extract first line of commit message (subject line)
COMMIT_MSG_SUBJECT=$(echo "$COMMIT_MSG" | head -n 1)

# Check if commit message contains JIRA ticket
if echo "$COMMIT_MSG_SUBJECT" | grep -qE "$JIRA_PATTERN"; then
  JIRA_TICKET=$(echo "$COMMIT_MSG_SUBJECT" | grep -oE "$JIRA_PATTERN" | head -n 1)
  echo -e "${green}✓ JIRA ticket found: ${bold}${JIRA_TICKET}${NC}${green}${NC}"
  exit 0
else
  echo -e "${red}✗ Error: No JIRA ticket found in commit message${NC}"
  echo -e "${yellow}Commit message subject: ${COMMIT_MSG_SUBJECT}${NC}"
  echo -e "${yellow}Expected pattern: ${JIRA_PATTERN}${NC}"
  echo -e ""
  echo -e "${cyan}Examples of valid commit messages:${NC}"
  echo -e "  ${green}PROJ-123: Add new feature${NC}"
  echo -e "  ${green}TEAM-456 Fix critical bug${NC}"
  echo -e "  ${green}[ABC-789] Update documentation${NC}"
  echo -e ""
  echo -e "${cyan}Tip: Start your commit message with a JIRA ticket reference (e.g., PROJ-123)${NC}"
  exit 1
fi
