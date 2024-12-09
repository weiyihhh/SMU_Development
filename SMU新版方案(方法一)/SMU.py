import nidcpower
import time
import csv

def SMU_MODE_SELECT(smu1_mode, smu2_mode, smu3_mode, smu4_mode):
    # 创建一个列表来存储所有的模式
    smu_modes = [smu1_mode, smu2_mode, smu3_mode, smu4_mode]

    # 计数选择了多少个'CONST'模式和'VAR2'模式
    CONST1_count = sum(1 for mode in smu_modes if mode == 'CONST1')
    CONST2_count = sum(1 for mode in smu_modes if mode == 'CONST2')
    CONST3_count = sum(1 for mode in smu_modes if mode == 'CONST3')
    VAR2_count = sum(1 for mode in smu_modes if mode == 'VAR2')

    # 使用字典来模拟switch语句
    switch_dict = {
        (0, 0, 0, 0): 1,  # VAR2_count == 0 and CONST_count == 0
        (0, 1, 0, 0): 2,  # VAR2_count == 0 and CONST_count == 1
        (0, 1, 1, 0): 3,  # VAR2_count == 0 and CONST_count == 2
        (0, 1, 1, 1): 4,  # VAR2_count == 0 and CONST_count == 3
        (1, 0, 0, 0): 5,  # VAR2_count == 1 and CONST_count == 0
        (1, 1, 0, 0): 6,  # VAR2_count == 1 and CONST_count == 1
        (1, 1, 1, 0): 7,  # VAR2_count == 1 and CONST_count == 2
    }

    # 尝试从字典中获取与当前VAR2_count和CONST_count对应的值
    return switch_dict.get((VAR2_count, CONST1_count, CONST2_count, CONST3_count,), 0)  # 如果没有找到匹配的情况，则返回0（或其他默认值）


"""
    smu模式说明：
        OPERATION_1: 只使用VAR1
        OPERATION_2: VAR1+CONST*1
        OPERATION_3: VAR1+CONST*2
        OPERATION_4: VAR1+CONST*3
        OPERATION_5: VAR1+VAR2
        OPERATION_6: VAR1+VAR2+CONST*1
        OPERATION_7: VAR1+VAR2+CONST*2
"""
#single:
def SMU_OPERATION_1_S(file_name, file_path, VAR1, current_limit_VAR1, VAR1_PLC, voltage_max_VAR1,
                voltage_min_VAR1, num_points_VAR1):
    # 添加CSV扩展名
    output_file = file_name
    output_file += '.csv'
    output_path = file_path  # .csv文件存储路径
    with open(output_path + output_file, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Step', 'V_VAR1', 'I_VAR1'])
            # 创建VAR1控制的会话并设置参数
            with nidcpower.Session(resource_name=VAR1) as session_VAR1:
                session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                session_VAR1.current_limit = current_limit_VAR1  # 设置VAR1端的电流限制
                session_VAR1.current_limit_autorange = True
                # 设置VAR1.PLC
                session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                session_VAR1.aperture_time = VAR1_PLC
                # 计算步进电压
                voltage_step_VAR1 = round((voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)
                # 启动所有会话
                session_VAR1.initiate()
                # 打印表头
                print('{:<10} {:<15} {:<15}'.format('Step', 'V_VAR1', 'I_VAR1'))
                # 逐步设置VAR1电压并测量VAR1的电流
                for i in range(num_points_VAR1):
                    voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                    session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                    time.sleep(0.001)  # 暂停0.001秒，等待稳定

                    # 执行测量VAR1电流
                    current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)

                    # 写入CSV文件
                    csv_writer.writerow([i + 1, voltage_value_VAR1, current_value_VAR1])

                    # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                    print('{:<10} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format(
                        i + 1, voltage_value_VAR1, current_value_VAR1,))

