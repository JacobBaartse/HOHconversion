import presentation_pb2
from uuid import uuid1

TEMPLATE = 0


def make_uuid():
    tmp = uuid1().urn.split("uuid:")[1]
    return tmp


text_block_names = {}

rtf_tags = [
    b"\\ansicpg1252",
    b"\\ansi",

    b"\\b",

    b"\\cocoartf2636",
    b"\\cocoatextscaling0",
    b"\\cocoaplatform0",
    b"\\cocoartf1671",
    B"\\cocoartf2578",
    b"\\cb1",
    b"\\cb3",

    b"\\deftab720",
    b"\\deftab708",

    b"\\expnd0",
    b"\\expndtw0",

    b"\\fs132",
    b"\\fs88",
    b"\\fs98",
    b"\\f10",
    b"\\fs148",
    b"\\f0",
    b"\\f1",
    b"\\f2",

    b"\\i0",
    b"\\i",

    b"\\kerning0",
    b"\\kerning1",

    b" \\\n",
    b"\n",

    b"\\nosupersub",

    b"\\outl0",

    b"\\pardeftab720",
    b"\\pardirnatural",
    b"\\partightenfactor0",
    b"\\pard",

    b"\\rtf1",

    b"\\slleading120",
    b"\\strokewidth0",
    b"\\strokec2",
    b"\\strokewidth-20",
    b"\\strokec0",
    ]


def rtf_remove_tabel(rtf_data, p_from):
    split_rtf_table_start = rtf_data.split(p_from)
    prepending_part = split_rtf_table_start[0]
    left_brace_count = 1
    right_brace_count = 0
    if len(split_rtf_table_start) > 1:
        remaining_part = split_rtf_table_start[1]
        for idx in range(len(remaining_part)):
            cur_char = chr(remaining_part[idx])
            if cur_char == "{":
                left_brace_count += 1
            if cur_char == "}":
                right_brace_count += 1
            if left_brace_count == right_brace_count:
                return prepending_part + remaining_part[idx+1:]
    else:
        return rtf_data


def rtf_get_data_first(rtf_data, p_from, p_to):
    tmp = rtf_data.split(p_from)
    if len(tmp) > 1:
        return tmp[1].split(p_to)[0].strip(b"\n")
    else:
        return b""


def get_color_table(rtf_data):
    color_table = rtf_get_data_first(rtf_data, b"{\\colortbl;", b"}")
    color_table = color_table.replace(b"\n", b"")
    return color_table.split(b";")


to_be_removed = [b"rtf", b"ansi", b"ansicpg", b'cocoartf', b'cocoaplatform', b'deftab', b'partightenfactor', b'fs',
                 b'nosupersub', b'strokewidth',  b'strokec', b'expndtw', b'cb', b'fsmilli', b'kerning',
                 b'f', b'b', b'i',  b'super', b'AppleTypeServicesF', b'AppleTypeServices'
                 ]

to_be_kept = [b'cf', b'u', b"'", b"par"]

quoted_values = set()


 #  '´ ä‘œ–Éãíâ°“ê—áëéó®ö…èñÓÔÄÕàÎôúÀ£î’”Ò

