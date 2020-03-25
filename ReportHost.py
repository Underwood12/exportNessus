import ReportItem
class ReportHost:
    def __init__(self, ip, mac, os, op_sys, netbios, fqdn, start, end, creds):
        self.ip = ip
        self.mac = mac
        self.os = os
        self.op_sys = op_sys
        self.netbios = netbios
        self.fqdn = fqdn
        self.start = start
        self.end = end
        self.creds = creds
        self.vulns = []
        self.host_crit = 'None'



    def addVulns(self, vulns):
        self.vulns = vulns


    def get_host_crit(self):
        return self.host_crit

    def get_all(self):
        records = ''
        for report_item in self.vulns:
            records += self.ip + ";" + self.mac+ ";" + self.os+ ";" + self.op_sys+ ";" +self.netbios+ ";" + self.fqdn + ";" + self.start+ ";" + self.end+ ";" +self.creds+ ";" + report_item.get_all()
        return records

