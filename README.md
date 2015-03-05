# PIVI #

This is the software that runs on the raspberry pi on each of the PIVI sensors along with the provisioning software to deploy the PIVI stack on a Raspberry Pi

All the code in this repository is licensed Creative Commons 

![Attribution-NonCommercial-ShareAlike 4.0 International ](https://bitbucket.org/repo/xj5nj8/images/1002571225-88x31.png)

**Copyright (C) 2014, 2015 LESS Induestries S.A.**

**Author: Lucas Chiesa <lucas@lessinduestries.com>**


## Contents ##

The different directories contain:

* **configs**: system configuration files that get installed on the rpi when deploying the software
* **setup**: scripts for creating the raspbian installation using python fabric.
* **pyvi**: python module which contains all the core logic (reading the measurements from the sensors, and sending them to the cloud). It also contains the main program that runs on the rpi during sensor operation.
* **webserver**: super simple debugging webserver, you can see the system logs and send them via email to a designated address.