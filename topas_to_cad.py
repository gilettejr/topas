import numpy as np


def get_cad_arrays_from_topas(topas_script):
    def rounded(str_third_last, str_second_last, str_last):
        third_last, second_last, last = (
            int(str_third_last),
            int(str_second_last),
            int(str_last),
        )
        if last < 5:
            pass
        elif last > 4:
            if second_last == 9:
                third_last = third_last + 1
                second_last = 0
            else:
                second_last = second_last + 1
        return [str(third_last), str(second_last)]

    file = open(topas_script, "r")
    lines = file.readlines()
    hls = []
    radii = []
    transz = []
    for i in lines:
        if i[5] == "s" and i[6] == "l":
            slice_no = i[10]
            try:
                int_slice_no = int(i[11])
                j = 1
                slice_no = i[10] + i[11]
            except:
                j = 0
            if i[12 + j] == "H":
                last_two = rounded(i[20 + j], i[21 + j], i[22 + j])
                str_HL = i[17 + j] + i[18 + j] + i[19 + j] + last_two[0] + last_two[1]
                hls.append(float(str_HL))
            elif i[12 + j] == "R" and i[14 + j] == "a":
                last_two = rounded(i[22 + j], i[23 + j], i[24 + j])
                str_rmax = i[19 + j] + i[20 + j] + i[21 + j] + last_two[0] + last_two[1]
                radii.append(float(str_rmax))
            elif i[12 + j] == "T" and i[13 + j] == "r":
                last_two = rounded(i[27 + j], i[28 + j], i[29 + j])
                str_transz = (
                    i[20 + j]
                    + i[21 + j]
                    + i[22 + j]
                    + i[23 + j]
                    + i[24 + j]
                    + i[25 + j]
                    + i[26 + j]
                    + last_two[0]
                    + last_two[1]
                )
                transz.append(float(str_transz))

    print("Longitudinal Thickness:")
    print(np.array(hls) * 2)
    print("Radii:")
    print(radii)
    print("TransZ:")
    print(transz)
    return hls, radii, transz


get_cad_arrays_from_topas(
    "/home/robertsoncl/topas/material_classifications/Al_foils/s1_30_s2_381.txt"
)
