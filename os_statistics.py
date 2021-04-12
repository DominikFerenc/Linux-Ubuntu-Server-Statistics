#!/usr/bin/python3.9 python3
import platform
import subprocess
import socket
import os
import time
import sys
import threading
import psutil


class Converter:
    KB_CONST = 1024
    CPU_CONST = 1000

    def convertBytesToGigaBytes(self, disk_total_bytes):
        return disk_total_bytes / (self.KB_CONST * self.KB_CONST * self.KB_CONST)

    def convertCpuTemperature(self, cpu_temperature):
        return cpu_temperature / self.CPU_CONST

    def calculatePercent(self, available_memory, available_memory_percent):
        return available_memory * available_memory_percent


class Device:
    converter = Converter()

    lsb_release_command = "lsb_release -d"
    echo_command = "echo $USER"
    ps_aux_command = "ps aux | wc -l"
    who_command = "who"
    # java_version_command = "java -version 2>&1 | awk -F[\"_] 'NR==1{print $1 $2 $3}'"
    updates_command = 'apt-get -s dist-upgrade | grep "^[[:digit:]]"'  # "\+ upgraded"'
    actual_date_command = 'date "+%d.%m.%y%n"'
    actual_time_command = 'date "+%H:%M:%S"'

    path_to_cpu_temperature = "/sys/class/thermal/thermal_zone0/temp"
    path_to_mac_address_eth0_ubuntu = "/sys/class/net/eth0/address"
    path_to_mac_address_enp1s0_ubuntu = "/sys/class/net/enp1s0/address"
    path_to_mac_address_enp0s25_ubuntu = "/sys/class/net/enp0s25/address"

    def getActualDate(self):
        return str(subprocess.check_output(self.actual_date_command, shell=True))

    def getActualTime(self):
        return str(subprocess.check_output(self.actual_time_command, shell=True))

    def getNumberOfUpdates(self):
        return str(subprocess.check_output(self.updates_command, shell=True))

    def getSystemName(self):
        return str(subprocess.check_output(self.lsb_release_command, shell=True))

    def getUserName(self):
        return subprocess.check_output(self.echo_command, shell=True)

    def getKernelInformations(self):
        return platform.system() + ' ' + platform.release() + ' ' + platform.processor()

    def getInformationAboutNumberLogicalCore(self):
        return psutil.cpu_count()

    def getCpuUsageInPercent(self):
        return psutil.cpu_percent(interval=1)

    def getGeneralInformationAboutDisk(self):
        return psutil.disk_usage('/')

    def getDiskUsageInPercent(self):
        return self.getGeneralInformationAboutDisk().percent

    def getDiskTotalSpace(self):
        return float(format(self.converter.convertBytesToGigaBytes(self.getGeneralInformationAboutDisk().total), '.2f'))

    def getDiskUsed(self):
        return float(format(self.converter.convertBytesToGigaBytes(self.getGeneralInformationAboutDisk().used), '.2f'))

    def getDiskFreeSpace(self):
        return float(format(self.converter.convertBytesToGigaBytes(self.getGeneralInformationAboutDisk().free), '.2f'))

    def getGeneralInformationAboutMemory(self):
        return psutil.virtual_memory()

    def getMemoryTotal(self):
        return float(format(self.converter.convertBytesToGigaBytes(self.getGeneralInformationAboutMemory().total), '.2f'))

    def getMemoryUsageInPercent(self):
        return self.getGeneralInformationAboutMemory().percent

    def getAvailableMemory(self):
        return float(format(self.converter.convertBytesToGigaBytes(self.getGeneralInformationAboutMemory().available), '.2f'))

    def getUsedMemory(self):
        return float(format(self.converter.convertBytesToGigaBytes(self.getGeneralInformationAboutMemory().used), '.2f'))

    def getFreeMemory(self):
        return float(format(self.converter.convertBytesToGigaBytes(self.getGeneralInformationAboutMemory().free), '.2f'))

    def getCacheMemory(self):
        return float(format(self.converter.convertBytesToGigaBytes(self.getGeneralInformationAboutMemory().cached), '.2f'))

    def getGenerInformationAboutSwapMemory(self):
        return psutil.swap_memory()

    def getTotalSwapMemory(self):
        return float(format(self.converter.convertBytesToGigaBytes(self.getGenerInformationAboutSwapMemory().total), '.2f'))

    def getUsedSwapMemory(self):
        return float(format(self.converter.convertBytesToGigaBytes(self.getGenerInformationAboutSwapMemory().used), '.2f'))

    def getFreeSwapMemory(self):
        return float(format(self.converter.convertBytesToGigaBytes(self.getGenerInformationAboutSwapMemory().free), '.2f'))

    def getCpuTemperature(self):
        if os.path.exists(self.path_to_cpu_temperature):
            with open(self.path_to_cpu_temperature) as cpu_thermal:
                cpu_temperature = float(cpu_thermal.read())
                cpu_thermal.close()
                return float(format(self.converter.convertCpuTemperature(cpu_temperature), '.2f'))
        else:
            print('\033[93mSorry, no correct temperature reading\033[0m')

    def getNumberOfProcesses(self):
        return str(subprocess.check_output(self.ps_aux_command, shell=True))

    def getJavaVersion(self):
        Java_version = subprocess.call(self.java_version_command, shell=True)
        print("Test Java Version", Java_version)

    def getPythonVersion(self):
        return platform.python_version()

    def getDeviceIPAddress(self):
        host_name = socket.gethostname()
        return socket.gethostbyname(host_name)

    def getDeviceMACAddress(self):
        pathToMACAddress = self.checkPathToMACAddressFile()
        MAC_Address = open(str(pathToMACAddress))
        return MAC_Address.read()

    def getLastUsersLogged(self):
        return str(subprocess.check_output(self.who_command, shell=True))

    def checkPathToMACAddressFile(self):
        if os.path.exists(self.path_to_mac_address_eth0_ubuntu):
            return self.path_to_mac_address_eth0_ubuntu
        elif os.path.exists(self.path_to_mac_address_enp1s0_ubuntu):
            return self.path_to_mac_address_enp1s0_ubuntu
        elif os.path.exists(self.path_to_mac_address_enp0s25_ubuntu):
            return self.path_to_mac_address_enp0s25_ubuntu
        else:
            MAC_Address_err_message = '\033[93mThe devices has no MAC Address\033[0m'
            print(str(MAC_Address_err_message))


