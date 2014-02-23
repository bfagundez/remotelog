remotelog
=========

Remote logging api / web ui

This application receives logging information to the /log endpoint to be used with standard Python logging module:

	http_handler = logging.handlers.HTTPHandler(
        	execution_parameters.remoteLogURL,
        	'/log/<appslug>',
        	method='POST',
    	)

	logger.addHandler(http_handler)

Logs are stored in a local sqlite database or a database provided as a environmental variable:

	$ export REMOTELOGDB=mysql://user:pwd@host/db

The logs can be viewed at
	http://localhost:9002/view_log/<appslug>

