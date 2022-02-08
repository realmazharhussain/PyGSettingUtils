project('PyGSettingUtils',
        version: '0.1-alpha',
  meson_version: '>= 0.57.0')

py_module_name = meson.project_name().replace('Py', '')

dependency('pygobject-3.0')

python = import('python').find_installation('python3')
py_modules_dir = python.get_install_dir()
py_proj_dir = py_modules_dir / py_module_name

conf = configuration_data()
conf.set('project_name',   meson.project_name() )
conf.set('version',        meson.project_version() )
conf.set('py_module_name', py_module_name)

bindir = get_option('bindir')

subdir('src')