special_character = {b'ce': b"\\u206 ",  # b"Î",  b"'",  # b"'",
                     b'91': b"'",  # b"´",
                     b'c4': b"\\u196 ",  # b"Ä",  b" ",  # b" ",
                     b'f6': b"\\u246 ",  # b"ö",  b"\\u228 ",  # b"ä",
                     b'a3': b"\\u163 ",  # b"£",  b"'",  # b"`",
                     b'97': b"-",        # b"-",  b"\\u339 ",  # b"œ",
                     b'c0': b"\\u192 ",  # b"À",  b"-",  # b"-",
                     b'fa': b"\\u250 ",  # b"ú",  b"\\u201 ",  # b"É",
                     b'b4': b"'",        # b"´",  b"\\u227 ",  # b"ã",
                     b'ee': b"\\u238 ",  # b"î",  b"\\u237 ",  # b"í",
                     b'd2': b"\\u210 ",  # b"Ò",  b"\\u226 ",  # b"â",
                     b'e3': b"\\u227 ",  # b"ã",  b"\\u186 ",  # b"°",
                     b'e4': b"\\u228 ",  # b"ä",  b'"',  # b'"',
                     b'ea': b"\\u234 ",  # b"ê",
                     b'9c': b"\\u339 ",  # b"œ",  b"-",  # b"-",
                     b'e2': b"\\u226 ",  # b"â",  b"\\u225 ",  # b"á",
                     b'e1': b"\\u225 ",  # b"á",  b"\\u235 ",  # b"ë",
                     b'96': b"-",        # b"-",  b"\\u233 ",  # b"é",
                     b'93': b'"',        # b'"',  b"\\u243 ",  # b"ó",
                     b'b0': b"\\u186 ",  # b"°",  b"\\u174 ",  # b"®",
                     b'92': b"'",        # b"´",  b"\\u246 ",  # b"ö",
                     b'e8': b"\\u232 ",  # b"è",  b"...",  # b"...",
                     b'ac': b"-",        # b"-",  b"\\u232 ",  # b"è",
                     b'd4': b"\\u212 ",  # b"Ô",  b"\\u241 ",  # b"ñ",
                     b'c9': b"\\u201 ",  # b"É",  b"\\u211 ",  # b"Ó",
                     b'eb': b"\\u235 ",  # b"ë",  b"\\u212 ",  # b"Ô",
                     b'a0': b" ",        # b" "   b"\\u196 ",  # b"Ä",
                     b'f1': b"\\u241 ",  # b"ñ",  b"\\u213 ",  # b"Õ",
                     b'd5': b"\\u213 ",  # b"Õ",  b"\\u224 ",  # b"à",
                     b'f4': b"\\u244 ",  # b"ô",  b"\\u206 ",  # b"Î",
                     b'e0': b"\\u224 ",  # b"à",  b"\\u244 ",  # b"ô",
                     b'85': b"...",      # b"...",b"\\u250 ",  # b"ú",
                     b'ed': b"\\u237 ",  # b"í",  b"\\u192 ",  # b"À",
                     b'94': b'"',        # b'"',  b"\\u163 ",  # b"£",
                     b'ae': b"\\u174 ",  # b"®",  b"\\u238 ",  # b"î",
                     b'f3': b"\\u243 ",  # b"ó",  b"'",  # b"'",
                     b'd3': b"\\u211 ",  # b"Ó",  b'"',  # b'"',
                     b'e9': b"\\u233 ",  # b"é",   b"\\u210 ",  # b"Ò",
                     }



def remove_rtf_tags(rtf_data, filename):
    # print(1, rtf_data)
    rtf_data = rtf_data.replace(b"\\\n", b"\\par ")
    rtf_data = rtf_data.replace(b"\n", b"")
    return_data = b""
    list_rtf_data = rtf_data.split(b"\\")
    for rtf_part in list_rtf_data:
        # if rtf_part == b"'e9":
        #     print("debug point")
        # print(2, rtf_part)
        rtf_element_name = None
        if len(rtf_part) == 0:
            # print("debug print")
            continue
        if rtf_part[0:1] == b"'":
            # return_data += b"\\" + rtf_part
            # print(21, rtf_part)
            return_data += special_character[rtf_part[1:3]]
            if len(rtf_part) > 3:
                return_data += rtf_part[3:]
            continue
        for idx in range(len(rtf_part)):
            if not rtf_element_name:
                if chr(rtf_part[idx]) in (r" \-0123456789"):
                    rtf_element_name = rtf_part[:idx]
                    # print(31, return_data)
            if rtf_element_name:
                if chr(rtf_part[idx]) not in (r"-0123456789"):
                    if rtf_element_name in to_be_removed:
                        return_data += rtf_part[idx:]
                        # print(40, return_data)
                        break
                    elif rtf_element_name in to_be_kept:
                        return_data += b"\\" + rtf_part
                        # print(41, return_data)
                        break
                    else:
                        # print(43, return_data)
                        exit(-1)

    # check special characters conversion.
    # return_data = b""
    # for key in special_character:
    #     return_data += key + b"-:\\'" + key + b"-" + special_character[key].replace(b"\\", b"") + b"-" + special_character[key] + b"\\par "
    # print(return_data)

    return return_data


color_to_name = {b'\\red255\\green255\\blue255': "SongText",
                 b'\\red0\\green190\\blue255': "Translation 1",
                 b'\\red255\\green247\\blue97': "Translation 2",
                 b'\\red91\\green237\\blue197': "SongText",
                 b'\\red51\\green51\\blue51': "SongText",
                 }


