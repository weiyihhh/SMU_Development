
def extract_v_i(measurement_data):
    """
    从 SMU 测量数据中提取指定的

    :param measurement_data: list, 包含多个测量数据字典
    :return: Vg_values, Id_values, Is_values（如果 I_VAR2 存在）
    """
    V_VAR1_values = []
    I_VAR1_values = []
    V_VAR2_values = []
    I_VAR2_values = []
    V_CONST1_values = []
    I_CONST1_values = []
    V_CONST2_values = []
    I_CONST2_values = []
    V_CONST3_values = []
    I_CONST3_values = []
    for entry in measurement_data:
        # 提取电压和电流
        if "V_VAR1" in entry and "I_VAR1" in entry:
            V_VAR1_values.append(entry["V_VAR1"])
            I_VAR1_values.append(entry["I_VAR1"])

        if "V_VAR2" in entry and "I_VAR2" in entry:
            V_VAR2_values.append(entry["V_VAR2"])
            I_VAR2_values.append(entry["I_VAR2"])

        if "V_CONST1" in entry and "I_CONST1" in entry:
            V_CONST1_values.append(entry["V_CONST1"])
            I_CONST1_values.append(entry["I_CONST1"])

        if "V_CONST2" in entry and "I_CONST2" in entry:
            V_CONST2_values.append(entry["V_CONST2"])
            I_CONST2_values.append(entry["I_CONST2"])

        if "V_CONST3" in entry and "I_CONST3" in entry:
            V_CONST3_values.append(entry["V_CONST3"])
            I_CONST3_values.append(entry["I_CONST3"])

    return V_VAR1_values, I_VAR1_values, V_VAR2_values, I_VAR2_values, V_CONST1_values, I_CONST1_values, V_CONST2_values, I_CONST2_values, V_CONST3_values, I_CONST3_values

def data_slice(data_name, data_values, line_num_points, line_nums):
    data_slices = {}  # 用字典存储切片数据
    data_slices[f"{data_name}_slide"] = []  # 初始化存储列表
    for i in range(line_nums):
        # 计算当前切片的起始和结束索引
        start_idx = i * line_num_points
        end_idx = start_idx + line_num_points

        # 获取切片
        data_slice = data_values[start_idx:end_idx]

        # 将切片数据存入字典
        data_slices[f"{data_name}_slide"].append(data_slice)

    return data_slices  # 返回存储所有切片的字典
