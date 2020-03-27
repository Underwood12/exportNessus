import xml.etree.cElementTree as ET
import ReportHost, ReportItem
import re
import time
import tkinter as tk
import filter
from tkinter import filedialog
from datetime import datetime


rt = tk.Tk()
rt.withdraw()

file = ''
crit_file = ''

def read_config_file():
    global filenames
    global keywords
    config_tree = ET.parse('config.xml')
    config_root = config_tree.getroot()
    keywords = []
    filenames = []
    for i in config_root:
        keywords.append(i[0].text)
        filenames.append(i[1].text)
    print(keywords)





def write_to_CSV(host):
    records = host.get_all()
    f = open(file, "a")
    f.write(records)

def write_to_crit_CSV(h):
    f = open(crit_file, "a")
    f.write(h.ip + ";" + h.mac + ";" + h.os + ";" + h.op_sys + ";" + h.netbios + ";" + h.fqdn + ";" + h.creds + ";" + h.host_crit + "\n")

def set_host_crit(current_host, crit):
    crit_rank = ['None', 'Low', 'Medium', 'High', 'Critical']
    highest_crit = crit_rank.index(current_host.get_host_crit())
    current_crit = crit_rank.index(crit)
    if highest_crit < current_crit:
        current_host.host_crit = crit


def get_vulns(HOST, current_host):
    vulns = []
    for i in range(1, len(root[1][HOST])): # ignore hostproperties
        plugin_id = root[1][HOST][i].get('pluginID')
        risk_factor = strip(root[1][HOST][i].find('risk_factor').text)
        plugin_name = root[1][HOST][i].get('pluginName')
        plugin_family = root[1][HOST][i].get('pluginFamily')
        plugin_type = strip(root[1][HOST][i].find('plugin_type').text)
        cvss_base_score = get_special_prop(HOST, i, 'cvss_base_score')
        cves = get_special_prop(HOST, i, 'cve')
        ri = ReportItem.ReportItem(plugin_id, risk_factor, plugin_name, plugin_family, plugin_type, cvss_base_score, cves)
        set_host_crit(current_host, risk_factor)
        vulns.append(ri)
    return vulns

def get_special_prop(HOST, element, prop):
    if prop == 'cve':
        res = root[1][HOST][element].findall(prop)
        if res == []: return ''
        else:
            res2 = []
            for i in res:
                res2.append(strip(i.text))
            return res2
    else:
        res = root[1][HOST][element].find(prop)
        if res is None:
            return ''
        else: return strip(res.text)


def strip(x):
    x = re.sub('\n\t\t\t\t\t', '', x)
    x = re.sub('\n', ' - ', x)
    return re.sub('\n\t\t\t\t', '', x)

def get_host_properties(HOST):
    fqdn, os, netbios, op_sys, creds, ip, start, end = "", "","", "","", "","", ""
    for i in range(len(root[1][HOST][0])):
        if root[1][HOST][0][i].get('name') == 'host-fqdn':
            fqdn = strip(root[1][HOST][0][i].text)
        elif root[1][HOST][0][i].get('name') == 'os':
            os = strip(root[1][HOST][0][i].text)
        elif root[1][HOST][0][i].get('name') == 'netbios-name':
            netbios = strip(root[1][HOST][0][i].text)
        elif root[1][HOST][0][i].get('name') == 'operating-system':
            op_sys = strip(root[1][HOST][0][i].text)
        elif root[1][HOST][0][i].get('name') == 'Credentialed_Scan':
            creds = strip(root[1][HOST][0][i].text)
        elif root[1][HOST][0][i].get('name') == 'host-ip':
            ip = strip(root[1][HOST][0][i].text)
        elif root[1][HOST][0][i].get('name') == 'HOST_START':
            start = strip(root[1][HOST][0][i].text)
        elif root[1][HOST][0][i].get('name') == 'HOST_END':
            end = strip(root[1][HOST][0][i].text)
    return ReportHost.ReportHost(ip, '', os, op_sys, netbios, fqdn, start, end, creds)

def initCSV():
    f = open(file, "a")
    f.write('Host IP;' + 'MAC Address;' + 'OS;'+'Operating system;' + 'Netbios;' + 'FQDN;' + 'Start;' + 'End;' + 'Credentialed;' + 'PluginID;' + 'Risk Factor;' + 'Plugin Name;' + 'Plugin Type;' + 'Plugin Family;' + 'CVSS Base Score;' + 'CVES\n' )
    f.close()
    #f = open(crit_file, "a")
    #f.write('Host IP;' + 'MAC Address;' + 'OS;'+'Operating system;' + 'Netbios;' + 'FQDN;' +  'Credentialed;' + 'Highest Crit\n')


def change_filename(file_path):
    for i in keywords:
        print(i, file_path)
        if i in file_path: return filenames[keywords.index(i)]
    raise Exception('NO keyword - filename mapping valid in config')

def init():
    read_config_file()
    csv_files = filedialog.askopenfilenames()
    files_to_excel = []
    for f in csv_files:
        global tree
        global root
        global file
        global crit_file
        time.sleep(1)
        file = change_filename(f) + ".csv"
        #file = datetime.today().strftime('%H_%M_%S') + ".csv"
        #crit_file = "crit_" + datetime.today().strftime('%H_%M_%S') + ".csv"
        tree = ET.parse(f)
        root = tree.getroot()
        files_to_excel.append(file)
        initCSV()
        for HOST in range(len(root[1])):
            current_host = get_host_properties(HOST)
            current_host.addVulns(get_vulns(HOST, current_host))

            write_to_CSV(current_host)
            #write_to_crit_CSV(current_host)
    filter.csvs_to_excel(files_to_excel)


def main():
    init()


if __name__== "__main__":
    main()

