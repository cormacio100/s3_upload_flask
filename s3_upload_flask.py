from flask import Flask, render_template, request, redirect, url_for
#   boto3 is a Python library that will generate the pre-signed POST request
import os, json, boto3

app = Flask(__name__)

"""
LOAD THE FORM CONTAINING FILE UPLOAD
"""
@app.route('/account/')
def account():
    return render_template('account.html')


"""
View responsible for:
    -   generating and returning the signature with which the client-side Javascript can upload the image
The View:
    -   receives request for signature and S3 Bucket name is loaded from (HEROKU) environment
    -   File name and MIME type extracted from GET parameters
    -   S3 Client is constructed using boto3 library
        -   AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY set earlier are automatically read from the environment
    -   Pre-signed POST request is then generated using the generate_presigned_post function
Returned:
    -   The pre-signed request data and the location of the eventual file on S3 are returned to the client as JSON
"""
@app.route('/sign_s3')
def sign_s3():
    S3_BUCKET = os.environ.get('S3_BUCKET')

    file_name = request.args.get('file_name')
    file_type = request.args.get('file_type')

    s3 = boto3.client('s3')

    presigned_post = s3.generate_presigned_post(
        Bucket = S3_BUCKET,
        Key = file_name,
        Fields = {"acl":"public-read", "Content-Type":file-type},
        Conditions = [
            {"acl":"public-read"},
            {"Content-Type":file_type}
        ],
        ExpiresIn = 3600
    )

    return json.dumps({
        'data': presigned_post,
        'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)    #   could perform a check at this time for file type
    })


"""
View responsible for receiving the account information after the user has:
-   uploaded an avatar
-   filled in the form
-   clicked submit

This is a POST Request also an 'allowed access method'
"""
@app.route('/submit_form/',methods=["POST"])
def submit_form():
    username = request.form['username']
    full_name = request.form['full-name']
    avatar_url = request.form['avatar-url']

    update_account(username, full_name, avatar_url)

    return redirect('/profile/')

"""
VIEW is a PLACEHOLDER.
Code should be included here to SAVE THE DETAILS TO A DB
and correctly asssociate the information with the rest of the user's account details
"""
def update_account(username,full_name, avatar_url):
    return render_template('update_account.html')

"""
VIEW is a PLACEHOLDER for the users PROFILE
"""
@app.route('/profile/')
def profile():
    return render_template('profile.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT',5000))
    app.run(host='127.0.0.1',port=port)


