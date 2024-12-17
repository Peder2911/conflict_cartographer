
# Conflict Cartographer

Conflict Cartographer is a web application designed for the [Conflict Cartographer](https://www.prio.org/projects/1900) research project, which aimed to assess the accuracy of human-expert predictions compared to statistical models.

Funding for Conflict Cartographer was provided by the Norwegian MFA, via the [Conflict Trends](https://www.prio.org/publications/13513) project.

To run Conflict Cartographer, simply do `docker compose up`. Administrative commands can be run from the Django container with `./manage.py`. To populate the database with fake data so that you can test adding your own predictions, run `./manage.py runscript scripts.mock_data`.
