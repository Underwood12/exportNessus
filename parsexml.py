import xml.etree.cElementTree as ET
import ReportHost, ReportItem
import re
import tkinter as tk
from tkinter import filedialog
from datetime import datetime

rt = tk.Tk()
rt.withdraw()


tree = ET.parse(filedialog.askopenfilename())
#tree = ET.parse('DIPLOBEL_DOMAIN_Win_2012_R2_Member_Server_SCAN_-_SLOW_uw359k.nessus')
root = tree.getroot()

file = datetime.today().strftime('%H_%M_%S') + ".csv"

def write_to_CSV(host):
    records = host.get_all()
    f = open(file, "a")
    f.write(records)

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

def main():
    initCSV()
    for HOST in range(len(root[1])):
        current_host = get_host_properties(HOST)
        current_host.addVulns(get_vulns(HOST, current_host))
        write_to_CSV(current_host)

if __name__== "__main__":
    main()

