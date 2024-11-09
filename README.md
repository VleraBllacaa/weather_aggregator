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

### Adding a new Weather Station

To add a new weather station:

1. Create a new app with the weather station type name:

    ```bash
    python manage.py startapp <weather_type_name>
    ```

2. Define the model:

    - Inherit from `BaseStation` in your new model within the app's `models.py`
    - Customize fields and methods specific to this weather station type
    - Register the app in `settings.py`, add it in `INSTALLED_APPS`
    - Run migrations

3. Customization

    - Fields: Extend or override fields in the inherited model to add details specific to each weather station type
    - API Endpoints: Define custom views and serializers for the new weather station app to expose its data via the API


### Approach

My approach was to create a base model that each weather station model could inherit from, allowing for shared fields and structure across different station types. Using serializers, I managed the field mapping for each station, ensuring they align with desired unified format. The list endpoints, regardless of station type, return a standardized, paginated response and I introduced a temperature type parameter in the serializer to handle conversion (Celcius to Fahrenheit and vice versa). This way, data conversion occurrs within the serializer, keeping the data clean and consistent at the endpoint level.
The historical endpoint helps you to filter data within a timeframe based on a selected city.
