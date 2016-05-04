# RatseDashboard #

RatseDashboard is a local Server/Service Monitoring solution optimized for ease of use and reliability. It is based on 3 components:

* The RESTful server backend written with flask in python (WSGI compliant / runs under apache2,nginx,...)
* The client reporting scripts. Used to report data to the backend server.
* The web frontend. Displays data as a dashboard to the user.

### RatseDashboard/server ###


### RatseDashboard/client ###
#### log_messages.py ####
The log_messages.py script is a CLI for the log_messages API endpoint of the RESTful server backend. Use it in all your
cronjobs / regular scripts to notify the backend.
Usage:

`log_messages.py <Origin> <Message> <LOG|NOTICE|WARNING|ERROR> <API endpoint>`

* The first parameter describes the origin of the message (usually the IP or hostname of the server) e.g. 10.0.0.5
* The second parameter is the message itself that gets logged e.g. "update-database cron failed!"
* The third parameter describes the message type e.g. ERROR
* The last parameter ist the API endpoint e.g. monitoring.server.local:5000

### RatseDashboard/web ###


### Prerequisites ###
* PostgreSQL server
* Python 2.7 with flask, jinja2, markupsafe, werkzeug, itsdangerous, psycopg2
* optional: web server (apache2,nginx,..) with wsgi module

### Contributors ###

* Sören Uhrbach <souhrbach@gmail.com>
* Daniel Laube <bitbucket@dlaube.de>