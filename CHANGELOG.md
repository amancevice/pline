# pline Changelog

0.4.3
* Added support for ondemand scheduleType
* Made it so setting a pipeline object property to None causes it to not appear in the pipeline 
  definition.

0.4.2
* Travis fixes

0.4.1
* Better setup.py

0.4.0
* boto3

0.3.0
* Moved imports into their modules because the main module was getting crowded

0.2.2
* Fixed regression in pipeline.add() 

0.2.1
* Fixed bug in Pipeline.validate()

0.2.0
* Added parameter support
* Re-tooled the way things work under the hood a bit
* Work-around for sending payloads with params

0.1.5
* Added version requirement to setup.py for boto

0.1.4
* Fixed bug in list assembly

0.1.3
* Made fields a property

0.1.1
* Fixed issue where field values could be duplicated

0.1.0
* Initial stable release

0.0.1
* Initial release
