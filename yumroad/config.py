import os 


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'c4d0da177fdf41b68da0f6728e86845f')
    

class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI="sqlite:///dev.db"
    SQLALCHEMY_ECHO = True
    SECRET_KEY= os.getenv('SECRET_KEY','c4d0da177fdf41b68da0f6728e86845f' )
    

class TestConfig(BaseConfig):
    TESTING = True 
    SQLALCHEMY_DATABASE_URI="sqlite:///test.db"
    SQLALCHEMY_ECHO = True
    WTF_CSRF_ENABLED = False
    

class ProdConfig(BaseConfig):
     SECRET_KEY= os.getenv('SECRET_KEY')


configurations = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "test": TestConfig
}