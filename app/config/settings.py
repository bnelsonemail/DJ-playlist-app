"""config / settings.py."""

import os
import logging
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.pool import NullPool

# Load environment variables from a .env file
load_dotenv(find_dotenv())

# Define the base directory of the project
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Base configuration class.

    Attributes
    ----------
    SECRET_KEY : str
        Secret key for securing sessions and cookies.
    SQLALCHEMY_TRACK_MODIFICATIONS : bool
        Whether to track modifications of objects and emit signals.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """
    Configuration class for development environment.

    Attributes
    ----------
    DEBUG : bool
        Enable debug mode for Flask.
    DEBUG_TB_INTERCEPT_REDIRECTS : bool
        Enable redirect interception for the Flask Debug Toolbar.
    FLASK_ENV : str
        Set Flask environment to 'development'.
    USE_RELOADER : bool
        Enable auto-reloader for development.
    SQLALCHEMY_ECHO : bool
        Print all SQL statements to the console.
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') 
    if not SQLALCHEMY_DATABASE_URI:
        raise RuntimeError("DEV_DATABASE_URL is not set in the environment or .env file.")
    DEBUG_TB_INTERCEPT_REDIRECTS = True
    FLASK_ENV = 'development'
    USE_RELOADER = True
    SQLALCHEMY_ECHO = True
    WTF_CSRF_SECRET_KEY = 'your-secret-key'
    WTF_CSRF_ENABLED = True  # Ensure CSRF protection is enabled



class ProductionConfig(Config):
    """
    Configuration class for production environment.

    Attributes
    ----------
    DEBUG : bool
        Disable debug mode for Flask.
    FLASK_ENV : str
        Set Flask environment to 'production'.
    SQLALCHEMY_ECHO : bool
        Disable logging of SQL statements.
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') 
    FLASK_ENV = 'production'
    SQLALCHEMY_ECHO = False
    WTF_CSRF_SECRET_KEY = 'your-secret-key'
    WTF_CSRF_ENABLED = True


class TestingConfig(Config):
    """
    Configuration class for testing environment.

    Attributes
    ----------
    TESTING : bool
        Enable testing mode for Flask.
    FLASK_ENV : str
        Set Flask environment to 'testing'.
    DEBUG_TB_HOSTS : str
        Hosts to avoid showing the debug toolbar.
    SQLALCHEMY_ECHO : bool
        Log SQL statements (set to True if debugging tests).
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') 
    FLASK_ENV = 'testing'
    DEBUG_TB_HOSTS = 'dont-show-debug-toolbar'
    SQLALCHEMY_ECHO = False
    WTF_CSRF_ENABLED = False  # Disable CSRF protection for tests
    SECRET_KEY = "test-secret-key"
    SQLALCHEMY_ENGINE_OPTIONS = {'poolclass': NullPool}

    
# Configurations dictionary    
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    }


# Initialize a logger for configuration debugging
def initialize_logger():
    """
    Initialize and configure the logger for debugging configuration settings.

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Define and set a formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(console_handler)

    return logger


# Initialize the logger
logger = initialize_logger()
logger.debug("Configuration module loaded successfully.")
