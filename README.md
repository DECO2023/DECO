# DHCAC

This repository is the Tensorflow implementation of the DHCAC reported in the paper:
Cooperative Order Dispatching for On-demand Delivery with Real-time Encounter Detection based on BLE Beacon Data.


# Installation
Requirements: Python >= 3.7, Anaconda3
1. Update conda:
conda update -n base -c defaults conda
2. Install basic dependencies to simulator environment.
3. Install Tensorflow = 1.1.4.

# Quick Start
Python train/train.py

Python train/test.py

# Documentation Introduction
1. DHCAC/simulator contains codes of the emulator. DHCAC/route_plan contains couriers' route plan methods in the emulator.
2. Directory DHCAC/algorithm contains main codes of our main model DHCAC.
3. Directory DHCAC/baseline contains main codes of our main model DHCAC.
4. Directory DHCAC/dataProcessing contains simulated encounter data, processing codes about our data similar to the public data published in the link https://tianchi.aliyun.com /dataset/dataDetail?dataId=76359.
5. Directory DHCAC/resultProcessing contains processing codes about our result visualization.
