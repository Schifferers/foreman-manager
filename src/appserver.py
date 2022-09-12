__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
appserver.py
- creates an application instance and runs the dev server
"""

if __name__ == '__main__':
    from minecraft_manager.main import create_app
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
