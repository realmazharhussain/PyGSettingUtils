from GSettingUtils import Settings

settings = Settings(schema_id='org.gtk.example')

#settings.add_setting("never-applied", "bool", 'true',
#        summary="Whether settings have been applied before",
#        description="No description here",
#        )

#appearance_section = settings.add_section("Appearance")
#appearance_section.add_setting("shell-theme","list", 'default')
#appearance_section.add_setting("icon-theme","list", 'Adwaita')
#appearance_section.add_setting("cursor-theme","list", 'Adwaita')
#appearance_section.add_setting("background-type","list", 'none', ["none", "image", "color"])
#appearance_section.add_setting("background-image","file", '')
#appearance_section.add_setting("background-color","color", 'rgb(40,40,40)')

fonts_section = settings.add_section("Fonts")
#fonts_section.add_setting("font", 'font', 'Sans 11')
#fonts_section.add_setting("antialiasing", 'list', 'grayscale', ["grayscale", "rgba", "none"])
#fonts_section.add_setting("hinting", 'list', 'slight', ["full", "medium", "slight", "none"])
fonts_section.add_setting("scaling-factor", 'real', '1', ['0.5','3'], widget_type='spinbutton')

top_bar_section = settings.add_section("Top Bar")
#top_bar_section.add_setting("change-text-color", "bool", 'false')
#top_bar_section.add_setting("text-color", "color", 'rgb(250,250,250)')
#top_bar_section.add_setting("change-background-color", "bool", 'false')
#top_bar_section.add_setting("background-color", "color", 'rgb(0,0,0)')
top_bar_section.add_setting("disable-arrows", "bool", 'false')
top_bar_section.add_setting("disable-rounded-corners", "bool", 'false')
top_bar_section.add_setting("show-weekday", "bool", 'false')
top_bar_section.add_setting("show-seconds", "bool", 'false')
#top_bar_section.add_setting("time-format", "list", '24h', ["24h", "12h"])
top_bar_section.add_setting("show-battery-percentage", "bool", 'false')

sound_section = settings.add_section("Sound")
#sound_section.add_setting("theme", "list", 'freedesktop')
sound_section.add_setting("over-amplification", "bool", 'false')
sound_section.add_setting("event-sounds", "bool", 'true')
sound_section.add_setting("feedback-sounds", "bool", 'false')

touchpad_section = settings.add_section("Touchpad")
touchpad_section.add_setting("tap-to-click", "bool", 'true')
touchpad_section.add_setting("natural-scrolling", "bool", 'true')
touchpad_section.add_setting("two-finger-scrolling", "bool", 'true')
touchpad_section.add_setting("speed", "real", '0.35', ['-1','1'], widget_type="scale")

night_light_section = settings.add_section("Night Light")
night_light_section.add_setting("enable", "bool", 'false')
night_light_section.add_setting("color-temperature", "real", '3000', ['1700','4700'], widget_type="scale")
night_light_schedule_section = night_light_section.add_section("schedule")
#night_light_schedule_section.add_setting("type", "list", 'automatic', ["automatic", "manual"])
night_light_schedule_section.add_setting("start-hour", "int", '19', ['0','23'], widget_type="spinbutton")
night_light_schedule_section.add_setting("start-minute", "int", '0', ['0','59'], widget_type="spinbutton")
night_light_schedule_section.add_setting("end-hour", "int", '6', ['0','23'], widget_type="spinbutton")
