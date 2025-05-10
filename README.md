# URL Shortener Service

This project is a URL shortener service built with FastAPI. It allows users to shorten URLs and retrieve the original URLs using a short identifier.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Alexstom007/url-shortener.git
   cd url-shortener
   ```

2. Create a `.env` file in the root directory with the following content:
   ```env
   DB_NAME=url_shortener
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_HOST=localhost
   DB_PORT=5432
   DB_ECHO=True
   ```

3. Build and run the Docker containers:
   ```bash
   docker-compose up --build
   ```

## Features

- URL shortening with unique identifiers
- Redirect to original URLs
- PostgreSQL database for persistent storage
- Docker containerization
- Environment variable configuration
- FastAPI with automatic API documentation

## Usage

### Endpoints

- **POST /**: Create a shortened URL.
  - Request Body: `{ "url": "<original-url>" }`
  - Response: `{ "short_id": "<short-id>" }`

- **GET /{short_id}**: Retrieve the original URL.
  - Response: Redirects to the original URL with a 307 status code.

## Requirements

- Python 3.11
- Docker
- FastAPI
- PostgreSQL

## Application Access

After starting the containers, the application will be available at:
- http://localhost:8080
- API documentation: http://localhost:8080/docs

## Author

- [Alexander Votinov](https://github.com/Alexstom007) 