# coding=utf-8
from app import app, mongo
from flask_pymongo import ObjectId, pymongo

class StripeClientModel:

    # Funciones para traer todos los datos
    def findAll(self):
        try:
            data = mongo.db.stripe_clients.find({})
            return self.makeResponse(200, ([doc for doc in data]))
        
        except (ValueError, Exception) as e:
            app.logger.error('error salvando la data: ' + str(e))
            return self.makeResponse(400, str(e))

    # Funciones para traer uno
    def findOne(self,data):
        try:
            response = mongo.db.stripe_clients.find_one({"_id": ObjectId(data)}, {"_id": 0})
            if response is None:
                return self.makeResponse(400, "It does not exist")
            else:
                return self.makeResponse(200, response)
        
        except (ValueError, Exception) as e:
            app.logger.error('error salvando la data: ' + str(e))
            return self.makeResponse(400, str(e))
    
     # Funciones para traer uno
    def findOneByEmail(self,data):
        try:
            response = mongo.db.stripe_clients.find_one({"email": data}, {"_id": 0})
            if response is None:
                return self.makeResponse(400, "It does not exist")
            else:
                return self.makeResponse(200, response)
        
        except (ValueError, Exception) as e:
            app.logger.error('error salvando la data: ' + str(e))
            return self.makeResponse(400, str(e))

    def findOneByCustomerId(self,data):
        try:
            response = mongo.db.stripe_clients.find_one({"customerId": data}, {"_id": 0})
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
            mongo.db.stripe_clients.create_index([('email', pymongo.DESCENDING)], unique=True)
            id = mongo.db.stripe_clients.insert(data)
            stripe_client = mongo.db.settings.find_one({"_id": id})
            return self.makeResponse(200, stripe_client)
            
        except pymongo.errors.DuplicateKeyError as be:
            app.logger.info(be)
            stripe_client = mongo.db.settings.find_one({"email": data["email"]})
            return self.makeResponse(200, stripe_client)
        except (ValueError, Exception) as e:
            app.logger.error('error salvando la data: ' + str(e))
            return self.makeResponse(400, str(e))

    # Funcion para agregar un documento 
    def updateOne(self, data):
        try:
            mongo.db.stripe_clients.update_one({"_id": ObjectId(data["_id"])}, {'$set': data["data"]})
            response = mongo.db.stripe_clients.find_one({"_id": ObjectId(data["_id"])}, {"_id": 0})
            return self.makeResponse(200, response)

        except (ValueError, Exception) as e:
            app.logger.error('error salvando la data: ' + str(e))
            return self.makeResponse(400, str(e))

    # Funcion para eliminar por  id
    def deleteOne(self, data):
        try:
            data = mongo.db.stripe_clients.delete_one({"_id": ObjectId(data)})
            return self.makeResponse(200, {"message":"Stripe Client deleted"})

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