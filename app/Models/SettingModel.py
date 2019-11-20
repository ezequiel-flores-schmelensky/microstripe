# coding=utf-8
from app import app, mongo
from flask_pymongo import ObjectId, pymongo

class SettingModel:

    # Funciones para traer todos los datos
    def findAll(self):
        try:
            data = mongo.db.settings.find({})
            return self.makeResponse(200, ([doc for doc in data]))
        
        except (ValueError, Exception) as e:
            app.logger.error('error salvando la data: ' + str(e))
            return self.makeResponse(400, str(e))

    # Funciones para traer uno
    def findOne(self,data):
        try:
            response = mongo.db.settings.find_one({"_id": ObjectId(data)}, {"_id": 0})
            if response is None:
                return self.makeResponse(400, "It does not exist")
            else:
                return self.makeResponse(200, response)
        
        except (ValueError, Exception) as e:
            app.logger.error('error salvando la data: ' + str(e))
            return self.makeResponse(400, str(e))
    
    # Funcion para agregar un documento 
    def insertOne(self, data):
        response = {}
        try:
            #mongo.db.settings.create_index(('name'), unique=True)
            mongo.db.settings.create_index([('project', pymongo.DESCENDING), ('email', pymongo.DESCENDING)], unique=True)
            id = mongo.db.settings.insert(data)
            setting = mongo.db.settings.find_one({"_id": id}, {"_id": 0})
            setting['apiKey'] = str(id)
            mongo.db.settings.update_one({"_id": id}, {'$set': setting})
            setting['_id'] = str(id)
            return self.makeResponse(200, setting)
            
        except pymongo.errors.DuplicateKeyError as be:
            app.logger.info(be)
            return self.makeResponse(400, 'Setting Already exist!')
        except (ValueError, Exception) as e:
            app.logger.error('error salvando la data: ' + str(e))
            return self.makeResponse(400, str(e))

    # Funcion para agregar un documento 
    def updateOne(self, data):
        try:
            mongo.db.settings.update_one({"_id": ObjectId(data["_id"])}, {'$set': data["data"]})
            response = mongo.db.settings.find_one({"_id": ObjectId(data["_id"])}, {"_id": 0})
            return self.makeResponse(200, response)

        except (ValueError, Exception) as e:
            app.logger.error('error salvando la data: ' + str(e))
            return self.makeResponse(400, str(e))

    # Funcion para eliminar por  id
    def deleteOne(self, data):
        try:
            data = mongo.db.settings.delete_one({"_id": ObjectId(data)})
            return self.makeResponse(200, {"message":"Setting deleted"})

        except (ValueError, Exception) as e:
            app.logger.error('error salvando la data: ' + str(e))
            return self.makeResponse(400, str(e))

    # Funcion para eliminar por  id
    def reset(self):
        try:
            data = mongo.db.settings.drop()
            return self.makeResponse(200, {"message":"Settings deleted"})

        except (ValueError, Exception) as e:
            app.logger.error('error salvando la data: ' + str(e))
            return self.makeResponse(400, str(e))

    # Función para crear respuesta
    def makeResponse(self, status, data):
        response = {}
        response["code"] = status
        if status == 200:
            response["response"] = data
        else:
            response["response"] = {"message":data}
        return response

    def __init__(self):
        pass