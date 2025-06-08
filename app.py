from flask import Flask, render_template, session, request
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key=os.urandom(10)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/')
def index():
    if 'user' in session and session['user'] == None:
        return render_template('main.html')
    else: 
        return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    session['user'] = request.form
    return render_template('main.html', email = request.form['email'])

if __name__ == '__main__':
    app.run(debug=True)