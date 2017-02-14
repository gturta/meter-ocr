from flask import Flask,request
from uuid import uuid4

app = Flask(__name__)

@app.route("/image", methods=['POST'])
def uploadImage():
    ids=[]
    if 'file' not in request.files:
        abort(400)
    img = request.files['file']
    filename=str(uuid4())+'.jpg'
    ids.append(filename)
    img.save('uploads/'+filename)
    
    return ('saved {}'.format(filename), 200,
            {"Access-Control-Allow-Origin":"*"})

