# Chatbot API

This project is a Django-based REST API for a chatbot application that allows users to start chat sessions, send messages, edit existing messages, and end chat sessions. The chat history is stored with timestamps and user information.

## Features

- Implementation of the Flan-T5 Model: The base version of the Flan-T5 model is used to optimize for performance and avoid heavy computation. To switch to a more powerful variant, such as the 'xxl' version, update the configuration in chatbot\chatbot\utils.py.
- User Authentication  (Django Token Authentication).
- SQLite database used.
- Start a new chat session.
- Add user messages / prompts and receive chatbot responses.
- Continue an existing chat session.
- Edit specific messages in chat history.
- End the current chat session.
- Delete specific chat room based on id.
- Timestamps are stored in PST time zone and formatted as `DD/MM/YYYY HH:MM:SS`.

## Requirements

- Python 3.10+
- Django 5.1.2
- Django REST Framework

## Installation

1. **Clone the repository**

    ```bash
    git clone https://github.com/Alijaffery5/chatbot-api.git
    cd chatbot-api
    ```

2. **Create a virtual environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run migrations**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Create a superuser**

    ```bash
    python manage.py createsuperuser
    ```

6. **Run the server**

    ```bash
    python manage.py runserver
    ```

7. **Access the API**

   - The API will be available at `http://127.0.0.1:8000/api/`

## API Endpoints
All Apis require these in the Header section except login and register.
```json
{
    "Content-Type":"application/json",
    "Authorization":"Token <enter_your_token_here>"
}
```

### Authentication

- `POST /api/login/`: Authenticate and Login the user.
- `POST /api/register/`: Register a new user.

### Register Operations

- **Register a new User**

    ```
    POST http://127.0.0.1:8000/api/register/
    ```

    Request Body:
    ```json
    {
        "username": "john_doe",
        "email": "john.doe@example.com",
        "password": "your_password"
    }

    ```

  -
    Example Response:
    ```json
    {
        "message": "Registered successfully!",
        "token": "token_displayed_here",
        "user": {
            "id": 1,
            "username": "john_doe",
            "email": "xyz@gmail.com",
            "password": "test12345678"
        }
    }

    ```
  
- **Login Endpoint**

    ```
    POST http://127.0.0.1:8000/api/login/
  ```
    Request Body:
    ```json
    {
        "username": "john_doe",
        "password": "your_password"
    }

    ```

  -
    Example Response:
    ```json
    {
        "message": "Logged-In successfully!",
        "token": "your_token_here",
        "user": {
            "id": 1,
            "username": "john_doe",
            "email": "xyz@gmail.com"
        }
    }

    ```

### Chat Operations

- **Start or Continue a Chat Session**

    ```
    POST /api/chats/
    ```

    Request Body:
    ```json
    {
        "content": "Your message here",
        "end_session": false
    }
    ```

    - `content`: The message content or body (Mandatory field).
    - `end_session`: Set to `true` to end the current session, or `false` to continue the chat (Optional - False by default).
    - Note: Each json request body must have **content** field and upon sending multiple requests with content, the chatbot will continue conversation with responses in the current session or chat room.

  Response:
  ```json
  {
    "chat_id": 118,
    "user_id": 2,
    "conversation": [
        {
            "message_id": "670a8acf-24af-4831-8c86-3f5863437b9a",
            "You": "How many plants are there in the universe?",
            "Bot": "seven"
        },
        {
            "id": "a4debb18-3fda-4bc2-afa7-ff330d339c03",
            "You": "What happens when coke is mixed with icecubes?",
            "Bot": "the ice cubes melt"
        }
    ],
    "start_time": "2024-10-24T22:47:26.507862Z",
    "end_time": null,
    "session_identifier": "b7d6a8f2-7986-4820-bd29-056cff5e32ec"
    }
  ```

## Read Chats

The `read_chats` endpoint allows users to retrieve their chat history, including all the messages exchanged during each chat session. User can also filter search chats using session_id.

