remotelog
=========

Remote logging api / web ui

This application receives logging information to the /log endpoint

Once running can be used with standard Python logging module:

	http_handler = logging.handlers.HTTPHandler(
        	execution_parameters.remoteLogURL,
        	'/log/<appslug>',
        	method='POST',
    	)

	logger.addHandler(http_handler)



