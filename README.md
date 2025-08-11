# 🎯 Color-Based Mouse Control Using OpenCV & PyAutoGUI

This project allows you to control your mouse using colored objects in front of your webcam. By tracking **red**, **green**, and **blue** objects, you can move the cursor and perform **left** and **right clicks** using gestures.

---

## 📹 Features

* 🟥 **Red Object** – Moves the mouse cursor
* 🟦 **Blue Object** – Triggers a **left click**
* 🟩 **Green Object** – Triggers a **right click**
* ⏱️ Cooldown of 1 second between clicks to prevent multiple triggers
* 🧠 Simple computer vision logic using OpenCV and color masks

---

## 📦 Requirements

Install the dependencies using `pip`:

```bash
pip install opencv-python imutils pyautogui
```

---

## 🚀 How to Run

1. Connect a webcam.
2. Place red, green, and blue colored objects in front of it.
3. Run the script:

```bash
python color_mouse_control.py
```

4. Use the colored objects:

   * **Red** – Move the mouse
   * **Blue** – Left click (when held up)
   * **Green** – Right click (when held up)

5. Press **`q`** to quit.

---

## 🛠️ How It Works

* Captures webcam frames using `cv2.VideoCapture`
* Converts the frame to HSV for better color detection
* Creates color masks for red, green, and blue
* Detects the largest contour in each color mask
* Calculates position (for red) to move the cursor
* Triggers clicks (for green and blue) with cooldown to avoid spam

---

## ⚠️ Notes

* Make sure the lighting conditions are good for accurate color detection.
* You can tune HSV ranges (`redLower`, `greenLower`, etc.) for better performance.
* This project disables `pyautogui.FAILSAFE` to allow edge-to-edge movement — use with caution.

