

docker kill mock-db
docker run -d --rm --name mock-db\
   -e POSTGRES_USER=fakedata -e POSTGRES_PASSWORD=fakedata -e POSTGRES_DB=fakedata\
   -p 2345:5432 postgres:11-bullseye

sleep 2 

./manage.py migrate && ./manage.py runscript mock_database