def split_on_color(rtf_data, color_table):
    prev_color_nr = 0
    rtf_data = rtf_data.replace(b"}", b"")
    rtf_datas = rtf_data.split(b"\\cf")
    return_value = {"SongText": b"",
                    "Translation 1": b"",
                    "Translation 2": b""}
    for rtf_data in rtf_datas:
        rtf_data = rtf_data.strip()
        if rtf_data:
            try:
                color_nr = int(chr(rtf_data[0]))-1
                if color_nr == -1:
                    color_nr = prev_color_nr
            except ValueError:
                color_nr = prev_color_nr
            color = color_table[color_nr]
            song_line = rtf_data[1:]
            song_line = song_line.strip()
            if song_line:
                if color in color_to_name:
                    text_block_name = color_to_name[color]
                    # print(text_block_name, song_line)
                    if return_value[text_block_name]:
                        return_value[text_block_name] += b"\\par " + song_line
                    else:
                        return_value[text_block_name] = song_line
                else:
                    print("ERROR: color not found in color_to_name", color)
                    exit(-3)
        for key, value in return_value.items():
            while b"\\par \\par" in return_value[key]:
                return_value[key] = return_value[key].replace(b"\\par \\par", b"\\par")
            while b"\\par\\par" in return_value[key]:
                return_value[key] = return_value[key].replace(b"\\par\\par", b"\\par")
    return return_value


rtf_data_big_font = b'{\\rtf0\\ansi\\ansicpg1252' \
                    b'{\\fonttbl\\f0\\fnil ArialMT;}' \
                    b'{\\colortbl;\\red255\\green255\\blue255;\\red255\\green255\\blue255;}' \
                    b'{\\*\\expandedcolortbl;\\csgenericrgb\\c100000\\c100000\\c100000\\c100000;\\csgenericrgb\\c100000\\c100000\\c100000\\c0;}' \
                    b'{\\*\\listtable}' \
                    b'{\\*\\listoverridetable}' \
                    b'\\uc0\\paperw37980\\margl0\\margr0\\margt0\\margb0\\pard\\li0\\fi0\\ri0\\qc\\sb0\\sa0\\sl240\\slmult1\\slleading0\\f0\\b0\\i0\\ul0\\strike0\\fs120\\expnd0\\expndtw0\\cf1\\strokewidth0\\strokec1\\nosupersub\\ulc0\\highlight2\\cb2 '


def convert_song(input_filename, output_filename):
    presentation_obj = presentation_pb2.Presentation()
    file1 = open(input_filename, mode='rb')
    presentation_obj.ParseFromString(file1.read())

    uuid_label_dict = dict()
    for cue_group in presentation_obj.cue_groups:
        # print(cue_group.group.name)  # slide_label
        for cue_identifier in cue_group.cue_identifiers:
            # print(cue_identifier.string)  # slide_uuid
            uuid_label_dict[cue_identifier.string] = cue_group.group.name
    # print(uuid_label_dict)

    slide_list = []

    for presentation_que in presentation_obj.cues:
        slide_list.append(dict())
        if presentation_que.uuid.string in uuid_label_dict:
            # print(uuid_label_dict[presentation_que.uuid.string])
            slide_list[-1]["label"] = uuid_label_dict[presentation_que.uuid.string]
        for action in presentation_que.actions:
            element_count = 0
            if len(action.slide.presentation.base_slide.elements) > 1:
                print("ERROR already multiple text elements in slide", input_filename)
                exit(-4)
            for element in action.slide.presentation.base_slide.elements:
                text_block_names[element.element.name] = 1
                rtf_data = element.element.text.rtf_data  # .split(b"\\f1\\")
                # for rtf_data in rtf_datas:
                color_table = get_color_table(rtf_data)
                # print(rtf_data)
                rtf_data = rtf_remove_tabel(rtf_data, b"{\\colortbl;")
                # print(rtf_data)
                rtf_data = rtf_remove_tabel(rtf_data, b"{\\fonttbl")
                # print(rtf_data)
                rtf_data = rtf_remove_tabel(rtf_data, b"{\\*\\expandedcolortbl;")
                rtf_data = rtf_remove_tabel(rtf_data, b"{\\*\\listtable")
                rtf_data = rtf_remove_tabel(rtf_data, b"{\\*\\listoverridetable")

                # print(rtf_data)
                rtf_data = remove_rtf_tags(rtf_data, filename=input_filename)
                rtf_data = rtf_data.replace(b"\\u8232 ?", b"\\par ")
                # print(rtf_data)
                rtf_datas = split_on_color(rtf_data, color_table)
                # print(rtf_datas)
            if (action.slide.presentation.base_slide.elements):
                # update current element
                action.slide.presentation.base_slide.elements[0].element.name = "SongText"
                action.slide.presentation.base_slide.elements[0].element.text.rtf_data = rtf_data_big_font + rtf_datas["SongText"] + b"}"

                # copy element for translation 1
                action.slide.presentation.base_slide.elements.add()
                action.slide.presentation.base_slide.elements[-1].CopyFrom(action.slide.presentation.base_slide.elements[0])
                action.slide.presentation.base_slide.elements[-1].element.uuid.string = make_uuid()
                action.slide.presentation.base_slide.elements[-1].element.name = "Translation 1"
                action.slide.presentation.base_slide.elements[-1].element.text.rtf_data = rtf_data_big_font + rtf_datas["Translation 1"] + b"}"

                # copy element for translation 2
                action.slide.presentation.base_slide.elements.add()
                action.slide.presentation.base_slide.elements[-1].CopyFrom(action.slide.presentation.base_slide.elements[0])
                action.slide.presentation.base_slide.elements[-1].element.uuid.string = make_uuid()
                action.slide.presentation.base_slide.elements[-1].element.name = "Translation 2"
                action.slide.presentation.base_slide.elements[-1].element.text.rtf_data = rtf_data_big_font + rtf_datas["Translation 2"] + b" }"

                # exit(-5)

    #print(text_block_names)
    with open(output_filename, "wb") as pro_file:
        pro_file.write(presentation_obj.SerializeToString())

    # todo  add \\qr   right allign to frasi ??


