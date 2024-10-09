#!/usr/bin/env python3

import random
import time
import statistics
from collections import defaultdict

# Simulated sensor network data collection and analysis

class SensorNetwork:
    def __init__(self, num_sensors):
        self.num_sensors = num_sensors
        self.sensor_data = defaultdict(list)

    def collect_data(self):
        """
        Simulate collecting data from each sensor in the network.
        """
        for i in range(1, self.num_sensors + 1):
            sensor_id = f'sensor_{i}'
            self.sensor_data[sensor_id].append(self.read_sensor(sensor_id))

    @staticmethod
    def read_sensor(sensor_id):
        """
        Simulate reading a value from a sensor. This is a stand-in for actual
        sensor data collection which might include reading from a hardware device.
        """
        # For this simulation, just return a random value
        return random.uniform(0, 100)

    def analyze_data(self):
        """
        Analyze collected sensor data and print summary statistics.
        """
        for sensor_id, data in self.sensor_data.items():
            if data:
                mean_val = statistics.mean(data)
                min_val = min(data)
                max_val = max(data)
                median_val = statistics.median(data)
                print(f'[{sensor_id}] Mean: {mean_val:.2f}, Min: {min_val:.2f}, Max: {max_val:.2f}, Median: {median_val:.2f}')
            else:
                print(f'[{sensor_id}] No data available for analysis.')

def main():
    # Initialize sensor network with 5 sensors
    sensor_network = SensorNetwork(num_sensors=5)

    # Collect data over 5 intervals
    for _ in range(5):
        sensor_network.collect_data()
        time.sleep(1)  # Wait for 1 second before collecting next data point

    # Analyze collected sensor data
    sensor_network.analyze_data()

if __name__ == "__main__":
    main()
