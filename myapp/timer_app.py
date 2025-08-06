
import tkinter as tk
import sys

# Pydroid3のtkinterで日本語が文字化けする場合の対策
if sys.platform == "android":
    from tkinter import font
    
# --- 定数 ---
# ウィンドウ設定
WINDOW_TITLE = "料理タイマー"
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 400

# フォント設定
FONT_FAMILY = "sans-serif" # Pydroid3で利用可能なフォント
TIME_FONT_SIZE = 60
BUTTON_FONT_SIZE = 14
STATUS_FONT_SIZE = 20

# 色設定
COLOR_BG = "#F0F0F0"       # 背景色
COLOR_FG = "#333333"       # 文字色
COLOR_HIGHLIGHT = "#FF5722" # 時間切れの時の色

# --- グローバル変数 ---
time_remaining = 0
timer_job = None # tkinterのafterメソッドのジョブIDを保存

# --- 関数 ---

def format_time(seconds):
    """秒を MM:SS 形式の文字列に変換する"""
    minutes = seconds // 60
    sec = seconds % 60
    return f"{minutes:02d}:{sec:02d}"

def update_countdown():
    """1秒ごとに時間を更新する"""
    global time_remaining, timer_job
    
    if time_remaining > 0:
        time_remaining -= 1
        time_label.config(text=format_time(time_remaining))
        # 1000ミリ秒(1秒)後にもう一度この関数を呼び出す
        timer_job = root.after(1000, update_countdown)
    else:
        # 時間が来たら表示を更新
        time_label.config(text="時間です！", fg=COLOR_HIGHLIGHT)
        status_label.config(text="")

def start_timer(duration):
    """タイマーを開始する"""
    global time_remaining
    
    # もし前のタイマーが動いていたら止める
    reset_timer()
    
    time_remaining = duration
    status_text = f"{duration//60}分のタイマーを開始しました"
    status_label.config(text=status_text)
    time_label.config(text=format_time(time_remaining), fg=COLOR_FG)
    update_countdown()

def reset_timer():
    """タイマーをリセットする"""
    global timer_job
    if timer_job:
        root.after_cancel(timer_job) # スケジュールされたジョブをキャンセル
        timer_job = None
    
    time_label.config(text="00:00", fg=COLOR_FG)
    status_label.config(text="ボタンを押して開始")


# --- GUIのセットアップ ---

# メインウィンドウ
root = tk.Tk()
root.title(WINDOW_TITLE)
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.configure(bg=COLOR_BG)

# Pydroid3用のフォント設定
if sys.platform == "android":
    time_font = font.Font(family=FONT_FAMILY, size=TIME_FONT_SIZE, weight="bold")
    button_font = font.Font(family=FONT_FAMILY, size=BUTTON_FONT_SIZE)
    status_font = font.Font(family=FONT_FAMILY, size=STATUS_FONT_SIZE)
else: # PCなど他の環境用
    time_font = (FONT_FAMILY, TIME_FONT_SIZE, "bold")
    button_font = (FONT_FAMILY, BUTTON_FONT_SIZE)
    status_font = (FONT_FAMILY, STATUS_FONT_SIZE)


# 時間表示ラベル
time_label = tk.Label(root, text="00:00", font=time_font, bg=COLOR_BG, fg=COLOR_FG)
time_label.pack(pady=30) # 上下に余白

# ステータス表示ラベル
status_label = tk.Label(root, text="ボタンを押して開始", font=status_font, bg=COLOR_BG, fg=COLOR_FG)
status_label.pack(pady=10)

# ボタンをまとめるフレーム
button_frame = tk.Frame(root, bg=COLOR_BG)
button_frame.pack(pady=10)

# --- ボタンの作成 ---
# commandにlambdaを使うことで、ボタンが押された時に引数付きの関数を呼び出せる
buttons_config = [
    {"text": "半熟卵 (6分)", "time": 6 * 60},
    {"text": "固ゆで卵 (10分)", "time": 10 * 60},
    {"text": "パスタ (11分)", "time": 11 * 60},
]

for config in buttons_config:
    btn = tk.Button(
        button_frame,
        text=config["text"],
        font=button_font,
        command=lambda t=config["time"]: start_timer(t)
    )
    btn.pack(fill=tk.X, padx=20, pady=5) # 横幅を揃え、上下左右に余白

# リセットボタン
reset_button = tk.Button(root, text="リセット", font=button_font, command=reset_timer)
reset_button.pack(pady=20)


# --- アプリの実行 ---
root.mainloop()