def SMU_OPERATION_2_S(file_name, file_path, VAR1, CONST1, current_limit_VAR1, current_limit_CONST1, VAR1_PLC, CONST_PLC,
                    voltage_max_VAR1, voltage_min_VAR1, num_points_VAR1, voltage_CONST1,):
    # 添加CSV扩展名
    output_file = file_name
    output_file += '.csv'
    output_path = file_path  # .csv文件存储路径
    with open(output_path + output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Step', 'V_VAR1', 'V_CONST', 'I_VAR1', 'I_CONST'])

        # 创建VAR1控制的会话并设置参数
        with nidcpower.Session(resource_name=VAR1) as session_VAR1:
            session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
            session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
            session_VAR1.current_limit = current_limit_VAR1  # 设置VAR1端的电流限制
            session_VAR1.current_limit_autorange = True
            # 设置VAR1.PLC
            session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
            session_VAR1.aperture_time = VAR1_PLC

            # 创建CONST控制的会话并设置参数
            with nidcpower.Session(resource_name=CONST1) as session_CONST:
                session_CONST.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                session_CONST.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                session_CONST.voltage_level = voltage_CONST1  # 设CONST端的电压
                session_CONST.current_limit = current_limit_CONST1
                session_CONST.current_limit_autorange = True

                # 设置CONST.PLC
                session_CONST.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                session_CONST.aperture_time = CONST_PLC

                # 计算步进电压
                voltage_step_VAR1 = round((voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)

                # 启动所有会话
                session_VAR1.initiate()
                session_CONST.initiate()

                # 打印表头
                print('{:<10} {:<15} {:<15} {:<15} {:<15}'.format('Step', 'V_VAR1', 'V_CONST', 'I_VAR1', 'I_CONST'))

                # 逐步设置VAR1电压并测量VAR1、CONST的电流
                for i in range(num_points_VAR1):
                    voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                    session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                    time.sleep(0.001)  # 暂停0.001秒，等待稳定

                    # 执行测量VAR1电流
                    current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)

                    # 执行测量CONST电流
                    current_value_CONST = session_CONST.measure(nidcpower.MeasurementTypes.CURRENT)

                    # 写入CSV文件
                    csv_writer.writerow([i + 1, voltage_value_VAR1, voltage_CONST1,
                                         current_value_VAR1, current_value_CONST])

                    # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                    print('{:<10} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format(
                        i + 1,
                        voltage_value_VAR1,
                        voltage_CONST1,
                        current_value_VAR1,
                        current_value_CONST))

def SMU_OPERATION_3_S(VAR1, CONST1, CONST2, num_points_VAR1, voltage_min_VAR1, voltage_max_VAR1,
                    voltage_CONST2, voltage_CONST1, current_limit_VAR1 ,current_limit_CONST1,
                    current_limit_CONST2, VAR1_PLC, CONST2_PLC, CONST1_PLC, file_name, file_path):
    # 添加CSV扩展名
    output_file = file_name
    output_file += '.csv'
    output_path = file_path  # .csv文件存储路径
    with open(output_path + output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Step', 'V_VAR1', 'V_CONST1', 'V_CONST2', 'I_VAR1', 'I_CONST1', 'I_CONST2'])

        # 创建VAR1控制的会话并设置参数
        with nidcpower.Session(resource_name=VAR1) as session_VAR1:
            session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
            session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
            session_VAR1.current_limit = current_limit_VAR1  # 设置VAR1端的电流限制
            session_VAR1.current_limit_autorange = True
            # 设置VAR1.PLC
            session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
            session_VAR1.aperture_time = VAR1_PLC

            # 创建两个CONST控制的会话并设置参数
            with nidcpower.Session(resource_name=CONST1) as session_CONST1:
                session_CONST1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                session_CONST1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                session_CONST1.voltage_level = voltage_CONST1  # 设CONST端的电压
                session_CONST1.current_limit = current_limit_CONST1
                session_CONST1.current_limit_autorange = True

                # 设置CONST1.PLC
                session_CONST1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                session_CONST1.aperture_time = CONST1_PLC

            with nidcpower.Session(resource_name=CONST2) as session_CONST2:
                session_CONST2.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                session_CONST2.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                session_CONST2.voltage_level = voltage_CONST2  # 设CONST端的电压
                session_CONST2.current_limit = current_limit_CONST2
                session_CONST2.current_limit_autorange = True

                # 设置CONST2.PLC
                session_CONST2.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                session_CONST2.aperture_time = CONST2_PLC

            # 计算步进电压
            voltage_step_VAR1 = round((voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)

            # 启动所有会话
            session_VAR1.initiate()
            session_CONST1.initiate()
            session_CONST2.initiate()
            # 打印表头
            print('{:<10} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}'.format('Step', 'V_VAR1', 'V_CONST1', 'V_CONST2', 'I_VAR1', 'I_CONST1', 'I_CONST2'))

            # 逐步设置VAR1电压并测量VAR1、CONST的电流
            for i in range(num_points_VAR1):
                voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                time.sleep(0.001)  # 暂停0.001秒，等待稳定

                # 执行测量VAR1电流
                current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)

                # 执行测量CONST1电流
                current_value_CONST1 = session_CONST1.measure(nidcpower.MeasurementTypes.CURRENT)
                # 执行测量CONST2电流
                current_value_CONST2 = session_CONST2.measure(nidcpower.MeasurementTypes.CURRENT)

                # 写入CSV文件
                csv_writer.writerow([i + 1, voltage_value_VAR1, voltage_CONST1, voltage_CONST2,
                                        current_value_VAR1, current_value_CONST1, current_value_CONST2])

                # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                print('{:<10} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format(
                        i + 1,
                        voltage_value_VAR1,
                        voltage_CONST1,
                        voltage_CONST2,
                        current_value_VAR1,
                        current_value_CONST1,
                        current_value_CONST2))

