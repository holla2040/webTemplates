#!/usr/bin/env python3
import json
class Config:
    def __init__(self, filename="config.json"):
        self.filename = filename
        self.settings = json.load(open(self.filename))

    def save(self):
        json.dump(self.settings,open(self.filename,'w'))

    def factory(self):
        self.settings['dbmq_host']        = "myhost"
        self.settings['dbmq_username']    = "myusername"
        self.settings['dbmq_password']    = "mypassword"
        self.settings['dbmq_listkey']     = "mylist"
        self.save()

if __name__ == "__main__":
    config = Config()
    print(config.settings)
    config.factory()
    print(config.settings)
