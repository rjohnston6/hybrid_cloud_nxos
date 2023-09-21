#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Python example script showing proper use of the Cisco Sample Code header.

Copyright (c) 2023 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""


from __future__ import absolute_import, division, print_function


__author__ = "Russell Johnston <rujohns2@cisco.com>"
__contributors__ = []
__copyright__ = "Copyright (c) 2023 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

import logging
from virl2_client import ClientLibrary

logging.basicConfig(
    level=logging.INFO,
    filename="initialize_cml.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%Y %H:%M:%S",
)

cml_url = ""
cml_user = ""
cml_password = ""
wait_counter_max = 20


def wait_for_cml():
    """
    Tries to connect to CML in the event of any HTTP Exceptions send back
    'unavailable' to be used with looping to wait for CML to be Ready
    """
    try:
        cml = ClientLibrary(
            url=cml_url, username=cml_user, password=cml_password, ssl_verify=False
        )
        return cml
    except:
        return "unavailable"


if __name__ == "__main__":
    wait_counter = 0

    while wait_counter <= wait_counter_max:
        cml = wait_for_cml()
        if cml == "unavailable":
            wait_counter += 1
        else:
            cml.is_system_ready(wait=True)
            logging.info("CML Server is Ready")
            break

    # Get list of all labs to start all labs
    all_lab_ids = cml.get_lab_list()

    for lab_id in all_lab_ids:
        lab = cml.join_existing_lab(lab_id)

        if lab.state() == "STOPPED":
            print(f"Lab: {lab.title}, is Starting please wait")
            lab.start()
            logging.info(f"{lab.title}, ID: {lab.id}, Started.")
        else:
            logging.info(f"Lab: {lab.title}, ID: {lab.id}, is Running.")

    print("All CML Labs are started!")
    logging.info("All CML Labs are Started.")