def SMU_OPERATION_4_S(VAR1, CONST1, CONST2, CONST3, num_points_VAR1, voltage_min_VAR1, voltage_max_VAR1,
                    voltage_CONST1, voltage_CONST2, voltage_CONST3, current_limit_VAR1 ,current_limit_CONST1,
                    current_limit_CONST2, current_limit_CONST3,VAR1_PLC, CONST1_PLC, CONST2_PLC,CONST3_PLC, file_name, file_path):
    # 添加CSV扩展名
    output_file = file_name
    output_file += '.csv'
    output_path = file_path  # .csv文件存储路径
    with open(output_path + output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Step', 'V_VAR1', 'V_CONST1', 'V_CONST2', 'I_VAR1', 'I_CONST1', 'I_CONST2'])

        # 创建VAR1控制的会话并设置参数
        with nidcpower.Session(resource_name=VAR1) as session_VAR1:
            session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
            session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
            session_VAR1.current_limit = current_limit_VAR1  # 设置VAR1端的电流限制
            session_VAR1.current_limit_autorange = True
            # 设置VAR1.PLC
            session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
            session_VAR1.aperture_time = VAR1_PLC

            # 创建三个CONST控制的会话并设置参数
            with nidcpower.Session(resource_name=CONST1) as session_CONST1:
                session_CONST1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                session_CONST1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                session_CONST1.voltage_level = voltage_CONST1  # 设CONST端的电压
                session_CONST1.current_limit = current_limit_CONST1
                session_CONST1.current_limit_autorange = True

                # 设置CONST.PLC
                session_CONST1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                session_CONST1.aperture_time = CONST1_PLC

            with nidcpower.Session(resource_name=CONST2) as session_CONST2:
                session_CONST2.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                session_CONST2.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                session_CONST2.voltage_level = voltage_CONST2  # 设CONST端的电压
                session_CONST2.current_limit = current_limit_CONST2
                session_CONST2.current_limit_autorange = True

                # 设置CONST.PLC
                session_CONST2.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                session_CONST2.aperture_time = CONST2_PLC

            with nidcpower.Session(resource_name=CONST3) as session_CONST3:
                session_CONST3.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                session_CONST3.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                session_CONST3.voltage_level = voltage_CONST3  # 设CONST端的电压
                session_CONST3.current_limit = current_limit_CONST3
                session_CONST3.current_limit_autorange = True

                # 设置CONST.PLC
                session_CONST3.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                session_CONST3.aperture_time = CONST3_PLC
            # 计算步进电压
            voltage_step_VAR1 = round((voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)

            # 启动所有会话
            session_VAR1.initiate()
            session_CONST1.initiate()
            session_CONST2.initiate()
            session_CONST3.initiate()
            # 打印表头
            print('{:<10} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}'.format('Step', 'V_VAR1', 'V_CONST1', 'V_CONST2', 'V_CONST3',
                                                                                               'I_VAR1', 'I_CONST1', 'I_CONST2', 'I_CONST3'))

            # 逐步设置VAR1电压并测量VAR1、CONST的电流
            for i in range(num_points_VAR1):
                voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                time.sleep(0.001)  # 暂停0.001秒，等待稳定

                # 执行测量VAR1电流
                current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)

                # 执行测量CONST1电流
                current_value_CONST1 = session_CONST1.measure(nidcpower.MeasurementTypes.CURRENT)
                # 执行测量CONST2电流
                current_value_CONST2 = session_CONST2.measure(nidcpower.MeasurementTypes.CURRENT)
                # 执行测量CONST3电流
                current_value_CONST3 = session_CONST3.measure(nidcpower.MeasurementTypes.CURRENT)

                # 写入CSV文件
                csv_writer.writerow([i + 1, voltage_value_VAR1, voltage_CONST1, voltage_CONST2, voltage_CONST3,
                                     current_value_VAR1, current_value_CONST1, current_value_CONST2, current_value_CONST3])

                # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                print('{:<10} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format(
                    i + 1,
                    voltage_value_VAR1,
                    voltage_CONST1,
                    voltage_CONST2,
                    voltage_CONST3,
                    current_value_VAR1,
                    current_value_CONST1,
                    current_value_CONST2,
                    current_value_CONST3))

