import os
from flask import Flask
from .db import init_db

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'demo_users.db'),
    )
    
    if test_config is not None:
        app.config.update(test_config)
        
    try:
        os.makedirs(app.instance_path)  
    except OSError:
        pass
    
    init_db(app.config['DATABASE'])
    
    from . import routes 
    app.register_blueprint(routes.bp)
    
    return app