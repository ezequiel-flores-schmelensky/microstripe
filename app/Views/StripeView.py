# coding=utf-8
from app import app
from flask import request, jsonify
from Controllers import *

@app.route('/', methods=['GET'])
def test():
    return StripeController().get()


""" Setting """
@app.route('/settings', methods=['POST'])
def setting_crud():
    response = StripeController().setting_crud(request)
    return jsonify(response['response']), response['code']


"""" Simple Payment """
@app.route('/simple-payment', methods=['POST'])
def simple_payment():
    response = StripeController().simple_payment(request)
    return jsonify(response['response']), response['code']


""" Create and Delete Subscription """
@app.route('/plan/<id>', methods=['GET', 'PATCH', 'DELETE'])
def plan_curd(id):
    response = StripeController().plan_crud(request, id)
    return jsonify(response['response']), response['code']


""" Create and Delete Subscription """
@app.route('/customer', methods=['POST'])
def customer_curd():
    response = StripeController().customer_crud(request)
    return jsonify(response['response']), response['code']


""" Webhook """
@app.route('/webhook/<apiKey>', methods=['POST'])
def webhook(apiKey):
    response = StripeController().webhook(request,apiKey)
    return jsonify(response['response']), response['code']


@app.route('/reset', methods=['GET'])
def reset():
    response = StripeController().reset(request)
    return jsonify(response['response']), response['code']