def SMU_OPERATION_5_S(VAR1, VAR2, current_limit_VAR1, current_limit_VAR2, VAR1_PLC, VAR2_PLC, voltage_max_VAR1, voltage_max_VAR2, voltage_min_VAR1, voltage_min_VAR2,
                    file_name, file_path, num_points_VAR1, num_points_VAR2):
    # 添加CSV扩展名
    output_file = file_name
    output_file += '.csv'
    output_path = file_path  # .csv文件存储路径
    # 创建VAR2测量的会话并设置参数
    with nidcpower.Session(resource_name=VAR2) as session_VAR2:
        session_VAR2.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
        session_VAR2.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
        session_VAR2.current_limit = current_limit_VAR2  # 设置VAR2端的电流限制
        session_VAR2.current_limit_autorange = True

        # 设置VAR2.PLC
        session_VAR2.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
        session_VAR2.aperture_time = VAR2_PLC

        # 增添if语句，当VAR2设置max=min时，执行一次single测量
        if voltage_max_VAR2 == voltage_min_VAR2:
            session_VAR2.initiate()

            with open(output_path + output_file, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['Step', 'V_VAR1', 'V_VAR2', 'I_VAR1', 'I_VAR2'])

                for j in range(num_points_VAR2):
                    voltage_value_VAR2 = voltage_min_VAR2
                    session_VAR2.voltage_level = voltage_value_VAR2  # 设置VAR2端的电压输出

                    # 创建VAR1控制的会话并设置参数
                    with nidcpower.Session(resource_name=VAR1) as session_VAR1:
                        session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                        session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                        session_VAR1.current_limit = current_limit_VAR1  # 设置VAR1端的电流限制
                        session_VAR1.current_limit_autorange = True
                        # 设置VAR1.PLC
                        session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                        session_VAR1.aperture_time = VAR1_PLC

                        # 计算步进电压
                        voltage_step_VAR1 = round((voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)

                        # 启动所有会话
                        session_VAR1.initiate()

                        # 打印表头
                        print('{:<10} {:<15} {:<15} {:<15} {:<15}'.format('Step', 'V_VAR1', 'V_VAR2',
                                                                                            'I_VAR1',
                                                                                            'I_VAR2'))

                        # 逐步设置VAR1电压并测量VAR1、VAR2、CONST的电流
                        for i in range(num_points_VAR1):
                            voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                            session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                            time.sleep(0.001)  # 暂停0.001秒，等待稳定

                            # 执行测量VAR1电流
                            current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)

                            # 执行测量VAR2电流
                            current_value_VAR2 = session_VAR2.measure(nidcpower.MeasurementTypes.CURRENT)

                            # 写入CSV文件
                            csv_writer.writerow([i + 1, voltage_value_VAR1, voltage_value_VAR2,
                                                     current_value_VAR1, current_value_VAR2])

                            # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                            print('{:<10} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format(
                                    i + 1,
                                    voltage_value_VAR1,
                                    voltage_value_VAR2,
                                    current_value_VAR1,
                                    current_value_VAR2,
                                   ))
        else:
            # 计算VAR2步进电压
            voltage_step_VAR2 = round((voltage_max_VAR2 - voltage_min_VAR2) / (num_points_VAR2 - 1), 8)
            session_VAR2.initiate()

            with open(output_path + output_file, 'w', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(['Step', 'V_VAR1', 'V_VAR2', 'I_VAR1', 'I_VAR2'])

                    for j in range(num_points_VAR2):

                        voltage_value_VAR2 = voltage_min_VAR2 + j * voltage_step_VAR2  # 计算当前步进的VAR2电压值
                        session_VAR2.voltage_level = voltage_value_VAR2  # 设置VAR2端的电压输出

                        # 创建VAR1控制的会话并设置参数
                        with nidcpower.Session(resource_name=VAR1) as session_VAR1:
                            session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                            session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                            session_VAR1.current_limit = current_limit_VAR1  # 设置VAR1端的电流限制
                            session_VAR1.current_limit_autorange = True

                            # 设置VAR1.PLC
                            session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                            session_VAR1.aperture_time = VAR1_PLC



                            # 计算VAR1步进电压
                            voltage_step_VAR1 = round((voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)

                            # 启动所有会话
                            session_VAR1.initiate()

                            # 打印表头
                            print('{:<10} {:<15} {:<15} {:<15} {:<15}'.format('Step', 'V_VAR1', 'V_VAR2',
                                                                              'I_VAR1',
                                                                              'I_VAR2'))

                            #扫描VAR1：逐步设置VAR1电压并测量VAR1、VAR2、CONST的电流
                            for i in range(num_points_VAR1):
                                    voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                    session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                    time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                    # 执行测量VAR1电流
                                    current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)

                                    # 执行测量VAR2电流
                                    current_value_VAR2 = session_VAR2.measure(nidcpower.MeasurementTypes.CURRENT)

                                    # 写入CSV文件
                                    csv_writer.writerow([i + 1, voltage_value_VAR1, voltage_value_VAR2,
                                                         current_value_VAR1, current_value_VAR2])

                                    # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                    print('{:<10} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format(
                                        i + 1,
                                        voltage_value_VAR1,
                                        voltage_value_VAR2,
                                        current_value_VAR1,
                                        current_value_VAR2,
                                    ))

        print(f"Data saved to {output_path + output_file }")

