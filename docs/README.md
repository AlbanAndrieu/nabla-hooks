<!-- markdown-link-check-disable-next-line -->

## [![Nabla](http://bababou.albandrieu.com/nabla/index/assets/nabla/nabla-4.png)](https://github.com/AlbanAndrieu) nabla-hooks

Nabla custom git hooks

[![License](http://img.shields.io/:license-apache-blue.svg?style=flat-square)](http://www.apache.org/licenses/LICENSE-2.0.html)
[![Gitter](https://badges.gitter.im/nabla-hooks/Lobby.svg)](https://gitter.im/nabla-hooks/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

[![GitHub pull requests](https://img.shields.io/github/issues-pr/AlbanAndrieu/nabla-hooks.svg)](https://github.com/AlbanAndrieu/nabla-hooks/pulls)

This project intend to be uses by all Nabla products

# Table of contents

<!-- markdown-link-check-disable -->

// spell-checker:disable

<!-- toc -->

<!-- tocstop -->

// spell-checker:enable

<!-- markdown-link-check-enable -->

# [Initialize](#table-of-contents)

```bash
direnv allow
pyenv install 3.8.10
pyenv local 3.8.10
python -m pipenv install --dev --ignore-pipfile
direnv allow
pre-commit install
```

## [Requirements](#table-of-contents)

This hooks requires the following to run:

<!-- markdown-link-check-disable-next-line -->

- [jira](https://pypi.org/project/jira/)

## [Diagrams](#table-of-contents)

Sample of mermaid:

<!-- markdown-link-check-disable -->

```mermaid
sequenceDiagram
title: Front end flow when a user request a summary

actor User

User->>Nabla: Request a summary
Nabla->>Main DB: Check if the summary exists
Alt The summary have been generated and the document is part of the allowed dataset
Nabla->>User: Return the summary
Else The summary does not exists and the document is part of the allowed dataset
Nabla->>User: Return an error "The server is busy come back later/The summary is generating"
Else The document is part of the allowed dataset
Nabla ->>User: Return an error "Available soon"
End

```

```mermaid
sequenceDiagram
title: Asynchronous back end flow to generate summaries

loop for each document into the queue
MVP->>OpenAI: Ask for completion with the good prompt
OpenAI->>MVP: get the completion
alt success
MVP->>Back Office: Store/Replace the generated summary
else error
MVP->>MVP: Log a fail error
end
end

```

```mermaid
erDiagram
DOCUMENT_TRANSLATION ||--o{ DOCUMENT_SUMMARY: have
DOCUMENT_SUMMARY ||--o{ DOCUMENT_SUMMARY_USER_VOTE: have
USER }o--o{ DOCUMENT_SUMMARY_USER_VOTE: add

DOCUMENT_TRANSLATION {
		int id
}

USER {
		int id
}

DOCUMENT_SUMMARY {
		int id
		int document_id
    string content
    timestamp added_at
}

DOCUMENT_SUMMARY_USER_VOTE {
		int summary_id
		int user_id
		string vote
}
```

```mermaid
sequenceDiagram
	participant User
  participant Front Office
  participant DB
  participant Queue
  participant Summarization Service
  User->>Front Office: Request a summary
  Front Office->>DB: Get summary
  alt Summary already generated
		DB-->>Front Office: Send latest summary
    Front Office-->>User: Display summary
  else No generated summary yet
    Front Office-->>User: Display "The summary is being generated, please wait"
    Front Office->>DB: Flag the document as "pending"
    Front Office->>Queue: Add document to summarization queue
    Summarization Service->>Queue: Take document from queue
    Summarization Service->>Summarization Service: Generate summary
    Summarization Service-->>DB: Store summary / error status
  end
loop every 5s, untill the document is flaged as success
	alt The summary is pending
		User->>Front Office: Request a summary
		Front Office->>DB: Get summary
		DB->>Front Office: Send nothing
	  Front Office->>User: Display "in progress" message
	else The summary has been generated
		User->>Front Office: Request a summary
		Front Office->>DB: Get summary
		DB->>Front Office: Send the last summary
	  Front Office->>User: Display summary
  else failled OR the request_at data is too far
		User->>Front Office: Request a summary
		Front Office->>DB: Get summary
		DB->>Front Office: Send failed summary
		Front Office->>Queue: Add document to summarization queue
	  Front Office->>User: Display "in progress" message
	end
end
```

```mermaid
flowchart TD
  A[Start vote] --> B{Is upvote?}
  B --> |Yes| D[Ask for additional comments]
  B --> |No| C[Display feedback popup]
  C --> D
  D --> Z[End]
```

<!-- markdown-link-check-enable -->
