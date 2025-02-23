from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.dialog import MDDialog
import sqlite3,os

class Main(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.entry_name = MDTextField(
            hint_text = "Enter Your Name",
            size_hint = (.6,None),
            pos_hint = {"center_x":.5,"center_y":.6},
            halign='center',
            font_size = 25,
            
        )
        self.phone = MDTextField(
            hint_text = "Enter Your Phone Number",
            size_hint = (.6,None),
            pos_hint = {"center_x":.5,"center_y":.5},
            halign='center',
            font_size = 25,
        )
        self.button = MDFillRoundFlatButton(
            text = "Press Me",
            size_hint = (.4,.1),
            pos_hint = {"center_x":.5,"center_y":.4},
            on_release = self.register
        )
        f = FloatLayout()
        f.add_widget(self.entry_name)
        f.add_widget(self.phone)
        f.add_widget(self.button)
        return f
    def register(self,event):
        name = self.entry_name.text
        phone = self.phone.text
        database = os.path.join(os.path.dirname(__file__),"database.db")
        if not os.path.exists(database):
            connection = sqlite3.connect(database)
            cursor = connection.cursor()
            cursor.execute('create table if not exists data(\
                id integer primary key autoincrement,\
                name text not null,\
                phone text not null)')
            cursor.execute('insert into data(name,phone) values (?,?)',(name,phone))
            connection.commit()
            cursor.close()
            self.dialog = MDDialog(
            title = "Success",
            text = "Data Saved Successfully!",
            buttons = [
                MDFillRoundFlatButton(text='Ok',on_release = lambda x: self.dialog.dismiss())
            ]
        )
        else:
            connection = sqlite3.connect(database)
            cursor = connection.cursor()
            cursor.execute('create table if not exists data(\
                id integer primary key autoincrement,\
                name text not null,\
                phone text not null)')
            cursor.execute('insert into data(name,phone) values (?,?)',(name,phone))
            connection.commit()
            cursor.close()
            self.dialog = MDDialog(
            title = "Success",
            text = "Data Saved Successfully!",
            buttons = [
                MDFillRoundFlatButton(text='Ok',on_release = lambda x: self.dialog.dismiss())
              ]
            )
            
        
        
        self.dialog.open()
Main().run()
# from kivymd.app import MDApp
# from kivymd.uix.button import MDRaisedButton
# from kivymd.uix.textfield import MDTextField
# from kivymd.uix.progressbar import MDProgressBar
# from kivymd.uix.label import MDLabel
# from kivymd.uix.floatlayout import FloatLayout
# from kivy.clock import Clock
# import requests
# import threading
# import yt_dlp
# import os
# from slugify import slugify
# # 😊🌟
# # Use slugify to handle file names

# os.chdir(os.path.dirname(__file__))
# class VideoDownloaderApp(MDApp):
#     def build(self):
#         self.is_paused = False
#         self.stop_event = threading.Event()

#         self.url_input = MDTextField(
#             hint_text="Enter YouTube URL",
#             size_hint=(0.8, None),
#             height=50,
#             pos_hint={"center_x": 0.5, "center_y": 0.75},
#         )

#         self.download_button = MDRaisedButton(
#             text="Start Download",
#             pos_hint={"center_x": 0.5, "center_y": 0.65},
#             on_release=self.start_download_thread
#         )

#         self.pause_button = MDRaisedButton(
#             text="Pause",
#             pos_hint={"center_x": 0.35, "center_y": 0.55},
#             on_release=self.pause_download
#         )

#         self.resume_button = MDRaisedButton(
#             text="Resume",
#             pos_hint={"center_x": 0.65, "center_y": 0.55},
#             on_release=self.resume_download
#         )

#         self.progress_label = MDLabel(
#             text="Progress: 0%",
#             halign="center",
#             pos_hint={"center_x": 0.5, "center_y": 0.45},
#             theme_text_color="Primary"
#         )

#         self.progress_bar = MDProgressBar(
#             value=0,
#             size_hint=(0.8, None),
#             height=20,
#             pos_hint={"center_x": 0.5, "center_y": 0.4},
#         )

#         self.status_label = MDLabel(
#             text="Status: Waiting for download...",
#             halign="center",
#             pos_hint={"center_x": 0.5, "center_y": 0.3},
#             theme_text_color="Secondary"
#         )

#         layout = FloatLayout()
#         layout.add_widget(self.url_input)
#         layout.add_widget(self.download_button)
#         layout.add_widget(self.pause_button)
#         layout.add_widget(self.resume_button)
#         layout.add_widget(self.progress_label)
#         layout.add_widget(self.progress_bar)
#         layout.add_widget(self.status_label)

#         return layout

#     def start_download_thread(self, instance):
#         url = self.url_input.text.strip()
#         if not url:
#             self.status_label.text = "Status: Please enter a YouTube URL."
#             return

#         self.status_label.text = "Status: Fetching video URL..."
#         self.progress_bar.value = 0
#         self.progress_label.text = "Progress: 0%"
#         self.stop_event.clear()
#         self.is_paused = False

#         threading.Thread(target=self.download_youtube_video, args=(url,), daemon=True).start()

#     def get_direct_url(self, url):
#         """Fetch direct video URL from YouTube using yt_dlp."""
#         ydl_opts = {
#             'format': 'best[ext=mp4]',
#             'quiet': True,
#         }
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info = ydl.extract_info(url, download=False)
#             video_url = info['url']
#             video_title = info['title']
#         return video_url, video_title

#     def download_youtube_video(self, url):
#         try:
#             video_url, video_title = self.get_direct_url(url)
#             # file_name = f"{video_title}.mp4"
#             file_name = slugify(video_title, allow_unicode=True) + '.mp4'
#             self.update_status(f"Status: Downloading {file_name}...")

#             response = requests.get(video_url, stream=True)
#             total_size = int(response.headers.get('content-length', 0))
#             downloaded_size = 0

#             with open(file_name, 'wb') as file:
#                 for chunk in response.iter_content(chunk_size=8192):
#                     if self.stop_event.is_set():
#                         break
#                     while self.is_paused:
#                         Clock.schedule_once(lambda dt: self.update_status("Status: Paused"))
#                         threading.Event().wait(0.1)
#                     if chunk:
#                         file.write(chunk)
#                         downloaded_size += len(chunk)
#                         progress = (downloaded_size / total_size) * 100
#                         Clock.schedule_once(lambda dt: self.update_progress(progress))

#             if self.stop_event.is_set():
#                 Clock.schedule_once(lambda dt: self.update_status("Status: Download stopped."))
#             else:
#                 Clock.schedule_once(lambda dt: self.update_status(f"Status: Download completed - {file_name}"))

#         except Exception as error:
#             error_message = f"Error: {str(error)}"
#             Clock.schedule_once(lambda dt: self.update_status(error_message))

#     def pause_download(self, instance):
#         self.is_paused = True
#         self.status_label.text = "Status: Paused"

#     def resume_download(self, instance):
#         self.is_paused = False
#         self.status_label.text = "Status: Resuming..."

#     def update_progress(self, progress):
#         self.progress_bar.value = progress
#         self.progress_label.text = f"Progress: {progress:.2f}%"

#     def update_status(self, message):
#         self.status_label.text = message


# if __name__ == "__main__":
#     VideoDownloaderApp().run()

















































# # from kivymd.app import MDApp
# # from kivymd.uix.button import MDRaisedButton
# # from kivymd.uix.textfield import MDTextField
# # from kivymd.uix.progressbar import MDProgressBar
# # from kivymd.uix.label import MDLabel
# # from kivymd.uix.floatlayout import FloatLayout
# # from kivy.clock import Clock
# # import requests
# # import threading
# # import os

# # os.chdir(os.path.dirname(__file__))
# # class VideoDownloaderApp(MDApp):
# #     def build(self):
# #         self.is_paused = False
# #         self.stop_event = threading.Event()

# #         self.url_input = MDTextField(
# #             hint_text="Enter video URL",
# #             size_hint=(0.8, None),
# #             height=50,
# #             pos_hint={"center_x": 0.5, "center_y": 0.75},
# #         )

# #         self.download_button = MDRaisedButton(
# #             text="Start Download",
# #             pos_hint={"center_x": 0.5, "center_y": 0.65},
# #             on_release=self.start_download_thread
# #         )

# #         self.pause_button = MDRaisedButton(
# #             text="Pause",
# #             pos_hint={"center_x": 0.35, "center_y": 0.55},
# #             on_release=self.pause_download
# #         )

# #         self.resume_button = MDRaisedButton(
# #             text="Resume",
# #             pos_hint={"center_x": 0.65, "center_y": 0.55},
# #             on_release=self.resume_download
# #         )

# #         self.progress_label = MDLabel(
# #             text="Progress: 0%",
# #             halign="center",
# #             pos_hint={"center_x": 0.5, "center_y": 0.45},
# #             theme_text_color="Primary"
# #         )

# #         self.progress_bar = MDProgressBar(
# #             value=0,
# #             size_hint=(0.8, None),
# #             height=20,
# #             pos_hint={"center_x": 0.5, "center_y": 0.4},
# #         )

# #         self.status_label = MDLabel(
# #             text="Status: Waiting for download...",
# #             halign="center",
# #             pos_hint={"center_x": 0.5, "center_y": 0.3},
# #             theme_text_color="Secondary"
# #         )

# #         layout = FloatLayout()
# #         layout.add_widget(self.url_input)
# #         layout.add_widget(self.download_button)
# #         layout.add_widget(self.pause_button)
# #         layout.add_widget(self.resume_button)
# #         layout.add_widget(self.progress_label)
# #         layout.add_widget(self.progress_bar)
# #         layout.add_widget(self.status_label)

# #         return layout

# #     def start_download_thread(self, instance):
# #         url = self.url_input.text.strip()
# #         if not url:
# #             self.status_label.text = "Status: Please enter a video URL."
# #             return

# #         self.status_label.text = "Status: Downloading..."
# #         self.progress_bar.value = 0
# #         self.progress_label.text = "Progress: 0%"
# #         self.stop_event.clear()
# #         self.is_paused = False

# #         threading.Thread(target=self.download_video, args=(url,), daemon=True).start()

# #     def download_video(self, url):
# #         try:
# #             response = requests.get(url, stream=True)
# #             total_size = int(response.headers.get('content-length', 0))
# #             file_name = "video.mp4"

# #             downloaded_size = 0
# #             mode = 'ab' if downloaded_size > 0 else 'wb'

# #             with open(file_name, mode) as file:
# #                 for chunk in response.iter_content(chunk_size=8192):
# #                     if self.stop_event.is_set():
# #                         break
# #                     while self.is_paused:
# #                         Clock.schedule_once(lambda dt: self.update_status("Status: Paused"))
# #                         threading.Event().wait(0.1)
# #                     if chunk:
# #                         file.write(chunk)
# #                         downloaded_size += len(chunk)
# #                         progress = (downloaded_size / total_size) * 100
# #                         Clock.schedule_once(lambda dt: self.update_progress(progress))

# #             if self.stop_event.is_set():
# #                 Clock.schedule_once(lambda dt: self.update_status("Status: Download stopped."))
# #             else:
# #                 Clock.schedule_once(lambda dt: self.update_status(f"Status: Download completed - {file_name}"))

# #         except Exception as error:
# #             error_message = f"Error: {str(error)}"
# #             Clock.schedule_once(lambda dt: self.update_status(error_message))


# #     def pause_download(self, instance):
# #         self.is_paused = True
# #         self.status_label.text = "Status: Paused"

# #     def resume_download(self, instance):
# #         self.is_paused = False
# #         self.status_label.text = "Status: Resuming..."

# #     def update_progress(self, progress):
# #         self.progress_bar.value = progress
# #         self.progress_label.text = f"Progress: {progress:.2f}%"

# #     def update_status(self, message):
# #         self.status_label.text = message


# # if __name__ == "__main__":
# #     VideoDownloaderApp().run()












# # from kivymd.app import MDApp
# # from kivymd.uix.progressbar import MDProgressBar
# # from kivy.clock import Clock
# # from kivymd.uix.floatlayout import FloatLayout

# # class MyApp(MDApp):
# #     def build(self):
# #         self.progress = MDProgressBar(
# #             value=0,
# #             pos_hint={"center_x": 0.5, "center_y": 0.4},
# #             size_hint=(0.7, None),
# #             height=20
# #         )
# #         layout = FloatLayout()
# #         layout.add_widget(self.progress)
# #         Clock.schedule_interval(self.update_progress, 0.1)
# #         return layout

# #     def update_progress(self, dt):
# #         if self.progress.value < 100:
# #             self.progress.value += 1
# #         else:
# #             self.progress.value = 0

# # MyApp().run()

















# # from kivymd.app import MDApp
# # from kivymd.uix.button import MDRaisedButton
# # from kivymd.uix.floatlayout import FloatLayout

# # class MyApp(MDApp):
# #     def build(self):
# #         btn = MDRaisedButton(
# #             text="press me",
# #             pos_hint={"center_x": 0.5, "center_y": 0.5},
# #             on_release=self.button_clicked,
# #             size_hint = {.5,.1}
# #         )
# #         layout = FloatLayout()
# #         layout.add_widget(btn)
# #         return layout

# #     def button_clicked(self, instance):
# #         print("Hello World")

# # MyApp().run()























# # from kivymd.app import MDApp
# # from kivymd.uix.button import MDFillRoundFlatButton
# # from kivymd.uix.floatlayout import FloatLayout

# # class MyApp(MDApp):
# #     def build(self):
# #         _label = MDFillRoundFlatButton(
# #             text='Press Me',halign='center',
# #             pos_hint={'center_x':.5,'center_y':.5},
# #             size_hint = {.5,.1},
# #             on_release=self.order)
# #         F = FloatLayout()
# #         F.add_widget(_label)
# #         return F
# #     def order(self,event):
# #         print("hello world")
# # MyApp().run()

































# # from kivymd.app import MDApp
# # from kivymd.uix.button import MDFillRoundFlatButton
# # from kivymd.uix.floatlayout import FloatLayout
# # from kivy.lang import Builder

# # kv = '''
# # <Main>
# # FloatLayout:
# #     MDFillRoundFlatButton:
# #         text : "press me"
# #         pos_hint : {'center_x':.5,'center_y':.5}
# #         size_hint : {.5,.1}
# # '''
# # class Main(MDApp):
# #     def build(self):
# #         v = Builder.load_string(kv)
# #         return v
# #     #     f = FloatLayout()
# #     #     button = MDFillRoundFlatButton(text="press me",
# #     #                                    pos_hint={'center_x':0.5,'center_y':0.5}
# #     #                                    ,size_hint=(.5,.1),on_press=self.func)
# #     #     f.add_widget(button)
# #     #     return f

# # Main().run()