def SMU_OPERATION_6_S(VAR1, VAR2, current_limit_VAR1, current_limit_VAR2, VAR1_PLC, VAR2_PLC, voltage_max_VAR1, voltage_max_VAR2, voltage_min_VAR1, voltage_min_VAR2,
                    file_name, file_path, num_points_VAR1, num_points_VAR2, CONST1, voltage_CONST1, current_limit_CONST1, CONST1_PLC):
    # 添加CSV扩展名
    output_file = file_name
    output_file += '.csv'
    output_path = file_path  # .csv文件存储路径
    # 创建VAR2测量的会话并设置参数
    with nidcpower.Session(resource_name=VAR2) as session_VAR2:
        session_VAR2.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
        session_VAR2.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
        session_VAR2.current_limit = current_limit_VAR2  # 设置VAR2端的电流限制
        session_VAR2.current_limit_autorange = True

        # 设置VAR2.PLC
        session_VAR2.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
        session_VAR2.aperture_time = VAR2_PLC

        # 增添if语句，当VAR2设置max=min时，执行一次single测量
        if voltage_max_VAR2 == voltage_min_VAR2:
            session_VAR2.initiate()

            with open(output_path + output_file, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['Step', 'V_VAR1', 'V_VAR2', 'V_CONST', 'I_VAR1', 'I_VAR2', 'I_CONST1'])

                for j in range(num_points_VAR2):
                    voltage_value_VAR2 = voltage_min_VAR2
                    session_VAR2.voltage_level = voltage_value_VAR2  # 设置VAR2端的电压输出

                    # 创建VAR1控制的会话并设置参数
                    with nidcpower.Session(resource_name=VAR1) as session_VAR1:
                        session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                        session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                        session_VAR1.current_limit = current_limit_VAR1  # 设置VAR1端的电流限制
                        session_VAR1.current_limit_autorange = True
                        # 设置VAR1.PLC
                        session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                        session_VAR1.aperture_time = VAR1_PLC

                        # 创建CONST控制的会话并设置参数
                        with nidcpower.Session(resource_name=CONST1) as session_CONST1:
                            session_CONST1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                            session_CONST1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                            session_CONST1.voltage_level = voltage_CONST1  # 设CONST端的电压
                            session_CONST1.current_limit = current_limit_CONST1
                            session_CONST1.current_limit_autorange = True

                            # 设置CONST.PLC
                            session_CONST1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                            session_CONST1.aperture_time = CONST1_PLC

                            # 计算步进电压
                            voltage_step_VAR1 = round((voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)

                            # 启动所有会话
                            session_VAR1.initiate()
                            session_CONST1.initiate()

                            # 打印表头
                            print('{:<10} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}'.format('Step', 'V_VAR1', 'V_VAR2',
                                                                                            'V_CONST1', 'I_VAR1',
                                                                                            'I_VAR2', 'I_CONST1'))

                            # 逐步设置VAR1电压并测量VAR1、VAR2、CONST的电流
                            for i in range(num_points_VAR1):
                                voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                # 执行测量VAR1电流
                                current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)

                                # 执行测量VAR2电流
                                current_value_VAR2 = session_VAR2.measure(nidcpower.MeasurementTypes.CURRENT)

                                # 执行测量CONST电流
                                current_value_CONST = session_CONST1.measure(nidcpower.MeasurementTypes.CURRENT)

                                # 写入CSV文件
                                csv_writer.writerow([i + 1, voltage_value_VAR1, voltage_value_VAR2, voltage_CONST1,
                                                     current_value_VAR1, current_value_VAR2, current_value_CONST])

                                # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                print('{:<10} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format(
                                    i + 1,
                                    voltage_value_VAR1,
                                    voltage_value_VAR2,
                                    voltage_CONST1,
                                    current_value_VAR1,
                                    current_value_VAR2,
                                    current_value_CONST))

        else:
            # 计算VAR2步进电压
            voltage_step_VAR2 = round((voltage_max_VAR2 - voltage_min_VAR2) / (num_points_VAR2 - 1), 8)
            session_VAR2.initiate()

            with open(output_path + output_file, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['Direction', 'Step', 'V_VAR1', 'V_VAR2', 'V_CONST1', 'I_VAR1', 'I_VAR2', 'I_CONST1'])

                for j in range(num_points_VAR2):

                    voltage_value_VAR2 = voltage_min_VAR2 + j * voltage_step_VAR2  # 计算当前步进的VAR2电压值
                    session_VAR2.voltage_level = voltage_value_VAR2  # 设置VAR2端的电压输出

                    # 创建VAR1控制的会话并设置参数
                    with nidcpower.Session(resource_name=VAR1) as session_VAR1:
                        session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                        session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                        session_VAR1.current_limit = current_limit_VAR1  # 设置VAR1端的电流限制
                        session_VAR1.current_limit_autorange = True

                        # 设置VAR1.PLC
                        session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                        session_VAR1.aperture_time = VAR1_PLC

                        # 创建CONST控制的会话并设置参数
                        with nidcpower.Session(resource_name=CONST1) as session_CONST1:
                            session_CONST1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                            session_CONST1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                            session_CONST1.voltage_level = voltage_CONST1 # 设CONST端的电压
                            session_CONST1.current_limit = current_limit_CONST1
                            session_CONST1.current_limit_autorange = True
                            # 设置CONST.PLC
                            session_CONST1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                            session_CONST1.aperture_time = CONST1_PLC

                            # 计算VAR1步进电压
                            voltage_step_VAR1 = round((voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)

                            # 启动所有会话
                            session_VAR1.initiate()
                            session_CONST1.initiate()

                            # 打印表头
                            print('{:<10} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}'.format('Direction', 'Step',
                                                                                                   'V_VAR1', 'V_VAR2',
                                                                                                   'V_CONST1', 'I_VAR1',
                                                                                                   'I_VAR2', 'I_CONST1'))

                            # 扫描VAR1：逐步设置VAR1电压并测量VAR1、VAR2、CONST的电流
                            for i in range(num_points_VAR1):
                                voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                # 执行测量VAR1电流
                                current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)

                                # 执行测量VAR2电流
                                current_value_VAR2 = session_VAR2.measure(nidcpower.MeasurementTypes.CURRENT)

                                # 执行测量CONST电流
                                current_value_CONST = session_CONST1.measure(nidcpower.MeasurementTypes.CURRENT)

                                # 写入CSV文件
                                csv_writer.writerow(['Forward', i + 1, voltage_value_VAR1, voltage_value_VAR2,
                                                     voltage_CONST1, current_value_VAR1, current_value_VAR2,
                                                     current_value_CONST])

                                # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                print(
                                    '{:<10} {:<15} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format(
                                        'Forward', i + 1,
                                        voltage_value_VAR1,
                                        voltage_value_VAR2,
                                        voltage_CONST1,
                                        current_value_VAR1,
                                        current_value_VAR2,
                                        current_value_CONST))
        print(f"Data saved to {output_path + output_file}")

