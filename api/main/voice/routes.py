from flask import Blueprint
from flask import current_app as app
from flask import request
from main.auth import token_required
from main.user.models import User
from main import tools
from werkzeug.utils import secure_filename
import os
import uuid
from jose import jwt
from main.engine.audio import AudioAnalyzer

voice_blueprint = Blueprint("voice", __name__)

allowedFiles = set(['mp3', 'wav'])
# basedir = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.abspath(os.getcwd())

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in allowedFiles

@voice_blueprint.route("/upload/", methods=["POST"])
@token_required
def upload_mine():
	token_data = jwt.decode(request.headers.get('AccessToken'), app.config['SECRET_KEY'])

	user = app.db.users.find_one({ "id": token_data['user_id'] }, {
      "_id": 0,
      "password": 0
    })

	if not user:
		tools.JsonResp({"success": False}, 500)

	files = request.files['file']
	if files and allowed_file(files.filename):
		filename = secure_filename(files.filename)
		updir = os.path.join(basedir, 'api/uploads/')
		filename = str(uuid.uuid4()) + filename
		files.save(os.path.join(updir, filename))

		app.db.users.update_one({ "id": user["id"] }, { "$set": {
			"voice_file": filename
		} })

		print("upload success: " + filename)
		file_size = os.path.getsize(os.path.join(updir, filename))
		return tools.JsonResp({ "name": filename, "size": file_size }, 200)
	return tools.JsonResp({"success": True}, 200)

@voice_blueprint.route("/upload/dialog/", methods=["POST"])
@token_required
def upload_dialog():
	token_data = jwt.decode(request.headers.get('AccessToken'), app.config['SECRET_KEY'])

	user = app.db.users.find_one({ "id": token_data['user_id'] }, {
      "_id": 0,
      "password": 0
    })

	if not user or not user['voice_file']:
		tools.JsonResp({"success": False}, 500)

	files = request.files['file']
	if files and allowed_file(files.filename):
		dialog_file = secure_filename(files.filename)
		updir = os.path.join(basedir, 'api/uploads/')
		dialog_file = str(uuid.uuid4()) + dialog_file
		files.save(os.path.join(updir, dialog_file))

		print("upload dialog success: " + dialog_file)
		file_size = os.path.getsize(os.path.join(updir, dialog_file))

		analyzer = AudioAnalyzer(user['voice_file'], dialog_file, user['first_name'])

		analyzer.read_files()
		analyzer.preprocess_files()
		analyzer.calc_utterances()
		result = analyzer.calc_similarities()

		return tools.JsonResp({ "success": True, "result": result }, 200)

	return tools.JsonResp({"success": False}, 200)