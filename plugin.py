#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PiMonitor Plugin
#
# Author: Xorfor
"""
<plugin key="xfr-pimonitor" name="PiMonitor" author="Xorfor" version="2.1.0" wikilink="https://github.com/Xorfor/Domoticz-PiMonitor-Plugin">
    <params>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal" default="true"/>
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
import subprocess
import os

class BasePlugin:

    __HEARTBEATS2MIN = 6
    __MINUTES = 1

    # Device units
    __UNIT_SoCTEMP = 1
    __UNIT_RAMUSE = 2
    __UNIT_CPUUSE = 3
    __UNIT_CPUSPEED = 4
    __UNIT_UPTIME = 5
    __UNIT_CPUMEMORY = 6
    __UNIT_GPUMEMORY = 7
    __UNIT_CONNECTIONS = 8
    __UNIT_COREVOLTAGE = 9
    __UNIT_SDRAMCVOLTAGE = 10
    __UNIT_SDRAMIVOLTAGE = 11
    __UNIT_SDRAMPVOLTAGE = 12
    __UNIT_DOMOTICZMEMORY = 13

    __UNITS = [
        # Unit, Name, Type, Subtype, Options, Used
        [__UNIT_SoCTEMP, "SoC temperature", 243, 31, {"Custom": "0;°C"}, 1],
        [__UNIT_RAMUSE, "Memory usage", 243, 31, {"Custom": "0;%"}, 1],
        [__UNIT_CPUUSE, "CPU usage", 243, 31, {"Custom": "0;%"}, 1],
        [__UNIT_CPUSPEED, "CPU speed", 243, 31, {"Custom": "0;Mhz"}, 1],
        [__UNIT_UPTIME, "Up time", 243, 31, {"Custom": "0;sec"}, 1],
        [__UNIT_CPUMEMORY, "CPU memory", 243, 31, {"Custom": "0;MB"}, 1],
        [__UNIT_GPUMEMORY, "GPU memory", 243, 31, {"Custom": "0;MB"}, 1],
        [__UNIT_CONNECTIONS, "Connections", 243, 31, {}, 1],
        [__UNIT_COREVOLTAGE, "Core voltage", 243, 31, {"Custom": "0;V"}, 1],
        [__UNIT_SDRAMCVOLTAGE, "SDRAM C voltage",
            243, 31, {"Custom": "0;V"}, 1],
        [__UNIT_SDRAMIVOLTAGE, "SDRAM I voltage",
            243, 31, {"Custom": "0;V"}, 1],
        [__UNIT_SDRAMPVOLTAGE, "SDRAM P voltage",
            243, 31, {"Custom": "0;V"}, 1],
        [__UNIT_DOMOTICZMEMORY, "Domoticz memory",
            243, 31, {"Custom": "0;KB"}, 1],
    ]

    def __init__(self):
        self.__runAgain = 0
        return

    def onStart(self):
        Domoticz.Debug("onStart called")
        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(1)
        else:
            Domoticz.Debugging(0)
        # Validate parameters
        # Images
        # Check if images are in database
        if "xfrpimonitor" not in Images:
            Domoticz.Image("xfrpimonitor.zip").Create()
        image = Images["xfrpimonitor"].ID
        Domoticz.Debug("Image created. ID: "+str(image))
        # Create devices
        if len(Devices) == 0:
            for unit in self.__UNITS:
                Domoticz.Device(Unit=unit[0],
                                Name=unit[1],
                                Type=unit[2],
                                Subtype=unit[3],
                                Options=unit[4],
                                Used=unit[5],
                                Image=image).Create()
        # Log config
        DumpAllToLog()

    def onStop(self):
        Domoticz.Debug("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Debug("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Debug("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Debug(
            "onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Debug("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(
            Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Debug("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Debug("onHeartbeat called")
        self.__runAgain -= 1
        if self.__runAgain <= 0:
            self.__runAgain = self.__HEARTBEATS2MIN * self.__MINUTES
            # Execute your command
            #
            fnumber = getSoCtemperature()
            Domoticz.Debug("GPU temp ..........: {} °C".format(fnumber))
            UpdateDevice(self.__UNIT_SoCTEMP, int(fnumber),
                         str(fnumber), AlwaysUpdate=True)
            #
            fnumber = getGPUmemory()
            Domoticz.Debug("GPU memory ........: {} Mb".format(fnumber))
            UpdateDevice(self.__UNIT_GPUMEMORY, int(fnumber),
                         str(fnumber), AlwaysUpdate=True)
            #
            fnumber = getCPUmemory()
            Domoticz.Debug("CPU memory ........: {} Mb".format(fnumber))
            UpdateDevice(self.__UNIT_CPUMEMORY, int(fnumber),
                         str(fnumber), AlwaysUpdate=True)
            #
            fnumber = getCPUuse()
            Domoticz.Debug("CPU use ...........: {} %".format(fnumber))
            UpdateDevice(self.__UNIT_CPUUSE, int(fnumber),
                         str(fnumber), AlwaysUpdate=True)
            #
            fnumber = getRAMinfo()
            Domoticz.Debug("RAM use ...........: {} %".format(fnumber))
            UpdateDevice(self.__UNIT_RAMUSE, int(fnumber),
                         str(fnumber), AlwaysUpdate=True)
            #
            fnumber = getCPUcurrentSpeed()
            Domoticz.Debug("CPU speed .........: {} Mhz".format(fnumber))
            UpdateDevice(self.__UNIT_CPUSPEED, int(fnumber),
                         str(fnumber), AlwaysUpdate=True)
            #
            fnumber = round(getVoltage("core"), 2)
            Domoticz.Debug("Core voltage ......: {} V".format(fnumber))
            UpdateDevice(self.__UNIT_COREVOLTAGE, int(fnumber),
                         str(fnumber), AlwaysUpdate=True)
            #
            fnumber = round(getVoltage("sdram_c"), 3)
            Domoticz.Debug("SDRAM C ...........: {} V".format(fnumber))
            UpdateDevice(self.__UNIT_SDRAMCVOLTAGE, int(fnumber),
                         str(fnumber), AlwaysUpdate=True)
            #
            fnumber = round(getVoltage("sdram_i"), 3)
            Domoticz.Debug("SDRAM I ...........: {} V".format(fnumber))
            UpdateDevice(self.__UNIT_SDRAMIVOLTAGE, int(fnumber),
                         str(fnumber), AlwaysUpdate=True)
            #
            fnumber = round(getVoltage("sdram_p"), 3)
            Domoticz.Debug("SDRAM P ...........: {} V".format(fnumber))
            UpdateDevice(self.__UNIT_SDRAMPVOLTAGE, int(fnumber),
                         str(fnumber), AlwaysUpdate=True)
            #
            res = getCPUuptime()  # in sec
            Domoticz.Debug("Up time ...........: {} sec".format(res))
            # if res < 60:
            fnumber = round(res, 2)
            options = {"Custom": "0;s"}
            # UpdateDeviceOptions(self.__UNIT_UPTIME, {"Custom": "0;s"})
            if res >= 60:
                fnumber = round(res / (60), 2)
                options = {"Custom": "0;min"}
                # UpdateDeviceOptions(self.__UNIT_UPTIME, {"Custom": "0;min"})
            if res >= 60 * 60:
                fnumber = round(res / (60 * 60), 2)
                options = {"Custom": "0;h"}
                # UpdateDeviceOptions(self.__UNIT_UPTIME, {"Custom": "0;h"})
            if res >= 60 * 60 * 24:
                fnumber = round(res / (60 * 60 * 24), 2)
                options = {"Custom": "0;d"}
                # UpdateDeviceOptions(self.__UNIT_UPTIME, {"Custom": "0;d"})
            UpdateDeviceOptions(self.__UNIT_UPTIME, options)
            UpdateDevice(self.__UNIT_UPTIME, int(fnumber),
                         str(fnumber), AlwaysUpdate=True)
            #
            inumber = getNetworkConnections("ESTABLISHED")
            #inumber = getNetworkConnections("CLOSE_WAIT")
            Domoticz.Debug("Connections .......: {}".format(inumber))
            UpdateDevice(self.__UNIT_CONNECTIONS, inumber,
                         str(inumber), AlwaysUpdate=True)
            #
            fnumber = getDomoticzMemory()
            Domoticz.Debug("Domoticz memory ...: {} KB".format(fnumber))
            UpdateDevice(self.__UNIT_DOMOTICZMEMORY, int(fnumber),
                         str(fnumber), AlwaysUpdate=True)
            #
        else:
            Domoticz.Debug(
                "onHeartbeat called, run again in {} heartbeats.".format(self.__runAgain))

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status,
                           Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

################################################################################
# Generic helper functions
################################################################################

def DumpDevicesToLog():
    # Show devices
    Domoticz.Debug("Device count.........: {}".format(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device...............: {} - {}".format(x, Devices[x]))
        Domoticz.Debug("Device Idx...........: {}".format(Devices[x].ID))
        Domoticz.Debug(
            "Device Type..........: {} / {}".format(Devices[x].Type, Devices[x].SubType))
        Domoticz.Debug("Device Name..........: '{}'".format(Devices[x].Name))
        Domoticz.Debug("Device nValue........: {}".format(Devices[x].nValue))
        Domoticz.Debug("Device sValue........: '{}'".format(Devices[x].sValue))
        Domoticz.Debug(
            "Device Options.......: '{}'".format(Devices[x].Options))
        Domoticz.Debug("Device Used..........: {}".format(Devices[x].Used))
        Domoticz.Debug(
            "Device ID............: '{}'".format(Devices[x].DeviceID))
        Domoticz.Debug("Device LastLevel.....: {}".format(
            Devices[x].LastLevel))
        Domoticz.Debug("Device Image.........: {}".format(Devices[x].Image))

def DumpImagesToLog():
    # Show images
    Domoticz.Debug("Image count..........: {}".format((len(Images))))
    for x in Images:
        Domoticz.Debug("Image '{}'...: '{}'".format(x, Images[x]))

def DumpParametersToLog():
    # Show parameters
    Domoticz.Debug("Parameters count.....: {}".format(len(Parameters)))
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug("Parameter '{}'...: '{}'".format(x, Parameters[x]))

def DumpSettingsToLog():
    # Show settings
    Domoticz.Debug("Settings count.......: {}".format(len(Settings)))
    for x in Settings:
        Domoticz.Debug("Setting '{}'...: '{}'".format(x, Settings[x]))

def DumpAllToLog():
    DumpDevicesToLog()
    DumpImagesToLog()
    DumpParametersToLog()
    DumpSettingsToLog()

def DumpHTTPResponseToLog(httpDict):
    if isinstance(httpDict, dict):
        Domoticz.Debug("HTTP Details (" + str(len(httpDict)) + "):")
        for x in httpDict:
            if isinstance(httpDict[x], dict):
                Domoticz.Debug(
                    "....'" + x + " (" + str(len(httpDict[x])) + "):")
                for y in httpDict[x]:
                    Domoticz.Debug("........'" + y + "':'" +
                                   str(httpDict[x][y]) + "'")
            else:
                Domoticz.Debug("....'" + x + "':'" + str(httpDict[x]) + "'")

def UpdateDevice(Unit, nValue, sValue, TimedOut=0, AlwaysUpdate=False):
    if Unit in Devices:
        if Devices[Unit].nValue != nValue or Devices[Unit].sValue != sValue or Devices[
                Unit].TimedOut != TimedOut or AlwaysUpdate:
            Devices[Unit].Update(
                nValue=nValue, sValue=str(sValue), TimedOut=TimedOut)
            # Domoticz.Debug("Update {}: {} - '{}'".format(Devices[Unit].Name, nValue, sValue))

def UpdateDeviceOptions(Unit, Options={}):
    if Unit in Devices:
        if Devices[Unit].Options != Options:
            Devices[Unit].Update(nValue=Devices[Unit].nValue,
                                 sValue=Devices[Unit].sValue, Options=Options)
            Domoticz.Debug("Device Options update: {} = {}".format(
                Devices[Unit].Name, Options))

def UpdateDeviceImage(Unit, Image):
    if Unit in Devices and Image in Images:
        if Devices[Unit].Image != Images[Image].ID:
            Devices[Unit].Update(nValue=Devices[Unit].nValue,
                                 sValue=Devices[Unit].sValue, Image=Images[Image].ID)
            Domoticz.Debug("Device Image update: {} = {}".format(
                Devices[Unit].Name, Images[Image].ID))

# --------------------------------------------------------------------------------

options = {
    "measure_temp": ["temp", "'C"],
    "get_mem gpu": ["gpu", "M"],
    "get_mem arm": ["arm", "M"],
    "measure_volts core": ["volt", "V"],
    "measure_volts sdram_c": ["volt", "V"],
    "measure_volts sdram_i": ["volt", "V"],
    "measure_volts sdram_p": ["volt", "V"],
}

def vcgencmd(option):
    if option in options:
        cmd = "/opt/vc/bin/vcgencmd {}".format(option)
        Domoticz.Debug("cmd: {}".format(cmd))
        try:
            res = os.popen(cmd).readline()
            Domoticz.Debug("res: {}".format(res))
            res = res.replace("{}=".format(options[option][0]), "")
            res = res.replace("{}\n".format(options[option][1]), "")
            Domoticz.Debug("res (replaced): {}".format(res))
        except:
            res = "0"
    else:
        res = "0"
    return float(res)

# --------------------------------------------------------------------------------

global _last_idle, _last_total
_last_idle = _last_total = 0

# Return % of CPU used by user
# Based on: https://rosettacode.org/wiki/Linux_CPU_utilization#Python

def getCPUuse():
    global _last_idle, _last_total
    try:
        with open('/proc/stat') as f:
            fields = [float(column)
                      for column in f.readline().strip().split()[1:]]
        idle, total = fields[3], sum(fields)
        idle_delta, total_delta = idle - _last_idle, total - _last_total
        _last_idle, _last_total = idle, total
        res = round(100.0 * (1.0 - idle_delta / total_delta), 2)
    except:
        res = 0.0
    return res

def getCPUuptime():
    try:
        with open('/proc/uptime') as f:
            fields = [float(column) for column in f.readline().strip().split()]
        res = round(fields[0])
    except:
        res = 0.0
    return res

def getNetworkConnections(state):
    # Return number of network connections
    res = 0
    try:
      p = subprocess.Popen(('/bin/netstat', '-tun'), stdout=subprocess.PIPE)
      for line in iter(p.communicate()[0].decode("utf-8").splitlines()):
        x = line.split()
        if len(x) > 5 and x[5] == state:
          res += 1
    except:
      res = 0 
    return res

def getSoCtemperature():
    # Return SoC temperature
    return float(vcgencmd("measure_temp"))

def getGPUmemory():
    # Return GPU memory size
    return float(vcgencmd("get_mem gpu"))

def getCPUmemory():
    # Return CPU memory size
    return float(vcgencmd("get_mem arm"))

def getCPUcurrentSpeed():
    # Return CPU speed in Mhz
    try:
        ps  = subprocess.Popen(('/usr/bin/cat', '/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq'), stdout=subprocess.PIPE)
        res = ps.communicate()[0].decode("utf-8").strip('"\n\t')
    except:
        res = "0"

    Domoticz.Debug("getCPUcurrentSpeed (res): "+res)
    return round(int(res)/1000)

def getDomoticzMemory():
    # ps aux | grep domoticz | awk '{sum=sum+$6}; END {print sum}'
    try:
        ps  = subprocess.Popen(('/usr/bin/ps', '-C', 'domoticz', '--no-headers', '-o', '"%z"'), stdout=subprocess.PIPE)
        res = ps.communicate()[0].decode("utf-8").strip('"\n\t')
    except:
        res = "0"

    Domoticz.Debug("getDomoticzMemory (res): "+res)
    return int(res)

def getRAMinfo():
    p = subprocess.Popen(('/usr/bin/free', '-b'), stdout=subprocess.PIPE)
    res = p.communicate()[0].decode("utf-8")
    res = res.splitlines()[1].split()
    return round(100 * (int(res[2])/int(res[1])))

# Based on: https://gist.github.com/funvill/5252169
# http://www.microcasts.tv/episodes/2014/03/15/memory-usage-on-the-raspberry-pi/
# https://www.raspberrypi.org/forums/viewtopic.php?f=63&t=164787
# https://stackoverflow.com/questions/22102999/get-total-physical-memory-in-python/28161352
# https://stackoverflow.com/questions/17718449/determine-free-ram-in-python
# https://www.reddit.com/r/raspberry_pi/comments/60h5qv/trying_to_make_a_system_info_monitor_with_an_lcd/

def getUpStats():
    # Get uptime of RPi
    # Based on: http://cagewebdev.com/raspberry-pi-showing-some-system-info-with-a-python-script/
    # Returns a tuple (uptime, 5 min load average)
    try:
        s = os.popen("uptime").readline()
        load_split = s.split("load average: ")
        # load_five = float(load_split[1].split(",")[1])
        up = load_split[0]
        up_pos = up.rfind(",", 0, len(up)-4)
        up = up[:up_pos].split("up ")[1]
        return up
    except:
        return ""

def getVoltage(p):
    # Get voltage
    # Based on: https://www.raspberrypi.org/forums/viewtopic.php?t=30697
    if p in ["core", "sdram_c", "sdram_i", "sdram_p"]:
        res = vcgencmd("measure_volts {}".format(p))
    else:
        res = "0"

    return float(res)