- **Endpoint:** `/api/chats/` OR `chats/?session_id=<session_id>`
- **Method:** `GET`
- **Authentication Required:** Yes (Token Authentication or Session Authentication)



### Request Headers

```http
Authorization: Token your_auth_token_here
```
Example Response:
```json
[
    {
        "chat_id": 101,
        "start_time": "25/10/2024 12:30:00",
        "end_time": "25/10/2024 13:00:00",
        "session_id": "c1f8f5e1-8e42-4ef3-bb35-9a62c5271c82",
        "conversation": [
        {
            "message_id": "670a8acf-24af-4831-8c86-3f5863437b9a",
            "You": "How many planets are there in the universe",
            "Bot": "seven",
            "timestamp": "25/10/2024 04:20:03"

        },
        {
            "id": "a4debb18-3fda-4bc2-afa7-ff330d339c03",
            "You": "What happens when coke is mixed with icecubes?",
            "Bot": "the ice cubes melt",
            "timestamp": "25/10/2024 04:20:38"

        }
      ]
    },
    {
        "chat_id": 102,
        "user_id": 1,
        "start_time": "26/10/2024 09:00:00",
        "end_time": null,
        "session_id": "b2f8a3c9-8d2f-4f3c-bb35-9a62c5272d34",
        "conversation": [
        {
            "message_id": "670a8acf-24af-4831-8c86-3f5863437b9a",
            "You": "How many planets are there in the universe",
            "Bot": "seven"
        },
        {
            "id": "a4debb18-3fda-4bc2-afa7-ff330d339c03",
            "You": "What happens when coke is mixed with icecubes?",
            "Bot": "the ice cubes melt"
        }
      ]
    }
]

```


- ## Edit a Specific Message

    ```
    PATCH /api/chats/<chat_id>/messages/<message_id>/
    ```

    Request Body:
    ```json
    {
        "content": "Updated message content"
    }
    ```

    Response:
    ```json
    {
        "message": "Message updated successfully"
    }
    ```
  
- **Delete a specific chat session based on chat_id**

    ```
    DELETE /api/chats/<int:chat_id>/
    ```
    
    Response:
    ```json
    {
        "message": "Chat deleted successfully"
    }
    ```

### Ending a Chat Session

- **End the Current Chat Session**

    ```
    POST /api/chats/
    ```

    Request Body:
    ```json
    {
        "content": "xyz",
        "end_session": true
    }
    ```

    Response:
    ```json
    {
        "message": "Chat session ended successfully",
        "start_time": "24/10/2024 10:00:00",
        "end_time": "24/10/2024 10:30:00",
        "session_id": "b7d6a8f2-7986-4820-bd29-056cff5e32ec"
    }
    ```

## Configuration

- **Time Zone Configuration**

    The API stores timestamps in PST time zone (`Asia/Karachi`). You can change this configuration in the code where the timezone is set.

## Models

- **Chat**
    - `user`: ForeignKey to the User model.
    - `content`: JSONField to store chat history (list of dictionaries).
    - `start_time`: DateTime when the chat started.
    - `end_time`: DateTime when the chat ended (nullable).
    - `session_id`: Unique identifier for each chat session.

## Utils

- Custom decorators for authentication and permissions (`@authenticated_view`) can be used to enforce authentication on specific endpoints.

## Testing

1. **Run Tests**

    ```bash
    python manage.py test
    ```

## Contributing

1. **Fork the repository**
2. **Create a new branch**
3. **Make your changes**
4. **Submit a pull request**

## License

This project is licensed under the MIT License.

## Troubleshooting

- **Common Errors**
    - `"AttributeError: 'str' object has no attribute 'append'"`: Ensure that the `content` field in the database is a JSON array, not a string.
    - `"JSONDecodeError"`: Check that the JSON being sent in the request is valid.

## Acknowledgements

- Django REST Framework for providing the tools to build the API.
