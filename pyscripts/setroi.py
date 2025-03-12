import cv2

def select_multiple_rois(rtsp_url):
    # VideoCapture object
    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return None

    # Read one frame from the video stream to get its resolution
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame from video stream.")
        cap.release()
        return None

    # Original frame dimensions
    original_height, original_width = frame.shape[:2]
    print(f"Original Resolution: {original_width}x{original_height}")

    # List to store ROIs
    rois = []

    # Loop to select multiple ROIs directly on the original frame
    while True:
        roi = cv2.selectROI("Select ROI (Press Enter to confirm, 'c' to continue, 'q' to quit)", frame, False, False)
        if roi[2] != 0 and roi[3] != 0:  # Check if ROI is not empty
            rois.append(roi)

        key = cv2.waitKey(0) & 0xFF
        if key == ord('q'):  # Quit on 'q'
            break
        elif key == ord('c'):  # Continue selecting on 'c'
            continue

    cv2.destroyAllWindows()
    cap.release()

    return rois

# RTSP URL
rtsp_url = 'rtsp://192.168.11.66:554/user=karma&password=asdf123456&channel=6&stream=0.sdp?'

# Get multiple ROIs without resizing the window, using the video's native resolution
selected_rois = select_multiple_rois(rtsp_url)
if selected_rois:
    print("Selected ROIs:")
    for roi in selected_rois:
        print(roi)
