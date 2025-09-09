#from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginManager
#from flask_bcrypt import Bcrypt
#from .web_routes import routes
#from .auth_routes import auth
#from .api_routes import api

#db = SQLAlchemy()
#bcrypt = Bcrypt()
#login_manager = LoginManager()

#def create_app():
#    app = Flask(__name__)
#    app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
#    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#    db.init_app(app)
#    bcrypt.init_app(app)
#    login_manager.init_app(app)

#    login_manager.login_view = 'auth.login'

    # Importa e registra os blueprints
#    from .routes.web_routes import routes as routes_blueprint
#    from .routes.auth_routes import auth as auth_blueprint
#   from .routes.api_routes import api as api_blueprint

#    app.register_blueprint(routes_blueprint)
#    app.register_blueprint(auth_blueprint)
#    app.register_blueprint(api_blueprint, url_prefix="/api")
