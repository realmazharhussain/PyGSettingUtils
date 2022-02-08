configure_file(
  input:  'info.py.in',
  output: 'info.py',
  configuration: conf,
  install: true,
  install_dir: py_proj_dir,
)

source_files = [
  '__init__.py',
  'utils.py',
]
install_data(source_files, install_dir: py_proj_dir)

configure_file(
  input: 'create-gschemas.in',
  output: '@BASENAME@',
  configuration: conf,
  install_dir: get_option('bindir'),
)
