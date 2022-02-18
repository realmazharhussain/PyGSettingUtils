#!/bin/env python3
import tests.example
import gi
from gi.repository import Adw, Gtk
app = Adw.Application()
app.builder = Gtk.Builder()
directory = '/home/mazhar/gitapps/gdm-settings/build/src/blueprints/gdm-settings'
for filename in ['main-window.ui', 'appearance-page.ui', 'night-light-page.ui', 'top-bar-page.ui', 'fonts-page.ui', 'misc-page.ui', 'sound-page.ui', 'touchpad-page.ui']:
    app.builder.add_from_file(directory + '/' + filename)
tests.example.settings.set_builder(app.builder)
tests.example.settings.connect_to_gsettings()
