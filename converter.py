def get_loc_full_length(transz, hl):
    fl = hl * 2
    loc = (-transz) - hl
    print("loc= " + str(round(loc, 4)))
    print("fl= " + str(round(fl, 4)))


get_loc_full_length(-760.6486374543344, 0.3703125456655545)
