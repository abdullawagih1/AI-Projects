import cv2
import time

# Open camera
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()

    # Get current time
    current_time = str(time.ctime())
    cv2.putText(frame, current_time, (10, 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 2)

    # Convert image to grayscale
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Clean up image using Gaussian Blur
    blur_img = cv2.GaussianBlur(img_gray, (5, 5), 0)

    # Extract edges
    can_img = cv2.Canny(blur_img, 1, 50)

    # Making threshold to convert a grey scale image to it's binary form
    ret, mask = cv2.threshold(can_img, 50, 255, cv2.THRESH_BINARY)

    # Horizontal flipping
    final_image = cv2.flip(mask, 1)

    # Show image
    cv2.imshow('Our Live Sketcher', final_image)

    # To exit from live, press Esc key
    if cv2.waitKey(1)& 0xFF == 27: #27 is the Esc Key
        break

# Release camera and close windows
cap.release()
cv2.destroyAllWindows()