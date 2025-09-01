from flask import Flask, request, redirect, Response
import os

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return redirect('/login')

    @app.route('/login')
    def login():
        file_path = os.path.join(os.path.dirname(__file__), '..', 'demo_app', 'login.html')
        with open(file_path, 'r', encoding='utf-8') as f:
            html = f.read()
        if request.args.get('variant') == 'broken':
            html = (html
                    .replace('id="username"', 'id="user"')
                    .replace('name="username"', 'name="user"')
                    .replace('>Username<', '>User ID<'))
        return Response(html, mimetype='text/html')

    @app.route('/dashboard')
    def dashboard():
        return '<h1>Dashboard</h1><p>You made it 🎉</p>'

    return app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '3000'))
    create_app().run(host='127.0.0.1', port=port, debug=False, use_reloader=False)
