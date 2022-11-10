#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import time
import requests


url = "https://stupefied-poitras.185-23-116-208.plesk.page/api/"
headers = {"Content-Type": "application/json"}


class HTTPClient(object):
    def __init__(self, node_handle, display_name) -> None:
        # Get the list of nodes currently on the website.
        self.node_handle = node_handle
        self.display_name = display_name
                
        if not self.node_exists(node_handle):
            self.add_node(node_handle, display_name)
        

    def node_exists(self, node_handle=None):
        """
        Checks if a given node already exists in the website/database

        Args:
            node_handle (str): handle of node to check, if None checks self

        Returns:
            True if node exists, False otherwise
        """
        if node_handle is None:
            node_handle = self.node_handle

        query = 'nodes'
        response = None
        while response is None:
            try:
                response = requests.request("GET", url + query, headers=headers, timeout=2.0)
            except requests.exceptions.Timeout:
                print("Timeout while waiting to GET current list of nodes. Trying again.")
                time.sleep(0.5)

        parsed = json.loads(response.text)
        return any(node['handle'] == node_handle for node in parsed['data'])
        

    def add_node(self, node_handle, display_name): #node_handle has to be a string with letters!!!
        """
        Adds a new node to the website/database

        Args:
            node_handle (str): Internal identifier of the node. Important: The string has to contain letters
                                to avoid an error on the website. Don't only use numbers, even if they are 
                                formatted as string it will still lead to problems
            display_name (str): Name of the node that is shown on the website

        Returns:
            True if a successful response is received, False otherwise
        """
        if node_handle is None:
            node_handle = self.node_handle
        if display_name is None:
            display_name = self.display_name
        
        query = 'nodes'
        payload = {
            'handle': node_handle,
            'name': display_name
        }
        response = None
        while response is None:
            try:
                response = requests.request("POST", url + query, json=payload, headers=headers, timeout=2.0)
            except requests.exceptions.Timeout:
                print("Timeout while waiting to POST the new node. Trying again.")
        
        if not response.ok:
            print(f"ERROR: Adding node. Status code {response.status_code}")
            return False
            
        return True

    
    def add_data_field(self, field_name, field_handle, unit, node_handle=None):
        """
        Does nothing? TODO

        Args:
            field_name (str): Name of the data field that is shown on the website
            field_handle (str): Internal identifier of the data field
            unit (str): Unit of the datatype measured. To display on the website
            node_handle (str): Is this really neaded? TODO

        Returns:
            True if a successful response is received, False otherwise
        """
        if node_handle is None:
            node_handle = self.node_handle
            
        query = 'data-field'
        payload = {
            "name": field_name,
            "handle": field_handle
        }
        response = None
        while response is None:
            try:
                response = requests.request("POST", url + query, json=payload, headers=headers, timeout=2.0)
            except requests.exceptions.Timeout:
                print("Timeout while waiting to POST the new data field. Trying again.")
        
        if not response.ok:
            print(f"ERROR: Adding data field. Status code {response.status_code}")
            return False
        
        return True
    

    def add_data(self, node_handle=None):
        """
        Adds a single measurement set to the database
        Args:
            node_handle (str): Node that collected the dataset, if None, it assumes itself as collector

        Returns:
            True if a successful response is received, False otherwise
        """
        if node_handle is None:
            node_handle = self.node_handle
        
        query = 'sensordata'
        payload = {
            "node_id": node_handle,
            "date": "2022-10-13 10:53:40",
            "data": {
                "temp_pcb": "0",
                "mag_x": "0",
                "mag_y": "0",
                "mag_z": "0",
                "temp_external": "50",
                "light_external": "0",
                "humidity_external": "4",
                "differential_potential_ch1": "10",
                "differential_potential_ch2": "0",
                "rf_power_emission": "0",
                "transpiration": "0",
                "air_pressure": "0",
                "soil_moisture": "0",
                "soil_temperature": "0",
                "mu_mm": "0",
                "mu_id": "0",
                "sender_hostname": "rpi0",
                "ozone": "0",
            }
        }
        response = None
        while response is None:
            try:
                response = requests.request("POST", url + query, json=payload, headers=headers, timeout=2.0)
            except requests.exceptions.Timeout:
                print("Timeout while waiting to POST the new data field. Trying again.")
        
        if not response.ok:
            print(f"ERROR: Adding data. Status code {response.status_code}")
            return False
        
        return True


    def get_data(self, node_handle=None):
        """
        Returns all data entries from a specified node

        Args:
            node_handle ([str]): List of node_handles whose data shall be extracted

        Returns:
            dictionary with all data entries from all given node_handles
            Format:
            Dictionary with node_handles as keys
                List with all data entries per node_handle
                    Dictionary with metadata keys and one 'data' key
                        'data' contains a dictionary with the actual measurements 
        """
        if node_handle is None:
            node_handle = [self.node_handle]

        query = 'sensordata-multiple'
        payload = {
            "node_ids": node_handle
        }

        response = None
        while response is None:
            try:
                response = requests.request("POST", url + query, json=payload, headers=headers, timeout=2.0)
            except requests.exceptions.Timeout:
                print("Timeout while waiting to retrieve data. Trying again.")

        if not response.ok:
            print(f"ERROR: Retrieving data. Status code {response.status_code}")
            return False

        parsed = json.loads(response.text)
        return parsed['data']

        
def main():
    client = HTTPClient('test_ID', 'test_display_name')

if __name__ == '__main__':
    main()