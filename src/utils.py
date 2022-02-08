from sys import stdout

underscorify = lambda string : string.lower().replace(' ', '_').replace('-', '_')
dashify = lambda string : string.lower().replace(' ', '-').replace('_', '-')

class Setting:
    def __init__(self, name:str, type:str, default:str, data:list=None, widget_type:str=None):
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

class Common:
    def __init__(self):
        self.parent = None
        self.__sections = set()
        self.__settings = set()

    def add_setting(self, name:str, type:str, default:str, data:list=None, widget_type:str=None):
        ''' Add a setting to current SettingsList or Section

        name: name of the setting
        type: type of setting
        data: choices or range for the value (depends on type)
        widget_type: the type of widget that should be associated with this setting '''

        setting = Setting(name, type, default, data, widget_type)
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

    def get_settings(self):
        return list(self.__settings)

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

    def get_sections(self):
        return self.__sections

    def get_children(self):
        return list(self.__sections) + list(self.__settings)

    def get_settings_recursively(self):
        settings = self.get_settings()
        for section in self.__sections:
            settings += section.get_settings_recursively()
        return settings

    def get_schema_id(self):
        return self.parent.get_schema_id() + '.' + self.name

    def get_schema_path(self):
        return '/' + self.get_schema_id().replace('.', '/') + '/'

    def print_schema(self, full:bool=False, recursive:bool=False, file=stdout):
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

class Section(Common):
    def __init__(self, name:str):
        super().__init__()
        self.name = dashify(name)

class SettingsList(Common):
    def __init__(self, schema_id:str):
        super().__init__()
        self.schema_id = schema_id

    def get_schema_id(self):
        return self.schema_id

