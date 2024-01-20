# Montblanc: LLM Chat Bot for Data Querying

## Introduction

Montblanc is an application that connects to a MariaDB database, enabling users to query data through natural language prompts. This simplifies database interactions, making data retrieval more accessible and intuitive.

## Installation

To get started with Montblanc, follow these steps:

```bash
git clone https://github.com/yokurang/montblanc
```

### Setting Up MariaDB

Install MariaDB:

```bash
brew install mariadb
```

```bash
brew services start mariadb
```

Populate your local database with seed data:

```bash
mariadb -u root -p evooq_test < montblanc-0500.sql
```

_Note: Replace `montblanc-0500.sql` with your seed data file._

### Configuring Environment Variables

Create a `.env` file in the project root with the following credentials:

```bash
OPENAI_API_KEY =
MARIADB_USER =
MARIADB_PASSWORD =
MARIADB_HOST =
MARIADB_PORT =
MARIADB_DATABASE_NAME =
```

### Installing Dependencies

Set up a Python virtual environment and install dependencies:

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

### Running the Application

Launch Montblanc:

```bash
python main.py
```

## System Design

### Project structure

The Montblanc application is structured as follows:

```
.
├── README.md
├── commands.py
├── data
│   └── montblanc-0500.sql
├── db_handler.py
├── gpt_handler.py
├── main.py
├── requirements.txt
└── test_gpt.py

2 directories, 8 files
```

### How It Works

Montblanc's workflow can be summarized in the following steps:

1. **Database Schema Collection**: Gathers information about the database tables and columns and provides it as context to the Large Language Model (LLM).
2. **LLM Prompt Processing**: Sends prompts and questions to the LLM, which then generates SQL queries to address the user's inquiries.
3. **SQL Query Execution**: Executes the SQL queries against the MariaDB database.
4. **JSON Response**: Returns the results of the successful SQL queries as a JSON object.

### File Descriptions

- **commands.py**: Defines various data types used in the application using `Pydantic` for data validation and settings management.

- **db_handler.py**: Manages connections with the MariaDB database, collects necessary schema information, and executes SQL queries. It also formats the query results as JSON objects.

- **gpt_handler.py**: Handles communication with the OpenAI GPT-4 model through API calls, facilitating the processing of natural language queries into SQL commands.

- **main.py**: Serves as the entry point of the application, orchestrating the overall functionality.

- **test_gpt.py**: Contains unit tests for validating the correctness and reliability of the application, focusing primarily on GPT-related functionalities.

## Demonstration

Here is an example of when I asked Montblanc to query my database with the following question: "Give me all of the batch ids whose status is SUCCESSFUL."

![image](https://github.com/yokurang/montblanc/assets/114996150/52c16f47-8347-45e6-9446-15fd2e7b6d49)


---
