from sys import stdout
import gi
from .errors import WidgetNotFoundError

from gi.repository import Gtk, Gio

underscorify = lambda string : string.lower().replace(' ', '_').replace('-', '_')
dashify = lambda string : string.lower().replace(' ', '-').replace('_', '-')

class Setting:
    def __init__(self,
            name:str,
            type:str,
            default:str,
            data:list=None,
            widget_type:str=None,
            summary:str=None,
            description:str=None,
            ):
        ''' Create a setting object

        name: name of the setting
        type: type of setting
        data: choices or range for the value (depends on type)
        widget_type: the type of widget that should be associated with this setting '''

        self.parent = None
        self.name = dashify(name)
        self.type = type
        self.default = default
        self.data = data
        self.widget_type = widget_type
        self.summary = summary
        self.description = description

class Common:
    def __init__(self):
        self.parent = None
        self.builder = None
        self.__sections = set()
        self.__settings = set()
        self.__connected = False

    def add_setting(self,
            name:str,
            type:str,
            default:str,
            data:list=None,
            widget_type:str=None,
            summary:str=None,
            description:str=None,
            ):
        ''' Add a setting to current SettingsList or Section

        name: name of the setting
        type: type of setting
        data: choices or range for the value (depends on type)
        widget_type: the type of widget that should be associated with this setting
        summary: a short summary of the setting
        description: detailed description of the setting
        '''

        setting = Setting(
                name=name,
                type=type,
                default=default,
                data=data,
                widget_type=widget_type,
                summary=summary,
                description=description,
                )
        setting.parent = self
        self.__settings.add(setting)
        return setting

    def remove_setting(self, name:str):
        for setting in self.__settings:
            if setting.name == name:
                self.__settings.remove(setting)

    def get_setting(self, name:str):
        for setting in self.__settings:
            if setting.name == name:
                return setting

    def get_settings(self, recursive:bool=False):
        settings = list(self.__settings)
        if recursive:
            for section in self.__sections:
                settings += section.get_settings(recursive=True)
        return settings

    def add_section(self, name:str):
        section = Section(name)
        section.parent = self
        self.__sections.add(section)
        return section

    def remove_section(self, name:str):
        for section in self.__sections:
            if section.name == name:
                self.__sections.remove(section)

    def get_section(self, name:str):
        for section in self.__sections:
            if section.name == name:
                return section

    def get_sections(self, recursive:bool=False):
        sections = list(self.__sections)
        if recursive:
            for section in self.__sections:
                sections += section.get_sections(recursive=True)
        return sections


    def get_children(self):
        return list(self.__sections) + list(self.__settings)

    def get_schema_id(self):
        return self.parent.get_schema_id() + '.' + self.name

    def get_schema_path(self):
        return '/' + self.get_schema_id().replace('.', '/') + '/'

    def print_schema(self, full:bool=True, recursive:bool=False, file=stdout):
        if full:
            print('<?xml version="1.0" encoding="UTF-8"?>', file=file)
            print('<schemalist>', file=file)

        print(file=file)
        print(' '*2 + f'<schema id="{self.get_schema_id()}" path="{self.get_schema_path()}">', file=file)

        if len(self.__sections):
            print(file=file)
        for section in self.__sections:
            print(' '*4 + f'<child name="{section.name}" schema="{section.get_schema_id()}"/>', file=file)

        for setting in self.__settings:
            print(file=file)
            key_type = ''
            if setting.type == 'bool':
                key_type = 'b'
            elif setting.type in ['text', 'font', 'file', 'color', 'list']:
                key_type = 's'
            elif setting.type == 'real':
                key_type = 'd'
            elif setting.type == 'int':
                key_type = 'i'
            print(' '*4 + f'<key name="{setting.name}" type="{key_type}">', file=file)

            if setting.summary:
                print(' '*6 + f'<summary>{setting.summary}</summary>', file=file)

            if setting.description:
                print(' '*6 + f'<description>{setting.description}</description>', file=file)

            if key_type == 's':
                print(' '*6 + f'<default>"{setting.default}"</default>', file=file)
            else:
                print(' '*6 + f'<default>{setting.default}</default>', file=file)

            if setting.type == 'list' and setting.data:
                print(' '*6 + f'<choices>', file=file)
                for choice in setting.data:
                    print(' '*8 + f'<choice value="{choice}"/>', file=file)
                print(' '*6 + f'</choices>', file=file)

            if setting.type in ['int', 'real'] and setting.data:
                min = setting.data[0]
                max = setting.data[1]
                print(' '*6 + f'<range min="{min}" max="{max}"/>', file=file)

            print(' '*4 + '</key>', file=file)

        print(file=file)
        print(' '*2 + '</schema>\n', file=file)

        if recursive:
            for section in self.__sections:
                section.print_schema(recursive=True, file=file)

        if full:
            print('</schemalist>', file=file)

    def set_builder(self, builder:Gtk.Builder):
        if type(builder) is Gtk.Builder:
            self.builder = builder
        else:
            raise TypeError("Provided builder is not a Gtk.Builder")

    def get_builder(self):
        return self.builder or self.parent.get_builder()

    def __connect_setting_to_gsettings(self, setting):
        get_object = self.get_builder().get_object
        setting_name = underscorify(setting.name)
        if setting.type == 'bool':
            if widget := get_object(setting_name + '_switch'):
                self.__gsettings.bind(setting.name, widget, 'active', Gio.SettingsBindFlags.DEFAULT)
                print(f"connected setting '{setting.name}'")
                return
        elif setting.type in ['int', 'real']:
            if setting.widget_type:
                if widget := get_object(setting_name + '_' + setting.widget_type):
                    self.__gsettings.bind(setting.name, widget, 'value', Gio.SettingsBindFlags.DEFAULT)        
                    print(f"connected setting '{setting.name}'")
                    return
            else:
                if widget := (get_object(setting_name + '_spinbutton') or get_object(setting_name + '_scale')):
                    self.__gsettings.bind(setting.name, widget, 'value', Gio.SettingsBindFlags.DEFAULT)        
                    print(f"connected setting '{setting.name}'")
                    return

        raise WidgetNotFoundError(f"could not find a suitable widget for setting '{setting.name}'")

    def connect_to_gsettings(self, force=False):
        if builder := self.get_builder():
            if force or not self.__connected:
                self.__gsettings = Gio.Settings(schema_id=self.get_schema_id())
                for setting in self.get_settings():
                    self.__connect_setting_to_gsettings(setting)
                for section in self.get_sections():
                    section.connect_to_gsettings()
                self.__connected = True
        else:
            raise ValueError("Tried to connect to gsettings without setting a builder first")

    def connect_to(self, obj):
        if self.get_builder():
            pass
        else:
            raise ValueError("Tried to connect to an object without setting a builder first")

class Section(Common):
    def __init__(self, name:str):
        super().__init__()
        self.name = dashify(name)

class Settings(Common):
    def __init__(self, schema_id:str):
        super().__init__()
        self.schema_id = schema_id

    def get_schema_id(self):
        return self.schema_id

    def get_builder(self):
        return self.builder

