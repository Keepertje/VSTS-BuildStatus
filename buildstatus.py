#!/usr/bin/env python
import pprint
import time
import signal

from vsts.vss_connection import VssConnection
from msrest.authentication import BasicAuthentication

import config as cfg
import lightcontroller as light

#global variables
keepAlive = True
currentStatus = 'none'
currentResult = 'none'


"""set up a connection to VSTS.
Relies on the parameters set in config.py
"""
credentials = BasicAuthentication('', cfg.vstspat)
connection = VssConnection(base_url=cfg.vstsurl, creds=credentials)
client =  connection.get_client('vsts.build.v4_0.build_client.BuildClient')

""" Determines what LED to switch on based on the status and result parameters provided
Actual switching of LED's is delegated to the lightcontroller.
"""
def setStatusLights(status, result):
    if status == 'completed':
        if result == 'succeeded':
            pprint.pprint("Green light lit!")
            light.setGreenOn()
        elif result == 'failed' or result == 'canceled':
            pprint.pprint("Red light lit!")
            light.setRedOn()
    elif status == 'inProgress':
        pprint.pprint("Yellow light blinking!")
        light.setYellowBlinking(3)
    return


""" Retrieves the latest build status from VSTS
This method will call setStatusLight if the retrieved status differed from the status currently shown.
"""
def checkBuildStatus():
    definition = client.get_definition(cfg.vstsbuilddefinition, cfg.vstsprojectname, include_latest_builds = True)
    build = definition.latest_build

    global currentStatus
    global currentResult
    if currentStatus != build.status or currentResult != build.result:
        currentStatus = build.status
        currentResult = build.result
        setStatusLights(currentStatus, currentResult)
    return


""" Main loop

Will call checkBuildStatus every second to see if any changes in build status have occurred.
It will terminate itself if a keyboardInterrupt is registered.
"""
def main():
    global keepAlive
    while keepAlive:
        try:
            time.sleep(1)
            checkBuildStatus()
	except KeyboardInterrupt:
            print("[NOTICE] program terminated!")
            light.setAllOff()
            keepAlive = False

main()
