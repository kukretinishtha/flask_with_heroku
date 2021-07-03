import os
from flask import Flask, render_template, request, redirect, url_for
from utils import save_img, load_img, bg_remove, convert_into_base64
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'jpeg'])
upload_folder = "images"
app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return "Bg removal is live"

@app.route("/removebg", methods= ['POST', 'GET'])
def upload_file():
    image_file = request.files["image"]
    if 'image' not in request.files:
        return({"msg":"Failure", "Reason":"Image not found. Please upload the image."})
    try: 
        image_location = os.path.join(upload_folder, image_file.filename)
        image_file.save(image_location)

        new_image = load_img(image_location)
        new_image_name = 'new_'+image_file.filename+'.jpg'
        new_image_location = save_img(new_image, new_image_name, upload_folder)

        pred = bg_remove(imgpath=new_image_location, img=None)
        pred_image_name = 'pred_'+image_file.filename
        pred_location = save_img(pred, pred_image_name, upload_folder)            

        base_64_data = convert_into_base64(pred_location)

        return base_64_data
    except Exception as error:
        return({"status" : "failure", "Error" : error})



@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return "404"


if __name__ == '__main__':
    app.run(debug=True)
