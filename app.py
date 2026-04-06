import os
from flask import Flask, request, render_template, send_from_directory, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'mobile_share_key'

# 共有フォルダの準備
UPLOAD_FOLDER = 'shared_files'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
PASSWORD = "1234" # スマホで打つ共通パスワード

@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('index.html', view='login')
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', view='share', files=files)

@app.route('/login', methods=['POST'])
def login():
    if request.form.get('password') == PASSWORD:
        session['logged_in'] = True
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if file and file.filename != '':
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
