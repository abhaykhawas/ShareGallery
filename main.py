from flask import Flask, request, render_template, redirect, jsonify
import json
import os
import base64
import random
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

UPLOAD_FOLDER = 'static'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        data = request.get_json()
        base64_image = data.get('imageFile')
        image_data = base64.b64decode(base64_image)
        username = data.get('username')


        # Generate a filename (you can modify this as needed)
        random_num = str(random.randint(100000, 999999))
        filename = f'{random_num}.png'
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        f = open('data.json', 'r')

        f = json.loads(f.read())

        if username in f:
            f[username].append(f'{random_num}.png')
        else: 
            f[username] = [f'{random_num}.png']

    
        

        fi = open('data.json', 'w')
        json.dump(f, fi, indent=2)
        fi.close()
            

        # Save the binary image data to a file
        with open(file_path, 'wb') as f:
            f.write(image_data)

        return jsonify({'message': f'Image saved successfully to {file_path}'}), 200

@app.route('/username', methods=['POST'])
def username():
    if request.method == 'POST':
        return "SUCCESS"

@app.route('/images', methods=['GET'])
def get_images():
    folder_path = "static" 

    file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    return jsonify({'images': file_names}), 200

@app.route('/delete', methods=['POST'])
def delete():
    img_id = json.loads(request.data)['image_id']
    file_path = f'static/{img_id}.png'
    if os.path.exists(file_path):
        os.remove(file_path)
        return "Cool"
    return "Something went wrong"

if __name__ == '__main__':
    app.debug = True
    app.run(host=os.getenv('HOST'), port=os.getenv('PORT'))