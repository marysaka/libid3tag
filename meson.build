project(
	'id3tag',
	'c',
	version: '0.16.2',
	license: 'GPL-2.0-or-later',
	default_options: [
		'c_std=c99',
	],
	meson_version: '>=0.56',
)

project_arguments = []

compiler = meson.get_compiler('c')

is_windows = target_machine.system() == 'windows' or target_machine.system() == 'cygwin'

id3tag_srcs = files(
	'compat.c',
	'crc.c',
	'debug.c',
	'field.c',
	'file.c',
	'frame.c',
	'frametype.c',
	'genre.c',
	'latin1.c',
	'parse.c',
	'render.c',
	'tag.c',
	'ucs4.c',
	'utf16.c',
	'utf8.c',
	'util.c',
	'version.c',
)

cdata = configuration_data()
cdata.set('CMAKE_PROJECT_VERSION_MAJOR', meson.project_version().split('.')[0])
cdata.set('CMAKE_PROJECT_VERSION_MINOR', meson.project_version().split('.')[1])
cdata.set('CMAKE_PROJECT_VERSION_PATCH', meson.project_version().split('.')[2])

id3tag_header = configure_file(
	input: 'id3tag.h.in',
	output: 'id3tag.h',
	configuration: cdata
)

if compiler.has_header('sys/stat.h')
	project_arguments += '-DHAVE_SYS_STAT_H'
endif

if compiler.has_header('unistd.h')
	project_arguments += '-DHAVE_UNISTD_H'
endif

if compiler.has_header('assert.h')
	project_arguments += '-DHAVE_ASSERT_H'
endif

if compiler.has_function('ftruncate')
	project_arguments += '-DHAVE_FTRUNCATE'
endif

zlib = dependency('zlib', required: true)

if is_windows
	id3tag = static_library(
		'id3tag',
		id3tag_srcs,
		sources: [id3tag_header],
		c_args: project_arguments,
		dependencies: zlib,
		install: true,
	)
else
	id3tag = library(
		'id3tag',
		id3tag_srcs,
		sources: [id3tag_header],
		c_args: project_arguments,
		version: meson.project_version(),
		soversion: meson.project_version(),
		dependencies: zlib,
		install: true,
	)
endif

install_headers(id3tag_header)

id3tag_dep = declare_dependency(
	link_with: id3tag,
	dependencies: zlib,
	include_directories: include_directories('.')
)

pkg = import('pkgconfig')

pkg.generate(
	id3tag,
	description: 'ID3 tag manipulation library for MP3 files',
	url: 'https://codeberg.org/tenacityteam/libid3tag',
)
