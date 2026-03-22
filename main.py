import flet as ft
import requests

# הכתובת הישירה למסד הנתונים שלך ב-Firebase
FIREBASE_URL = "https://mybrowser-bdd4a-default-rtdb.firebaseio.com/logs.json"

def main(page: ft.Page):
    page.title = "Rafael Digital Browser"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0

    # תיבת חיפוש
    url_input = ft.TextField(
        hint_text="הקלד כתובת אתר (למשל google.com)...",
        expand=True,
        border_radius=30,
        bgcolor=ft.colors.GREY_100,
        content_padding=15,
        prefix_icon=ft.icons.SEARCH
    )

    # רכיב תצוגת האתר
    webview = ft.WebView("https://google.com", expand=True)

    def log_visit(target):
        # פונקציה ששולחת את הנתונים ל-Firebase ברקע
        try:
            data = {"url": target, "device": page.platform.name}
            requests.post(FIREBASE_URL, json=data)
        except Exception as e:
            print("Error saving log:", e)

    def on_go(e):
        target = url_input.value
        # השלמה אוטומטית ל-https אם חסר
        if not target.startswith("http"):
            target = "https://" + target
        
        # שמירה במסד נתונים וטעינת האתר
        log_visit(target)
        webview.url = target
        page.update()

    # בניית המסך
    page.add(
        ft.Container(
            content=ft.Row([
                url_input,
                ft.IconButton(ft.icons.ARROW_FORWARD_ROUNDED, on_click=on_go, icon_color="blue")
            ]),
            padding=10,
            bgcolor=ft.colors.BLUE_50
        ),
        webview
    )

ft.app(target=main)
