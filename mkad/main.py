from mkad.settings import AppSettings
from mkad.app.api import app


if __name__=='__main__':
    app.run(host= '0.0.0.0', port=AppSettings.get_int('api_port'))