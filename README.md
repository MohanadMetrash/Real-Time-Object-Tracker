# AI Real-Time Object Tracker

A user-friendly desktop application for real-time object tracking in a live webcam feed. This tool allows users to select an object with a bounding box and track its movement using various state-of-the-art tracking algorithms.

  
*(Replace the URL above with a real screenshot of your application)*

---

## Features

- **Intuitive GUI:** A clean, modern interface built with `ttkbootstrap` guides the user through the process.
- **Multiple Tracker Options:** Users can choose from seven different OpenCV tracking algorithms, including CSRT, KCF, and MOSSE.
- **Real-Time Bounding Box:** The application draws a bounding box around the tracked object in real-time.
- **Performance Metrics:** Displays the live Frames Per Second (FPS) to gauge performance.
- **Status Updates:** Clearly indicates tracking success or failure on the video feed.

## Tech Stack

- **Language:** Python 3
- **Core Vision Library:** OpenCV (`opencv-contrib-python`)
- **GUI Framework:** Tkinter with `ttkbootstrap` for modern themes and widgets.
- **Image Handling:** Pillow (`PIL`) for displaying the creator photo in the GUI.

---

## Deployment and Installation

To run this application on your local machine, please follow these steps:

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Create a Virtual Environment** (Recommended)
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install Dependencies**
    Install all required packages using the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Application**
    ```bash
    python tracker_app.py
    ```

---

## How to Use

1.  Launch the application. You will be greeted by the welcome screen.
2.  Click **Continue to Setup**.
3.  Select a tracking algorithm from the dropdown menu.
    - **CSRT**: High accuracy, but slower. Recommended for best results.
    - **KCF**: Good balance of speed and accuracy.
    - **MOSSE**: Extremely fast, but less accurate.
4.  Click **Launch Tracker**. Your webcam will activate.
5.  In the webcam window, **click and drag** your mouse to draw a box around the object you wish to track.
6.  Press **ENTER** or **SPACE** to confirm your selection.
7.  The tracking will begin. To stop, press the **ESC** key. This will close the tracking window and return you to the GUI.

---

## Implementation Details

This project is built on the robust computer vision capabilities of **OpenCV**. The core tracking functionality leverages algorithms available in the `cv2.legacy` module, providing a range of options to balance tracking accuracy and computational performance.

The application architecture separates the user interface from the core logic.
-   **GUI (`tkinter`, `ttkbootstrap`)**: A multi-frame `tkinter` structure provides a non-blocking, user-friendly experience. The `WelcomeScreen` onboards the user with instructions, while the `SetupScreen` allows for configuration.
-   **Tracking Logic (`OpenCV`)**: The `run_object_tracking` function encapsulates all computer vision operations. It handles video capture, user ROI selection (`cv2.selectROI`), and the real-time tracking loop (`tracker.update()`). This separation makes the code cleaner and easier to maintain.

---
## Recorded Demo

[Link to your recorded demo video]

*(Record a short video showcasing the app's functionality and add the link here.)*