if __name__ == "__main__":
    rtf_data = b'{\\cf1\\strokewidth0 Ik ben de ware wijnstok\\par\\pard\\expndtw0\\cf1\\strokewidth0\\strokec1 Mijn Vader is de landman\\par\\pard\\li0\\fi0\\ri0\\qj\\sb0\\sa0\\sl20\\slmult0\\slleading0\\f0\\b0\\i0\\ul0\\strike0\\fs90\\expnd0\\expndtw0\\cf1\\strokewidth0\\strokec1\\nosupersub\\ulc0\\highlight2\\cb2 Jullie zijn de ranken\\par\\pard\\li0\\fi0\\ri0\\qj\\sb0\\sa0\\sl20\\slmult0\\slleading0\\f0\\b0\\i0\\ul0\\strike0\\fs90\\expnd0\\expndtw0\\cf1\\strokewidth0\\strokec1\\nosupersub\\ulc0\\highlight2\\cb2 Dus blijf in Mij\\par\\pard\\li0\\fi0\\ri0\\qj\\sb0\\sa0\\sl20\\slmult0\\slleading0\\f0\\b0\\i0\\ul0\\strike0\\fs90\\expnd0\\expndtw0\\cf1\\strokewidth0\\strokec1\\nosupersub\\ulc0\\highlight2\\cb2 Want wie in Mij wil leven\\par\\pard\\li0\\fi0\\ri0\\qj\\sb0\\sa0\\sl20\\slmult0\\slleading0\\f0\\b0\\i0\\ul0\\strike0\\fs90\\expnd0\\expndtw0\\cf1\\strokewidth0\\strokec1\\nosupersub\\ulc0\\highlight2\\cb2 Die zal Ik leven geven\\par\\pard\\li0\\fi0\\ri0\\qj\\sb0\\sa0\\sl20\\slmult0\\slleading0\\f0\\b0\\i0\\ul0\\strike0\\fs90\\expnd0\\expndtw0\\cf1\\strokewidth0\\strokec1\\nosupersub\\ulc0\\highlight2\\cb2 Blijf in Mijn liefde\\par\\pard\\li0\\fi0\\ri0\\qj\\sb0\\sa0\\sl20\\slmult0\\slleading0\\f0\\b0\\i0\\ul0\\strike0\\fs90\\expnd0\\expndtw0\\cf1\\strokewidth0\\strokec1\\nosupersub\\ulc0\\highlight2\\cb2 Blijf in Mij}'
    test = remove_rtf_tags(rtf_data, "test")
    print([test])
