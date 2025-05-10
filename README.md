# URL Shortener Service

This project is a URL shortener service built with FastAPI. It allows users to shorten URLs and retrieve the original URLs using a short identifier.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
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

3. Build the Docker image:
   ```bash
   docker build -t url-shortener .
   ```

4. Run the Docker container:
   ```bash
   docker run -p 8080:8080 url-shortener
   ```

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

## Author

- [Alexander Votinov](https://github.com/Alexstom007) 