import os
import subprocess
from flask import Flask, request, redirect, send_from_directory
import socket
import mimetypes
import pyqrcode
from flask_cors import CORS

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
SHARE_PATH = "/home/black-mamba/Desktop/share"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return '''
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Upload new File</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4; }
            .navbar { overflow: hidden; background-color: #333; }
            .navbar a { float: left; display: block; color: white; text-align: center; padding: 14px 20px; text-decoration: none; }
            .navbar a:hover { background-color: #ddd; color: black; }
            .container { display: flex; justify-content: center; align-items: center; height: 80vh; }
            .box { background: white; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); padding: 40px; text-align: center; }
            .box h1 { margin-top: 0; }
            .box input[type=file] { margin: 10px 0; }
            @media screen and (max-width: 600px) {
                .container { padding: 20px; }
                .box { padding: 20px; overflow: scroll; }
            }
        </style>
    </head>
    <body>
        <div class="navbar">
            <a href="/">Home</a>
            <a href="/files">Files</a>
        </div>
        <div class="container">
            <div class="box">
                <h1>Upload Files here!</h1>
                <form action="/upload" method=post enctype=multipart/form-data>
                    <input type=file name=file>
                    <input type=submit value=Upload>
                </form>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/files')
def files():
    files = os.listdir(SHARE_PATH)
    content = '''
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Files</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4; }
            .navbar { overflow: hidden; background-color: #333; }
            .navbar a { float: left; display: block; color: white; text-align: center; padding: 14px 20px; text-decoration: none; }
            .navbar a:hover { background-color: #ddd; color: black; }
            .container { padding: 40px; }
            .box { background: white; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); padding: 20px;}
            .box h1 { margin-top: 0; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            table, th, td { border: 1px solid #ddd; }
            th, td { padding: 12px; text-align: left; }
            th { background-color: #f2f2f2; }
            .btn-danger { color: #dc3545; }
            @media only screen and (max-width: 760px) {
                .container { padding: 20px; }
                 .box { overflow: scroll;}
            }
        </style>
    </head>
    <body>
        <div class="navbar">
            <a href="/">Home</a>
            <a href="/files">Files</a>
        </div>
        <div class="container">
            <div class="box">
                <h1>Files</h1>
                <table>
                    <tr>
                        <th>File Name</th>
                        <th></th>
                        <th></th>

                    </tr>
    '''
    for file in files:
        if file.endswith('.sh'):
            content += f'''
                        <tr>
                            <td>{file}</td>
                            <td><a href="/run-script/{file}" class="btn-danger">Run Script</a></td>
                            <td><a href="/preview/{file}" target="_blank">Preview</a></td>
                        </tr>
        
            '''
        else:
            content += f'''
                        <tr>
                            <td>{file}</td>
                            <td><a href="/uploads/{file}" download>Downlaod</a></td>
                            <td><a href="/preview/{file}" target="_blank">Preview</a></td>
                        </tr>
        
            '''  
    content += '''
                </table>
            </div>
        </div>
    </body>
    </html>
    '''
    return content



@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = file.filename
        file.save(os.path.join(SHARE_PATH, filename))
        return f'File uploaded successfully: {filename}'

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(SHARE_PATH, filename)


@app.route('/preview/<filename>')
def preview(filename):
    filepath = os.path.join(SHARE_PATH, filename)
    mimetype, _ = mimetypes.guess_type(filename)
    if mimetype and mimetype.startswith('image'):
        return f'<img src="/uploads/{filename}" alt="{filename}" style="max-width: 100%;">'
    elif mimetype == 'application/pdf':
        return f'<embed src="/uploads/{filename}" type="application/pdf" width="100%" height="100%" style="margin:0; padding:0;" />'
    elif mimetype and mimetype.startswith('text'):
        with open(filepath, 'r') as f:
            text_content = f.read()
        return f'<pre>{text_content}</pre>'
    else:
        return 'Preview not available for this file type.'


@app.route('/run-script/<filename>')
def run_script(filename):
    if filename.endswith('.sh'):
        script_path = os.path.join(SHARE_PATH, filename)
        result = subprocess.run(['bash', script_path], capture_output=True, text=True)
        return f'<pre>{result.stdout}</pre>' if result.returncode == 0 else f'<pre>{result.stderr}</pre>'
    else:
        return 'Invalid script', 400

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

if __name__ == '__main__':
    ip_address = get_ip_address()
    port = 5000
    url = f'http://{ip_address}:{port}/'
    
    # Generate a dynamically sized QR code
    qr = pyqrcode.create(url, error='L', mode='binary')  # Adjusts version automatically
    
    # Display the QR code in the terminal
    print("Access the application using the following URL or scan the QR code below:")
    print(url)
    print(qr.terminal(quiet_zone=1))  # Display a smaller QR code
    
    CORS(app, resources={r"/*": {"origins": ["*"]}})
    app.run(debug=True, host='0.0.0.0', port=5000)



