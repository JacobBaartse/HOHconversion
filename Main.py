#!/usr/bin/python
import os.path

from SongEditorPro7Generic import convert_song
import glob


if __name__ == "__main__":

    # input_dir = r"C:\Users\fam_b\Downloads\HOH_7mei2024\Beamer Song Database"
    # input_dir = r"C:\Users\fam_b\Downloads\HOH_7mei2024\snel"
    input_dir = r"C:\Users\fam_b\Downloads\HOH_7mei2024\afterCleanup"
    output_dir = r"C:\Users\fam_b\Downloads\HOH_7mei2024\Converted"

    for input_filename in glob.glob(input_dir + r"\*"):
        # input_dir = r"D:\testHOHSamples"
        # input_filename = os.path.join(input_dir, "test farsi.pro")
        filename = os.path.basename(input_filename)
        output_filename = os.path.join(output_dir, filename)
        # print(filename)
        convert_song(input_filename, output_filename)
        # exit()