class DataView:
    converter = Converter()

    def __init__(self, number_of_update_os, actual_date, actual_time, system_name, kernel_information,
                 number_logical_core, cpu_percent, disk_percent, disk_total, disk_used, disk_free_space,
                 memory_total, memory_usage, available_memory, used_memory, free_memory, cache_memory,
                 total_swap_memory, used_swap_memory, cpu_temperature, number_of_processes, python_version,
                 IP_address, MAC_Address, last_users_logged):
        self.number_of_update_os = number_of_update_os
        self.actual_date = actual_date
        self.actual_time = actual_time
        self.system_name = system_name
        self.kernel_information = kernel_information
        self.number_logical_core = number_logical_core
        self.cpu_percent = cpu_percent
        self.disk_percent = disk_percent
        self.disk_total = disk_total
        self.disk_used = disk_used
        self.disk_free_space = disk_free_space
        self.memory_total = memory_total
        self.memory_usage = memory_usage
        self.available_memory = available_memory
        self.used_memory = used_memory
        self.free_memory = free_memory
        self.cache_memory = cache_memory
        self.total_swap_memory = total_swap_memory
        self.used_swap_memory = used_swap_memory
        self.cpu_temperature = cpu_temperature
        self.number_of_processes = number_of_processes
        self.python_version = python_version
        self.IP_address = IP_address
        self.MAC_Address = MAC_Address
        self.last_users_logged = last_users_logged

        self.showTitle()
        self.showInformationAboutUpdates(self.number_of_update_os)
        self.showActualDate(self.actual_date)
        self.showActualTime(self.actual_time)
        self.showSystemName(self.system_name)
        self.showKernelInformation(self.kernel_information)
        self.showInformationAboutNumberLogicalCore(self.number_logical_core)
        self.showInformationAboutCpuUsage(self.cpu_percent)
        self.showInformationAboutDiskUsage(self.disk_percent)
        self.showDiskTotalSpace(self.disk_total)
        self.showInformationAboutDiskUsed(self.disk_used)
        self.showInformationAboutDiskFreeSpace(self.disk_free_space)
        self.showMemoryTotal(self.memory_total)
        self.showInformationAboutMemoryUsage(self.memory_usage)
        self.showInformationAboutAvailableMemory(self.available_memory)
        self.showInformationAboutUsedMemory(self.used_memory)
        self.showInformationAboutFreeMemory(self.free_memory)
        self.showInformationAboutCacheMemory(self.cache_memory)
        self.showTotalSwapMemory(self.total_swap_memory)
        self.showUsedSwapMemory(self.used_swap_memory)
        self.showCPUTemperature(self.cpu_temperature)
        self.showNumberOfProcesses(self.number_of_processes)
        self.showPythonVersion(self.python_version)
        self.showDeviceIPAddress(self.IP_address)
        self.showDeviceMACAddress(self.MAC_Address)
        self.showLastUsersLogged(self.last_users_logged)

    def showTitle(self):
        print("\033[33m *--Your Environment Information--*\033[0m")
        print(psutil.swap_memory())

    def showInformationAboutUpdates(self, number_of_update_os):
        CONSTANT_ZERO_STR_ENG = '0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.'
        CONSTANT_ZERO_STR_PL = '0 aktualizowanych, 0 nowo instalowanych, 0 usuwanych i 0 nieaktualizowanych.'
        number_of_update_os_str = number_of_update_os.replace('\\n', '').replace('b', '').replace('\'', '')

        if number_of_update_os_str == CONSTANT_ZERO_STR_ENG or number_of_update_os_str == CONSTANT_ZERO_STR_PL:
            print("\033[32m     Your operating system is up to date.\033[0m")
        else:
            print(" \033[33m    Updates\033[0m\033[93m              ", number_of_update_os_str, '\033[0m')

    def showActualDate(self, actual_date):
        actual_date_fix_value = actual_date.replace('\\n', '').replace('b', '').replace('\'', '')
        print("\033[33m     Actual date:         \033[0m\033[36m", actual_date_fix_value, '\033[0m')

    def showActualTime(self, actual_time):
        actual_time_fix_value = actual_time.replace('\\n', '').replace('b', '').replace('\'', '')
        print("\033[33m     Actual time:         \033[0m\033[36m", actual_time_fix_value, '\033[0m')

    def showSystemName(self, system_name):
        system_name_value = system_name.replace('Description:', '').replace('b', '', 1).replace('\\t', '')\
            .replace('\'','').replace('\\n', '')
        print('\033[33m     System name: \033[0m        \033[36m', system_name_value, '\033[0m')

    def showKernelInformation(self, kernel_information):
        print("\033[33m     Kernel: \033[0m             \033[36m", kernel_information, '\033[0m')

    def showInformationAboutNumberLogicalCore(self, number_logical_core):
        print("\033[33m     Logical core:        \033[0m\033[36m", number_logical_core, '\033[0m')

    def showInformationAboutCpuUsage(self, cpu_percent):
        LIMIT_VALUE_FOR_CPU_USAGE_IN_PERCENT = 90.0
        if cpu_percent >= LIMIT_VALUE_FOR_CPU_USAGE_IN_PERCENT:
            print("\033[33m     Cpu usage:           \033[0m\033[31m", cpu_percent, '\033[33m% \033[0m')
        else:
            print("\033[33m     Cpu usage:           \033[0m\033[32m", cpu_percent, '\033[33m% \033[0m')

    def showInformationAboutDiskUsage(self, disk_percent):
        LIMIT_VALUE_FOR_DISK_USAGE_IN_PERCENT = 90.0
        if disk_percent >= LIMIT_VALUE_FOR_DISK_USAGE_IN_PERCENT:
            print("\033[33m     Disk usage:          \033[0m\033[31m", disk_percent, '\033[33m% \033[0m')
        else:
            print("\033[33m     Disk usage:          \033[0m\033[32m", disk_percent, '\033[33m% \033[0m')

    def showDiskTotalSpace(self, disk_total):
        print("\033[33m     Disk total space:    \033[0m\033[36m", disk_total, '\033[33mGB \033[0m')
