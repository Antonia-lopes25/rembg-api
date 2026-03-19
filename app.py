from flask import Flask, request, jsonify
from rembg import remove
from PIL import Image
import io, base64

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/remove', methods=['POST'])
def remove_bg():
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({'error': 'Campo image obrigatorio'}), 400
    img_bytes = base64.b64decode(data['image'])
    input_img = Image.open(io.BytesIO(img_bytes))
    output_img = remove(input_img)
    buf = io.BytesIO()
    output_img.save(buf, format='PNG')
    result = base64.b64encode(buf.getvalue()).decode()
    return jsonify({'image': result, 'mimeType': 'image/png'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)