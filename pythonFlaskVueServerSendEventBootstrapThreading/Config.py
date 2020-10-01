#!/usr/bin/env python3
import json
class Config:
    def __init__(self, filename="config.json"):
        self.filename = filename
        self.settings = json.load(open(self.filename))

    def save(self):
        json.dump(self.settings,open(self.filename,'w'))

    def factory(self):
        self.settings['db_host']        = "horton"
        self.settings['db_dbname']      = "synsysco"
        self.settings['db_table']       = "telemetry"
        self.save()

if __name__ == "__main__":
    config = Config()
    print(config.settings)
    config.factory()
    print(config.settings)
