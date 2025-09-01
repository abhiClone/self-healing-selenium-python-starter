from flask import Flask, request


app = Flask(__name__)


@app.route("/login")
def login():
    broken = request.args.get('broken')
    # Render login form; change id attribute for broken variant
    if broken:
        return """<!DOCTYPE html>
<html>
<head>
    <title>Login - Broken</title>
</head>
<body>
    <h1>Login Form (Broken)</h1>
    <form method='post' action='/dashboard'>
        <label for='user'>Username:</label>
        <input type='text' id='user' name='username'><br><br>
        <label for='password'>Password:</label>
        <input type='password' id='password' name='password'><br><br>
        <button type='submit'>Sign In</button>
    </form>
</body>
</html>"""
    else:
        return """<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h1>Login Form</h1>
    <form method='post' action='/dashboard'>
        <label for='username'>Username:</label>
        <input type='text' id='username' name='username'><br><br>
        <label for='password'>Password:</label>
        <input type='password' id='password' name='password'><br><br>
        <button type='submit'>Sign In</button>
    </form>
</body>
</html>"""


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    return "<h1>Welcome to Dashboard</h1>"


def run_app(port: int = 5000):
    app.run(host='127.0.0.1', port=port)