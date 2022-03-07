from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
import cv2
from werkzeug.utils import secure_filename
import numpy as np

app = Flask(__name__)


@app.route("/")
def uploader():
    path = 'static/uploads/'

    uploads = sorted(os.listdir(path), key=lambda x: os.path.getctime(
        path+x))        # Sorting as per image upload date and time
    print(uploads)
    #uploads = os.listdir('static/uploads')
    uploads = ['uploads/' + file for file in uploads]
    uploads.reverse()
    # Pass filenames to front end for display in 'uploads' variable
    return render_template("index.html", uploads=uploads)


app.config['UPLOAD_FOLDER'] = 'static/uploads'             # Storage path


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route("/upload", methods=['GET', 'POST'])
def upload_file():                                       # This method is used to upload files
    if request.method == 'POST':
        f = request.files['file']
        print(f.filename)
        # f.save(secure_filename(f.filename))
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect to route '/' for displaying images on fromt end
        return redirect("/")


#capture Frames
@app.route('/video_cap/')
def video_cap():
    inPath = 'static/uploads/'
    os.chdir(inPath)
    
    webCam = cv2.VideoCapture(0)
    currentframe = 0

    while (True):
        success, frame = webCam.read()

    # Save Frame by Frame into disk using imwrite method
        cv2.imshow("Output", frame)
        cv2.imwrite('Frame' + str(currentframe) + '.jpg', frame)
        currentframe += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    webCam.release()
    cv2.destroyAllWindows()
    return render_template('index.html')



#Capture video

@app.route('/my_record/')
def my_record():
    
    inPath = 'static/uploads/'
    os.chdir(inPath)
    
# Create an object to read camera video 
    cap = cv2.VideoCapture(0)

# Check if camera opened successfully
    if (cap.isOpened() == False): 
      print("Camera is unable to open.")

# Set resolutions of frame.
# convert from float to integer.
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

# Create VideoWriter object.
# and store the output in 'captured_video.avi' file.

    video_cod = cv2.VideoWriter_fourcc(*'XVID')
    video_output= cv2.VideoWriter('falgun.mp4',
                      video_cod,
                      10,
                      (frame_width,frame_height))

    while(True):
      ret, frame = cap.read()

      if ret == True: 
    
    # Write the frame into the file 'captured_video.avi'
        video_output.write(frame)

    # Display the frame, saved in the file   
        cv2.imshow('frame',frame)

    # Press x on keyboard to stop recording
        if cv2.waitKey(1) & 0xFF == ord('x'):
          break

  # Break the loop
      else:
        break  

# release video capture
# and video write objects
    cap.release()
    video_output.release()

# Closes all the frames
    cv2.destroyAllWindows() 
    return render_template('index.html')


#capture image

@app.route('/my_link/')
def my_link():
    inPath = 'static/uploads/'
    os.chdir(inPath)
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("test")

    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            img_name = "Captured_Img_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1
    cam.release()
    cv2.destroyAllWindows()
    return render_template('index.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
