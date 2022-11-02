import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DEBUG = True
    POSTGRES_URL="hieuvn1-postgre-server.postgres.database.azure.com"  #TODO: Update value
    POSTGRES_USER="hieuvn1@hieuvn1-postgre-server" #TODO: Update value
    POSTGRES_PW="L1ndsaylohan"   #TODO: Update value
    POSTGRES_DB="techconfdb"   #TODO: Update value
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or DB_URL
    CONFERENCE_ID = 1
    SECRET_KEY = 'IT6PobYxKVEbANaBalpHqWgqFM2X5n29uLnvIBoPxbE='
    SERVICE_BUS_CONNECTION_STRING ='Endpoint=sb://hieuvn1-service-bus.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=IT6PobYxKVEbANaBalpHqWgqFM2X5n29uLnvIBoPxbE=' #TODO: Update value
    SERVICE_BUS_QUEUE_NAME ='notificationqueue'
    ADMIN_EMAIL_ADDRESS: 'ngochieuvnu@gmail.com'
    SENDGRID_API_KEY = '' #Configuration not required, required SendGrid Account

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False