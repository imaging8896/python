# python utils
## module
* code/adb : adb as python utils
* code/aliasUtils : 
  - File name is case-insensitive in sdcard. We call each different case file name as 'alias' of file. 
  - Test tool is for testing 'alias'. This tool can 'ls' all alias and concurrent file modification along with 'ls' alias.
* code/androidUtils : depends on adb. am(activity manager), file system operation, system information
* code/docker : docker as python utils
* code/dockerBuildUtils : docker build(make or gradle) as python utils
* code/fileGenerator : it's a python tool for test files generator in device linux using c
* code/hcfsUtils : test device operation as python utils
* code/tedUtils : coding helper function for python 
* code/LogcatUtils.py : logcat parser. Instrument logcat utils
* code/FuncSpec.py : verify function input/ouput by function signature

## unit test
* use doc test
* unit test python files are any file name with 'startXXXTest.py' in the root directory
