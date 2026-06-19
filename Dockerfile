FROM postgres:16

# for simplicity purposes database credentials are hardcoded (they should be in a .env file)
ENV POSTGRES_DB=index_db
ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=the_password
