![pyMetric](https://raw.githubusercontent.com/laubed/pyMetric/master/images/header_scaled.png)


pyMetric is a LAN Server/Service Monitoring solution optimized for ease of use and reliability. It is based on 3 components:

* The RESTful server backend written with flask in python (WSGI compliant / runs under apache2,nginx,...)
* The client reporting scripts. Used to report data to the backend server.
* The web frontend. Displays data as a dashboard to the user.


### pyMetric/pyMetricServer ###


### pyMetric/pyMetricClients ###
There are several client API scripts available to report data to the backend server. Use them on your clients.

#### log_messages.py ####
> The log_messages.py script is a CLI for the log_messages API endpoint of the RESTful server backend. Use it in all your
> cronjobs / regular scripts to notify the backend.
> Usage:
>
> `log_messages.py <Origin> <Message> <LOG|NOTICE|WARNING|ERROR> <API endpoint>`
>
> * The first parameter describes the origin of the message (usually the IP or hostname of the server) e.g. 10.0.0.5
> * The second parameter is the message itself that gets logged e.g. "update-database cron failed!"
> * The third parameter describes the message type e.g. ERROR
> * The last parameter ist the API endpoint e.g. monitoring.server.local:5000


#### report_cpu.py ####
> The report_cpu.py script reports the cpu usage to the metric API endpoint of the RESTful server backend. Use as often as you like to know cpu usage on your hardware
> Usage:
>
> `report_cpu.py <Origin> <API endpoint>`
>
> * The first parameter describes the origin of the message (usually the IP or hostname of the server) e.g. 10.0.0.5
> * The last parameter ist the API endpoint e.g. monitoring.server.local:5000


#### run_cron.py ####
> The run_log.py script runs the server side cron task via the RESTful API for deleting old entries in database etc.
> Usage:
>
> `run_cron.py <API endpoint>`
>
> * The first parameter ist the API endpoint e.g. monitoring.server.local:5000


### pyMetric/pyMetricWeb ###


### Prerequisites ###
* PostgreSQL server
* Python 2.7 with flask, jinja2, markupsafe, werkzeug, itsdangerous, psycopg2, psutil
* optional: web server (apache2,nginx,..) with wsgi module


### Usage ###
1. Make sure every prerequisites are fulfilled
2. Rename config.py.dist into config.py
3. Edit the config.py to match your auth credentials for the PostgreSQL database
4. To run the server either setup your webserver to use the pyMetricServer/pyMetric.py as WSGI application or just run pyMetricServer/pyMetric.py to use the standalone server
5. Use the client API scripts to insert data

![pyMetric Info Graphic](https://raw.githubusercontent.com/laubed/pyMetric/master/images/explanation.png)



### Contributors ###
* Sören Uhrbach <souhrbach@gmail.com> Frontend Developer
* Daniel Laube <bitbucket@dlaube.de> Backend Developer


### Credit ###
* Icons used in logo and graphics: [Octicons by Github](https://octicons.github.com/)
* Font used in logo and graphics: [Roboto by Google](https://www.google.com/fonts/specimen/Roboto)
* JavaScript/CSS Libraries:
    * [Bootstrap by Twitter](https://github.com/twbs/bootstrap)
    * [Chart.js](https://github.com/chartjs/Chart.js)
    * [jQuery](https://github.com/jquery/jquery)
    * [Knockout.js by Steven Sanderson](http://knockoutjs.com/)
    * [Moment.js by Tim Wood, Iskren Chernev](http://momentjs.com/)