# Trivia API | Backend

Udacity, as part of its proposal to create ties between its employees, is looking to develop a web page to manage a question-and-answer game, that is, the creation of a Trivia App.

As students in the Full Stack Developer course, we were tasked with finishing the trivia app using Flask for the backend and React for the front end.

## Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 


### Install Dependencies

1. **Python Latest Version** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file, in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Error Handling

Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 
- 500: Internal Error 

## Endpoints 
### GET /categories
- General:
    - Returns a list of categories objects, success value, total number of categories, paginated total of categories, and current page.

- Request Arguments:
    - Page (INT): Starting from 1; You can decide which of the paginated groups must be returned.
    - Limit (INT): 10 by default; Decide what is the limit of items per group.

- Sample: `curl http://127.0.0.1:5000/categories`

```
{
    "categories": [
        {
            "id": 1,
            "type": "Science"
        },
        {
            "id": 2,
            "type": "Art"
        },
        {
            "id": 3,
            "type": "Geography"
        },
        {
            "id": 4,
            "type": "History"
        },
        {
            "id": 5,
            "type": "Entertainment"
        },
        {
            "id": 6,
            "type": "Sports"
        }
    ],
    "real_total": 6,
    "success": true,
    "paginated_total": 6,
    "current_page": 1,
}
``` 

### GET /categories/{int:category_id}
- General:
    - Returns a specific category object, success value.

- Sample: `curl http://127.0.0.1:5000/categories/1`

``` 
{
    "category": {
        "id": 1,
        "type": "Science"
    },
    "success": true
}
```

### GET /categories/{int:category_id}/questions
- General:
    - Returns a list of questions objects, success value, total number of questions, paginated total of questions, and current page.

- Request Arguments:
    - Page (INT): Starting from 1; You can decide which of the paginated groups must be returned.
    - Limit (INT): 10 by default; Decide what is the limit of items per group.

- Sample: `curl http://127.0.0.1:5000/categories/2/questions`

``` 
{
    "current_page": 1,
    "paginated_total": 4,
    "questions": [
        {
            "answer": "Escher",
            "category": "Art",
            "category_id": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Mona Lisa",
            "category": "Art",
            "category_id": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "One",
            "category": "Art",
            "category_id": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
            "answer": "Jackson Pollock",
            "category": "Art",
            "category_id": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        }
    ],
    "real_total": 4,
    "success": true
}
```

### GET /questions
- General:
    - Returns a list of questions objects, success value, total number of questions, paginated total of questions, and current page.

- Request Arguments:
    - Page (INT): Starting from 1; You can decide which of the paginated groups must be returned.
    - Limit (INT): 10 by default; Decide what is the limit of items per group.

- Sample: `curl http://127.0.0.1:5000/questions?page=2&limit=5`

```
{
    "current_page": 2,
    "paginated_total": 5,
    "questions": [
        {
            "answer": "Brazil",
            "category": "Sports",
            "category_id": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": "Sports",
            "category_id": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": "History",
            "category_id": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Lake Victoria",
            "category": "Geography",
            "category_id": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": "Geography",
            "category_id": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        }
    ],
    "real_total": 19,
    "success": true
}
``` 

### GET /questions/{int:question_id}
- General:
    - Returns a specific question object, success value.

- Sample: `curl http://127.0.0.1:5000/questions/5`

```
{
    "question": {
        "answer": "Maya Angelou",
        "category": "History",
        "category_id": 4,
        "difficulty": 2,
        "id": 5,
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    "success": true
}
```

### POST /categories
- Creating a new Category:
    - Creates a new category using the submitted type. Returns a list of categories objects, success value, total number of categories, paginated total of categories, and current page.

- `curl http://127.0.0.1:5000/categories -X POST -H "Content-Type: application/json" -d '{"type":"Test"}'`

```
{
    "categories": [
        {
            "id": 1,
            "type": "Science"
        },
        {
            "id": 2,
            "type": "Art"
        },
        {
            "id": 3,
            "type": "Geography"
        },
        {
            "id": 4,
            "type": "History"
        },
        {
            "id": 5,
            "type": "Entertainment"
        },
        {
            "id": 6,
            "type": "Sports"
        },
        {
            "id": 7,
            "type": "Test"
        }
    ],
    "current_page": 1,
    "paginated_total": 7,
    "real_total": 7,
    "success": true
}
```

- General:
    - Returns a list of categories objects, success value, total number of categories, paginated total of categories, and current page.

- `curl http://127.0.0.1:5000/categories -X POST -H "Content-Type: application/json" -d '{"search":"ar"}'`

```
{
    "categories": [
        {
            "id": 2,
            "type": "Art"
        }
    ],
    "current_page": 1,
    "paginated_total": 1,
    "real_total": 1,
    "success": true
}
```

### POST /questions

- Filter categories:
    - Returns a list of questions objects, success value, total number of questions, paginated total of questions, and current page.

- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"search":"what?"}'`

```
{
    "current_page": 1,
    "paginated_total": 2,
    "questions": [
        {
            "answer": "Mona Lisa",
            "category": "Art",
            "category_id": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "Blood",
            "category": "Science",
            "category_id": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        }
    ],
    "real_total": 2,
    "success": true
}
```