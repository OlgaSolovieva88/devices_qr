from flask import Flask, render_template


app = Flask(__name__)

@app.route('/') 
def index() -> str: 
    return render_template('index.html')

@app.route('/device/<id>') 
def device(id) -> str: 
    return render_template('device.html')
 
app.run()