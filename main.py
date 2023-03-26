from flask import Flask, request, jsonify
import requests
from werkzeug.datastructures import FileStorage
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*")
            

MESHULAM_PAGE_CODE = 'b73ca07591f8' # generic-page
    #credit: '0b7a16e03b25'
    #google-pay: '77a2993849cd'
    #apple-pay: '9eeea7787d67'
    #bit: 'e20c9458e9f3'
    #bit QR: '39bf173ce7d0'
MESHULAM_USER_ID = '4ec1d595ae764243'
MESHULAM_API_URL = 'https://sandbox.meshulam.co.il/api/light/server/1.0/'
successUrl = "https://localhost:44374/static/success.html?success=1"
failureUrl = "https://localhost:44374/static/failure.html?failure=1"

@app.route('/')
def index():
    return app.send_static_file('index.html')
 

@app.route('/api/payment/getPaymentLink', methods=['POST'])
def get_payment_link():

    sum = request.json['sum']
    paymentsNum = request.json['paymentsNum']
    description = request.json['description']

    formData = {
        'pageCode': MESHULAM_PAGE_CODE,
        'userId': MESHULAM_USER_ID,
        'sum': sum,
        'paymentNum': str(paymentsNum),
        'description': description,
        'transactionTypes': ['1', '6', '13', '14'], #[Credit, Bit, ApplePay, GooglePay] If you don't need one of them, give it a value of '1'
        'successUrl': "http://localhost:5000/static/success.html?success=1",
        'cancelUrl': "http://localhost:5000/static/failure.html?failure=1",
        # With the help of cFields you can transfer information that will be retrieved on the success page (limited to 5 cFields)
        'cField1': MESHULAM_PAGE_CODE,
        'cField2': 'blabla',
        'cField3': 'blabla',
        'cField4': 'blabla',
        'cField5': 'blabla',   
        # Here you can use the two parameters you chose for your payment-page. In this case full name and phone number.
        # You can send them here, or not and the user will fill them in
        "pageField[fullName]": 'John Smit',
        "pageField[phone]": '0500000000',
    }

    form = {}
    for key, value in formData.items():
        if key == 'transactionTypes':
            form[key] = []
            for item in value:
                form[key].append(item)
        else:
            form[key] = value
            
    try:
        print(form)
        response = requests.post(f'{MESHULAM_API_URL}createPaymentProcess', data=form)
        data = response.json()
        status = data['status']

        url = data['data']['url'] if 'data' in data and 'url' in data['data'] else None
        message = data['err']['message'] if 'err' in data and 'message' in data['err'] else None
        result = {
            'isSuccess': int(status) > 0,
            'message': url if int(status) > 0 else message
        }
        return jsonify(result)
    except Exception as e:
        return '', 500

if __name__ == '__main__':
    app.run(debug=True)
