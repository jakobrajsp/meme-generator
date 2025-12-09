import os
import uuid
from flask import Flask, request, redirect, url_for, send_from_directory

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["GENERATED_FOLDER"] = "generated"

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["GENERATED_FOLDER"], exist_ok=True)

from PIL import Image, ImageDraw, ImageFont

DEFAULT_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    
@app.route("/", methods=["GET"])
def index():
    return """
    <h1>Meme Generator</h1>
    <form action="/generate" method="post" enctype="multipart/form-data">
      <div><input type="file" name="image" accept="image/*" required></div>
      <div><input type="text" name="top_text" placeholder="Zgornji tekst"></div>
      <div><input type="text" name="bottom_text" placeholder="Spodnji tekst"></div>
      <div><button type="submit">Ustvari meme</button></div>
    </form>
    """



@app.route("/generate", methods=["POST"])
def generate():
    file = request.files.get("image")
    if not file or file.filename == "":
        return redirect(url_for("index"))

    in_name = f"{uuid.uuid4().hex}_{file.filename}"
    in_path = os.path.join(app.config["UPLOAD_FOLDER"], in_name)
    file.save(in_path)

    top_text = (request.form.get("top_text") or "").upper()
    bottom_text = (request.form.get("bottom_text") or "").upper()

    img = Image.open(in_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    W, H = img.size
    font_size = max(20, int(W * 0.06))
    try:
        font = ImageFont.truetype(DEFAULT_FONT_PATH, font_size)
    except Exception:
        font = ImageFont.load_default()

    def draw_centered_line(text, y):
        if not text:
            return
        bbox = draw.textbbox((0, 0), text, font=font, stroke_width=3)
        w = bbox[2] - bbox[0]
        x = (W - w) // 2
        draw.text((x, y), text, font=font, fill="white", stroke_width=3, stroke_fill="black")

    margin = max(10, int(H * 0.03))
    draw_centered_line(top_text, margin)               
    draw_centered_line(bottom_text, H - margin - font_size)  

    out_name = f"{uuid.uuid4().hex}.jpg"
    out_path = os.path.join(app.config["GENERATED_FOLDER"], out_name)
    img.save(out_path, "JPEG", quality=90)

    return f"""
    <h2>Tvoj meme</h2>
    <img src="/generated/{out_name}" style="max-width: 600px; display:block; margin-bottom:12px;">
    <div><a href="/">Nazaj</a></div>
    """

@app.route("/generated/<name>")
def serve_generated(name):
    return send_from_directory(app.config["GENERATED_FOLDER"], name, mimetype="image/jpeg")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
