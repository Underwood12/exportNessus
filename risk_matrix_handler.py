import openpyxl


COLUMNS = ["IP", "FQDN", "Status", "Business criticality", "Name"]
crit_dict = {}
row = 0

path = "itop_hosts.xlsx"
wb = openpyxl.load_workbook(path)
ws = wb.active
row = ws.max_row

def init_dict():
    for i in range(1, row +1):
        ip      = ws.cell(row=i, column=COLUMNS.index("IP") + 1).value
        fqdn    = ws.cell(row=i, column=COLUMNS.index("FQDN") + 1).value
        stat    = ws.cell(row=i, column=COLUMNS.index("Status") +1).value
        crit    = ws.cell(row=i, column=COLUMNS.index("Business criticality") +1).value
        crit_dict[ip] = crit
        #print('{}:{}:{} --> {}'.format(ip, fqdn, stat, crit))


def get_crit_from(ip):
    try: return crit_dict[ip]
    except: return 'High by Default'


