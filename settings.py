import json
import logging
import constants

class Settings():
    def __init__(self, settings_file):
        self.settings_file = settings_file
        self.token = None
        self.ping_channel = None
        self.mvp_channel = None
        self.admin = []
        self.mvps = []
    
    def parse_settings(self):
        try:
            with open(self.settings_file, 'r') as f:
                data = json.loads(f.read())
            self.token = data.get("token")
            self.admin = data.get("admin")
            constants.ADMIN_LIST = self.admin
            
            self.mvp_channel = int(data.get("mvp_channel"))
            self.ping_channel = int(data.get("ping_channel"))
            
            return True
        except Exception as e:
            logging.critical(f'Failed to parse_settings: {e}')
            return False