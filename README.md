# ABC Tourism Crawler

Web crawler that applies web scraping techniques to get informations from the TripAdvisor website to about restaurants and touristic spots in the Grande ABC region. Also, it is being used the Google Places API to get detailed informations (like address, opening hours, geolocation, phone and many others properties) about these places.

## ⚒️ Technologies
- [Python](https://www.python.org/)
- [Selenium](https://www.selenium.dev/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Google Places API](https://developers.google.com/maps/documentation/places/web-service/overview)

## :computer: Running locally
1. Install the project dependencies
```
$ pip install -r requirements.txt
```

2. Create a `.env` file based on the `.env.example` file
```
$ cp .env.example .env
```

3. Complete the `.env`file with the requested informations (in this project, we are using SQL Server as our database, but, if you want to use SQLite, don't add the DATABASE_URL in the `.env`file)

4. Create the tables and add basic data to your database
```
$ python database/migrations.py
```

5. Run the web crawler
```
$ python main.py
```

6. The application will start running in the background (headless mode).

## :whale: Running with Docker
1. Run the following commands in the cmd
```
$ docker build -t <CONTAINER_NAME>:latest .
$ docker run <CONTAINER_NAME>:latest
```

2. The application will start running when the container starts.
