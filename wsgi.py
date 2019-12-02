import os
from app import create_app

app = create_app(config_name=os.getenv("APP_ENVIRON"))

if __name__ == '__main__':
    app.run(port=7000, debug=True)