##kolorki
    def showInformationAboutDiskUsed(self, disk_used):
        print("\033[33m     Disk used:           \033[0m\033[36m", disk_used, '\033[33mGB \033[0m')

    def showInformationAboutDiskFreeSpace(self, disk_free_space):
        LIMIT_VALUE_FOR_DISK_FREE_SPACE = 10.00

        if disk_free_space <= LIMIT_VALUE_FOR_DISK_FREE_SPACE:
            print("\033[33m     Disk free space:     \033[0m\033[31m", disk_free_space, '\033[33mGB \033[0m')
        else:
            print("\033[33m     Disk free space:     \033[0m\033[32m", disk_free_space, '\033[33mGB \033[0m')

    def showInformationAboutMemoryUsage(self, memory_usage):
        LIMIT_VALUE_FOR_MEMORY_USAGE_IN_PERCENT = 90.0
        MIDDLE_VALUE_FOR_MEMORY_USAGE_IN_PERCENT = 60.0
        if memory_usage >= LIMIT_VALUE_FOR_MEMORY_USAGE_IN_PERCENT:
            print("\033[33m     Memory usage:        \033[0m\033[31m", memory_usage, '\033[33m% \033[0m')
        elif MIDDLE_VALUE_FOR_MEMORY_USAGE_IN_PERCENT <= memory_usage < LIMIT_VALUE_FOR_MEMORY_USAGE_IN_PERCENT:
            print("\033[33m     Memory usage:        \033[0m\033[35m", memory_usage, '\033[33m% \033[0m')
        else:
            print("\033[33m     Memory usage:        \033[0m\033[32m", memory_usage, '\033[33m% \033[0m')


    def showMemoryTotal(self, memory_total):
        print("\033[33m     Memory total:        \033[0m\033[36m", memory_total, '\033[33mGB \033[0m')

    def showInformationAboutAvailableMemory(self, available_memory):
        LIMIT_VALUE = self.converter.calculatePercent(self.memory_total, 0.30)
        MIDDLE_VALUE = self.converter.calculatePercent(self.memory_total, 0.60)

        LIMIT_VALUE_FOR_AVAILABLE_MEMORY = float(format(LIMIT_VALUE, '.2f'))
        MIDDLE_VALUE_FOR_AVAILABLE_MEMORY = float(format(MIDDLE_VALUE, '.2f'))

        if available_memory<= LIMIT_VALUE_FOR_AVAILABLE_MEMORY:
            print("\033[33m     Available Memory:   \033[0m\033[36m \033[31m", available_memory,
                  '\033[33mGB \033[0m')
        elif MIDDLE_VALUE_FOR_AVAILABLE_MEMORY > available_memory:
            print("\033[33m     Available Memory:   \033[0m\033[36m \033[35m", available_memory,
                  '\033[33mGB \033[0m')
        else:
            print("\033[33m     Available Memory:   \033[0m\033[36m \033[32m", available_memory,
                  '\033[33mGB \033[0m')

    def showInformationAboutUsedMemory(self, used_memory):
        print("\033[33m     Used memory:        \033[0m\033[36m \033[32m", used_memory,
              '\033[33mGB \033[0m')

    def showInformationAboutFreeMemory(self, free_memory):
        print("\033[33m     Free memory:        \033[0m\033[36m \033[32m", free_memory,
              '\033[33mGB \033[0m')

    def showInformationAboutCacheMemory(self, cache_memory):
        print("\033[33m     Cache memory:       \033[0m\033[36m \033[32m", cache_memory,
              '\033[33mGB \033[0m')

    def showTotalSwapMemory(self, total_swap_memory):
        print("\033[33m     Swap total:          \033[0m\033[36m %.2f" % total_swap_memory, '\033[33mGB \033[0m')

    def showUsedSwapMemory(self, used_swap_memory):
        print("\033[33m     Used swap memory:   \033[0m\033[36m \033[32m", used_swap_memory,
              '\033[33mGB \033[0m')

    def showCPUTemperature(self, cpu_temperature):
        CRITICAL_TEMPERATURE = 120.00
        HIGH_TEMPERATURE = 90.00
        MIDDLE_TEMPERATURE = 60.00

        if CRITICAL_TEMPERATURE <= cpu_temperature:
            print(
                "\033[33m     Cpu Temperature:\033[0m      \033[31mCPU TEMPERATURE HAS REACHED A CRITICAL LEVEL\033[31m: ",
                cpu_temperature_format,
                '\033[33m\u00B0C', '\033[0m')
        elif HIGH_TEMPERATURE <= cpu_temperature < CRITICAL_TEMPERATURE:
            print("\033[33m     Cpu Temperature:\033[0m\033[31m     ", cpu_temperature, '\033[33m\u00B0C',
                  '\033[0m')
        elif MIDDLE_TEMPERATURE <= cpu_temperature < HIGH_TEMPERATURE:
            print("\033[33m     Cpu Temperature:\033[0m\033[35m     ", cpu_temperature, '\033[33m\u00B0C',
                  '\033[0m')
        else:
            print("\033[33m     Cpu Temperature:\033[0m\033[32m     ", cpu_temperature, '\033[33m\u00B0C',
                  '\033[0m')

    def showNumberOfProcesses(self, number_of_processes):
        number_of_processes_str = number_of_processes.replace('\\n', '').replace('b', '').replace('\'', '')
        print("\033[33m     Processes: \033[0m          \033[36m", number_of_processes_str, '\033[0m')

    def showPythonVersion(self, python_version):
        print("\033[33m     Python Version: \033[0m     \033[36m", python_version, '\033[0m')

    def showDeviceIPAddress(self, IP_Address):
        print("\033[33m     Device IP Address:   \033[0m\033[36m", IP_Address, '\033[0m')

    def showDeviceMACAddress(self, MAC_Address):
        print("\033[33m     Device MAC Address:  \033[0m\033[36m", MAC_Address, '\033[0m')

    def showLastUsersLogged(self, last_users_logged):
        last_users_logged_str = last_users_logged.replace("b'", '').replace("'", '').replace('(', '\t   ').replace(')',
                                                                                                                   '').replace(
            '\\n', '\n')
        print("\n\033[33mUSER     TTY          DATE/TIME            IP\033[0m")
        print('\033[33m*----------------------------------------------------*\033[0m')
        print('\033[36m' + last_users_logged_str, '\033[0m')


