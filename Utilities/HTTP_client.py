#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import time
import requests


url = "https://stupefied-poitras.185-23-116-208.plesk.page/api/"
headers = {"Content-Type": "application/json"}


class HTTPClient(object):
    def __init__(self, node_id, display_name) -> None:
        # Get the list of nodes currently on the website.
        self.node_id = node_id
        self.display_name = display_name
                
        if not self.node_exists(node_id):
            self.add_node(node_id, display_name)
        
    def node_exists(self, node_id=None):
        if node_id is None:
            node_id = self.node_id
        
        query = 'nodes'
        response = None
        while response is None:
            try:
                response = requests.request("GET", url + query, headers=headers, timeout=2.0)
            except requests.exceptions.Timeout:
                print("Timeout while waiting to GET current list of nodes. Trying again.")
                time.sleep(0.5)
                
        parsed = json.loads(response.text)

        for node in parsed['data']:
            if node['handle'] == node_id:
                return True
        
        return False
        
    def add_node(self, node_id, display_name):
        if node_id is None:
            node_id = self.node_id
        if display_name is None:
            display_name = self.display_name
        
        query = 'nodes'
        payload = {
            'handle': node_id,
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
    
    def add_data_field(self, name, handle, node_id=None):
        if node_id is None:
            node_id = self.node_id
            
        query = 'data-field'
        payload = {
            "name": name,
            "handle": handle
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
    
    def add_data(self, node_id=None):
        if node_id is None:
            node_id = self.node_id
        
        query = 'sensordata'
        payload = {
            "node_id": node_id,
            "date": "2022-10-13 10:53:00",
            "data": {
                "date": "2022-10-13 10:51:00",
                "temp_pcb": "0",
                "mag_x": "0",
                "mag_y": "0",
                "mag_z": "0",
                "temp_external": "30",
                "light_external": "0",
                "humidity_external": "0",
                "differential_potential_ch1": "0",
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
        
def main():
    client = HTTPClient('marko1', 'Marko 1')
#    client.add_data_field("Testing sensor", "test_sensor", "test_node_0")
    client.add_data()

if __name__ == '__main__':
    main()