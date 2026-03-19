from flask import Flask, request, jsonify
from rembg import remove, new_session
from PIL import Image
import io, base64

app = Flask(__name__)
session = new_session("u2netp")

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/remove', methods=['POST'])
def remove_bg():
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({'error': 'Campo image obrigatorio'}), 400
    img_bytes = base64.b64decode(data['image'])
    input_img = Image.open(io.BytesIO(img_bytes)).convert('RGBA')
    input_img.thumbnail((1024, 1024), Image.LANCZOS)
    output_img = remove(input_img, session=session)
    buf = io.BytesIO()
    output_img.save(buf, format='PNG', optimize=True)
    result = base64.b64encode(buf.getvalue()).decode()
    return jsonify({'image': result, 'mimeType': 'image/png'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860
