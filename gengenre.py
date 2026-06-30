# Replacement of genre.dat.cmake that reproduce the same output
import sys
import re

if len(sys.argv[1:]) != 2:
    print(f"Usage: {sys.argv[0]} <input_file> <output_file>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]


genres = list()
with open(input_file, "r") as f:
    for line in f.readlines():
        match = re.search("^[a-zA-Z]", line.strip())
        if not match:
            continue
        genres.append(match.string)


with open(output_file, "w") as f:
    f.write("/* Automatically generated from src/genre.dat.in */\n\n")

    genre_string_names = list()
    for genre in genres:
        genre_string_name = re.sub("[^a-zA-Z0-9]", "_", genre.upper())
        f.write(f"static id3_ucs4_t const genre_{genre_string_name}[] =\n")
        f.write(f"  {{ ")
        for letter in list(genre):
            f.write(f"'{letter}', ")
        f.write(f"0 }};\n")
        genre_string_names.append(f"  genre_{genre_string_name}")

    f.write("static id3_ucs4_t const *const genre_table[] = {\n")
    f.write(f'{',\n'.join(genre_string_names)}\n')
    f.write("};\n")
