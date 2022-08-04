# OWASP ModSecurity Core Rule Set - Machine Learning Plugin

## Description

Plugin to use Machine Learning for reducing false positives and as an additional detection rule.

## Installation

For full and up to date instructions for the different available plugin
installation methods, refer to [How to Install a Plugin](https://coreruleset.org/docs/concepts/plugins/#how-to-install-a-plugin)
in the official CRS documentation.

## Working

This plugin works in two modes - 
1. False positive detection mode
2. General detection mode.

In mode 1, the requests which have an inbound anomaly score greater than the inbound anomaly threshold are scanned by the machine learning model. Only if the machine learning model give anomaly score greater than the machine learning anomaly threshold the request is blocked. Else, the request is passed and labeled as a false positive.

In mode 2, all requests are scanned by the machine learning model and the decision to pass or block the request is made solely by the model. If the machine learning anomaly score crosses the machine learning threshold, the request is blocked.

## Testing

To be updated

## License

Copyright (c) 2022 OWASP ModSecurity Core Rule Set project. All rights reserved.

The OWASP ModSecurity Core Rule Set and its official plugins are distributed
under Apache Software License (ASL) version 2. Please see the enclosed LICENSE
file for full details.