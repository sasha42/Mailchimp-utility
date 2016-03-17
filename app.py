import json, requests, sys, time, ast
from collections import OrderedDict
from flask import Flask, request, send_from_directory, render_template, jsonify
from flask.ext.cors import CORS

app = Flask(__name__, static_url_path='/static')
CORS(app)
app.config.from_pyfile('settings.py')

url = app.config['MAILCHIMP_LIST_URL']
api_key = app.config['MAILCHIMP_API_KEY']

def signup(email, ip):
    """Communicates with the Mailchimp API, returns error status"""
    error = False
    error_detail = ""
    if email != None:
        print("submitting")
        data = {'email_address': str(email), 'status': 'subscribed', 'ip_opt': ip}
        headers = {'Content-Type': 'application/json'}
        try:
            r = requests.post(url, data=json.dumps(data), headers=headers, auth=("apikey", api_key))
            print r.json()
            if r.status_code == 200:
                error = False
            elif r.status_code == 400:
                error = True
                error_detail = r.json()['detail']
                print(r.text)
            else:
                error = True
                error_detail = "Something broke... try again later"
        except:
            error = True
            error_detail = "Something broke... try again later"
        return error, error_detail

@app.route('/', methods=['POST', 'OPTIONS'])
def signup_api():
    """API endpoint with AWS Lambda-specific stuff""" 
    if request.method == 'OPTIONS':
    # for CORS pre-flight check
        print "api options"
        return jsonify(request="options")
    else:
        email = ast.literal_eval(request.data)['email']
        ip = request.headers.get('X-Forwarded-For').split(',')[0]
        print "api post", email, ip
        error, error_detail = signup(email, ip)
        return jsonify(email=email, error=error, error_detail=error_detail)



@app.route('/signup')
def signup_generic():
    """Generic signup method which works on any server"""
    email = ""
    email = request.args.get('email')
    ip = request.remote_addr
    error = ""
    error_detail = ""
    if email != None:
        error, error_detail = signup(email, ip)
    return render_template('thanks.html', email=email, error=error, error_detail=error_detail, mailchimp_url=app.config['MAILCHIMP_POST_URL'])

@app.route('/static')
def serve_static(path):
    return send_from_directory('/static', path)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8005)