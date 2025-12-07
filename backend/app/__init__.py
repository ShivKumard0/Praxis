from flask import Flask
from flask_cors import CORS
from .config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register Blueprints
    from .routes.health import health_bp
    from .routes.auth import auth_bp
    
    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    from .routes.kpis import kpis_bp
    from .routes.profit import profit_bp
    from .routes.incidents import incidents_bp
    
    app.register_blueprint(kpis_bp, url_prefix='/api')
    app.register_blueprint(profit_bp, url_prefix='/api')
    app.register_blueprint(incidents_bp, url_prefix='/api')
    
    from .routes.forecast import forecast_bp
    app.register_blueprint(forecast_bp, url_prefix='/api')
    
    from .routes.inventory import inventory_bp
    app.register_blueprint(inventory_bp, url_prefix='/api')
    
    from .routes.pricing import pricing_bp
    from .routes.clv import clv_bp
    from .routes.anomalies import anomalies_bp
    
    app.register_blueprint(pricing_bp, url_prefix='/api')
    app.register_blueprint(clv_bp, url_prefix='/api')
    app.register_blueprint(anomalies_bp, url_prefix='/api')
    
    return app
