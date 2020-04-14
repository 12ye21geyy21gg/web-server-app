import time,os
from os.path import isfile,join
class Gc: # Garbage Collector
    def __init__(self,logger):
        self.stack = list()
        self.logger = logger
    def clean(self):
        onlyfiles = [f for f in os.listdir('../static') if isfile(join('../static', f))]
        for i in onlyfiles:
            try:
                os.remove('../static/'+onlyfiles)
            except Exception as e:
                self.logger.debug(e)
    def check(self):
        for i in self.stack:
            if time.time() - i[2] > 1*60:
                self.delete_file_function(i[0],i[1])
                self.stack.remove(i)
    def add_files(self,names,dir):
        self.stack.append([names,dir,time.time()])

    def delete_file_function(self,list_of_files, directory):
        for i in list_of_files:
            try:
                file = directory + '/' + i
                os.remove(file)
            except Exception as e:
                self.logger.debug(e)
