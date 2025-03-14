def update_measurement(measurement, *args):
    """
    更新measurement字典中的电压和电流值，支持多种类型的电压/电流对。

    :param measurement: 要更新的字典
    :param args: 每个参数包含一个元组，元组格式为 ('方向', Direction)，以及 ('V_<类型>', voltage_value, 'I_<类型>', current_value)
    :return: 更新后的measurement字典
    """
    for args_tuple in args:
        if len(args_tuple) == 2:  # 方向元组，只有方向和值
            Direction_key, Direction_value = args_tuple
            measurement[Direction_key] = Direction_value
        elif len(args_tuple) == 4:  # 电压和电流元组
            voltage_key, voltage_value, current_key, current_value = args_tuple
            measurement[voltage_key] = voltage_value
            measurement[current_key] = current_value

    return measurement
