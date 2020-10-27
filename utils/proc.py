def de_noise(input_list=[]):
    input_list_len = len(input_list)
    if input_list_len == 0:
        return None
    elif input_list_len == 1:
        return input_list[0]
    
    max_unit = max(input_list)
    min_unit = min(input_list)
    if max_unit == min_unit:
        return max_unit

    rough_avg_unit = (max_unit - min_unit)/2
    if (max_unit-min_unit)/rough_avg_unit <0.1:
        return rough_avg_unit

    list_sum=0
    for unit in input_list:
        list_sum = list_sum + unit
    avg_unit = list_sum / input_list_len
    min_unit_distance = input_list[0]
    ret = input_list[0]
    for unit in input_list:
        if min_unit_distance > abs(unit - avg_unit):
            min_unit_distance = abs(unit - avg_unit)
            ret = unit
    return ret
