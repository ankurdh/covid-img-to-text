import cv2
from flask import Flask
from flask import request
from flask import Response
import json
import uuid

from ocr.JKOcrParser import JKOcrParser
from ocr.PunjabOcrParser import PunjabOcrParser

app = Flask(__name__)


def get_class(s):
    if s.lower() == 'punjab':
        return PunjabOcrParser

    if s.lower() == 'jk' or s.lower() == 'jammukashmir' or s.lower() == 'jammuandkashmir':
        return JKOcrParser

    return None


@app.route("/ocr", methods=['POST'])
def ocr():
    if 'state' not in request.headers:
        return Response('{"Error": "No state in header"}', status=408, mimetype='application/json')

    s = request.headers['state']
    state = get_class(s)
    if not state:
        return Response('{"Error": "Invalid state. Allowed values: punjab, jk"}', status=409, mimetype='application/json')

    if 'img' not in request.files:
        return Response('{"Error":"Must have a file in form data", "Example usage": "curl --location --request POST '
                        '\'http://localhost:5000/ocr\' --header \'state: punjab\' --form '
                        '\'img=@/Users/huralikoppia/code/covid-img-to-text/data/punjab/sample1.jpg\'"}', status=408,
                        mimetype='application/json')

    f_name = '%s.jpg' % uuid.uuid1()
    img = request.files['img']
    img.save(f_name)
    i = cv2.imread(f_name)
    o = state(i)
    unprocessed, processed = o.parse()
    return Response(json.dumps(processed), status=201, mimetype='application/json')


if __name__ == "__main__":
    app.run(threaded=True, debug=True)
