## Important: this project requires python 3.10+ and Docker to run.

1) Please execute pip install -r requirements.txt before atempting to run any file

2) To instantiate the PostgreSQL database execute:

- docker buildx build -t "postgre_db" "."
- docker run -p 5432:5432 "postgre_db"

3) Run database migrations to create tables:

- python manage.py migrate

4) To run the Django server execute: 

- python manage.py runserver 8000 
