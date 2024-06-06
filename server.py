from flask import Flask, render_template, request, redirect, url_for
import cv2
import easyocr
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploaded_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
reader = easyocr.Reader(["es"], gpu=False)

@app.route("/", methods=["GET", "POST"])
def index():
    recognized_text = []
    if request.method == "POST":
        # Guardar la imagen subida
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            # Leer la imagen
            image = cv2.imread(filepath)
            result = reader.readtext(image, paragraph=True)

            for res in result:
                pt0 = tuple(map(int, res[0][0]))
                pt1 = tuple(map(int, res[0][1]))
                pt2 = tuple(map(int, res[0][2]))
                pt3 = tuple(map(int, res[0][3]))

                recognized_text.append(res[1])

                cv2.rectangle(image, pt0, (pt1[0], pt1[1] - 23), (166, 56, 242), -1)
                cv2.putText(image, res[1], (pt0[0], pt0[1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1)

                cv2.rectangle(image, pt0, pt2, (166, 56, 242), 2)
                cv2.circle(image, pt0, 2, (255, 0, 0), 2)
                cv2.circle(image, pt1, 2, (0, 255, 0), 2)
                cv2.circle(image, pt2, 2, (0, 0, 255), 2)
                cv2.circle(image, pt3, 2, (0, 255, 255), 2)

            output_path = os.path.join(app.config['UPLOAD_FOLDER'], "result_" + file.filename)
            cv2.imwrite(output_path, image)
            return render_template("index.html", uploaded_image=file.filename, result_image="result_" + file.filename, recognized_text=recognized_text )

    return render_template("index.html", uploaded_image=None, result_image=None)

if __name__ == "__main__":
    app.run(debug=True)
