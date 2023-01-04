import os

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    return username == os.getenv("USERNAME") and password == os.getenv("PASSWORD")

@app.route('/login')
@auth.login_required
def login():
    return 'Please login with your username and password'
