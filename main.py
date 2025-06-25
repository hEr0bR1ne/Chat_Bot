import tkinter as tk
from ui.medical_robot_tk import MedicalRobotUI

if __name__ == "__main__":
    root = tk.Tk()
    app = MedicalRobotUI(root)
    root.mainloop() 