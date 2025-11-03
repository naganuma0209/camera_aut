import cv2
import tkinter as tk
from datetime import datetime
import os
import socket
import csv

# --- 初期設定 ---
os.makedirs("photos", exist_ok=True)
if not os.path.exists("photo_log.csv"):
    with open("photo_log.csv", mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["日時", "ファイル名", "PC名"])

cap = cv2.VideoCapture(0)

# --- 写真撮影関数 ---
def capture_photo():
    ret, frame = cap.read()
    if ret:
        # テキストボックスの内容を取得
        name = entry_name.get()
        if name == "":
            name = "photo"
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"photos/{name}_{now}.jpg"
        cv2.imwrite(filename, frame)
        with open("photo_log.csv", mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), filename, socket.gethostname()])
        print(f"{filename} を保存しました")

        # 撮影後にボタンの色を変える
        btn_capture.config(bg="lightgreen", activebackground="green")

        # 2秒後に元の色に戻す
        root.after(2000, lambda: btn_capture.config(bg="SystemButtonFace", activebackground="SystemButtonFace"))

# --- 終了関数 ---
def close_app():
    cap.release()
    cv2.destroyAllWindows()
    root.destroy()

# --- Tkinter GUI作成 ---
root = tk.Tk()
root.title("カメラ撮影アプリ")

# ファイル名入力用テキストボックス
tk.Label(root, text="ファイル名:").pack()
entry_name = tk.Entry(root, width=20)
entry_name.pack(pady=5)

# 撮影ボタン
btn_capture = tk.Button(root, text="撮影", command=capture_photo, height=2, width=10)
btn_capture.pack(pady=10)

# 終了ボタン
btn_exit = tk.Button(root, text="終了", command=close_app, height=2, width=10)
btn_exit.pack(pady=10)

# --- カメラ映像表示関数 ---
def show_frame():
    ret, frame = cap.read()
    if ret:
        cv2.imshow("Camera Preview", frame)
    root.after(25, show_frame)

show_frame()
root.mainloop()
