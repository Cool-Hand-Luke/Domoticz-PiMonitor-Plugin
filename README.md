# PiMonitor
Python plugin to monitor temperature, memory usage, etc. from a Raspberry Pi.

Forked from https://github.com/Xorfor/Domoticz-PiMonitor-Plugin

## Prerequisites
Only works on Raspberry Pi

## Parameters
None

## Devices
The following parameters are displayed:

| Name            | Description
| :---            | :---
| SoC temperature | Shows the current SoC temperature
| CPU memory      | Size of allocated memory for CPU
| GPU memory      | Size of allocated memory for GPU (specified with eg. raspi-config)
| Memory usage    | Percentage of CPU memory in use
| CPU usage       | Percentage of CPU usage
| CPU speed       | Current CPU speed
| Up time         | Up time of the Pi, in sec, minutes, hours or days
| Connections     | Number of active network connections
| Core voltage    | Core voltage
| SDRAM C voltage | SDRAM C voltage
| SDRAM I voltage | SDRAM I voltage
| SDRAM P voltage | SDRAM P voltage
| Domoticz memory | Amount of memory used by Domoticz
