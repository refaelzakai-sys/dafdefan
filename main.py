import flet as ft
from supabase import create_client, Client

# פרטי ה-Supabase שלך (כבר מעודכנים)
URL = "https://yphtzqxooetllrvddbcm.supabase.co"
KEY = "sb_publishable_3nNyvPGbuZ2NA1BqVek2TA_NjyIKvzh"
ADMIN_EMAIL = "rplzky7@gmail.com"

supabase: Client = create_client(URL, KEY)

def main(page: ft.Page):
    page.title = "Rafael Digital Browser"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    
    # משתנה לשמירת הסטטוס (מנהל או לא)
    is_admin = True # כרגע מוגדר כ-True כדי שתוכל לראות את זה בבדיקה

    # פונקציה לשמירת היסטוריה ב-Supabase
    def log_visit(url_to_log):
        try:
            supabase.table("user_logs").insert({
                "url": url_to_log,
                "device_info": page.platform.name
            }).execute()
        except:
            pass

    # רכיב תצוגת האתר
    webview = ft.WebView("https://google.com", expand=True)

    # תיבת חיפוש מעוצבת
    url_input = ft.TextField(
        hint_text="הקלד כתובת אתר...",
        expand=True,
        border_radius=30,
        bgcolor=ft.colors.WHITE,
        content_padding=15,
        prefix_icon=ft.icons.SEARCH
    )

    def on_go(e):
        target = url_input.value
        if not target.startswith("http"):
            target = "https://" + target
        log_visit(target)
        webview.url = target
        page.update()

    # חלון ניהול (Admin Panel) - יוצג למנהל בלבד
    def show_admin_logs(e):
        try:
            # שליפת 10 ביקורים אחרונים מהמסד נתונים
            response = supabase.table("user_logs").select("*").order("created_at", desc=True).limit(10).execute()
            logs = response.data
            
            log_list = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)
            for item in logs:
                log_list.controls.append(
                    ft.ListTile(
                        title=ft.Text(item['url']),
                        subtitle=ft.Text(f"זמן: {item['created_at']} | מכשיר: {item['device_info']}"),
                        trailing=ft.IconButton(ft.icons.BLOCK, icon_color="red", tooltip="חסום משתמש")
                    )
                )
            
            # הצגת חלון קופץ (Dialog) עם הנתונים
            dlg = ft.AlertDialog(
                title=ft.Text("ניהול היסטוריית משתמשים"),
                content=log_list,
                actions=[ft.TextButton("סגור", on_click=lambda _: page.close(dlg))]
            )
            page.open(dlg)
        except Exception as ex:
            print(ex)

    # בניית הממשק (UI)
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

    # הוספת כפתור ניהול צף בפינה (רק אם אתה מחובר)
    if is_admin:
        page.floating_action_button = ft.FloatingActionButton(
            icon=ft.icons.ADMIN_PANEL_SETTINGS,
            on_click=show_admin_logs,
            bgcolor=ft.colors.ORANGE_700,
            tooltip="לוח בקרה למנהל"
        )
    
    page.update()

ft.app(target=main)

