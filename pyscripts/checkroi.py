import cv2
from ultralytics import YOLO
import time

def is_car_in_roi(frame, model, roi):
  
    # Run the model on the frame
    results = model(frame)
    boxes = results[0].boxes.xyxy.tolist()
    classes = results[0].boxes.cls.tolist()
    names = results[0].names
    confidences = results[0].boxes.conf.tolist()

    # Iterate through the results
    for box, cls, conf in zip(boxes, classes, confidences):
        x1, y1, x2, y2 = box
        x, y, w, h = roi
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        if x <= center_x <= x + w and y <= center_y <= y + h:
            return True

    return False


# Define RTSP URLs
rtsp_urls = [
    'rtsp://192.168.11.66:554/user=karma&password=asdf123456&channel=1&stream=0.sdp?',
    'rtsp://192.168.11.66:554/user=karma&password=asdf123456&channel=2&stream=0.sdp?',
    'rtsp://192.168.11.66:554/user=karma&password=asdf123456&channel=3&stream=0.sdp?',
    'rtsp://192.168.11.66:554/user=karma&password=asdf123456&channel=4&stream=0.sdp?',
    'rtsp://192.168.11.66:554/user=karma&password=asdf123456&channel=5&stream=0.sdp?',
    'rtsp://192.168.11.66:554/user=karma&password=asdf123456&channel=6&stream=0.sdp?',
    'rtsp://192.168.11.66:554/user=karma&password=asdf123456&channel=8&stream=0.sdp?',
    'rtsp://192.168.11.66:554/user=karma&password=asdf123456&channel=9&stream=0.sdp?',
    #RTSP URLs as needed
]

# Define multiple ROIs for each stream with unique IDs (x, y, width, height)
rois_per_stream = [
    {
        1: (318, 58, 131, 356),
        2: (466, 67, 125, 362),
        3: (618, 87, 155, 385),
        4: (811, 82, 140, 437),
        5: (966, 128, 145, 414),
    },
    {
        1: (40, 309, 199, 530),
        2: (298, 319, 254, 574),
        3: (686, 259, 180, 488),
        4: (870, 274, 184, 510),
        5: (1075, 315, 171, 540),
    },
    {
        1: (387, 448, 181, 366),
        2: (592, 417, 182, 405),
        3: (787, 416, 155, 433),
        4: (951, 413, 169, 465),
    },
    {
        1: (170, 344, 222, 502),
        2: (399, 328, 193, 490),
        3: (601, 303, 174, 488),
        4: (784, 314, 153, 461),
        5: (951, 312, 125, 444),
        #6: (1087, 337, 96, 393),
    },
    {
        1: (23, 190, 212, 388),
        2: (247, 177, 231, 400),
        3: (490, 223, 181, 384),
        4: (673, 227, 171, 392),
        5: (858, 261, 289, 382),
    },
    {
        1: (0, 252, 152, 425),
        2: (140, 207, 209, 467),
        3: (350, 184, 205, 459),
        4: (561, 176, 182, 453),
        5: (754, 189, 150, 418),
        6: (907, 204, 133, 402),
    },
    {
        1: (2, 601, 179, 443),
        2: (191, 562, 209, 486),
        3: (390, 569, 174, 466),
        4: (576, 573, 199, 461),
        5: (783, 574, 217, 472),
    },
    {
        1: (597, 6, 235, 301),
        2: (788, 91, 328, 419),
        3: (1104, 178, 176, 502),
    },
]

# Load the YOLO model
model = YOLO('vehicle_detect.pt')

# Define a timer for each stream to check at the defined interval
stream_timers = [time.time()] * len(rtsp_urls)
check_interval = 0  # Interval set to 5 minutes

# Process the video streams
while True:
    current_time = time.time()
    for i, rtsp_url in enumerate(rtsp_urls):
        if current_time - stream_timers[i] >= check_interval:
            cap = cv2.VideoCapture(rtsp_url)
            ret, frame = cap.read()

            if not ret:
                print(f"Failed to capture frame from Stream {i+1}")
                cap.release()
                continue

            # Check each ROI for a car
            for roi_id, roi in rois_per_stream[i].items():
                if is_car_in_roi(frame, model, roi):
                    print(f"Car detected in ROI {roi_id} of Stream {i+1}")
                else:
                    print(f"No car detected in ROI {roi_id} of Stream {i+1}")

            # Release the capture object
            cap.release()

            # Update the stream timer
            stream_timers[i] = current_time

