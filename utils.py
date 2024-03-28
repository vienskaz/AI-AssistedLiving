import cv2
from tensorflow.keras.models import load_model
import numpy as np
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def resize_image(image, target_size=(640, 480)):
    normalized = image / 255.0
    arr = cv2.resize(normalized, target_size)
    return np.array(arr)


def detect(preprocessed_image):
    model = load_model("C:/Users/User/Desktop/detect/stand_lie.h5")
    result = model.predict(preprocessed_image.reshape(
        1, *preprocessed_image.shape))

    prediction = np.argmax(result)

    if prediction == 0:
        print("lezy")
        return True

    else:
        print("stoi")
        return False


def send_alert():

    email_host = 'smtp.gmail.com'
    email_port = 587
    email_login = 'alert.faint.bot@gmail.com'
    # email_password = 'alertbotfaint'
    email_password = 'dlic msqh wtsw ljcd'

    msg = MIMEMultipart()
    msg['From'] = email_login
    msg['To'] = 'adwiesek@wp.pl'
    msg['Subject'] = 'ALERT!!!!!'

    messege = 'ALERT the patient has fainted!!!!!!'
    msg.attach(MIMEText(messege, 'plain'))

    with open("C:/Users/User/Desktop/detect/ss.jpg", "rb") as attachment:
        image_mime = MIMEImage(attachment.read())
        image_mime.add_header('Content-Disposition',
                              'attachment', filename="image.jpg")
        msg.attach(image_mime)

    server = smtplib.SMTP(email_host, email_port)
    server.starttls()
    server.login(email_login, email_password)

    text = msg.as_string()
    server.sendmail(email_login, 'adwiesek@wp.pl', text)

    server.quit()
