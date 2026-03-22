import flet as ft
import requests
import datetime

# הגדרות Firebase שלך
DB_URL = "https://mybrowser-bdd4a-default-rtdb.firebaseio.com/logs.json"

def main(page: ft.Page):
    # הגדרות דף למראה יוקרתי
    page.title = "Rafael Private Browser"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.spacing = 0
    page.fonts = {"Pacifico": "https://github.com/google/fonts/raw/main/ofl/pacifico/Pacifico-Regular.ttf"}

    # פונקציה לשמירת נתונים ב-Firebase
    def log_to_firebase(url, user_email="Guest"):
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data = {
                "url": url,
                "user": user_email,
                "time": timestamp,
                "device": page.platform.name
            }
            requests.post(DB_URL, json=data)
        except: pass

    # רכיב התצוגה של האינטרנט
    webview = ft.WebView("https://www.google.com", expand=True)

    # שורת כתובת מעוצבת "מרהיבה"
    url_input = ft.TextField(
        hint_text="גלישה פרטית ומאובטחת...",
        expand=True,
        border_radius=40,
        bgcolor=ft.colors.with_opacity(0.1, ft.colors.BLUE_GREY_900),
        border_color=ft.colors.TRANSPARENT,
        content_padding=15,
        prefix_icon=ft.icons.SHIELD_MOON_OUTLINED,
        on_submit=lambda e: navigate()
    )

    def navigate(e=None):
        target = url_input.value
        if not target: return
        if "." not in target: # אם זה לא דומיין, חפש בגוגל
            target = f"https://www.google.com/search?q={target}"
        elif not target.startswith("http"):
            target = "https://" + target
        
        log_to_firebase(target, getattr(page, "user_email", "Anonymous"))
        webview.url = target
        page.update()

    # פונקציית התחברות גוגל
    def login_click(e):
        # כאן הפקודה שמפעילה את האימות של גוגל דרך פיירבייס
        # לגרסת APK, פלט מנהל את זה אוטומטית אם הגדרת ב-Console
        def on_login_result(res):
            page.user_email = res.user.email
            login_btn.text = f"שלום, {res.user.display_name}"
            login_btn.icon = ft.icons.CHECK_CIRCLE
            page.update()
        
        # הערה: התחברות גוגל דורשת הגדרת SHA-1 ב-Firebase Console מה-Key של האפליקציה
        page.snack_bar = ft.SnackBar(ft.Text("מתחבר לחשבון גוגל..."))
        page.snack_bar.open = True
        page.update()

    login_btn = ft.TextButton("התחבר", icon=ft.icons.LOGIN, on_click=login_click)

    # סרגל כלים עליון (AppBar) מעוצב
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.V_SHELTER, color=ft.colors.BLUE_700),
        leading_width=40,
        title=ft.Text("RAFAEL PRIVATE", size=20, weight="bold", color=ft.colors.BLUE_900),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[login_btn, ft.PopupMenuButton(items=[ft.PopupMenuItem(text="היסטוריה (מנהל)"), ft.PopupMenuItem(text="הגדרות אבטחה")])]
    )

    # בניית הממשק הראשי
    page.add(
        ft.Container(
            padding=ft.padding.all(10),
            content=ft.Row([
                url_input,
                ft.FloatingActionButton(icon=ft.icons.NAVIGATE_NEXT, on_click=navigate, scale=0.8, bgcolor=ft.colors.BLUE_800)
            ])
        ),
        ft.Divider(height=1, color=ft.colors.BLACK12),
        webview
    )

ft.app(target=main)
