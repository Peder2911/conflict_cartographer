
# CC ADMIN

Admin dashboard for the conflict cartographer project.  Has the following
configuration settings (defaults are for dev environment):

|Environment value       |Hint                        |
|------------------------|----------------------------|
|API_URL                 |URL to a cc_api instance    |
|SCHEDULER_URL           |URL to a ccsched instance   |
|STATIC_URL              |Static resource host url    |
|STATIC_VERSION          |Path on static_url (version)|

Development does not require config, but uses mocked data from the APIs.  
To develop, run `docker-compose up`.

The backend API is set up so that it does _not_ expose any user data, only
summaries. 
