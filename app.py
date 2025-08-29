from flask import Flask, request, jsonify
import easyocr, tempfile, os

app = Flask(__name__)
reader = easyocr.Reader(['en','ch_sim'])

@app.route("/health", methods=["GET"])
def health():
    return "ok", 200

@app.route("/ocr", methods=["POST"])
def ocr():
    if 'file' not in request.files: return jsonify(error="no file"), 400
    f = request.files['file']
    if f.filename == '': return jsonify(error="empty"), 400
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    f.save(tmp.name)
    
    try:
        lines = reader.readtext(tmp.name, detail=0, paragraph=True)
        text = "\n".join(t.strip() for t in lines if t.strip())
        return jsonify(text=text)
    finally:
        if os.path.exists(tmp.name): os.remove(tmp.name)
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
