class report_item:
    def __init__(self, plugin_id, risk_factor, plugin_name, plugin_family, plugin_type, cvss_base_score, available_exploit , cves):
        self.plugin_id = plugin_id
        self.risk_factor = risk_factor
        self.plugin_name = plugin_name
        self.plugin_family = plugin_family
        self.plugin_type = plugin_type
        self.cvss_base_score = cvss_base_score
        self.available_exploit = available_exploit
        self.cves = cves
        

    def get_all(self):
        return self.plugin_id+ ";" + self.risk_factor+ "; '" +self.plugin_name+ "';" +self.plugin_type+ "; '" + self.plugin_family+ "' ;" + self.cvss_base_score + ";" + str(self.available_exploit) + ";" + ' '.join(self.cves) + "\n"
