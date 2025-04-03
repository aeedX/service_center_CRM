from flask import Flask, request, redirect, render_template, url_for, send_file

import forms
import stuff

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ZxrC#@wx-%08xKA9w-#ug2YB8c-A4IWoN#y'

@app.route('/')
def index():
    user = request.cookies.get('user')
    if user:
        return redirect('/dashboard')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        return redirect('/dashboard')
    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    return send_file(stuff.create_qr('http://127.0.0.1:8080/dashboard'), mimetype='image/png')

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