def SMU_OPERATION_7_S(VAR1, VAR2, CONST2, current_limit_VAR1, current_limit_VAR2, VAR1_PLC, VAR2_PLC, voltage_max_VAR1, voltage_max_VAR2, voltage_min_VAR1, voltage_min_VAR2,
                    file_name, file_path, num_points_VAR1, num_points_VAR2, CONST1, voltage_CONST1, current_limit_CONST1, current_limit_CONST2,  CONST1_PLC, voltage_CONST2, CONST2_PLC):
    # 添加CSV扩展名
    output_file = file_name
    output_file += '.csv'
    output_path = file_path  # .csv文件存储路径
    # 创建VAR2测量的会话并设置参数
    with nidcpower.Session(resource_name=VAR2) as session_VAR2:
        session_VAR2.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
        session_VAR2.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
        session_VAR2.current_limit = current_limit_VAR2  # 设置VAR2端的电流限制
        session_VAR2.current_limit_autorange = True

        # 设置VAR2.PLC
        session_VAR2.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
        session_VAR2.aperture_time = VAR2_PLC

        # 增添if语句，当VAR2设置max=min时，执行一次single测量
        if voltage_max_VAR2 == voltage_min_VAR2:
            session_VAR2.initiate()

            with open(output_path + output_file, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['Step', 'V_VAR1', 'V_VAR2', 'V_CONST1', 'V_CONST2', 'I_VAR1', 'I_VAR2', 'I_CONST1', 'I_CONST2'])

                for j in range(num_points_VAR2):
                    voltage_value_VAR2 = voltage_min_VAR2
                    session_VAR2.voltage_level = voltage_value_VAR2  # 设置VAR2端的电压输出

                    # 创建VAR1控制的会话并设置参数
                    with nidcpower.Session(resource_name=VAR1) as session_VAR1:
                        session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                        session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                        session_VAR1.current_limit = current_limit_VAR1  # 设置VAR1端的电流限制
                        session_VAR1.current_limit_autorange = True
                        # 设置VAR1.PLC
                        session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                        session_VAR1.aperture_time = VAR1_PLC

                        # 创建两个CONST控制的会话并设置参数
                        with nidcpower.Session(resource_name=CONST1) as session_CONST1:
                            session_CONST1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                            session_CONST1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                            session_CONST1.voltage_level = voltage_CONST1  # 设CONST端的电压
                            session_CONST1.current_limit = current_limit_CONST1
                            session_CONST1.current_limit_autorange = True

                            # 设置CONST1.PLC
                            session_CONST1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                            session_CONST1.aperture_time = CONST1_PLC

                        with nidcpower.Session(resource_name=CONST2) as session_CONST2:
                            session_CONST2.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                            session_CONST2.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                            session_CONST2.voltage_level = voltage_CONST2  # 设CONST端的电压
                            session_CONST2.current_limit = current_limit_CONST2
                            session_CONST2.current_limit_autorange = True

                            # 设置CONST2.PLC
                            session_CONST2.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                            session_CONST2.aperture_time = CONST2_PLC

                        # 计算步进电压
                        voltage_step_VAR1 = round((voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)

                        # 启动所有会话
                        session_VAR1.initiate()
                        session_CONST1.initiate()

                        # 打印表头
                        print('{:<10} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}'.format('Step', 'V_VAR1', 'V_VAR2', 'V_CONST1', 'V_CONST2', 'I_VAR1', 'I_VAR2', 'I_CONST1', 'I_CONST2'))

                        # 逐步设置VAR1电压并测量VAR1、VAR2、CONST的电流
                        for i in range(num_points_VAR1):
                                voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                # 执行测量VAR1电流
                                current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)

                                # 执行测量VAR2电流
                                current_value_VAR2 = session_VAR2.measure(nidcpower.MeasurementTypes.CURRENT)

                                # 执行测量CONST电流
                                current_value_CONST1 = session_CONST1.measure(nidcpower.MeasurementTypes.CURRENT)
                                current_value_CONST2 = session_CONST2.measure(nidcpower.MeasurementTypes.CURRENT)
                                # 写入CSV文件
                                csv_writer.writerow([i + 1, voltage_value_VAR1, voltage_value_VAR2, voltage_CONST1,
                                                     current_value_VAR1, current_value_VAR2, current_value_CONST1,
                                                     current_value_CONST2])

                                # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                print('{:<10} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format(
                                    i + 1,
                                    voltage_value_VAR1,
                                    voltage_value_VAR2,
                                    voltage_CONST1,
                                    voltage_CONST2,
                                    current_value_VAR1,
                                    current_value_VAR2,
                                    current_value_CONST1,
                                    current_value_CONST2))

        else:
            # 计算VAR2步进电压
            voltage_step_VAR2 = round((voltage_max_VAR2 - voltage_min_VAR2) / (num_points_VAR2 - 1), 8)
            session_VAR2.initiate()

            with open(output_path + output_file, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(
                    ['Step', 'V_VAR1', 'V_VAR2', 'V_CONST1', 'V_CONST2', 'I_VAR1', 'I_VAR2', 'I_CONST1', 'I_CONST2'])

                for j in range(num_points_VAR2):

                    voltage_value_VAR2 = voltage_min_VAR2 + j * voltage_step_VAR2  # 计算当前步进的VAR2电压值
                    session_VAR2.voltage_level = voltage_value_VAR2  # 设置VAR2端的电压输出

                    # 创建VAR1控制的会话并设置参数
                    with nidcpower.Session(resource_name=VAR1) as session_VAR1:
                        session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                        session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                        session_VAR1.current_limit = current_limit_VAR1  # 设置VAR1端的电流限制
                        session_VAR1.current_limit_autorange = True

                        # 设置VAR1.PLC
                        session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                        session_VAR1.aperture_time = VAR1_PLC

                        # 创建两个CONST控制的会话并设置参数
                        with nidcpower.Session(resource_name=CONST1) as session_CONST1:
                            session_CONST1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                            session_CONST1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                            session_CONST1.voltage_level = voltage_CONST1  # 设CONST端的电压
                            session_CONST1.current_limit = current_limit_CONST1
                            session_CONST1.current_limit_autorange = True

                            # 设置CONST1.PLC
                            session_CONST1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                            session_CONST1.aperture_time = CONST1_PLC

                        with nidcpower.Session(resource_name=CONST2) as session_CONST2:
                            session_CONST2.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                            session_CONST2.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                            session_CONST2.voltage_level = voltage_CONST2  # 设CONST端的电压
                            session_CONST2.current_limit = current_limit_CONST2
                            session_CONST2.current_limit_autorange = True

                            # 设置CONST2.PLC
                            session_CONST2.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                            session_CONST2.aperture_time = CONST2_PLC

                        # 计算步进电压
                        voltage_step_VAR1 = round((voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)

                        # 启动所有会话
                        session_VAR1.initiate()
                        session_CONST1.initiate()

                        # 打印表头
                        print('{:<10} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}'.format('Step', 'V_VAR1', 'V_VAR2',
                                                                                            'V_CONST1', 'V_CONST2',
                                                                                            'I_VAR1', 'I_VAR2',
                                                                                            'I_CONST1', 'I_CONST2'))

                        # 逐步设置VAR1电压并测量VAR1、VAR2、CONST的电流
                        for i in range(num_points_VAR1):
                                voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                # 执行测量VAR1电流
                                current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)

                                # 执行测量VAR2电流
                                current_value_VAR2 = session_VAR2.measure(nidcpower.MeasurementTypes.CURRENT)

                                # 执行测量CONST电流
                                current_value_CONST1 = session_CONST1.measure(nidcpower.MeasurementTypes.CURRENT)
                                current_value_CONST2 = session_CONST2.measure(nidcpower.MeasurementTypes.CURRENT)
                                # 写入CSV文件
                                csv_writer.writerow([i + 1, voltage_value_VAR1, voltage_value_VAR2, voltage_CONST1,
                                                     current_value_VAR1, current_value_VAR2, current_value_CONST1,
                                                     current_value_CONST2])

                                # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                print(
                                    '{:<10} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format(
                                        i + 1,
                                        voltage_value_VAR1,
                                        voltage_value_VAR2,
                                        voltage_CONST1,
                                        voltage_CONST2,
                                        current_value_VAR1,
                                        current_value_VAR2,
                                        current_value_CONST1,
                                        current_value_CONST2))

