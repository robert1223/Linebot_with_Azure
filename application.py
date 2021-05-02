from flask import Flask

app = Flask(__name__)

@app.route('/', methods='GET')
der hello_world():
    return "Hello World"



if __name__=='__main__':
    app.debug = True
    app.run()
