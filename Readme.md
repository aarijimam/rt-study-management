# Study Management API

This is a FastAPI-based Study Management API that allows you to manage allergies and other related data. The API is secured using API keys.

## Features

- Create, read, update, and delete allergies
- Secure endpoints with API key authentication
- SQLite database for data storage

## Requirements

- Python 3.11+
- FastAPI
- SQLAlchemy
- Uvicorn
- python-dotenv

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/your-username/study-management-api.git
    cd study-management-api
    ```

2. Create and activate a virtual environment:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory with the following content:

    ```properties
    DATABASE_URL="sqlite:///db/study-management.db"
    API_KEY="your-api-key"
    ```
5. A new database can be created if needed but running the `create_tables_lite.sql` script.

## Running the Application

1. Start the FastAPI server:

    ```sh
    uvicorn app.main:app --host 0.0.0.0 --port 8000
    ```

2. The API will be available at `http://localhost:8000`.

## API Endpoints

### Authentication

All endpoints require an API key for authentication. Include the API key in the request headers:

```http
access_token: your-api-key
```

### Allergies

- **Create new allergies**

    ```sh
    curl -X POST "http://localhost:8000/allergies/" \
         -H "Content-Type: application/json" \
         -H "access_token: your-api-key" \
         -d '[
               {"allergyname": "Peanuts", "type": "Food"},
               {"allergyname": "Dust", "type": "Environmental"}
             ]'
    ```

- **Get all allergies**

    ```sh
    curl -X GET "http://localhost:8000/allergies/" \
         -H "accept: application/json" \
         -H "access_token: your-api-key"
    ```

- **Get allergy by ID**

    ```sh
    curl -X GET "http://localhost:8000/allergies/{allergy_id}" \
         -H "accept: application/json" \
         -H "access_token: your-api-key"
    ```

- **Delete an allergy**

    ```sh
    curl -X DELETE "http://localhost:8000/allergies/{allergy_id}" \
         -H "access_token: your-api-key"
    ```

## Securing the API

To secure the API, ensure that you are using HTTPS in production. You can use a reverse proxy like Nginx to handle SSL termination.

## Database

The program can use any SQL databse thanks to SQLAlchemy, just change the `DATABASE_URL` to the desired database url in the `.env`.

### Database Design

<img width="1231" alt="image" src="https://github.com/user-attachments/assets/f66e3d53-9715-4f20-800e-08073ed36f8e" />

## Running Tests

To run the tests, follow these steps:

1. Ensure your virtual environment is activated:

    ```sh
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2. Install the test dependencies if not already installed:

    ```sh
    pip install pytest httpx
    ```

3. Run the tests using `pytest`:

    ```sh
    python -m pytest app/
    ```

This will discover and run all the test cases in the `tests` directory.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
