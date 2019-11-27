import pymongo
import os
import sys
import pprint

class MongoDB:
    def __init__(self):
        self.CreateConnection()
        self.SetupInstanceVariables()

    def CreateConnection(self):
        if 'MONGO_DB_ADMIN_PASSWORD' in os.environ:
            username = os.environ['MONGO_DB_USERNAME']
            password = os.environ['MONGO_DB_PASSWORD']
            self.client = pymongo.MongoClient('mongodb+srv://{}:{}@privatecluster-i2ans.mongodb.net/test?retryWrites=true&w=majority'.format(username, password))
        else:
            print("\nSet the MONGO_DB_USERNAME and MONGO_DB_PASSWORD environment variable.\n**Restart your shell or IDE for changes to take effect.**")
            sys.exit()

    def SetupInstanceVariables(self):
        try:
            self.database = self.client['ZRecognition']
            self.collection = self.database['licenseplates']
        except:
            print('Error connecting to database...')

    def InsertPlate(self, plate):
        result = self.collection.insert_one(plate)
        print(result)

    def GetAllPlates(self):
        return self.collection.find()

    def CheckAuthorization(self, licenseplate):
        return True if self.collection.find_one({'licensePlate':licenseplate}) else False