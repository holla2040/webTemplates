#!/usr/bin/env python3
import json
class Config:
    def __init__(self, filename="config.json"):
        self.filename = filename
        self.settings = json.load(open(self.filename))

    def save(self):
        json.dump(self.settings,open(self.filename,'w'))

    def factory(self):
        self.settings['db_host']        = "myhost"
        self.settings['db_username']    = "myusername"
        self.settings['db_password']    = "mypassword"
        self.settings['db_database']    = "mydatabase"
        self.settings['db_table']       = "mytable"
        self.save()

if __name__ == "__main__":
    config = Config()
    print(config.settings)
    config.factory()
    print(config.settings)
