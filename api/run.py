from main import create_app
import logging

if __name__ == "__main__":
  app = create_app()
  app.secret_key = "secret key"
  # app.run(host=app.config["FLASK_DOMAIN"], port=app.config["FLASK_PORT"])
  from waitress import serve
  print("Server started at %d" % app.config["FLASK_PORT"])
  serve(app, host="0.0.0.0", port=5000)
else:
  logging.basicConfig(app.config["FLASK_DIRECTORY"] + "trace.log", level=logging.DEBUG)