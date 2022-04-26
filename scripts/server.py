from flask import Flask, request, jsonify
import os
from uuid import uuid4
from handler_db import get_results

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
if not os.path.exists(UPLOAD_FOLDER): os.mkdir(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.post('/upload')
def upload_data():
    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({"message": "Request has no file part"}), 400
   

    file = request.files['file']
    if file and allowed_file(file.filename):
        id = str(uuid4())
        filename = id + '.' + file.filename.rsplit('.', 1)[1].lower()
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # saves the file 
        file.save(file_path)
        if os.path.exists(file_path):
            return jsonify({"id": id,
            "message" : "upload succesful!"}), 201
        else:
            return jsonify(
              {"message": "something went wrong, couldn't save the file!"}
              ), 500
    else:
        return jsonify(
          {"message" : "File extension not valid, accepted file extensions are " \
            + str(ALLOWED_EXTENSIONS)}), 400
    

@app.get('/results/<id>')
def handle_result(id):
  data = get_results(id)
  if data is None:
    return jsonify({"message": "No results found for this id"}), 404
  else:
    res = {
      "id": id,
      "generated_on": data["datetime"],
      "freq_items": data["frequent_items"],
      "rules": data["association-rules"]
    }

    return jsonify(res), 200 


@app.get('/frequent_itemsets/<id>')
@app.get('/rules/<id>')
def handle_frequent_itemsets(id):
  data = get_results(id)
  
  if data is None:
    return jsonify({"message": "No results found for this id"}), 404  
  
  else:
    res = None
    if request.url_rule.rule == '/frequent_itemsets/<id>':
      res = {
        "id": id,
        "generated_on": data["datetime"],
        "freq_items": data["frequent_items"]
      }   
    else:
      res = {
        "id": id,
        "generated_on": data["datetime"],
        "rules": data["association-rules"]
      }

    return jsonify(res), 200



if __name__ == "__main__":
    app.run(debug=True)


"""
ENDPOINTS 
- /upload
- /results/<id>
- /frequent_itemsets/<id>
- /rules/<id>
"""


"""
- Add a file size limit
"""