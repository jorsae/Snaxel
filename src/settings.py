import json
import logging
import constants

class Settings():
    def __init__(self, settings_file):
        self.settings_file = settings_file
        self.token = None
        self.bot_id = None
        self.ping_channel = None
        self.mvp_channel = None
        self.admin = []
        self.mvps = []
        self.local_time_offset = None
        self.aest_offset = None
    
    def parse_settings(self):
        try:
            with open(self.settings_file, 'r') as f:
                data = json.loads(f.read())
            self.token = data.get("token")
            self.admin = data.get("admin")
            self.bot_id = int(data.get("bot_id"))
            constants.ADMIN_LIST = self.admin
            
            self.mvp_channel = int(data.get("mvp_channel"))
            self.ping_channel = int(data.get("ping_channel"))

            self.local_time_offset = int(data.get("local_time_offset"))
            self.aest_offset = int(data.get("aest_offset"))
            
            return True
        except Exception as e:
            logging.critical(f'Failed to parse_settings: {e}')
            return False