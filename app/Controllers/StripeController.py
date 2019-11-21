import os
import json
import stripe
import requests
from app import app 
from Schemes import *
from Models import *
from flask import render_template, jsonify


class StripeController():
    
    def get(self):
        #print(str(app.config['STRIPE_SECRET_KEY']))
        response = SettingModel().findAll()
        if response['code'] == 200:
          if len(response["response"]) > 0:
            return jsonify(response["response"]), response['code']
          else:
            return render_template("form.html",name=None)
        else:
          return jsonify(response["response"]), response['code']


    def setting_crud(self, request):    
      if request.method == 'POST':
        if request.form is not None:
          #print("si entro")
          #fields = request.form
          fields = {
            "project":request.form["project"],
            "email":request.form["email"],
            "productionKey":request.form["productionKey"],
            "developKey":request.form["developKey"],
            "inProduction":True if "inProduction" in request.form and request.form["inProduction"] == "on" else False,
            "subProductName":request.form["subProductName"],
            "subPlanAmount":float(request.form["subPlanAmount"]),
            "subPlanCurrency":request.form["subPlanCurrency"],
            "subPlanInterval":request.form["subPlanInterval"],
            "successfulWebhook":request.form["successfulWebhook"],
            "cancelWebhook":request.form["cancelWebhook"]
          }
        else:
          fields = request.get_json()
        data = validate_stting(fields) 
        if data["ok"]:
          setting = data["data"]
          ##### Production #####
          stripe.api_key = setting["productionKey"]
          #Create Product and save
          response = stripe.Product.create(
            name=setting["subProductName"],
            type="service",
            active=True
          )
          setting["subProductId"] = response["id"]
          #Create Plan and save
          response = stripe.Plan.create(
            amount=int(float(setting["subPlanAmount"])*100),
            currency=setting["subPlanCurrency"],
            interval=setting["subPlanInterval"],
            interval_count=1,
            product={"name": setting["subProductName"]},
          )
          setting["subPlanId"] = response["id"]
          ###### develop #######
          stripe.api_key = setting["developKey"]
          #Create Product and save
          response = stripe.Product.create(
            name=setting["subProductName"],
            type="service",
            active=True
          )
          setting["subProductDevId"] = response["id"]
          #Create Plan and save
          response = stripe.Plan.create(
            amount=int(float(setting["subPlanAmount"])*100),
            currency=setting["subPlanCurrency"],
            interval=setting["subPlanInterval"],
            interval_count=1,
            product={"name": setting["subProductName"]},
          )
          setting["subPlanDevId"] = response["id"]
          return SettingModel().insertOne(data["data"])
        else:
          return {"response":{'message': 'Bad request parameters: {}'.format(data['data'])}, "code":400}
      else:
        return {"response":{'message': 'Method not allow'}, "code":400}


    def simple_payment(self, request):
      if request.method == 'POST':
        queryParams = request.args

        data = validate_simple_payment(request.get_json())
        
        if data['ok']:
            data = data["data"]
        else:
            return {"response":{'message': 'Bad request parameters: {}'.format(data['data'])}, "code":400}

        try:
          setting = {}
          if "apiKey" in queryParams:
            setting = SettingModel().findOne(queryParams["apiKey"])
            if setting["code"] == 200:
              setting = setting["response"]
            else:
              return setting
          else:
            return {"response": "You need a apiKey", "code": 400}
          
          stripe.api_key = setting["productionKey"] if setting["inProduction"] else setting["developKey"]
          customer = stripe.Customer.create(email=data.get('email'), source=data.get('stripeToken'))

          charge = stripe.Charge.create(
            customer=customer.id,
            amount=int(float(data.get('amount'))*100),
            currency=data.get('currency'),
            description=data.get('description')
          )

          return {"response": {'message': "ok"}, "code": 200}

        except stripe.error.CardError as e:

          print('Status is: %s' % e.http_status)
          print('Type is: %s' % e.error.type)
          print('Code is: %s' % e.error.code)
          # param is '' in this case
          print('Param is: %s' % e.error.param)
          print('Message is: %s' % e.error.message)

          return {"response": {'message': e.error.message}, "code": e.error.code}
        
        except stripe.error.RateLimitError as e:
          # Too many requests made to the API too quickly
          return {"response": {'message': e.error.message}, "code": e.error.code}

        except stripe.error.InvalidRequestError as e:
          # Invalid parameters were supplied to Stripe's API
          return {"response": {'message': e.error.message}, "code": e.error.code}
          
        except stripe.error.AuthenticationError as e:
          # Authentication with Stripe's API failed
          # (maybe you changed API keys recently)
          return {"response": {'message': e.error.message}, "code": e.error.code}
          
        except stripe.error.APIConnectionError as e:
          # Network communication with Stripe failed
          return {"response": {'message': e.error.message}, "code": e.error.code}
          
        except stripe.error.StripeError as e:
          # Display a very generic error to the user, and maybe send
          # Yourself an email
          return {"response": {'message': e.error.message}, "code": e.error.code}
          
        except Exception as e:
          # Something else happened, completely unrelated to Stripe
          return {"response": {'message': "Otro error"}, "code": 500}
      else:
        return {"response":{'message': 'Method not allow'}, "code":400}

    
    def plan_crud(self, request, id):    
      setting = SettingModel().findOne(id)
      if setting["code"] == 200:
        setting = setting["response"]
        #stripe.api_key = setting["productionKey"] if setting["inProduction"] else setting["developKey"]
      else:
        return setting
      
      #setting = {}
      if request.method == 'GET': 
        return SettingModel().findOne(id)
      if request.method == 'PATCH':
        data = request.get_json()
        if data["productionKey"] is not None and setting["productionKey"] != data["productionKey"]:
          setting["productionKey"] = data["productionKey"]
        if data["developKey"] is not None and setting["developKey"] != data["developKey"]:
          setting["developKey"] = data["developKey"]
        if data["inProduction"] is not None and setting["inProduction"] != data["inProduction"]:  
          setting["inProduction"] = data["inProduction"]
        if data["successfulWebhook"] is not None and setting["successfulWebhook"] != data["successfulWebhook"]:  
          setting["successfulWebhook"] = data["successfulWebhook"]
        if data["cancelWebhook"] is not None and setting["cancelWebhook"] != data["cancelWebhook"]:  
          setting["cancelWebhook"] = data["cancelWebhook"]
        if data["subProductName"] is not None and setting["subProductName"] != data["subProductName"]:
          #### Update Stripe Production ####
          stripe.api_key = setting["productionKey"]
          stripe.Product.modify(
            setting["subProductId"],
            name = data["subProductName"]
          )
          #Update Stripe Plan 
          stripe.Plan.modify(
            setting["subPlanId"],
            product = {"name": setting["subProductName"]}
          )
          #### Update Stripe Develop ####
          stripe.api_key = setting["developKey"]
          stripe.Product.modify(
            setting["subProductId"],
            name = data["subProductName"]
          )
          #Update Stripe Plan 
          stripe.Plan.modify(
            setting["subPlanId"],
            product = {"name": setting["subProductName"]}
          )
          setting["subProductName"] = data["subProductName"]
          
        return SettingModel().updateOne({"_id": id, "data":setting})
      if request.method == 'DELETE':
        stripe.api_key = setting["productionKey"]
        stripe.Plan.delete(setting["subPlanId"])
        stripe.Product.delete(setting["subProductId"])
        stripe.api_key = setting["developKey"]
        stripe.Plan.delete(setting["subPlanDevId"])
        stripe.Product.delete(setting["subProductDevId"])
        setting = {}
        setting["subProductId"] = ""
        setting["subPlanId"] = ""
        setting["subProductDevId"] = ""
        setting["subPlanDevId"] = ""
        return SettingModel().updateOne({"_id": id, "data":setting})
      else:
        return {"response":{'message': 'Bad request parameters: {}'.format(data['message'])}, "code":400}


    def customer_crud(self, request):
      queryParams = request.args    
      if request.method == 'POST':
        data = request.get_json() 
        if "email" in data and "apiKey" in data and "token" in data and "name" in data:
          client = StripeClientModel().findOneByEmail(queryParams["email"])
          if client["code"] == 200:
            return {"response":{'message': 'Usuario ya registrado'}, "code":400}
          setting = SettingModel().findOne(data["apiKey"])
          if setting["code"] == 200:
            setting = setting["response"]
            stripe.api_key = setting["productionKey"] if setting["inProduction"] else setting["developKey"]
            
            response = stripe.PaymentMethod.create(
              type = 'card',
              card = {'token': data["token"]}
            )
            stripeClient = {"settingId":data["apiKey"] , 
                            "email":data["email"], 
                            "name":data["name"], 
                            "token": data["token"], 
                            "paymentMethodId":response["id"]}
            #print("PaymentMethod: "+str(response))
            response = stripe.Customer.create(
              description = data["email"],
              payment_method = response["id"],
              name = data["name"]
            )
            stripeClient["customerId"] = response["id"]
            response = stripe.Subscription.create(
              customer=response["id"],
              items=[
                {
                  "plan": setting["subPlanId"] if setting["inProduction"] else setting["subPlanDevId"],
                },
              ]
            )
            stripeClient["subscriptionId"] = response["id"]
            return StripeClientModel().insertOne(stripeClient)
          else:
            return setting
        else:
          return {"response":{'message': 'Bad request parameters: '}, "code":400}
      if request.method == 'DELETE':
        if "email" in queryParams and "apiKey" in queryParams:
          setting = SettingModel().findOne(queryParams["apiKey"])
          if setting["code"] == 200:
            setting = setting["response"]
            stripe.api_key = setting["productionKey"] if setting["inProduction"] else setting["developKey"]
            client = StripeClientModel().findOneByEmail(queryParams["email"])
            if client["code"] == 200:
              stripe.Subscription.delete(client["subscriptionId"])
              stripe.Customer.delete(client["customerId"])
              return {"response":{'message': 'Success'}, "code":200}
            else:
              return client
          else:  
            return setting
      else:
        return {"response":{'message': 'Method not allow'}, "code":400}


    def webhook(self, request, apiKey):    
      if request.method == 'POST':  
        setting = SettingModel().findOne(apiKey)
        if setting["code"] != 200:
          return setting
          
        print("Entra en el webhook: ")
        event = request.json
        print("Tipo de evento : " + event["type"])
        # Handle the event
        if event["type"] == 'invoice.payment_succeeded':
          print('invoice.payment_succeeded')
          print("customer: " + event["data"]["object"]["customer"])
          return {"response":{'message': 'Success'}, "code":200}
        elif event["type"] == 'customer.subscription.created':
          print('customer.subscription.deleted')
          print("customer: " + event["data"]["object"]["customer"])
          client = StripeClientModel().findOneByCustomerId(event["data"]["object"]["customer"])
          if client["code"] != 200:
            print("Error: "+ str(clien["response"]))
          try: 
            r = requests.put(setting["successfulWebhook"], json={"correo":client["response"]["email"]})
            print( "Code successfulWebhook" + str(r.status_code))
          except (Exception) as e:
            print("Error successfulWebhook: " + str(e))
          return {"response":{'message': 'Success'}, "code":200}
        elif event["type"] == 'customer.subscription.deleted':
          print('customer.subscription.deleted')
          print("customer: " + event["data"]["object"]["customer"])
          client = StripeClientModel().findOneByCustomerId(event["data"]["object"]["customer"])
          if client["code"] != 200:
            print("Error: "+ str(clien["response"]))
          try:   
            response = requests.put(setting["cancelWebhook"], json={"correo":client["response"]["email"]})
            print( "Code cancelWebhook" + str(r.status_code))
          except (Exception) as e:
            print("Error cancelWebhook: " + str(e))
          return {"response":{'message': 'Success'}, "code":200}
      else:
        return {"response":{'message': 'Bad request parameters: {}'.format(data['message'])}, "code":400}

    def reset(self, request):   
      if request.method == 'GET':
        return SettingModel().reset()