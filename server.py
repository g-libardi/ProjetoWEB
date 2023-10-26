from gunicorn.app.base import BaseApplication
from app import app

class GUnicornFlaskApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        for key, value in self.options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key, value)

    def load(self):
        return self.application
    
if __name__ == '__main__':
    options = {
        'bind': '0.0.0.0:50135',
        'workers': 1,
    }
    GUnicornFlaskApplication(app, options).run()