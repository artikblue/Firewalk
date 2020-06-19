import quart
from views import fireapi
#from views import home
from config import settings
import services.fireservice
from mongoengine import connect
from quart_cors import cors, route_cors




app = quart.Quart(__name__)
app = cors(app)

is_debug = True
connect("flat_renting")

#app.register_blueprint(home.blueprint)
app.register_blueprint(fireapi.blueprint)


def configure_app():
    mode = 'dev' if is_debug else 'prod'
    data = settings.load(mode)


def run_web_app():
    app.run(debug=is_debug, port=5001)


configure_app()

if __name__ == '__main__':
    run_web_app()