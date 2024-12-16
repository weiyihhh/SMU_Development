"""
这是编写的实时绘图代码
"""
def plot_key_match(**params):


def send_measurement(measurement):
    """
    将测量数据传递给绘图模块并更新图表
    :param measurement: 创建的测量数据字典
    """
    plot_key_match()
    # 获取步骤和电流数据(获取的是所有的数据，不管有没有)
    step = measurement['Step']
    voltage_value_VAR1 = measurement.get['V_VAR1']
    current_value_VAR1 = measurement.get['I_VAR1']

    voltage_value_VAR2 = measurement.get['V_VAR2', None]
    current_value_VAR2 = measurement.get('I_VAR2', None)

    current_value_CONST1 = measurement.get('I_CONST1', None)
    current_value_CONST2 = measurement.get('I_CONST2', None)
    current_value_CONST3 = measurement.get('I_CONST3', None)

    voltage_CONST1 = measurement.get('V_CONST1', None)
    voltage_CONST2 = measurement.get('V_CONST2', None)
    voltage_CONST3 = measurement.get('V_CONST3', None)

    if voltage_value_VAR2 is not None:
    # 将新的数据添加到存储的列表中
    x_data.append(X_label)
    y1_data.append(Y1_label)
    y2_data.append(Y2_label)
    y3_data.append(Y3_label)
    y4_data.append(Y4_label)
    y5_data.append(Y5_label)
    y6_data.append(Y6_label)
    y7_data.append(Y7_label)
    y8_data.append(Y8_label)

    if current_value_VAR2 is not None:
        y_data_VAR2.append(current_value_VAR2)

    if current_value_CONST1 is not None:
        y_data_CONST1.append(current_value_CONST1)

    if current_value_CONST2 is not None:
        y_data_CONST2.append(current_value_CONST2)

    # 更新图表
    update_plot()

    # 输出当前数据
    print(f"Step {step} - Current(VAR1): {current_value_VAR1:.6f} A, "
          f"Current(VAR2): {current_value_VAR2:.6f} A, "
          f"Current(CONST1): {current_value_CONST1:.6f} A, "
          f"Current(CONST2): {current_value_CONST2:.6f} A")
