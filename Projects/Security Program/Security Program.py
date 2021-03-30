from cv2 import *
from datetime import datetime
import numpy as np
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Code to send email when motion is detected
def sendEmail():
	print("sending")
	fromaddr = "motionalertsender@gmail.com"  # Email address that sends alerts
	toaddr = "aryansaw03@gmail.com"  # Email address that recieves alerts
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "MOTION DETECTED"
	body = ""
	msg.attach(MIMEText(body, 'plain'))
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login("motionalertsender@gmail.com", "motionalertpassword")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)


# Initialize webcam
cap = VideoCapture(0)

# Read first frame
_, frame = cap.read()
last_frame = frame

# Variables for motion detection
threshold = 120000
record_buffer_max = 15
record_buffer = 0

# Variables for email notification
emailSent = True

# Initialize and create variables for video and photo output
fourcc = VideoWriter_fourcc(*'XVID')
numFiles1 = len(next(os.walk("output_files"))[2])
output = VideoWriter("output_files/cctv_of_movement_" + str(numFiles1) + ".avi", fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

# Pre-trained face detection classifier
face_cascade = CascadeClassifier('face_haarcascade.xml')

# Continuous while loop to capture frames
while True:
	# Current time and frame
	now = datetime.now()
	_, frame = cap.read()
	net_diff = 0.0

	# Convert to grayscale
	gray_curr = cvtColor(frame, COLOR_BGR2GRAY)
	gray_prev = cvtColor(last_frame, COLOR_BGR2GRAY)

	# Subtract frames
	diff = subtract(gray_curr, gray_prev)

	w = np.size(diff, 0)
	h = np.size(diff, 1)

	# Find total difference by summing up diff array (computing every 5th pixel in order to save computing space)
	for i in range(0, w):
		for j in range(0, h):
			if i % 5 == 0 and j % 5 == 0:
				r = diff[i, j]
				g = diff[i, j]
				b = diff[i, j]
				net_diff += (r + g + b)

	# Check if total difference is above a preset threshold so that extremely minor movement is not detected.
	if net_diff > threshold:
		record_buffer = record_buffer_max

	# Draw rectangle and date/time stamp
	rectangle(frame, (int(cap.get(3)) - 254, int(cap.get(4) - 70)), (int(cap.get(3)) - 30, int(cap.get(4) - 35)), (0, 0, 0), -10)
	putText(frame, now.strftime("%d/%m/%y %H:%M:%S"), (int(cap.get(3)) - 250, int(cap.get(4) - 50)), FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

	# Draw "No Movement Detected" if no movement is detected and "Movement Detected" if movement is detected.
	# Send email if movement is detected
	# Capture video footage if movement is detected and save to folder
	# Capture faces if movement is detected and save them to folder
	if record_buffer < 0:
		putText(frame, "No Movement Detected", (20, 20), FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
		emailSent = False
	else:
		putText(frame, "Movement Detected", (20, 20), FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
		if not emailSent:
			sendEmail()
			emailSent = True
		output.write(frame)
		faces = face_cascade.detectMultiScale(gray_curr, 1.1, 4)
		for (x, y, w, h) in faces:
			output_folder = "output_files/faces_caught"
			numFiles2 = len(next(os.walk("output_files/faces_caught"))[2])
			imwrite(output_folder + "/" + str(numFiles2) + ".jpg", frame[y:y + h, x:x + w])

	record_buffer -= 1
	if record_buffer < -100:
		record_buffer = -100

	# Show video and make quit key
	imshow("Frame", frame)
	last_frame = frame
	if waitKey(1) == ord('q'):
		break

# Cleanup
cap.release()
output.release()
destroyAllWindows()
