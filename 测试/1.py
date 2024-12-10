csv_writer.writerow(['Direction', 'Step', 'V_VAR1', 'V_CONST1', 'I_VAR1', 'I_CONST1'])
with nidcpower.Session(resource_name=VAR1) as session_VAR1:
    session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT
    session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE
    session_VAR1.current_limit = current_limit_VAR1
    session_VAR1.current_limit_autorange = True
    # 设置VAR1.PLC
    session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
    session_VAR1.aperture_time = VAR1_PLC
    session_VAR1.initiate()
    # 计算VAR1步进电压
    voltage_step_VAR1 = round((voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)
    # 打印表头
    print('{:<10} {:<15} {:<15} {:<15} {:<15} {:<15}'.format('Direction', 'Step', 'V_VAR1', 'V_CONST1', 'I_VAR1',
                                                             'I_CONST1'))
    # 创建CONST1控制的会话并设置参数
    with nidcpower.Session(resource_name=CONST1) as session_CONST1:
        session_CONST1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
        session_CONST1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
        session_CONST1.voltage_level = voltage_CONST1  # 设CONST端的电压
        session_CONST1.current_limit = current_limit_CONST1
        session_CONST1.current_limit_autorange = True

        # 设置CONST1.PLC
        session_CONST1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
        session_CONST1.aperture_time = CONST1_PLC
    # 扫描VAR1：逐步设置VAR1电压并测量VAR1的电流
    for i in range(num_points_VAR1):
        voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
        session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
        time.sleep(0.001)  # 暂停0.001秒，等待稳定

        # 执行测量VAR1电流
        current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)
        # 执行测量CONST1电流
        current_value_CONST1 = session_CONST1.measure(nidcpower.MeasurementTypes.CURRENT)

        # 写入CSV文件
        csv_writer.writerow(
            ['Forward', i + 1, voltage_value_VAR1, voltage_CONST1, current_value_VAR1, current_value_CONST1])

        # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
        print('{:<10} {:<15} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format('Forward', i + 1,
                                                                                 voltage_value_VAR1, voltage_CONST1,
                                                                                 current_value_VAR1,
                                                                                 current_value_CONST1))