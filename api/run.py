import os

from app import create_app

config_name = os.getenv('APP_SETTINGS', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    app.run(app.run(host='0.0.0.0', port=os.getenv('PORT', 5000))
)