#double:
def SMU_OPERATION_1_d(file_name, file_path, VAR1, current_limit_VAR1, VAR1_PLC, voltage_max_VAR1,
                voltage_min_VAR1, num_points_VAR1):
    # 添加CSV扩展名
    output_file = file_name
    output_file += '.csv'
    output_path = file_path  # .csv文件存储路径
    with open(output_path + output_file, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Step', 'V_VAR1', 'I_VAR1'])
            # 创建VAR1控制的会话并设置参数
            with nidcpower.Session(resource_name=VAR1) as session_VAR1:
                session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                session_VAR1.current_limit = current_limit_VAR1  # 设置VAR1端的电流限制
                session_VAR1.current_limit_autorange = True
                # 设置VAR1.PLC
                session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                session_VAR1.aperture_time = VAR1_PLC
                # 计算步进电压
                voltage_step_VAR1 = round((voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)
                # 启动所有会话
                session_VAR1.initiate()
                # 打印表头
                print('{:<10} {:<15} {:<15}'.format('Step', 'V_VAR1', 'I_VAR1'))
                # 逐步设置VAR1电压并测量VAR1的电流
                for i in range(num_points_VAR1):
                    voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                    session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                    time.sleep(0.001)  # 暂停0.001秒，等待稳定

                    # 执行测量VAR1电流
                    current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)

                    # 写入CSV文件
                    csv_writer.writerow([i + 1, voltage_value_VAR1, current_value_VAR1])

                    # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                    print('{:<10} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format(
                        i + 1, voltage_value_VAR1, current_value_VAR1,))