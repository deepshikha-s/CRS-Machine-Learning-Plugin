# OWASP ModSecurity Core Rule Set - Machine Learning Plugin

## Description

Plugin to use Machine Learning for reducing false positives and as an additional detection rule.

## Installation

For full and up to date instructions for the different available plugin
installation methods, refer to [How to Install a Plugin](https://coreruleset.org/docs/concepts/plugins/#how-to-install-a-plugin)
in the official CRS documentation.

## Setup:

### Pre-Requisites:
You will need to install the following libraries-

1.  Lua: 
- lua-socket

2. Python: 
- flask
- request 
- pickle 
- sklearn
- psutil
- os
- random
- helper
- werkzeug

1. Clone the repository and copy all the files in the plugin folder of the repository into the plugins folder of your local Core Rule Set installation.
2. Copy the ml_model_server folder into /var/www/html
3. Add your machine learning model in ml_model_server/saved_models and follow the directives in placeholder.py to include the model in the server.
4. Start the flask server. To run the flask server, 
   1. Create a file runflash.sh in the home directory.
   2. Add the following lines in the file:
      '''
       export FLASK_APP=/var/www/html/ml-model-server/placeholder.py
       <path of your local flask installation> run
      '''
   3. Start your virtual environment.
   4. Run the command ''' ./runflash.sh '''
5. The plugin is now ready to use.

## Working

This plugin works in two modes - 
1. False positive detection mode
2. General detection mode.

In mode 1, the requests which have an inbound anomaly score greater than the inbound anomaly threshold are scanned by the machine learning model. Only if the machine learning model give anomaly score greater than the machine learning anomaly threshold the request is blocked. Else, the request is passed and labeled as a false positive.

In mode 2, all requests are scanned by the machine learning model and the decision to pass or block the request is made solely by the model. If the machine learning anomaly score crosses the machine learning threshold, the request is blocked.

You can change the mode by going to machine-learning-config.conf and modifying the value of '''machine-learning-plugin_mode'''. If the value of this variable is 1 the plugin works in false positive detection mode and if the value of the variable is 2, the plugin works in general detection mode.
This plugin has been developed without an actual machine learning model in place. Hence, the score has been stubbed to generate a random score. A user can choose to run the plugin with any machine learning model of his/her choice. To do so, directives have been provided to add the machine learning model file.

## Testing

To be updated

## License

Copyright (c) 2022 OWASP ModSecurity Core Rule Set project. All rights reserved.

The OWASP ModSecurity Core Rule Set and its official plugins are distributed
under Apache Software License (ASL) version 2. Please see the enclosed LICENSE
file for full details.
