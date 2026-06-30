project(
	'id3tag',
	'c',
	version: '0.16.4',
	license: 'GPL-2.0-or-later',
	default_options: [
		'c_std=gnu99',
	],
	meson_version: '>=0.56',
)

project_arguments = []

compiler = meson.get_compiler('c')

is_windows = target_machine.system() == 'windows' or target_machine.system() == 'cygwin'

foreach p : ['python3', 'python']
	prog_python = find_program(p, required: false, version: '>= 3.6')
	if not prog_python.found()
		continue
	endif
endforeach

if not prog_python.found()
	error('Python 3.6+ not found')
endif

genre_dat = custom_target(
	'genre.dat',
	input: ['gengenre.py', 'src/genre.dat.in'],
	output: 'genre.dat',
	command: [prog_python, '@INPUT0@', '@INPUT1@', '@OUTPUT0@'],
)

id3tag_srcs = files(
	'src/crc.c',
	'src/debug.c',
	'src/field.c',
	'src/file.c',
	'src/frame.c',
	'src/genre.c',
	'src/latin1.c',
	'src/parse.c',
	'src/render.c',
	'src/tag.c',
	'src/ucs4.c',
	'src/utf16.c',
	'src/utf8.c',
	'src/util.c',
	'src/version.c',
)

# See CMakeLists.txt but in case of old gperf (like on macOS) report gperf weirdness.
prog_gperf = find_program('gperf', required: false, version: '>= 3.1')
if not prog_gperf.found()
	prog_gperf = find_program('gperf', required: true)
	project_arguments += '-DGPERF_LEN_TYPE_UNSIGNED'
endif

gen_gperf = generator(
	prog_gperf,
	output: '@BASENAME@.c',
	arguments: ['-L', 'ANSI-C',
				'-tCcTonD', '-K', 'id',
				'-N', 'id3_@BASENAME@_lookup',
				'-s', '-3', '-k', '*',
				'--output-file=@OUTPUT0@',
				'@INPUT@'],
)

compat_c = gen_gperf.process(files('src/compat.gperf'))
frametype_c = gen_gperf.process(files('src/frametype.gperf'))

cdata = configuration_data()
cdata.set('PROJECT_VERSION_MAJOR', meson.project_version().split('.')[0])
cdata.set('PROJECT_VERSION_MINOR', meson.project_version().split('.')[1])
cdata.set('PROJECT_VERSION_PATCH', meson.project_version().split('.')[2])

id3tag_header = configure_file(
	input: 'include/id3tag.h.in',
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

if compiler.has_function('fseeko')
	project_arguments += '-DHAVE_FSEEKO'
	project_arguments += '-DHAVE_FTELLO'
endif

zlib = dependency('zlib', required: true)

if is_windows
	id3tag = static_library(
		'id3tag',
		id3tag_srcs,
		sources: [id3tag_header, genre_dat, compat_c, frametype_c],
		include_directories: include_directories('src'),
		c_args: project_arguments,
		dependencies: zlib,
		install: not meson.is_subproject(),
	)
else
	id3tag = library(
		'id3tag',
		id3tag_srcs,
		sources: [id3tag_header, genre_dat, compat_c, frametype_c],
		include_directories: include_directories('src'),
		c_args: project_arguments,
		version: meson.project_version(),
		soversion: meson.project_version(),
		dependencies: zlib,
		install: true,
	)
endif

if not meson.is_subproject()
	install_headers(id3tag_header)
endif

id3tag_dep = declare_dependency(
	link_with: id3tag,
	dependencies: zlib,
	include_directories: include_directories('.')
)

pkg = import('pkgconfig')

if not meson.is_subproject()
	pkg.generate(
		id3tag,
		description: 'ID3 tag manipulation library for MP3 files',
		url: 'https://codeberg.org/tenacityteam/libid3tag',
	)
endif
