# Recommender System

A Recommender System to recommend cancer hospitals to the patients using Machine Learning and Blockchain. 

## Installation Instructions

1. Clone the project.
    ```shell
    $ git clone https://github.com/shreyasrami/recommender.git
    ```

2. Create a new virtual environment activate it.
    ```shell
    $ python3 -m venv env
    $ source env/bin/activate
    ```
3. Install dependencies from requirements.txt:
    ```shell
    (env)$ pip install -r requirements.txt
    ```
     
4. Migrate the database.
    ```shell
    (env)$ python manage.py migrate
    ```

5. Run the local server via:
    ```shell
    (env)$ python manage.py runserver
    ```

### Done!

### Detailed API Documentation can be viewed at <a href="http://localhost:8000/" target="_blank">http://localhost:8000/</a>.