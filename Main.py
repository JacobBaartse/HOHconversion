#!/usr/bin/python
import os.path

from SongEditorPro7Generic import convert_song
import glob


if __name__ == "__main__":

    # input_dir = r"C:\Users\fam_b\Downloads\HOH_7mei2024\Beamer Song Database"
    # input_dir = r"C:\Users\fam_b\Downloads\HOH_7mei2024\snel"
    input_dir = r"C:\Users\fam_b\Downloads\Beamer Song Database-20250326T195341Z-001\Beamer Song Database"
    output_dir = r"C:\Users\fam_b\Downloads\Beamer Song Database-20250326T195341Z-001\Converted"

    for input_filename in glob.glob(input_dir + r"\*"):
        # input_dir = r"C:\Users\fam_b\Downloads\Beamer Song Database-20250326T195341Z-001\Beamer Song Database"
        input_filename = os.path.join(input_dir, "O-0012 All over the world.pro")
        filename = os.path.basename(input_filename)
        output_filename = os.path.join(output_dir, filename)
        print(filename)
        convert_song(input_filename, output_filename)
        exit()



