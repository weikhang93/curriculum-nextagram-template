import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or os.urandom(32)
    S3_BUCKET = os.environ.get("S3_BUCKET_NAME")
    S3_KEY = os.environ.get("S3_ACCESS_KEY")
    S3_SECRET = os.environ.get("S3_SECRET_ACCESS_KEY")
    S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
    BRAINTREE_MERCHANT_ID= os.environ.get("BRAINTREE_MERCHANT_ID")
    BRAINTREE_PUBLIC_KEY= os.environ.get("BRAINTREE_PUBLIC_KEY")
    BRAINTREE_PRIVATE_KEY= os.environ.get("BRAINTREE_PRIVATE_KEY")
    MAILGUN_DOMAIN= os.environ.get("MAILGUN_DOMAIN")
    MAILGUN_API_KEY= os.environ.get("MAILGUN_API_KEY")
    GOOGLE_OAUTH_CLIENT_ID=os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    GOOGLE_OAUTH_CLIENT_SECRET=os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")

    # MUST CAP FOR ATTRIBUTE NAME AS WELL OTHERWISE SHIT WONT WORK
    # MUST CAP FOR ATTRIBUTE NAME AS WELL OTHERWISE SHIT WONT WORK
    # MUST CAP FOR ATTRIBUTE NAME AS WELL OTHERWISE SHIT WONT WORK
    


    


class ProductionConfig(Config):
    DEBUG = False
    ASSETS_DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    ASSETS_DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    ASSETS_DEBUG = False

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    ASSETS_DEBUG = True
