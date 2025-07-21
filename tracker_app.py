import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import sys
import os

def create_tracker(tracker_name):
   
    tracker_constructors = {
        'BOOSTING': cv2.legacy.TrackerBoosting_create,
        'MIL': cv2.legacy.TrackerMIL_create,
        'KCF': cv2.legacy.TrackerKCF_create,
        'TLD': cv2.legacy.TrackerTLD_create,
        'MEDIANFLOW': cv2.legacy.TrackerMedianFlow_create,
        'MOSSE': cv2.legacy.TrackerMOSSE_create,
        "CSRT": cv2.legacy.TrackerCSRT_create,
    }
    constructor = tracker_constructors.get(tracker_name.upper())
    return constructor() if constructor else None

def run_object_tracking(tracker_name): # Initializes and runs the OpenCV object tracking window.
    
    tracker = create_tracker(tracker_name)
    if tracker is None:
        messagebox.showerror("Error", f"Unknown tracker type '{tracker_name}' selected.")
        return
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        messagebox.showerror("Error", "Could not open webcam.")
        return
    success, initial_frame = video_capture.read()
    if not success:
        messagebox.showerror("Error", "Cannot read from webcam.")
        video_capture.release()
        return
        
    # Selects the object to track
    roi = cv2.selectROI("Select Object to Track", initial_frame, fromCenter=False, showCrosshair=True)
    
    # Check a valid region of interest (ROI)
    if roi[2] > 0 and roi[3] > 0:
        tracker.init(initial_frame, roi)
    else:
        print("No region selected. Exiting tracking.")
        video_capture.release()
        cv2.destroyAllWindows()
        return
    cv2.destroyWindow("Select Object to Track")
    while True:
        is_reading, frame = video_capture.read()
        if not is_reading:
            break
        timer_start = cv2.getTickCount()
        is_tracking, bbox = tracker.update(frame)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer_start)
        if is_tracking:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (0, 255, 0), 2, 1)
        else:
            cv2.putText(frame, "Tracking Failure", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        cv2.putText(frame, f"{tracker_name} Tracker", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
        cv2.putText(frame, f"FPS: {int(fps)}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
        cv2.putText(frame, "Press ESC to Exit", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        cv2.imshow("Object Tracking", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC key
            break
            
    video_capture.release()
    cv2.destroyAllWindows()

# Constants for consistent styling
FONT_TITLE = ("Helvetica", 24, "bold")
FONT_HEADING = ("Helvetica", 14, "bold")
FONT_BODY = ("Helvetica", 11)
FONT_CREATOR = ("Helvetica", 12, "italic")
class TrackingApp(ttk.Window): 
    def __init__(self):
        
        super().__init__(themename="cyborg")  # 'cyborg' theme for a professional dark look
        
        self.title("AI Object Tracker by Mohanad Metrash")
        self.geometry("650x700")
        # Container frame to hold all pages
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (WelcomeScreen, SetupScreen):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("WelcomeScreen")
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class WelcomeScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Title
        title_label = ttk.Label(self, text="Welcome to the AI Object Tracker!", font=FONT_TITLE, bootstyle="primary")
        title_label.pack(pady=(10, 20))
        
        photo_path = "creator_photo.png"
        if os.path.exists(photo_path):
            img = Image.open(photo_path).resize((150, 150), Image.Resampling.LANCZOS)
            self.creator_photo = ImageTk.PhotoImage(img)
            # Add a colored border using a frame
            photo_frame = ttk.Frame(self, bootstyle="primary", padding=3)
            photo_label = ttk.Label(photo_frame, image=self.creator_photo)
            photo_label.pack()
            photo_frame.pack(pady=10)
        
        
        name_label = ttk.Label(self, text="Created by Mohanad Metrash", font=FONT_CREATOR, bootstyle="secondary")
        name_label.pack(pady=(0, 20))
        # INSTRUCTIONS Part
        instr_frame = ttk.Frame(self, bootstyle="secondary", padding=20)
        instr_frame.pack(pady=10, padx=20, fill="x")
        instr_heading = ttk.Label(instr_frame, text="How to Use This Application", font=FONT_HEADING, bootstyle="inverse-secondary")
        instr_heading.pack(anchor="w")
        
        
        steps = [
            ("1. Proceed to Setup:", "Click the Continue button below."),
            ("2. Choose an Algorithm:", "Select a tracker. CSRT is accurate, KCF is fast."),
            ("3. Launch the Tracker:", "Click Launch Tracker to open your webcam."),
            ("4. Select an Object:", "In the new window, CLICK and DRAG a box around an object."),
            ("5. Confirm Selection:", "Press the ENTER or SPACE key."),
            ("6. Stop Tracking:", "Press the ESC key at any time to exit and return here.")
        ]
        for title, text in steps:
            step_frame = ttk.Frame(instr_frame, bootstyle="secondary")
            step_frame.pack(fill="x", pady=4)
            ttk.Label(step_frame, text=title, font=FONT_BODY + ("bold",), bootstyle="inverse-secondary").pack(side="left", anchor="nw")
            ttk.Label(step_frame, text=text, font=FONT_BODY, bootstyle="inverse-secondary", wraplength=450).pack(side="left", anchor="nw", padx=5)
        
        continue_button = ttk.Button(
            self, text="Continue to Setup",
            command=lambda: controller.show_frame("SetupScreen"),
            bootstyle="success-outline", # A nice green outline button
            width=20
        )
        continue_button.pack(pady=25, ipady=5)

class SetupScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        title_label = ttk.Label(self, text="Tracker Configuration", font=FONT_TITLE, bootstyle="primary")
        title_label.pack(pady=40)
        info_label = ttk.Label(self, text="Please select a tracking algorithm:", font=FONT_HEADING)
        info_label.pack(pady=10)
        
        self.tracker_var = tk.StringVar()
        tracker_options = ['CSRT', 'KCF', 'MOSSE', 'MIL', 'BOOSTING', 'TLD', 'MEDIANFLOW']
        
        self.tracker_menu = ttk.Combobox(self, textvariable=self.tracker_var, values=tracker_options, state="readonly", font=FONT_HEADING, width=15, bootstyle="primary")
        self.tracker_menu.set('CSRT') # A recommended default
        self.tracker_menu.pack(pady=20)
        
        launch_button = ttk.Button(self, text="Launch Tracker", command=self.launch_tracking, bootstyle="success", width=20)
        launch_button.pack(pady=20, ipady=10)
       
        back_button = ttk.Button(self, text="< Back to Welcome", command=lambda: controller.show_frame("WelcomeScreen"), bootstyle="secondary-outline")
        back_button.pack(pady=(60, 20))
    def launch_tracking(self):
        selected_tracker = self.tracker_var.get()
        if not selected_tracker:
            messagebox.showwarning("Warning", "Please select a tracker first.")
            return
        
        self.controller.withdraw()
        try:
            run_object_tracking(selected_tracker)
        except Exception as e:
            messagebox.showerror("Runtime Error", f"An error occurred during tracking: {e}")
        finally:
            self.controller.deiconify()

if __name__ == "__main__":
    app = TrackingApp()
    app.mainloop()