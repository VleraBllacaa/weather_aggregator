# Weather Data Hub for Bulgarian Cities

This system handles different types of weather stations, each providing data in unique formats and displays those data.

### Prerequisites

- Python 3.12
- [Poetry] (https://python-poetry.org/docs/)

### Setup Instructions

- Step 1: Create Virtual Environment

    1. Open your terminal
    2. Navigate to your project directory
    3. Run the following command too create virtual environment:

    ```bash
    python -m venv .venv
    ``` 
    4. Activate the virtual environment:
    
        On Windows:
        ```bash
        .venv\Scripts\activate
        ```

        On macOS/Linux:
        ```bash
        source .venv/bin/activate
        ```
    
    5. In case you need to deactivate your virtual environment you run `deactivate` in your terminal

- Step 2: Install Poetry (if not already installed)

    Check if Pooetry is installed by running:
    ```bash
    poetry --version
    ```

    If not, install Poetry by following instruction in [this link] (https://python-poetry.org/docs/)


- Step 3: Install Project Dependencies:

    With Poetry installed, run the following command to install all dependencies:

    ```bash
    poetry install
    ```
    This will install all the dependencies listed in the `pyproject.toml` file


### Running the project

- Database schema

    To setup the database schema, run the following commands to apply migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

- Create a superuser (Optional)

    To create an admin user for accessing the Django admin panel, run:
    
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompt to setup a username, email and password for the superuser

- Run the Development Server

    To start the Django development server, run:
    ```bash
    python manage.py runserver
    ```

    The server will start at `http://127.0.0.1:8000/` by default. You can access your project by navigating to this URL in your browser

    The admin panel can be found in this url: `http://127.0.0.1:8000/admin`

    In the `postman` folder there is a collection which contains all endpoints with the sample data, you can use it by importing it in the postman app. There are also docs that explain in details the body and response examples for each endpoint.

    If you want to run tests you can run the tests with:

    ```bash
    python manage.py test
    ```