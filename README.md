# Mailchimp Signup Utility
Tool that enables you to sign up people to your Mailchimp mailing list through an API or API-Like interface - useful for copying people between lists for example. If the signup is successful, the user will get a thank you notice. If it fails, they'll get an error message. If no email is provided they'll be shown a signup form.

The app uses Flask for the server, Semantic-UI for the design, and Mailchimp for the mailing list. The experimental version **can be used directly with AWS Lambda** to avoid running a server all the time, using [flask-zappa](https://github.com/Miserlou/flask-zappa).

## Setup (traditional)
You'll need to configure the `settings.py` file with your Mailchimp API Key, LIST URL and your POST URL for submitting forms. Then:
```bash
sudo pip install -r requirements.txt
python app.py
```

## Setup (AWS Lambda experimental)
You'll need to have `aws` set up on your computer, with `~/.aws/config` and `~/.aws/credentials` in place. You will also need to set up [flask-zappa](https://github.com/Miserlou/flask-zappa) by hand as it is not in pip yet.

Configure your zappa_settings.json file with your bucket and project name at a minimum. Then:
```bash
flask-zappa deploy production thf_settings.json
# to update use update instead of deploy
```
You'll likely want CORS enabled, for that you have to go into the AWS API Endpoint console, click 'Enable CORS', then 'Deploy', select a stage, 'Deploy'. It's really confusing. 