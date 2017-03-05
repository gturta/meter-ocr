from flask import Flask,request,json,make_response,url_for,send_from_directory
from uuid import uuid4
from os import mkdir,path
from lib.meter import MeterOCR

app = Flask(__name__)

@app.route("/image", methods=['POST'])
def uploadImage():
    if 'file' not in request.files:
        abort(400)
    img = request.files['file']
    imgId = str(uuid4())
    filename=imgId+'.jpg'
    mkdir('uploads/'+imgId)
    img.save('uploads/'+imgId+'/'+filename)
    return (imgId, 200,
            {"Access-Control-Allow-Origin":"*"})

#expected: {
#  img:<path_to_image>,
#  band:<path_to_image>, 
#  image_digits:[<path_to_image>, ...<path_to_image>],
#  identified_digits:[d0,...d8]
#}
@app.route("/image/<fileid>", methods=['GET'])
def getResults(fileid):
    folder="uploads/"+fileid+"/"
    img=fileid+".jpg"

    mocr = MeterOCR(img,folder,debug=True)
    res = mocr.process()
    print([r[0] for r in res])

    image_digits = [path.join(fileid,"d{}.jpg".format(d)) \
                    if path.exists(path.join(folder,"d{}.jpg".format(d))) \
                    else ""
                    for d in range(len(res))]
    print(image_digits)

    return make_response(
        json.dumps({
            'img':url_for('uploads',filename=path.join(fileid,img)),
            'band':url_for('uploads',filename=path.join(fileid,"digitband.jpg")),
            'image_digits':[url_for('uploads',filename=d)\
                            if d is not "" else d for d in image_digits],
            'identified_digits':[r[0] for r in res]}),
        200, {"Access-Control-Allow-Origin":"*"})

@app.route("/uploads/<path:filename>", methods=['GET'])
def uploads(filename):
    return send_from_directory('uploads',filename)