def main():
    device_obj = Device()
    number_of_updates_os = device_obj.getNumberOfUpdates()
    actual_date = device_obj.getActualDate()
    actual_time = device_obj.getActualTime()
    system_name = device_obj.getSystemName()
    kernel_information = device_obj.getKernelInformations()
    number_logical_core = device_obj.getInformationAboutNumberLogicalCore()
    cpu_percent = device_obj.getCpuUsageInPercent()
    disk_percent = device_obj.getDiskUsageInPercent()
    disk_total = device_obj.getDiskTotalSpace()
    disk_used = device_obj.getDiskUsed()
    disk_free_space = device_obj.getDiskFreeSpace()
    memory_total = device_obj.getMemoryTotal()
    memory_usage = device_obj.getMemoryUsageInPercent()
    available_memory = device_obj.getAvailableMemory()
    used_memory = device_obj.getUsedMemory()
    free_memory = device_obj.getFreeMemory()
    cache_memory = device_obj.getCacheMemory()
    total_swap_memory = device_obj.getTotalSwapMemory()
    used_swap_memory = device_obj.getUsedSwapMemory()
    device_obj.getFreeSwapMemory()
    cpu_temperature = device_obj.getCpuTemperature()
    number_of_processes = device_obj.getNumberOfProcesses()
    # device_obj.getJavaVersion()
    python_version = device_obj.getPythonVersion()
    IP_Address = device_obj.getDeviceIPAddress()
    MAC_Address = device_obj.getDeviceMACAddress()
    last_users_logged = device_obj.getLastUsersLogged()

    print('\n')
    view = DataView(number_of_updates_os, actual_date, actual_time, system_name, kernel_information,
                    number_logical_core, cpu_percent, disk_percent, disk_total, disk_used,
                    disk_free_space, memory_total, memory_usage, available_memory,
                    used_memory, free_memory, cache_memory, total_swap_memory, used_swap_memory,
                    cpu_temperature, number_of_processes, python_version, IP_Address, MAC_Address, last_users_logged)
    print('\n')


if __name__ == '__main__':
    main()
