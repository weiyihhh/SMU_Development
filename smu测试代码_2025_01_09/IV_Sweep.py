"""

 需要设定Unit、V Name、I Name、Mode（I、V、common）、Function（VAR1、VAR2、CONST）
 4140有四个smu模块
 新增Double模式

"""

import nidcpower
import time
import csv
import sys


def smu_common_mode(smu_common_list):
    for smu_resource in smu_common_list:
        try:
            with nidcpower.Session(resource_name=smu_resource) as session:
                session.source_mode = nidcpower.SourceMode.SINGLE_POINT
                session.output_function = nidcpower.OutputFunction.DC_VOLTAGE
                session.current_limit_autorange = True
                session.voltage_level = 0
                print(f"Successfully configured SMU-COMMON: {smu_resource}\n\n\n")
        except Exception as e:
            print(f"Failed to configure SMU-COMMON: {smu_resource}. Error: {e}\n\n\n")

def smu_selection_test(**params):
    VAR1 = params.get('VAR1')
    if VAR1 is None :
        print("Error:Output function (VAR1) must be assigned to any unit.....")
        sys.exit()
    else:
        return True

def IV_Sweep_Single(VAR1, VAR2, CONST1, CONST2, CONST3, num_points_VAR1, voltage_min_VAR1, voltage_max_VAR1, current_limit_range_VAR1,current_limit_range_CONST1,
                    current_limit_range_CONST2, current_limit_range_CONST3, num_points_VAR2, voltage_min_VAR2, voltage_max_VAR2, voltage_CONST1, voltage_CONST2,
                    voltage_CONST3, current_limit_VAR1,current_limit_VAR2, current_limit_range_VAR2, current_limit_CONST1, current_limit_CONST2, current_limit_CONST3,
                    VAR1_PLC, VAR2_PLC, CONST1_PLC, CONST2_PLC, CONST3_PLC, file_name,file_path):
    # 添加CSV扩展名
    output_file = file_name
    output_file += '.csv'
    output_path = file_path  # .csv文件存储路径
    if VAR2 is not None:
        # 创建VAR2测量的会话并设置参数
        with nidcpower.Session(resource_name=VAR2) as session_VAR2:
            session_VAR2.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
            session_VAR2.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
            session_VAR2.current_limit = current_limit_VAR2  # 设置VAR2端的电流限制
            session_VAR2.current_limit_range = current_limit_range_VAR2

            # 设置VAR2.PLC
            session_VAR2.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
            session_VAR2.aperture_time = VAR2_PLC
            # 增添if语句，当VAR2设置max=min时，执行一次single测量
            if voltage_max_VAR2 == voltage_min_VAR2:
                session_VAR2.initiate()
                with open(output_path + output_file, 'w', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    for j in range(num_points_VAR2):
                        voltage_value_VAR2 = voltage_min_VAR2
                        session_VAR2.voltage_level = voltage_value_VAR2  # 设置VAR2端的电压输出
                        if CONST1 is not None:
                            if CONST2 is not None:#这时候用了两个CONST
                                csv_writer.writerow(['Direction', 'Step', 'V_VAR1', 'V_VAR2', 'V_CONST1', 'V_CONST2', 'I_VAR1', 'I_VAR2', 'I_CONST1', 'I_CONST2'])
                                # 创建VAR1控制的会话并设置参数
                                with nidcpower.Session(resource_name=VAR1) as session_VAR1:
                                    session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                    session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出1
                                    session_VAR1.current_limit = current_limit_VAR1  # 设置VAR1端的电流限制
                                    session_VAR1.current_limit_range = current_limit_range_VAR1

                                    # 设置VAR1.PLC
                                    session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                    session_VAR1.aperture_time = VAR1_PLC

                                    # 创建2个CONST控制的会话并设置参数
                                    with nidcpower.Session(resource_name=CONST1) as session_CONST1:
                                        session_CONST1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                        session_CONST1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                        session_CONST1.voltage_level = voltage_CONST1  # 设CONST端的电压
                                        session_CONST1.current_limit = current_limit_CONST1
                                        session_CONST1.current_limit_range = current_limit_range_CONST1
                                        # 设置CONST1.PLC
                                        session_CONST1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                        session_CONST1.aperture_time = CONST1_PLC


                                        with nidcpower.Session(resource_name=CONST2) as session_CONST2:
                                            session_CONST2.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                            session_CONST2.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                            session_CONST2.voltage_level = voltage_CONST2  # 设CONST端的电压
                                            session_CONST2.current_limit = current_limit_CONST2
                                            session_CONST2.current_limit_range = current_limit_range_CONST2
                                            # 设置CONST2.PLC
                                            session_CONST2.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                            session_CONST2.aperture_time = CONST2_PLC

                                            # 启动所有会话
                                            session_VAR1.initiate()
                                            session_CONST1.initiate()
                                            session_CONST2.initiate()
                                            # 计算步进电压
                                            voltage_step_VAR1 = round((voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)

                                            # 打印表头
                                            print('{:<10} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}'.format('Direction', 'Step', 'V_VAR1', 'V_VAR2',
                                                                                                               'V_CONST1', 'V_CONST2', 'I_VAR1',
                                                                                                               'I_VAR2', 'I_CONST1', 'I_CONST2'))
                                            # 逐步设置VAR1电压并测量VAR1、VAR2、CONST的电流
                                            for i in range(num_points_VAR1):
                                                voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                                session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                                time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                                direction = "Forward"
                                                step = i+1
                                                # 执行测量VAR1电流
                                                current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)
                                                # 执行测量VAR2电流
                                                current_value_VAR2 = session_VAR2.measure(nidcpower.MeasurementTypes.CURRENT)
                                                # 执行测量CONST1电流
                                                current_value_CONST1 = session_CONST1.measure(nidcpower.MeasurementTypes.CURRENT)
                                                # 执行测量CONST2电流
                                                current_value_CONST2 = session_CONST2.measure(nidcpower.MeasurementTypes.CURRENT)

                                                #每一步的测量数据存入 measurement_data 字典
                                                measurement_data = create_measurement(
                                                    direction = direction,
                                                    step = step,
                                                    voltage_value_VAR1 = voltage_value_VAR1,
                                                    voltage_value_VAR2 = voltage_value_VAR2,
                                                    current_value_VAR1 = current_value_VAR1,
                                                    current_value_VAR2 = current_value_VAR2,
                                                    voltage_CONST1 = voltage_CONST1,
                                                    voltage_CONST2 = voltage_CONST2,
                                                    current_value_CONST1 = current_value_CONST1,
                                                    current_value_CONST2 = current_value_CONST2,
                                                    )
                                                send_measurement(measurement_data)
                                                # 写入CSV文件
                                                csv_writer.writerow([i + 1, voltage_value_VAR1, voltage_value_VAR2, voltage_CONST1, voltage_CONST2,
                                                                    current_value_VAR1, current_value_VAR2, current_value_CONST1, current_value_CONST2])

                                                # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                                print('{:<10} {:<15} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format(
                                                        'Forward', i + 1,
                                                        voltage_value_VAR1,
                                                        voltage_value_VAR2,
                                                        voltage_CONST1,
                                                        voltage_CONST2,
                                                        current_value_VAR1,
                                                        current_value_VAR2,
                                                        current_value_CONST1,
                                                        current_value_CONST2
                                                    ))
                            else:#这时候说明只启用CONST1
                                csv_writer.writerow(
                                    ['Step', 'V_VAR1', 'V_VAR2', 'V_CONST1', 'I_VAR1', 'I_VAR2', 'I_CONST1'
                                     ])
                                with nidcpower.Session(resource_name=VAR1) as session_VAR1:
                                    session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                    session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                    session_VAR1.current_limit = current_limit_VAR1  # 设置VAR1端的电流限制
                                    session_VAR1.current_limit_range = current_limit_range_VAR1
                                    # 设置VAR1.PLC
                                    session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                    session_VAR1.aperture_time = VAR1_PLC

                                    # 创建CONST1控制的会话并设置参数
                                    with nidcpower.Session(resource_name=CONST1) as session_CONST1:
                                        session_CONST1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                        session_CONST1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                        session_CONST1.voltage_level = voltage_CONST1  # 设CONST端的电压
                                        session_CONST1.current_limit = current_limit_CONST1
                                        session_CONST1.current_limit_range = current_limit_range_CONST1

                                        # 设置CONST1.PLC
                                        session_CONST1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                        session_CONST1.aperture_time = CONST1_PLC

                                        # 计算步进电压
                                        voltage_step_VAR1 = round(
                                            (voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)

                                        # 启动所有会话
                                        session_VAR1.initiate()
                                        session_CONST1.initiate()

                                        # 打印表头
                                        print(
                                            '{:<10} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}'.format('Step', 'V_VAR1',
                                                                                                      'V_VAR2',
                                                                                                      'V_CONST1',
                                                                                                      'I_VAR1',
                                                                                                      'I_VAR2',
                                                                                                      'I_CONST1'))

                                        # 逐步设置VAR1电压并测量VAR1、VAR2、CONST的电流
                                        for i in range(num_points_VAR1):
                                            direction = "Forward"
                                            step = i + 1
                                            voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                            session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                            time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                            # 执行测量VAR1电流
                                            current_value_VAR1 = session_VAR1.measure(
                                                nidcpower.MeasurementTypes.CURRENT)

                                            # 执行测量VAR2电流
                                            current_value_VAR2 = session_VAR2.measure(
                                                nidcpower.MeasurementTypes.CURRENT)

                                            # 执行测量CONST1电流
                                            current_value_CONST1 = session_CONST1.measure(
                                                nidcpower.MeasurementTypes.CURRENT)

                                            # 每一步的测量数据存入 measurement_data 字典
                                            measurement_data = create_measurement(
                                                direction=direction,
                                                step=step,
                                                voltage_value_VAR1=voltage_value_VAR1,
                                                voltage_value_VAR2=voltage_value_VAR2,
                                                current_value_VAR1=current_value_VAR1,
                                                current_value_VAR2=current_value_VAR2,
                                                voltage_CONST1=voltage_CONST1,
                                                current_value_CONST1=current_value_CONST1,
                                            )
                                            send_measurement(measurement_data)
                                            # 写入CSV文件
                                            csv_writer.writerow(
                                                [i + 1, voltage_value_VAR1, voltage_value_VAR2, voltage_CONST1,
                                                 current_value_VAR1, current_value_VAR2, current_value_CONST1])

                                            # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                            print(
                                                '{:<10} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format(
                                                    i + 1,
                                                    voltage_value_VAR1,
                                                    voltage_value_VAR2,
                                                    voltage_CONST1,
                                                    current_value_VAR1,
                                                    current_value_VAR2,
                                                    current_value_CONST1))
                        else:#这时候没有用到CONST
                            csv_writer.writerow(
                                ['Step', 'V_VAR1', 'V_VAR2', 'I_VAR1', 'I_VAR2'
                                 ])
                            # 创建VAR1控制的会话并设置参数
                            with nidcpower.Session(resource_name=VAR1) as session_VAR1:
                                session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                session_VAR1.current_limit = current_limit_VAR1  # 设置VAR1端的电流限制
                                session_VAR1.current_limit_range = current_limit_range_VAR1
                                # 设置VAR1.PLC
                                session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                session_VAR1.aperture_time = VAR1_PLC
                                voltage_step_VAR1 = round((voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1),
                                                          8)
                                # 启动所有会话
                                session_VAR1.initiate()
                                # 打印表头
                                print('{:<10} {:<15} {:<15} {:<15} {:<15} '.format('Step', 'V_VAR1', 'V_VAR2','I_VAR1', 'I_VAR2'))
                                # 逐步设置VAR1电压并测量VAR1、VAR2、CONST的电流
                                for i in range(num_points_VAR1):
                                    direction = "Forward"
                                    step = i + 1
                                    voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                    session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                    time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                    # 执行测量VAR1电流
                                    current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)

                                    # 执行测量VAR2电流
                                    current_value_VAR2 = session_VAR2.measure(nidcpower.MeasurementTypes.CURRENT)

                                    # 每一步的测量数据存入 measurement_data 字典
                                    measurement_data = create_measurement(
                                        direction=direction,
                                        step=step,
                                        voltage_value_VAR1=voltage_value_VAR1,
                                        voltage_value_VAR2=voltage_value_VAR2,
                                        current_value_VAR1=current_value_VAR1,
                                        current_value_VAR2=current_value_VAR2,
                                    )
                                    send_measurement(measurement_data)
                                    # 写入CSV文件
                                    csv_writer.writerow(
                                        [i + 1, voltage_value_VAR1, voltage_value_VAR2,
                                         current_value_VAR1, current_value_VAR2])

                                    # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                    print(
                                        '{:<10} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} '.format(
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
                    for j in range(num_points_VAR2):
                        voltage_value_VAR2 = voltage_min_VAR2 + j * voltage_step_VAR2
                        session_VAR2.voltage_level = voltage_value_VAR2  # 设置VAR2端的电压输出
                        if CONST1 is not None:
                            if CONST2 is not None:  # 这时候用了两个CONST
                                csv_writer.writerow(
                                    ['Step', 'V_VAR1', 'V_VAR2', 'V_CONST1', 'V_CONST2', 'I_VAR1', 'I_VAR2', 'I_CONST1',
                                     'I_CONST2'])
                                # 创建VAR1控制的会话并设置参数
                                with nidcpower.Session(resource_name=VAR1) as session_VAR1:
                                    session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                    session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                    session_VAR1.current_limit = current_limit_VAR1  # 设置VAR1端的电流限制
                                    session_VAR1.current_limit_range = current_limit_range_VAR1
                                    # 设置VAR1.PLC
                                    session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                    session_VAR1.aperture_time = VAR1_PLC

                                    # 创建2个CONST控制的会话并设置参数
                                    with nidcpower.Session(resource_name=CONST1) as session_CONST1:
                                        session_CONST1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                        session_CONST1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                        session_CONST1.voltage_level = voltage_CONST1  # 设CONST端的电压
                                        session_CONST1.current_limit = current_limit_CONST1
                                        session_CONST1.current_limit_range = current_limit_range_CONST1
                                        # 设置CONST1.PLC
                                        session_CONST1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                        session_CONST1.aperture_time = CONST1_PLC

                                        with nidcpower.Session(resource_name=CONST2) as session_CONST2:
                                            session_CONST2.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                            session_CONST2.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                            session_CONST2.voltage_level = voltage_CONST2  # 设CONST端的电压
                                            session_CONST2.current_limit = current_limit_CONST2
                                            session_CONST2.current_limit_range = current_limit_range_CONST2
                                            # 设置CONST2.PLC
                                            session_CONST2.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                            session_CONST2.aperture_time = CONST2_PLC
                                            # 计算步进电压
                                            voltage_step_VAR1 = round(
                                                (voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)
                                            # 启动所有会话
                                            session_VAR1.initiate()
                                            session_CONST1.initiate()
                                            session_CONST2.initiate()
                                            # 打印表头
                                            print(
                                                '{:<10} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}'.format('Step',
                                                                                                                        'V_VAR1',
                                                                                                                        'V_VAR2',
                                                                                                                        'V_CONST1',
                                                                                                                        'V_CONST2',
                                                                                                                        'I_VAR1',
                                                                                                                        'I_VAR2',
                                                                                                                        'I_CONST1',
                                                                                                                        'I_CONST2'))
                                            # 逐步设置VAR1电压并测量VAR1、VAR2、CONST的电流
                                            for i in range(num_points_VAR1):
                                                direction = "Forward"
                                                step = i + 1
                                                voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                                session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                                time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                                # 执行测量VAR1电流
                                                current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)

                                                # 执行测量VAR2电流
                                                current_value_VAR2 = session_VAR2.measure(nidcpower.MeasurementTypes.CURRENT)

                                                # 执行测量CONST1电流
                                                current_value_CONST1 = session_CONST1.measure(
                                                    nidcpower.MeasurementTypes.CURRENT)
                                                # 执行测量CONST2电流
                                                current_value_CONST2 = session_CONST2.measure(
                                                    nidcpower.MeasurementTypes.CURRENT)

                                                # 每一步的测量数据存入 measurement_data 字典
                                                measurement_data = create_measurement(
                                                    direction=direction,
                                                    step=step,
                                                    voltage_value_VAR1=voltage_value_VAR1,
                                                    voltage_value_VAR2=voltage_value_VAR2,
                                                    current_value_VAR1=current_value_VAR1,
                                                    current_value_VAR2=current_value_VAR2,
                                                    voltage_CONST1=voltage_CONST1,
                                                    voltage_CONST2=voltage_CONST2,
                                                    current_value_CONST1=current_value_CONST1,
                                                    current_value_CONST2=current_value_CONST2,
                                                )
                                                send_measurement(measurement_data)
                                                # 写入CSV文件
                                                csv_writer.writerow(
                                                    [i + 1, voltage_value_VAR1, voltage_value_VAR2, voltage_CONST1,
                                                     voltage_CONST2,
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
                                                        current_value_CONST2
                                                    ))
                            else:  # 这时候说明只启用CONST1
                                csv_writer.writerow(
                                    ['Step', 'V_VAR1', 'V_VAR2', 'V_CONST1', 'I_VAR1', 'I_VAR2', 'I_CONST1'
                                     ])
                                with nidcpower.Session(resource_name=VAR1) as session_VAR1:
                                    session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                    session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                    session_VAR1.current_limit = current_limit_VAR1  # 设置VAR1端的电流限制
                                    session_VAR1.current_limit_range = current_limit_range_VAR1
                                    # 设置VAR1.PLC
                                    session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                    session_VAR1.aperture_time = VAR1_PLC

                                    # 创建CONST1控制的会话并设置参数
                                    with nidcpower.Session(resource_name=CONST1) as session_CONST1:
                                        session_CONST1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                        session_CONST1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                        session_CONST1.voltage_level = voltage_CONST1  # 设CONST端的电压
                                        session_CONST1.current_limit = current_limit_CONST1
                                        session_CONST1.current_limit_range = current_limit_range_CONST1

                                        # 设置CONST1.PLC
                                        session_CONST1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                        session_CONST1.aperture_time = CONST1_PLC

                                        # 计算步进电压
                                        voltage_step_VAR1 = round(
                                            (voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)

                                        # 启动所有会话
                                        session_VAR1.initiate()
                                        session_CONST1.initiate()

                                        # 打印表头
                                        print(
                                            '{:<10} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}'.format('Step', 'V_VAR1',
                                                                                                      'V_VAR2',
                                                                                                      'V_CONST1',
                                                                                                      'I_VAR1',
                                                                                                      'I_VAR2',
                                                                                                      'I_CONST1'))

                                        # 逐步设置VAR1电压并测量VAR1、VAR2、CONST1的电流
                                        for i in range(num_points_VAR1):
                                            direction = "Forward"
                                            step = i + 1
                                            voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                            session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                            time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                            # 执行测量VAR1电流
                                            current_value_VAR1 = session_VAR1.measure(
                                                nidcpower.MeasurementTypes.CURRENT)

                                            # 执行测量VAR2电流
                                            current_value_VAR2 = session_VAR2.measure(
                                                nidcpower.MeasurementTypes.CURRENT)

                                            # 执行测量CONST1电流
                                            current_value_CONST1 = session_CONST1.measure(
                                                nidcpower.MeasurementTypes.CURRENT)

                                            measurement_data = create_measurement(
                                                direction=direction,
                                                step=step,
                                                voltage_value_VAR1=voltage_value_VAR1,
                                                voltage_value_VAR2=voltage_value_VAR2,
                                                current_value_VAR1=current_value_VAR1,
                                                current_value_VAR2=current_value_VAR2,
                                                voltage_CONST1=voltage_CONST1,
                                                current_value_CONST1=current_value_CONST1,
                                            )
                                            send_measurement(measurement_data)
                                            # 写入CSV文件
                                            csv_writer.writerow(
                                                [i + 1, voltage_value_VAR1, voltage_value_VAR2, voltage_CONST1,
                                                 current_value_VAR1, current_value_VAR2, current_value_CONST1])

                                            # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                            print(
                                                '{:<10} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format(
                                                    i + 1,
                                                    voltage_value_VAR1,
                                                    voltage_value_VAR2,
                                                    voltage_CONST1,
                                                    current_value_VAR1,
                                                    current_value_VAR2,
                                                    current_value_CONST1))
                        else:  # 这时候没有用到CONST
                            csv_writer.writerow(
                                ['Step', 'V_VAR1', 'V_VAR2', 'I_VAR1', 'I_VAR2'
                                 ])
                            # 创建VAR1控制的会话并设置参数
                            with nidcpower.Session(resource_name=VAR1) as session_VAR1:
                                session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                session_VAR1.current_limit = current_limit_VAR1  # 设置VAR1端的电流限制
                                session_VAR1.current_limit_range = current_limit_range_VAR1
                                # 设置VAR1.PLC
                                session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                session_VAR1.aperture_time = VAR1_PLC
                                voltage_step_VAR1 = round((voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1),
                                                          8)
                                # 启动所有会话
                                session_VAR1.initiate()
                                # 打印表头
                                print('{:<10} {:<15} {:<15} {:<15} {:<15} '.format('Step', 'V_VAR1', 'V_VAR2', 'I_VAR1',
                                                                                   'I_VAR2'))
                                # 逐步设置VAR1电压并测量VAR1、VAR2、CONST的电流
                                for i in range(num_points_VAR1):
                                    direction = "Forward"
                                    step = i + 1
                                    voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                    session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                    time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                    # 执行测量VAR1电流
                                    current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)

                                    # 执行测量VAR2电流
                                    current_value_VAR2 = session_VAR2.measure(nidcpower.MeasurementTypes.CURRENT)

                                    measurement_data = create_measurement(
                                        direction=direction,
                                        step=step,
                                        voltage_value_VAR1=voltage_value_VAR1,
                                        voltage_value_VAR2=voltage_value_VAR2,
                                        current_value_VAR1=current_value_VAR1,
                                        current_value_VAR2=current_value_VAR2,
                                    )
                                    send_measurement(measurement_data)
                                    # 写入CSV文件
                                    csv_writer.writerow(
                                        [i + 1, voltage_value_VAR1, voltage_value_VAR2,
                                         current_value_VAR1, current_value_VAR2])

                                    # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                    print('{:<10} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} '.format(
                                            i + 1,
                                            voltage_value_VAR1,
                                            voltage_value_VAR2,
                                            current_value_VAR1,
                                            current_value_VAR2,

                                        ))

            print(f"Data saved to {output_path + output_file }")
    else:#这时候只使用VAR1,那么需要接着考虑用几个CONST的问题
        with open(output_path + output_file, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            if CONST1 is not None:#说明使用了CONST1
                if CONST2 is not None:#说明使用了CONST2
                    if CONST3 is not None:#三个CONST都用了
                        csv_writer.writerow(
                            ['Direction', 'Step', 'V_VAR1', 'V_CONST1', 'V_CONST2', 'V_CONST3', 'I_VAR1', 'I_CONST1', 'I_CONST2', 'I_CONST3'])
                        with nidcpower.Session(resource_name=VAR1) as session_VAR1:
                            session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT
                            session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE
                            session_VAR1.current_limit = current_limit_VAR1
                            session_VAR1.current_limit_range = current_limit_range_VAR1
                            # 设置VAR1.PLC
                            session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                            session_VAR1.aperture_time = VAR1_PLC

                            # 创建CONST1控制的会话并设置参数
                            with nidcpower.Session(resource_name=CONST1) as session_CONST1:
                                session_CONST1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                session_CONST1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                session_CONST1.voltage_level = voltage_CONST1  # 设CONST端的电压
                                session_CONST1.current_limit = current_limit_CONST1
                                session_CONST1.current_limit_range = current_limit_range_CONST1

                                # 设置CONST1.PLC
                                session_CONST1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                session_CONST1.aperture_time = CONST1_PLC

                                # 创建CONST2控制的会话并设置参数
                                with nidcpower.Session(resource_name=CONST2) as session_CONST2:
                                    session_CONST2.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                    session_CONST2.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                    session_CONST2.voltage_level = voltage_CONST1  # 设CONST端的电压
                                    session_CONST2.current_limit = current_limit_CONST1
                                    session_CONST2.current_limit_range = current_limit_range_CONST2

                                    # 设置CONST2.PLC
                                    session_CONST2.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                    session_CONST2.aperture_time = CONST2_PLC

                                    # 创建CONST3控制的会话并设置参数
                                    with nidcpower.Session(resource_name=CONST3) as session_CONST3:
                                        session_CONST3.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                        session_CONST3.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                        session_CONST3.voltage_level = voltage_CONST3  # 设CONST端的电压
                                        session_CONST3.current_limit = current_limit_CONST3
                                        session_CONST3.current_limit_range = current_limit_range_CONST3

                                        # 设置CONST3.PLC
                                        session_CONST3.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                        session_CONST3.aperture_time = CONST3_PLC

                                        #启动所有会话
                                        session_VAR1.initiate()
                                        session_CONST1.initiate()
                                        session_CONST2.initiate()
                                        session_CONST3.initiate()

                                        # 计算VAR1步进电压
                                        voltage_step_VAR1 = round((voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1),
                                                                      8)
                                            # 打印表头
                                        print('{:<10} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}'.format('Direction', 'Step',
                                                                                                                    'V_VAR1', 'V_CONST1', 'V_CONST2', 'V_CONST3', 'I_VAR1', 'I_CONST1', 'I_CONST2', 'I_CONST3'))

                                            # 扫描VAR1：逐步设置VAR1电压并测量VAR1的电流
                                        for i in range(num_points_VAR1):
                                            direction = "Forward"
                                            step = i + 1
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

                                            measurement_data = create_measurement(
                                                direction = direction,
                                                step = step,
                                                voltage_value_VAR1 = voltage_value_VAR1,
                                                current_value_VAR1 = current_value_VAR1,
                                                voltage_CONST1 = voltage_CONST1,
                                                current_value_CONST1=current_value_CONST1,
                                                voltage_CONST2 =voltage_CONST2,
                                                current_value_CONST2 = current_value_CONST2,
                                                voltage_CONST3 = voltage_CONST3,
                                                current_value_CONST3 = current_value_CONST3,
                                            )
                                            send_measurement(measurement_data)
                                            # 写入CSV文件
                                            csv_writer.writerow(
                                                    ['Forward', i + 1, voltage_value_VAR1, voltage_CONST1, voltage_CONST2, voltage_CONST3,
                                                     current_value_VAR1,
                                                     current_value_CONST1, current_value_CONST2, current_value_CONST3])

                                            # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                            print(
                                                    '{:<10} {:<15} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format(
                                                        'Forward', i + 1,
                                                        voltage_value_VAR1,
                                                        voltage_CONST1, voltage_CONST2, voltage_CONST3,
                                                        current_value_VAR1,
                                                        current_value_CONST1,
                                                        current_value_CONST2, current_value_CONST3))
                    else:#VAR1+CONST1+CONST2
                        csv_writer.writerow(['Direction', 'Step', 'V_VAR1', 'V_CONST1', 'V_CONST2', 'I_VAR1', 'I_CONST1', 'I_CONST2'])
                        with nidcpower.Session(resource_name=VAR1) as session_VAR1:
                            session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT
                            session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE
                            session_VAR1.current_limit = current_limit_VAR1
                            session_VAR1.current_limit_range = current_limit_range_VAR1
                            # 设置VAR1.PLC
                            session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                            session_VAR1.aperture_time = VAR1_PLC

                            # 创建CONST1控制的会话并设置参数
                            with nidcpower.Session(resource_name=CONST1) as session_CONST1:
                                session_CONST1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                session_CONST1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                session_CONST1.voltage_level = voltage_CONST1  # 设CONST端的电压
                                session_CONST1.current_limit = current_limit_CONST1
                                session_CONST1.current_limit_range = current_limit_range_CONST1

                                # 设置CONST1.PLC
                                session_CONST1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                session_CONST1.aperture_time = CONST1_PLC

                                # 创建CONST2控制的会话并设置参数
                                with nidcpower.Session(resource_name=CONST2) as session_CONST2:
                                    session_CONST2.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                    session_CONST2.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                    session_CONST2.voltage_level = voltage_CONST1  # 设CONST端的电压
                                    session_CONST2.current_limit = current_limit_CONST1
                                    session_CONST2.current_limit_range = current_limit_range_CONST2

                                    # 设置CONST2.PLC
                                    session_CONST2.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                    session_CONST2.aperture_time = CONST2_PLC
                                    # 计算VAR1步进电压
                                    voltage_step_VAR1 = round((voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)
                                    # 打印表头
                                    print('{:<10} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} '.format('Direction', 'Step', 'V_VAR1', 'V_CONST1', 'V_CONST2', 'I_VAR1', 'I_CONST1', 'I_CONST2'))

                                    # 启动所有会话
                                    session_VAR1.initiate()
                                    session_CONST1.initiate()
                                    session_CONST2.initiate()

                                    # 扫描VAR1：逐步设置VAR1电压并测量VAR1的电流
                                    for i in range(num_points_VAR1):
                                        direction = "Forward"
                                        step = i + 1
                                        voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                        session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                        time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                        # 执行测量VAR1电流
                                        current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)
                                        # 执行测量CONST1电流
                                        current_value_CONST1 = session_CONST1.measure(nidcpower.MeasurementTypes.CURRENT)
                                        # 执行测量CONST2电流
                                        current_value_CONST2 = session_CONST2.measure(nidcpower.MeasurementTypes.CURRENT)

                                        measurement_data = create_measurement(
                                            direction=direction,
                                            step=step,
                                            voltage_value_VAR1=voltage_value_VAR1,
                                            current_value_VAR1=current_value_VAR1,
                                            voltage_CONST1=voltage_CONST1,
                                            current_value_CONST1=current_value_CONST1,
                                            voltage_CONST2=voltage_CONST2,
                                            current_value_CONST2=current_value_CONST2,
                                        )
                                        send_measurement(measurement_data)
                                        # 写入CSV文件
                                        csv_writer.writerow(['Forward', i + 1, voltage_value_VAR1, voltage_CONST1, voltage_CONST2, current_value_VAR1,
                                        current_value_CONST1, current_value_CONST2])

                                        # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                        print('{:<10} {:<15} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format('Forward', i + 1,
                                                                                               voltage_value_VAR1,
                                                                                               voltage_CONST1, voltage_CONST2,
                                                                                               current_value_VAR1,
                                                                                               current_value_CONST1,
                                                                                               current_value_CONST2 ))
                else:#VAR1+CONST1
                    csv_writer.writerow(['Direction', 'Step', 'V_VAR1', 'V_CONST1', 'I_VAR1', 'I_CONST1'])
                    with nidcpower.Session(resource_name=VAR1) as session_VAR1:
                        session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT
                        session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE
                        session_VAR1.current_limit = current_limit_VAR1
                        session_VAR1.current_limit_range = current_limit_range_VAR1
                        # 设置VAR1.PLC
                        session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                        session_VAR1.aperture_time = VAR1_PLC

                        # 计算VAR1步进电压
                        voltage_step_VAR1 = round((voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)
                        # 打印表头
                        print('{:<10} {:<15} {:<15} {:<15} {:<15} {:<15}'.format('Direction', 'Step', 'V_VAR1',
                                                                                 'V_CONST1', 'I_VAR1',
                                                                                 'I_CONST1'))
                        # 创建CONST1控制的会话并设置参数
                        with nidcpower.Session(resource_name=CONST1) as session_CONST1:
                            session_CONST1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                            session_CONST1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                            session_CONST1.voltage_level = voltage_CONST1  # 设CONST端的电压
                            session_CONST1.current_limit = current_limit_CONST1
                            session_CONST1.current_limit_range = current_limit_range_CONST1

                            # 设置CONST1.PLC
                            session_CONST1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                            session_CONST1.aperture_time = CONST1_PLC

                            # 启动所有会话
                            session_VAR1.initiate()
                            session_CONST1.initiate()

                            # 扫描VAR1：逐步设置VAR1电压并测量VAR1的电流
                            for i in range(num_points_VAR1):
                                direction = "Forward"
                                step = i + 1
                                voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                # 执行测量VAR1电流
                                current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)
                                # 执行测量CONST1电流
                                current_value_CONST1 = session_CONST1.measure(nidcpower.MeasurementTypes.CURRENT)

                                measurement_data = create_measurement(
                                    direction=direction,
                                    step=step,
                                    voltage_value_VAR1=voltage_value_VAR1,
                                    current_value_VAR1=current_value_VAR1,
                                    voltage_CONST1=voltage_CONST1,
                                    current_value_CONST1=current_value_CONST1,
                                )
                                send_measurement(measurement_data)
                                # 写入CSV文件
                                csv_writer.writerow(
                                    ['Forward', i + 1, voltage_value_VAR1, voltage_CONST1, current_value_VAR1,
                                     current_value_CONST1])

                                # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                print('{:<10} {:<15} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format('Forward', i + 1,
                                                                                                         voltage_value_VAR1,
                                                                                                         voltage_CONST1,
                                                                                                         current_value_VAR1,
                                                                                                         current_value_CONST1))
            else:#VAR1
                csv_writer.writerow(['Direction', 'Step', 'V_VAR1', 'I_VAR1'])
                with nidcpower.Session(resource_name=VAR1) as session_VAR1:
                    session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT
                    session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE
                    session_VAR1.current_limit = current_limit_VAR1
                    session_VAR1.current_limit_range = current_limit_range_VAR1
                    # 设置VAR1.PLC
                    session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                    session_VAR1.aperture_time = VAR1_PLC
                    session_VAR1.initiate()
                    # 计算VAR1步进电压
                    voltage_step_VAR1 = round((voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)
                    # 打印表头
                    print('{:<10} {:<15} {:<15} {:<15} '.format('Direction', 'Step', 'V_VAR1', 'I_VAR1'))

                    # 扫描VAR1：逐步设置VAR1电压并测量VAR1的电流
                    for i in range(num_points_VAR1):
                        direction = "Forward"
                        step = i + 1
                        voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                        session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                        time.sleep(0.001)  # 暂停0.001秒，等待稳定

                        # 执行测量VAR1电流
                        current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)
                        measurement_data = create_measurement(
                            direction=direction,
                            step=step,
                            voltage_value_VAR1=voltage_value_VAR1,
                            current_value_VAR1=current_value_VAR1,
                        )
                        send_measurement(measurement_data)
                        # 写入CSV文件
                        csv_writer.writerow(['Forward', i + 1, voltage_value_VAR1, current_value_VAR1])

                        # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                        print('{:<10} {:<15} {:<15.15f} {:<15.15f}'.format('Forward', i + 1,
                                                                           voltage_value_VAR1, current_value_VAR1, ))

        print(f"Data saved to {output_path + output_file}")

def IV_Sweep_Double(VAR1, VAR2, CONST1, CONST2, CONST3, num_points_VAR1, voltage_min_VAR1, voltage_max_VAR1, current_limit_range_VAR1,current_limit_range_CONST1,
                    current_limit_range_CONST2, current_limit_range_CONST3, num_points_VAR2, voltage_min_VAR2, voltage_max_VAR2, voltage_CONST1, voltage_CONST2,
                    voltage_CONST3, current_limit_VAR1,current_limit_VAR2, current_limit_range_VAR2, current_limit_CONST1, current_limit_CONST2, current_limit_CONST3,
                    VAR1_PLC, VAR2_PLC, CONST1_PLC, CONST2_PLC, CONST3_PLC, file_name,file_path):
    # 添加CSV扩展名
    output_file = file_name
    output_file += '.csv'
    output_path = file_path  # .csv文件存储路径
    if VAR2 is not None:
        # 创建VAR2测量的会话并设置参数
        with nidcpower.Session(resource_name=VAR2) as session_VAR2:
            session_VAR2.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
            session_VAR2.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
            session_VAR2.current_limit = current_limit_VAR2  # 设置VAR2端的电流限制
            session_VAR2.current_limit = current_limit_VAR2
            session_VAR2.current_limit_range = current_limit_range_VAR2

            # 设置VAR2.PLC
            session_VAR2.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
            session_VAR2.aperture_time = VAR2_PLC

            #增添if语句，当VAR2只有一个点时，执行一次double测量
            if voltage_max_VAR2 == voltage_min_VAR2:
                session_VAR2.initiate()
                with open(output_path + output_file, 'w', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    for j in range(num_points_VAR2):
                        #设置VAR端输出参数
                        voltage_value_VAR2 = voltage_min_VAR2
                        session_VAR2.voltage_level = voltage_value_VAR2  # 设置VAR2端的电压输出
                        if CONST1 is not None:
                            if CONST2 is not None:#这时候用了两个CONST
                                csv_writer.writerow(['Direction', 'Step', 'V_VAR1', 'V_VAR2', 'V_CONST1', 'V_CONST2', 'I_VAR1', 'I_VAR2', 'I_CONST1', 'I_CONST2'])
                                # 创建VAR1控制的会话并设置参数
                                with nidcpower.Session(resource_name=VAR1) as session_VAR1:
                                    session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                    session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                    session_VAR1.current_limit = current_limit_VAR1  # 设置VAR1端的电流限制
                                    session_VAR1.current_limit = current_limit_VAR1
                                    session_VAR1.current_limit_range = current_limit_range_VAR1

                                    # 设置VAR1.PLC
                                    session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                    session_VAR1.aperture_time = VAR1_PLC

                                    # 创建CONST1控制的会话并设置参数
                                    with nidcpower.Session(resource_name=CONST1) as session_CONST1:
                                        session_CONST1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                        session_CONST1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                        session_CONST1.voltage_level = voltage_CONST1  # 设CONST1端的电压
                                        session_CONST1.current_limit = current_limit_CONST1
                                        session_CONST1.current_limit_range = current_limit_range_CONST1

                                        # 设置CONST1.PLC
                                        session_CONST1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                        session_CONST1.aperture_time = CONST1_PLC

                                        # 创建CONST2控制的会话并设置参数
                                        with nidcpower.Session(resource_name=CONST2) as session_CONST2:
                                            session_CONST2.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                            session_CONST2.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                            session_CONST2.voltage_level = voltage_CONST2  # 设CONST2端的电压
                                            session_CONST2.current_limit = current_limit_CONST2
                                            session_CONST2.current_limit_range = current_limit_range_CONST2

                                            # 设置CONST2.PLC
                                            session_CONST2.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                            session_CONST2.aperture_time = CONST2_PLC

                                            # 计算VAR1步进电压
                                            voltage_step_VAR1 = round((voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)

                                            # 启动所有会话
                                            session_VAR1.initiate()
                                            session_CONST1.initiate()
                                            session_CONST2.initiate()
                                            # 打印表头
                                            print('{:<10} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}'.format('Direction', 'Step',
                                                    'V_VAR1', 'V_VAR2', 'V_CONST1', 'V_CONST2', 'I_VAR1', 'I_VAR2', 'I_CONST1', 'I_CONST2'))
                                                # 正向扫描VAR1：逐步设置VAR1电压并测量VAR1、VAR2、CONST的电流
                                            for i in range(num_points_VAR1):
                                                direction = "Forward"
                                                step = i + 1
                                                voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                                session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                                time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                                # 执行测量VAR1电流
                                                current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)


                                                # 执行测量VAR2电流
                                                current_value_VAR2 = session_VAR2.measure(nidcpower.MeasurementTypes.CURRENT)


                                                # 执行测量CONST1电流
                                                current_value_CONST1 = session_CONST1.measure(nidcpower.MeasurementTypes.CURRENT)

                                                # 执行测量CONST2电流
                                                current_value_CONST2 = session_CONST2.measure(nidcpower.MeasurementTypes.CURRENT)

                                                measurement_data = create_measurement(
                                                    direction=direction,
                                                    step=step,
                                                    voltage_value_VAR1=voltage_value_VAR1,
                                                    current_value_VAR1=current_value_VAR1,
                                                    voltage_value_VAR2=voltage_value_VAR2,
                                                    current_value_VAR2=current_value_VAR2,
                                                    voltage_CONST1=voltage_CONST1,
                                                    current_value_CONST1=current_value_CONST1,
                                                    voltage_CONST2=voltage_CONST2,
                                                    current_value_CONST2=current_value_CONST2,

                                                )
                                                send_measurement(measurement_data)
                                                # 写入CSV文件
                                                csv_writer.writerow(['Forward', i + 1, voltage_value_VAR1, voltage_value_VAR2,
                                                                    voltage_CONST1, voltage_CONST2, current_value_VAR1, current_value_VAR2,
                                                                    current_value_CONST1, current_value_CONST2])

                                                # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                                print('{:<10} {:<15} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format(
                                                        'Forward', i + 1, voltage_value_VAR1, voltage_value_VAR2,
                                                                    voltage_CONST1, voltage_CONST2, current_value_VAR1, current_value_VAR2,
                                                                    current_value_CONST1, current_value_CONST2))

                                            # 反向扫描VAR1
                                            for i in range(num_points_VAR1 - 1, -1, -1):
                                                direction = "Reverse"
                                                step = i + 1
                                                voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                                session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                                time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                                # 执行测量VAR1电流
                                                current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)


                                                # 执行测量VAR2电流
                                                current_value_VAR2 = session_VAR2.measure(nidcpower.MeasurementTypes.CURRENT)


                                                # 执行测量CONST1电流
                                                current_value_CONST1 = session_CONST1.measure(nidcpower.MeasurementTypes.CURRENT)
                                                # 执行测量CONST2电流
                                                current_value_CONST2 = session_CONST2.measure(nidcpower.MeasurementTypes.CURRENT)

                                                measurement_data = create_measurement(
                                                    direction=direction,
                                                    step=step,
                                                    voltage_value_VAR1=voltage_value_VAR1,
                                                    current_value_VAR1=current_value_VAR1,
                                                    voltage_value_VAR2=voltage_value_VAR2,
                                                    current_value_VAR2=current_value_VAR2,
                                                    voltage_CONST1=voltage_CONST1,
                                                    current_value_CONST1=current_value_CONST1,
                                                    voltage_CONST2=voltage_CONST2,
                                                    current_value_CONST2=current_value_CONST2,

                                                )
                                                send_measurement(measurement_data)
                                                # 写入CSV文件
                                                csv_writer.writerow(['Reverse', i + 1, voltage_value_VAR1, voltage_value_VAR2,
                                                                    voltage_CONST1, voltage_CONST2, current_value_VAR1, current_value_VAR2,
                                                                    current_value_CONST1, current_value_CONST2])

                                                # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                                print('{:<10} {:<15} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format('Reverse', i + 1,
                                                                    voltage_value_VAR1, voltage_value_VAR2,
                                                                    voltage_CONST1, voltage_CONST2, current_value_VAR1, current_value_VAR2,
                                                                    current_value_CONST1, current_value_CONST2))
                            else:#这时候说明只启用CONST1
                                csv_writer.writerow(
                                    ['Direction', 'Step', 'V_VAR1', 'V_VAR2', 'V_CONST1', 'I_VAR1',
                                     'I_VAR2', 'I_CONST1'])
                                # 创建VAR1控制的会话并设置参数
                                with nidcpower.Session(resource_name=VAR1) as session_VAR1:
                                    session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                    session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                    session_VAR1.current_limit = current_limit_VAR1  # 设置VAR1端的电流限制
                                    session_VAR1.current_limit = current_limit_VAR1
                                    session_VAR1.current_limit_range = current_limit_range_VAR1

                                    # 设置VAR1.PLC
                                    session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                    session_VAR1.aperture_time = VAR1_PLC

                                    # 创建CONST1控制的会话并设置参数
                                    with nidcpower.Session(resource_name=CONST1) as session_CONST1:
                                        session_CONST1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                        session_CONST1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                        session_CONST1.voltage_level = voltage_CONST1  # 设CONST1端的电压
                                        session_CONST1.current_limit = current_limit_CONST1
                                        session_CONST1.current_limit_range = current_limit_range_CONST1

                                        # 设置CONST1.PLC
                                        session_CONST1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                        session_CONST1.aperture_time = CONST1_PLC
                                        # 计算VAR1步进电压
                                        voltage_step_VAR1 = round(
                                            (voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)

                                        # 启动所有会话
                                        session_VAR1.initiate()
                                        session_CONST1.initiate()
                                        # 打印表头
                                        print('{:<10} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}'.format(
                                            'Direction', 'Step',
                                            'V_VAR1', 'V_VAR2', 'V_CONST1', 'I_VAR1', 'I_VAR2', 'I_CONST1'))
                                        # 正向扫描VAR1：逐步设置VAR1电压并测量VAR1、VAR2、CONST的电流
                                        for i in range(num_points_VAR1):
                                            direction = "Forward"
                                            step = i + 1
                                            voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                            session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                            time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                            # 执行测量VAR1电流
                                            current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)

                                            # 执行测量VAR2电流
                                            current_value_VAR2 = session_VAR2.measure(nidcpower.MeasurementTypes.CURRENT)

                                            # 执行测量CONST1电流
                                            current_value_CONST1 = session_CONST1.measure(
                                                nidcpower.MeasurementTypes.CURRENT)

                                            measurement_data = create_measurement(
                                                direction=direction,
                                                step=step,
                                                voltage_value_VAR1=voltage_value_VAR1,
                                                current_value_VAR1=current_value_VAR1,
                                                voltage_value_VAR2=voltage_value_VAR2,
                                                current_value_VAR2=current_value_VAR2,
                                                voltage_CONST1=voltage_CONST1,
                                                current_value_CONST1=current_value_CONST1,
                                            )
                                            send_measurement(measurement_data)
                                            # 写入CSV文件
                                            csv_writer.writerow(['Forward', i + 1, voltage_value_VAR1, voltage_value_VAR2,
                                                                 voltage_CONST1, current_value_VAR1, current_value_VAR2,
                                                                 current_value_CONST1])

                                            # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                            print(
                                                '{:<10} {:<15} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format(
                                                    'Forward', i + 1, voltage_value_VAR1, voltage_value_VAR2,
                                                    voltage_CONST1, current_value_VAR1, current_value_VAR2,
                                                    current_value_CONST1))

                                        # 反向扫描VAR1
                                        for i in range(num_points_VAR1 - 1, -1, -1):
                                            direction = "Reverse"
                                            step = i + 1
                                            voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                            session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                            time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                            # 执行测量VAR1电流
                                            current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)

                                            # 执行测量VAR2电流
                                            current_value_VAR2 = session_VAR2.measure(nidcpower.MeasurementTypes.CURRENT)

                                            # 执行测量CONST1电流
                                            current_value_CONST1 = session_CONST1.measure(
                                                nidcpower.MeasurementTypes.CURRENT)

                                            measurement_data = create_measurement(
                                                direction=direction,
                                                step=step,
                                                voltage_value_VAR1=voltage_value_VAR1,
                                                current_value_VAR1=current_value_VAR1,
                                                voltage_value_VAR2=voltage_value_VAR2,
                                                current_value_VAR2=current_value_VAR2,
                                                voltage_CONST1=voltage_CONST1,
                                                current_value_CONST1=current_value_CONST1,
                                            )
                                            send_measurement(measurement_data)
                                            # 写入CSV文件
                                            csv_writer.writerow(['Reverse', i + 1, voltage_value_VAR1, voltage_value_VAR2,
                                                                 voltage_CONST1, current_value_VAR1, current_value_VAR2,
                                                                 current_value_CONST1])

                                            # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                            print('{:<10} {:<15} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format(
                                                    'Reverse', i + 1,
                                                    voltage_value_VAR1, voltage_value_VAR2,
                                                    voltage_CONST1, current_value_VAR1, current_value_VAR2,
                                                    current_value_CONST1))
                        else:#这时候没有用到CONST
                                csv_writer.writerow(['Direction', 'Step', 'V_VAR1', 'V_VAR2', 'I_VAR1', 'I_VAR2'])
                                with nidcpower.Session(resource_name=VAR1) as session_VAR1:
                                    session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT
                                    session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE
                                    session_VAR1.current_limit = current_limit_VAR1
                                    session_VAR1.current_limit_range = current_limit_range_VAR1
                                    # 设置VAR1.PLC
                                    session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                    session_VAR1.aperture_time = VAR1_PLC
                                    session_VAR1.initiate()
                                    # 计算VAR1步进电压
                                    voltage_step_VAR1 = round(
                                        (voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)
                                    # 打印表头
                                    print(
                                        '{:<10} {:<15} {:<15} {:<15} {:<15} {:<15}'.format('Direction', 'Step', 'V_VAR1','V_VAR2', 'I_VAR1', 'I_VAR2'))

                                    # 正向扫描VAR1：逐步设置VAR1电压并测量VAR1的电流
                                    for i in range(num_points_VAR1):
                                        direction = "Forward"
                                        step = i + 1
                                        voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                        session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                        time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                        # 执行测量VAR1电流
                                        current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)
                                        current_value_VAR2 = session_VAR2.measure(nidcpower.MeasurementTypes.CURRENT)

                                        measurement_data = create_measurement(
                                            direction=direction,
                                            step=step,
                                            voltage_value_VAR1=voltage_value_VAR1,
                                            current_value_VAR1=current_value_VAR1,
                                            voltage_value_VAR2=voltage_value_VAR2,
                                            current_value_VAR2=current_value_VAR2,
                                        )
                                        send_measurement(measurement_data)
                                        # 写入CSV文件
                                        csv_writer.writerow(['Forward', i + 1, voltage_value_VAR1,voltage_value_VAR2, current_value_VAR1, current_value_VAR2])

                                        # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                        print('{:<10} {:<15} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format('Forward', i + 1,
                                                                                                                    voltage_value_VAR1, voltage_value_VAR2,
                                                                                                                    current_value_VAR1,current_value_VAR2 ))

                                    # 反向扫描VAR1
                                    for i in range(num_points_VAR1 - 1, -1, -1):
                                        direction = "Reverse"
                                        step = i + 1
                                        voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                        session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                        time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                        # 执行测量VAR1电流
                                        current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)
                                        current_value_VAR2 = session_VAR2.measure(nidcpower.MeasurementTypes.CURRENT)

                                        measurement_data = create_measurement(
                                            direction=direction,
                                            step=step,
                                            voltage_value_VAR1=voltage_value_VAR1,
                                            current_value_VAR1=current_value_VAR1,
                                            voltage_value_VAR2=voltage_value_VAR2,
                                            current_value_VAR2=current_value_VAR2,
                                        )
                                        send_measurement(measurement_data)
                                        # 写入CSV文件
                                        csv_writer.writerow(['Reverse', i + 1, voltage_value_VAR1,voltage_value_VAR2, current_value_VAR1, current_value_VAR2])

                                        # 打印步数
                                        print('{:<10} {:<15} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format('Reverse', i + 1,
                                                                                                                 voltage_value_VAR1,
                                                                                                                 voltage_value_VAR2,
                                                                                                                 current_value_VAR1,
                                                                                                                 current_value_VAR2 ))
            else:
                # 计算VAR2步进电压
                voltage_step_VAR2 = round((voltage_max_VAR2 - voltage_min_VAR2) / (num_points_VAR2 - 1), 8)
                session_VAR2.initiate()
                with open(output_path + output_file, 'w', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    for j in range(num_points_VAR2):
                        # 设置VAR端输出参数
                        voltage_value_VAR2 = voltage_min_VAR2 + j * voltage_step_VAR2
                        session_VAR2.voltage_level = voltage_value_VAR2  # 设置VAR2端的电压输出
                        if CONST1 is not None:
                            if CONST2 is not None:  # 这时候用了两个CONST
                                csv_writer.writerow(
                                    ['Direction', 'Step', 'V_VAR1', 'V_VAR2', 'V_CONST1', 'V_CONST2', 'I_VAR1',
                                     'I_VAR2', 'I_CONST1', 'I_CONST2'])
                                # 创建VAR1控制的会话并设置参数
                                with nidcpower.Session(resource_name=VAR1) as session_VAR1:
                                    session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                    session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                    session_VAR1.current_limit = current_limit_VAR1  # 设置VAR1端的电流限制
                                    session_VAR1.current_limit = current_limit_VAR1
                                    session_VAR1.current_limit_range = current_limit_range_VAR1

                                    # 设置VAR1.PLC
                                    session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                    session_VAR1.aperture_time = VAR1_PLC

                                    # 创建CONST1控制的会话并设置参数
                                    with nidcpower.Session(resource_name=CONST1) as session_CONST1:
                                        session_CONST1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                        session_CONST1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                        session_CONST1.voltage_level = voltage_CONST1  # 设CONST1端的电压
                                        session_CONST1.current_limit = current_limit_CONST1
                                        session_CONST1.current_limit_range = current_limit_range_CONST1

                                        # 设置CONST1.PLC
                                        session_CONST1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                        session_CONST1.aperture_time = CONST1_PLC

                                        # 创建CONST2控制的会话并设置参数
                                        with nidcpower.Session(resource_name=CONST2) as session_CONST2:
                                            session_CONST2.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                            session_CONST2.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                            session_CONST2.voltage_level = voltage_CONST2  # 设CONST2端的电压
                                            session_CONST2.current_limit = current_limit_CONST2
                                            session_CONST2.current_limit_range = current_limit_range_CONST2

                                            # 设置CONST2.PLC
                                            session_CONST2.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                            session_CONST2.aperture_time = CONST2_PLC

                                            # 计算VAR1步进电压
                                            voltage_step_VAR1 = round(
                                                (voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)

                                            # 启动所有会话
                                            session_VAR1.initiate()
                                            session_CONST1.initiate()
                                            session_CONST2.initiate()
                                            # 打印表头
                                            print('{:<10} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}'.format(
                                                'Direction', 'Step',
                                                'V_VAR1', 'V_VAR2', 'V_CONST1', 'V_CONST2', 'I_VAR1', 'I_VAR2', 'I_CONST1',
                                                'I_CONST2'))
                                            # 正向扫描VAR1：逐步设置VAR1电压并测量VAR1、VAR2、CONST的电流
                                            for i in range(num_points_VAR1):
                                                direction = "Forward"
                                                step = i + 1
                                                voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                                session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                                time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                                # 执行测量VAR1电流
                                                current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)

                                                # 执行测量VAR2电流
                                                current_value_VAR2 = session_VAR2.measure(nidcpower.MeasurementTypes.CURRENT)

                                                # 执行测量CONST1电流
                                                current_value_CONST1 = session_CONST1.measure(
                                                    nidcpower.MeasurementTypes.CURRENT)

                                                # 执行测量CONST2电流
                                                current_value_CONST2 = session_CONST2.measure(
                                                    nidcpower.MeasurementTypes.CURRENT)
                                                measurement_data = create_measurement(
                                                    direction=direction,
                                                    step=step,
                                                    voltage_value_VAR1=voltage_value_VAR1,
                                                    current_value_VAR1=current_value_VAR1,
                                                    voltage_value_VAR2=voltage_value_VAR2,
                                                    current_value_VAR2=current_value_VAR2,
                                                    voltage_CONST1=voltage_CONST1,
                                                    current_value_CONST1=current_value_CONST1,
                                                    voltage_CONST2=voltage_CONST2,
                                                    current_value_CONST2=current_value_CONST2,

                                                )
                                                send_measurement(measurement_data)
                                                # 写入CSV文件
                                                csv_writer.writerow(['Forward', i + 1, voltage_value_VAR1, voltage_value_VAR2,
                                                                     voltage_CONST1, voltage_CONST2, current_value_VAR1,
                                                                     current_value_VAR2,
                                                                     current_value_CONST1, current_value_CONST2])

                                                # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                                print(
                                                    '{:<10} {:<15} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format(
                                                        'Forward', i + 1, voltage_value_VAR1, voltage_value_VAR2,
                                                        voltage_CONST1, voltage_CONST2, current_value_VAR1, current_value_VAR2,
                                                        current_value_CONST1, current_value_CONST2))

                                            # 反向扫描VAR1
                                            for i in range(num_points_VAR1 - 1, -1, -1):
                                                direction = "Reverse"
                                                step = i + 1
                                                voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                                session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                                time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                                # 执行测量VAR1电流
                                                current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)

                                                # 执行测量VAR2电流
                                                current_value_VAR2 = session_VAR2.measure(nidcpower.MeasurementTypes.CURRENT)

                                                # 执行测量CONST1电流
                                                current_value_CONST1 = session_CONST1.measure(
                                                    nidcpower.MeasurementTypes.CURRENT)
                                                # 执行测量CONST2电流
                                                current_value_CONST2 = session_CONST2.measure(
                                                    nidcpower.MeasurementTypes.CURRENT)
                                                measurement_data = create_measurement(
                                                    direction=direction,
                                                    step=step,
                                                    voltage_value_VAR1=voltage_value_VAR1,
                                                    current_value_VAR1=current_value_VAR1,
                                                    voltage_value_VAR2=voltage_value_VAR2,
                                                    current_value_VAR2=current_value_VAR2,
                                                    voltage_CONST1=voltage_CONST1,
                                                    current_value_CONST1=current_value_CONST1,
                                                    voltage_CONST2=voltage_CONST2,
                                                    current_value_CONST2=current_value_CONST2,

                                                )
                                                send_measurement(measurement_data)
                                                # 写入CSV文件
                                                csv_writer.writerow(['Reverse', i + 1, voltage_value_VAR1, voltage_value_VAR2,
                                                                     voltage_CONST1, voltage_CONST2, current_value_VAR1,
                                                                     current_value_VAR2,
                                                                     current_value_CONST1, current_value_CONST2])

                                                # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                                print(
                                                    '{:<10} {:<15} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format(
                                                        'Reverse', i + 1,
                                                        voltage_value_VAR1, voltage_value_VAR2,
                                                        voltage_CONST1, voltage_CONST2, current_value_VAR1, current_value_VAR2,
                                                        current_value_CONST1, current_value_CONST2))
                            else:  # 这时候说明只启用CONST1
                                csv_writer.writerow(
                                    ['Direction', 'Step', 'V_VAR1', 'V_VAR2', 'V_CONST1', 'I_VAR1',
                                     'I_VAR2', 'I_CONST1'])
                                # 创建VAR1控制的会话并设置参数
                                with nidcpower.Session(resource_name=VAR1) as session_VAR1:
                                    session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                    session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                    session_VAR1.current_limit = current_limit_VAR1  # 设置VAR1端的电流限制
                                    session_VAR1.current_limit = current_limit_VAR1
                                    session_VAR1.current_limit_range = current_limit_range_VAR1

                                    # 设置VAR1.PLC
                                    session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                    session_VAR1.aperture_time = VAR1_PLC

                                    # 创建CONST1控制的会话并设置参数
                                    with nidcpower.Session(resource_name=CONST1) as session_CONST1:
                                        session_CONST1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                        session_CONST1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                        session_CONST1.voltage_level = voltage_CONST1  # 设CONST1端的电压
                                        session_CONST1.current_limit = current_limit_CONST1
                                        session_CONST1.current_limit_range = current_limit_range_CONST1

                                        # 设置CONST1.PLC
                                        session_CONST1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                        session_CONST1.aperture_time = CONST1_PLC
                                        # 计算VAR1步进电压
                                        voltage_step_VAR1 = round(
                                            (voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)

                                        # 启动所有会话
                                        session_VAR1.initiate()
                                        session_CONST1.initiate()
                                        # 打印表头
                                        print('{:<10} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}'.format(
                                            'Direction', 'Step',
                                            'V_VAR1', 'V_VAR2', 'V_CONST1', 'I_VAR1', 'I_VAR2', 'I_CONST1'))
                                        # 正向扫描VAR1：逐步设置VAR1电压并测量VAR1、VAR2、CONST的电流
                                        for i in range(num_points_VAR1):
                                            direction = "Forward"
                                            step = i + 1
                                            voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                            session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                            time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                            # 执行测量VAR1电流
                                            current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)

                                            # 执行测量VAR2电流
                                            current_value_VAR2 = session_VAR2.measure(nidcpower.MeasurementTypes.CURRENT)

                                            # 执行测量CONST1电流
                                            current_value_CONST1 = session_CONST1.measure(
                                                nidcpower.MeasurementTypes.CURRENT)
                                            measurement_data = create_measurement(
                                                direction=direction,
                                                step=step,
                                                voltage_value_VAR1=voltage_value_VAR1,
                                                current_value_VAR1=current_value_VAR1,
                                                voltage_value_VAR2=voltage_value_VAR2,
                                                current_value_VAR2=current_value_VAR2,
                                                voltage_CONST1=voltage_CONST1,
                                                current_value_CONST1=current_value_CONST1,


                                            )
                                            send_measurement(measurement_data)
                                            # 写入CSV文件
                                            csv_writer.writerow(['Forward', i + 1, voltage_value_VAR1, voltage_value_VAR2,
                                                                 voltage_CONST1, current_value_VAR1, current_value_VAR2,
                                                                 current_value_CONST1])

                                            # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                            print(
                                                '{:<10} {:<15} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format(
                                                    'Forward', i + 1, voltage_value_VAR1, voltage_value_VAR2,
                                                    voltage_CONST1, current_value_VAR1, current_value_VAR2,
                                                    current_value_CONST1))

                                        # 反向扫描VAR1
                                        for i in range(num_points_VAR1 - 1, -1, -1):
                                            direction = "Reverse"
                                            step = i + 1
                                            voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                            session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                            time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                            # 执行测量VAR1电流
                                            current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)

                                            # 执行测量VAR2电流
                                            current_value_VAR2 = session_VAR2.measure(nidcpower.MeasurementTypes.CURRENT)

                                            # 执行测量CONST1电流
                                            current_value_CONST1 = session_CONST1.measure(
                                                nidcpower.MeasurementTypes.CURRENT)
                                            measurement_data = create_measurement(
                                                direction=direction,
                                                step=step,
                                                voltage_value_VAR1=voltage_value_VAR1,
                                                current_value_VAR1=current_value_VAR1,
                                                voltage_value_VAR2=voltage_value_VAR2,
                                                current_value_VAR2=current_value_VAR2,
                                                voltage_CONST1=voltage_CONST1,
                                                current_value_CONST1=current_value_CONST1,

                                            )
                                            send_measurement(measurement_data)
                                            # 写入CSV文件
                                            csv_writer.writerow(['Reverse', i + 1, voltage_value_VAR1, voltage_value_VAR2,
                                                                 voltage_CONST1, current_value_VAR1, current_value_VAR2,
                                                                 current_value_CONST1])

                                            # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                            print('{:<10} {:<15} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format(
                                                'Reverse', i + 1,
                                                voltage_value_VAR1, voltage_value_VAR2,
                                                voltage_CONST1, current_value_VAR1, current_value_VAR2,
                                                current_value_CONST1))
                        else:  # 这时候没有用到CONST
                            csv_writer.writerow(['Direction', 'Step', 'V_VAR1', 'V_VAR2', 'I_VAR1', 'I_VAR2'])
                            with nidcpower.Session(resource_name=VAR1) as session_VAR1:
                                session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT
                                session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE
                                session_VAR1.current_limit = current_limit_VAR1
                                session_VAR1.current_limit_range = current_limit_range_VAR1
                                # 设置VAR1.PLC
                                session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                session_VAR1.aperture_time = VAR1_PLC
                                session_VAR1.initiate()
                                # 计算VAR1步进电压
                                voltage_step_VAR1 = round(
                                    (voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)
                                # 打印表头
                                print(
                                    '{:<10} {:<15} {:<15} {:<15} {:<15} {:<15}'.format('Direction', 'Step', 'V_VAR1', 'V_VAR2', 'I_VAR1', 'I_VAR2'))

                                # 正向扫描VAR1：逐步设置VAR1电压并测量VAR1的电流
                                for i in range(num_points_VAR1):
                                    direction = "Forward"
                                    step = i + 1
                                    voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                    session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                    time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                    # 执行测量VAR1电流
                                    current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)
                                    # 执行测量VAR2电流
                                    current_value_VAR2 = session_VAR2.measure(nidcpower.MeasurementTypes.CURRENT)
                                    measurement_data = create_measurement(
                                        direction=direction,
                                        step=step,
                                        voltage_value_VAR1=voltage_value_VAR1,
                                        current_value_VAR1=current_value_VAR1,
                                        voltage_value_VAR2=voltage_value_VAR2,
                                        current_value_VAR2=current_value_VAR2,

                                    )
                                    send_measurement(measurement_data)
                                    # 写入CSV文件
                                    csv_writer.writerow(['Forward', i + 1, voltage_value_VAR1, current_value_VAR1])

                                    # 打印步数、VAR1、VAR2电压和IVAR1、IVAR2电流值
                                    print('{:<10} {:<15} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format('Forward', i + 1,
                                                                                       voltage_value_VAR1, voltage_value_VAR2,
                                                                                       current_value_VAR1, current_value_VAR2))

                                # 反向扫描VAR1
                                for i in range(num_points_VAR1 - 1, -1, -1):
                                    direction = "Reverse"
                                    step = i + 1
                                    voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                    session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                    time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                    # 执行测量VAR1电流
                                    current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)
                                    # 执行测量VAR2电流
                                    current_value_VAR2 = session_VAR2.measure(nidcpower.MeasurementTypes.CURRENT)
                                    measurement_data = create_measurement(
                                        direction=direction,
                                        step=step,
                                        voltage_value_VAR1=voltage_value_VAR1,
                                        current_value_VAR1=current_value_VAR1,
                                        voltage_value_VAR2=voltage_value_VAR2,
                                        current_value_VAR2=current_value_VAR2,

                                    )
                                    send_measurement(measurement_data)
                                    # 写入CSV文件
                                    csv_writer.writerow(['Reverse', i + 1, voltage_value_VAR1, current_value_VAR1])

                                    # 打印步数
                                    print('{:<10} {:<15} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format('Reverse', i + 1,
                                                                                       voltage_value_VAR1, voltage_value_VAR2,
                                                                                       current_value_VAR1, current_value_VAR2 ))
            print(f"Data saved to {output_path + output_file }")
    else:#说明使用VAR1，但是不使用VAR2
        with open(output_path + output_file, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            if CONST1 is not None:#说明使用了CONST1
                if CONST2 is not None:#说明使用了CONST2
                    if CONST3 is not None:#三个CONST都使用了
                        csv_writer.writerow(
                            ['Direction', 'Step', 'V_VAR1', 'V_CONST1', 'V_CONST2', 'V_CONST3', 'I_VAR1', 'I_CONST1',
                             'I_CONST2', 'I_CONST3'])
                        with nidcpower.Session(resource_name=VAR1) as session_VAR1:
                            session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT
                            session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE
                            session_VAR1.current_limit = current_limit_VAR1
                            session_VAR1.current_limit_range = current_limit_range_VAR1
                            # 设置VAR1.PLC
                            session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                            session_VAR1.aperture_time = VAR1_PLC

                            # 创建CONST1控制的会话并设置参数
                            with nidcpower.Session(resource_name=CONST1) as session_CONST1:
                                session_CONST1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                session_CONST1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                session_CONST1.voltage_level = voltage_CONST1  # 设CONST端的电压
                                session_CONST1.current_limit = current_limit_CONST1
                                session_CONST1.current_limit_range = current_limit_range_CONST1

                                # 设置CONST1.PLC
                                session_CONST1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                session_CONST1.aperture_time = CONST1_PLC

                                # 创建CONST2控制的会话并设置参数
                                with nidcpower.Session(resource_name=CONST2) as session_CONST2:
                                    session_CONST2.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                    session_CONST2.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                    session_CONST2.voltage_level = voltage_CONST1  # 设CONST端的电压
                                    session_CONST2.current_limit = current_limit_CONST1
                                    session_CONST2.current_limit_range = current_limit_range_CONST2

                                    # 设置CONST2.PLC
                                    session_CONST2.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                    session_CONST2.aperture_time = CONST2_PLC

                                    # 创建CONST3控制的会话并设置参数
                                    with nidcpower.Session(resource_name=CONST3) as session_CONST3:
                                        session_CONST3.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                        session_CONST3.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                        session_CONST3.voltage_level = voltage_CONST3  # 设CONST端的电压
                                        session_CONST3.current_limit = current_limit_CONST3
                                        session_CONST3.current_limit_range = current_limit_range_CONST3

                                        # 设置CONST3.PLC
                                        session_CONST3.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                        session_CONST3.aperture_time = CONST3_PLC
                                        # 启动所有会话
                                        session_VAR1.initiate()
                                        session_CONST1.initiate()
                                        session_CONST2.initiate()
                                        session_CONST3.initiate()
                                        # 计算VAR1步进电压
                                        voltage_step_VAR1 = round((voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1),
                                                                  8)
                                        # 打印表头
                                        print('{:<10} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}'.format(
                                            'Direction', 'Step',
                                            'V_VAR1', 'V_CONST1', 'V_CONST2', 'V_CONST3', 'I_VAR1', 'I_CONST1', 'I_CONST2',
                                            'I_CONST3'))

                                        # 扫描VAR1：逐步设置VAR1电压并测量VAR1的电流
                                        for i in range(num_points_VAR1):
                                            direction = "Forward"
                                            step = i+1
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
                                            measurement_data = create_measurement(
                                                direction=direction,
                                                step=step,
                                                voltage_value_VAR1=voltage_value_VAR1,
                                                current_value_VAR1=current_value_VAR1,

                                                voltage_CONST1=voltage_CONST1,
                                                current_value_CONST1=current_value_CONST1,
                                                voltage_CONST2=voltage_CONST2,
                                                current_value_CONST2=current_value_CONST2,
                                                voltage_CONST3=voltage_CONST3,
                                                current_value_CONST3=current_value_CONST3,

                                            )
                                            send_measurement(measurement_data)
                                            # 写入CSV文件
                                            csv_writer.writerow(
                                                ['Forward', i + 1, voltage_value_VAR1, voltage_CONST1, voltage_CONST2,
                                                 voltage_CONST3,
                                                 current_value_VAR1,
                                                 current_value_CONST1, current_value_CONST2, current_value_CONST3])

                                            # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                            print(
                                                '{:<10} {:<15} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format(
                                                    'Forward', i + 1,
                                                    voltage_value_VAR1,
                                                    voltage_CONST1, voltage_CONST2, voltage_CONST3,
                                                    current_value_VAR1,
                                                    current_value_CONST1,
                                                    current_value_CONST2, current_value_CONST3))
                                            # 反向扫描VAR1
                                        for i in range(num_points_VAR1 - 1, -1, -1):
                                            direction = "Reverse"
                                            step = i + 1
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
                                            measurement_data = create_measurement(
                                                direction=direction,
                                                step=step,
                                                voltage_value_VAR1=voltage_value_VAR1,
                                                current_value_VAR1=current_value_VAR1,

                                                voltage_CONST1=voltage_CONST1,
                                                current_value_CONST1=current_value_CONST1,
                                                voltage_CONST2=voltage_CONST2,
                                                current_value_CONST2=current_value_CONST2,
                                                voltage_CONST3=voltage_CONST3,
                                                current_value_CONST3=current_value_CONST3,

                                            )
                                            send_measurement(measurement_data)
                                            # 写入CSV文件
                                            csv_writer.writerow(['Reverse', i + 1, voltage_value_VAR1, voltage_CONST1, voltage_CONST2,
                                                 voltage_CONST3,
                                                 current_value_VAR1,
                                                 current_value_CONST1, current_value_CONST2, current_value_CONST3])

                                            # 打印步数
                                            print('{:<10} {:<15} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format('Reverse', i + 1,
                                                                                                                                                                 voltage_value_VAR1,
                                                                                                                                                                 voltage_CONST1,
                                                                                                                                                                 voltage_CONST2,
                                                                                                                                                                 voltage_CONST3,
                                                                                                                                                                 current_value_VAR1,
                                                                                                                                                                 current_value_CONST1,
                                                                                                                                                                 current_value_CONST2,
                                                                                                                                                                 current_value_CONST3 ))
                    else:#VAR1+CONST1+CONST2
                        csv_writer.writerow(
                            ['Direction', 'Step', 'V_VAR1', 'V_CONST1', 'V_CONST2', 'I_VAR1', 'I_CONST1',
                             'I_CONST2'])
                        with nidcpower.Session(resource_name=VAR1) as session_VAR1:
                            session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT
                            session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE
                            session_VAR1.current_limit = current_limit_VAR1
                            session_VAR1.current_limit_range = current_limit_range_VAR1
                            # 设置VAR1.PLC
                            session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                            session_VAR1.aperture_time = VAR1_PLC

                            # 创建CONST1控制的会话并设置参数
                            with nidcpower.Session(resource_name=CONST1) as session_CONST1:
                                session_CONST1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                session_CONST1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                session_CONST1.voltage_level = voltage_CONST1  # 设CONST端的电压
                                session_CONST1.current_limit = current_limit_CONST1
                                session_CONST1.current_limit_range = current_limit_range_CONST1

                                # 设置CONST1.PLC
                                session_CONST1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                session_CONST1.aperture_time = CONST1_PLC

                                # 创建CONST2控制的会话并设置参数
                                with nidcpower.Session(resource_name=CONST2) as session_CONST2:
                                    session_CONST2.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                                    session_CONST2.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                                    session_CONST2.voltage_level = voltage_CONST1  # 设CONST端的电压
                                    session_CONST2.current_limit = current_limit_CONST1
                                    session_CONST2.current_limit_range = current_limit_range_CONST2

                                    # 设置CONST2.PLC
                                    session_CONST2.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                                    session_CONST2.aperture_time = CONST2_PLC
                                    # 启动所有会话
                                    session_VAR1.initiate()
                                    session_CONST1.initiate()
                                    session_CONST2.initiate()

                                    # 计算VAR1步进电压
                                    voltage_step_VAR1 = round((voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1),
                                                              8)
                                    # 打印表头
                                    print('{:<10} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}'.format(
                                        'Direction', 'Step',
                                        'V_VAR1', 'V_CONST1', 'V_CONST2', 'I_VAR1', 'I_CONST1', 'I_CONST2'))

                                    # 扫描VAR1：逐步设置VAR1电压并测量VAR1的电流
                                    for i in range(num_points_VAR1):
                                        direction = "Forward"
                                        step = i + 1
                                        voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                        session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                        time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                        # 执行测量VAR1电流
                                        current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)
                                        # 执行测量CONST1电流
                                        current_value_CONST1 = session_CONST1.measure(nidcpower.MeasurementTypes.CURRENT)
                                        # 执行测量CONST2电流
                                        current_value_CONST2 = session_CONST2.measure(nidcpower.MeasurementTypes.CURRENT)
                                        measurement_data = create_measurement(
                                            direction=direction,
                                            step=step,
                                            voltage_value_VAR1=voltage_value_VAR1,
                                            current_value_VAR1=current_value_VAR1,
                                            voltage_CONST1=voltage_CONST1,
                                            current_value_CONST1=current_value_CONST1,
                                            voltage_CONST2=voltage_CONST2,
                                            current_value_CONST2=current_value_CONST2,
                                        )
                                        send_measurement(measurement_data)
                                        # 写入CSV文件
                                        csv_writer.writerow(
                                            ['Forward', i + 1, voltage_value_VAR1, voltage_CONST1, voltage_CONST2,
                                             current_value_VAR1,
                                             current_value_CONST1, current_value_CONST2])

                                        # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                        print(
                                            '{:<10} {:<15} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format(
                                                'Forward', i + 1,
                                                voltage_value_VAR1,
                                                voltage_CONST1, voltage_CONST2,
                                                current_value_VAR1,
                                                current_value_CONST1,
                                                current_value_CONST2))
                                        # 反向扫描VAR1
                                    for i in range(num_points_VAR1 - 1, -1, -1):
                                        direction = "Reverse"
                                        step = i + 1
                                        voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                        session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                        time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                        # 执行测量VAR1电流
                                        current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)
                                        # 执行测量CONST1电流
                                        current_value_CONST1 = session_CONST1.measure(nidcpower.MeasurementTypes.CURRENT)
                                        # 执行测量CONST2电流
                                        current_value_CONST2 = session_CONST2.measure(nidcpower.MeasurementTypes.CURRENT)
                                        measurement_data = create_measurement(
                                            direction=direction,
                                            step=step,
                                            voltage_value_VAR1=voltage_value_VAR1,
                                            current_value_VAR1=current_value_VAR1,
                                            voltage_CONST1=voltage_CONST1,
                                            current_value_CONST1=current_value_CONST1,
                                            voltage_CONST2=voltage_CONST2,
                                            current_value_CONST2=current_value_CONST2,
                                        )
                                        send_measurement(measurement_data)
                                        # 写入CSV文件
                                        csv_writer.writerow(
                                            ['Reverse', i + 1, voltage_value_VAR1, voltage_CONST1, voltage_CONST2,
                                             current_value_VAR1,
                                             current_value_CONST1, current_value_CONST2])

                                        # 打印步数
                                        print(
                                            '{:<10} {:<15} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format(
                                                'Reverse', i + 1,
                                                voltage_value_VAR1,
                                                voltage_CONST1,
                                                voltage_CONST2,
                                                current_value_VAR1,
                                                current_value_CONST1,
                                                current_value_CONST2,))
                else:#VAR1+CONST1
                    csv_writer.writerow(
                        ['Direction', 'Step', 'V_VAR1', 'V_CONST1', 'I_VAR1', 'I_CONST1'])
                    with nidcpower.Session(resource_name=VAR1) as session_VAR1:
                        session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT
                        session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE
                        session_VAR1.current_limit = current_limit_VAR1
                        session_VAR1.current_limit_range = current_limit_range_VAR1
                        # 设置VAR1.PLC
                        session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                        session_VAR1.aperture_time = VAR1_PLC

                        # 创建CONST1控制的会话并设置参数
                        with nidcpower.Session(resource_name=CONST1) as session_CONST1:
                            session_CONST1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                            session_CONST1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                            session_CONST1.voltage_level = voltage_CONST1  # 设CONST端的电压
                            session_CONST1.current_limit = current_limit_CONST1
                            session_CONST1.current_limit_range = current_limit_range_CONST1

                            # 设置CONST1.PLC
                            session_CONST1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                            session_CONST1.aperture_time = CONST1_PLC
                            # 启动所有会话
                            session_VAR1.initiate()
                            session_CONST1.initiate()

                            # 计算VAR1步进电压
                            voltage_step_VAR1 = round((voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1),
                                                      8)
                            # 打印表头
                            print('{:<10} {:<15} {:<15} {:<15} {:<15} {:<15}'.format('Direction', 'Step',
                                'V_VAR1', 'V_CONST1', 'I_VAR1', 'I_CONST1'))

                            # 扫描VAR1：逐步设置VAR1电压并测量VAR1的电流
                            for i in range(num_points_VAR1):
                                direction = "Forward"
                                step = i + 1
                                voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                # 执行测量VAR1电流
                                current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)
                                # 执行测量CONST1电流
                                current_value_CONST1 = session_CONST1.measure(nidcpower.MeasurementTypes.CURRENT)
                                measurement_data = create_measurement(
                                    direction=direction,
                                    step=step,
                                    voltage_value_VAR1=voltage_value_VAR1,
                                    current_value_VAR1=current_value_VAR1,
                                    voltage_CONST1=voltage_CONST1,
                                    current_value_CONST1=current_value_CONST1,

                                )
                                send_measurement(measurement_data)
                                # 写入CSV文件
                                csv_writer.writerow(
                                    ['Forward', i + 1, voltage_value_VAR1, voltage_CONST1,
                                     current_value_VAR1,
                                     current_value_CONST1])

                                # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                print(
                                    '{:<10} {:<15} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format(
                                        'Forward', i + 1,
                                        voltage_value_VAR1,
                                        voltage_CONST1,
                                        current_value_VAR1,
                                        current_value_CONST1))
                                # 反向扫描VAR1
                            for i in range(num_points_VAR1 - 1, -1, -1):
                                direction = "Reverse"
                                step = i + 1
                                voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                # 执行测量VAR1电流
                                current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)
                                # 执行测量CONST1电流
                                current_value_CONST1 = session_CONST1.measure(nidcpower.MeasurementTypes.CURRENT)
                                measurement_data = create_measurement(
                                    direction=direction,
                                    step=step,
                                    voltage_value_VAR1=voltage_value_VAR1,
                                    current_value_VAR1=current_value_VAR1,
                                    voltage_CONST1=voltage_CONST1,
                                    current_value_CONST1=current_value_CONST1,

                                )
                                send_measurement(measurement_data)
                                # 写入CSV文件
                                csv_writer.writerow(['Reverse', i + 1, voltage_value_VAR1, voltage_CONST1,
                                                     current_value_VAR1,
                                                     current_value_CONST1])

                                # 打印步数
                                print(
                                    '{:<10} {:<15} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} '.format(
                                        'Reverse', i + 1,
                                        voltage_value_VAR1,
                                        voltage_CONST1,
                                        current_value_VAR1,
                                        current_value_CONST1))
            else:#VAR1
                csv_writer.writerow(['Direction', 'Step', 'V_VAR1', 'I_VAR1'])
                with nidcpower.Session(resource_name=VAR1) as session_VAR1:
                    session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT
                    session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE
                    session_VAR1.current_limit = current_limit_VAR1
                    session_VAR1.current_limit_range = current_limit_range_VAR1
                    # 设置VAR1.PLC
                    session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                    session_VAR1.aperture_time = VAR1_PLC
                    session_VAR1.initiate()
                    # 计算VAR1步进电压
                    voltage_step_VAR1 = round((voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)
                    # 打印表头
                    print('{:<10} {:<15} {:<15} {:<15} '.format('Direction', 'Step', 'V_VAR1', 'I_VAR1'))

                    # 正向扫描VAR1：逐步设置VAR1电压并测量VAR1的电流
                    for i in range(num_points_VAR1):
                        direction = "Forward"
                        step = i + 1
                        voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                        session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                        time.sleep(0.001)  # 暂停0.001秒，等待稳定

                        # 执行测量VAR1电流
                        current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)
                        measurement_data = create_measurement(
                            direction=direction,
                            step=step,
                            voltage_value_VAR1=voltage_value_VAR1,
                            current_value_VAR1=current_value_VAR1,
                        )
                        send_measurement(measurement_data)
                        # 写入CSV文件
                        csv_writer.writerow(['Forward', i + 1, voltage_value_VAR1, current_value_VAR1])

                        # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                        print('{:<10} {:<15} {:<15.15f} {:<15.15f}'.format('Forward', i + 1,
                                                                       voltage_value_VAR1, current_value_VAR1, ))

                    # 反向扫描VAR1
                    for i in range(num_points_VAR1 - 1, -1, -1):
                        direction = "Reverse"
                        step = i + 1

                        voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                        session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                        time.sleep(0.001)  # 暂停0.001秒，等待稳定

                        # 执行测量VAR1电流
                        current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)
                        measurement_data = create_measurement(
                            direction=direction,
                            step=step,
                            voltage_value_VAR1=voltage_value_VAR1,
                            current_value_VAR1=current_value_VAR1,
                        )
                        send_measurement(measurement_data)
                        # 写入CSV文件
                        csv_writer.writerow(['Reverse', i + 1, voltage_value_VAR1, current_value_VAR1])

                        # 打印步数
                        print('{:<10} {:<15} {:<15.15f} {:<15.15f}'.format('Reverse', i + 1, voltage_value_VAR1,
                            current_value_VAR1,))


def choose_sweep_mode(**params):
    VAR1 = params.get('VAR1')
    VAR2 = params.get('VAR2')
    CONST1 = params.get('CONST1')
    CONST2 = params.get('CONST2')
    CONST3 = params.get('CONST3')
    num_points_VAR1 = params.get('num_points_VAR1')
    voltage_min_VAR1 = params.get('voltage_min_VAR1')
    voltage_max_VAR1 = params.get('voltage_max_VAR1')
    current_limit_VAR1 = params.get('current_limit_VAR1')
    current_limit_range_VAR1 = params.get('current_limit_range_VAR1')
    VAR1_PLC = params.get('VAR1_PLC')
    num_points_VAR2 = params.get('num_points_VAR2')
    voltage_min_VAR2 = params.get('voltage_min_VAR2')
    voltage_max_VAR2 = params.get('voltage_max_VAR2')
    current_limit_VAR2 = params.get('current_limit_VAR2')
    current_limit_range_VAR2 = params.get('current_limit_range_VAR2')
    VAR2_PLC = params.get('VAR2_PLC')
    voltage_CONST1 = params.get('voltage_CONST1')
    current_limit_CONST1 = params.get('current_limit_CONST1')
    current_limit_range_CONST1 = params.get('current_limit_range_CONST1')
    CONST1_PLC = params.get('CONST1_PLC')
    voltage_CONST2 = params.get('voltage_CONST2')
    current_limit_CONST2 = params.get('current_limit_CONST2')
    current_limit_range_CONST2 = params.get('current_limit_range_CONST2')
    CONST2_PLC = params.get('CONST2_PLC')
    voltage_CONST3 = params.get('voltage_CONST3')
    current_limit_CONST3 = params.get('current_limit_CONST3')
    current_limit_range_CONST3 = params.get('current_limit_range_CONST3')
    CONST3_PLC = params.get('CONST3_PLC')
    file_name = params.get('file_name')
    file_path = params.get('file_path')
    sweep_mode = params.get('sweep_mode')
    smu_common_list = params.get('smu_common')

    if sweep_mode == 'single':
        smu_selection_test(**params)
        smu_common_mode(smu_common_list)
        IV_Sweep_Single(VAR1, VAR2, CONST1, CONST2, CONST3, num_points_VAR1, voltage_min_VAR1, voltage_max_VAR1, current_limit_range_VAR1,current_limit_range_CONST1,
                    current_limit_range_CONST2, current_limit_range_CONST3, num_points_VAR2, voltage_min_VAR2, voltage_max_VAR2, voltage_CONST1, voltage_CONST2,
                    voltage_CONST3, current_limit_VAR1,current_limit_VAR2, current_limit_range_VAR2, current_limit_CONST1, current_limit_CONST2, current_limit_CONST3,
                    VAR1_PLC, VAR2_PLC, CONST1_PLC, CONST2_PLC, CONST3_PLC, file_name,file_path)

    elif sweep_mode == 'double':
        smu_selection_test(**params)
        smu_common_mode(smu_common_list)
        IV_Sweep_Double(VAR1, VAR2, CONST1, CONST2, CONST3, num_points_VAR1, voltage_min_VAR1, voltage_max_VAR1, current_limit_range_VAR1,current_limit_range_CONST1,
                    current_limit_range_CONST2, current_limit_range_CONST3, num_points_VAR2, voltage_min_VAR2, voltage_max_VAR2, voltage_CONST1, voltage_CONST2,
                    voltage_CONST3, current_limit_VAR1,current_limit_VAR2, current_limit_range_VAR2, current_limit_CONST1, current_limit_CONST2, current_limit_CONST3,
                    VAR1_PLC, VAR2_PLC, CONST1_PLC, CONST2_PLC, CONST3_PLC, file_name,file_path)
    else:
        print("无效的扫描模式选择。")


def create_measurement(
        direction, step,
        voltage_value_VAR1, current_value_VAR1,
        voltage_value_VAR2=None, current_value_VAR2=None,
        voltage_CONST1=None, current_value_CONST1=None,
        voltage_CONST2=None, current_value_CONST2=None,
        voltage_CONST3=None, current_value_CONST3=None,
        include_VAR2=False,
        include_const1=False,
        include_const2=False,
        include_const3=False,
):
    # 初始化字典，确保至少包含 Direction 和 Step
    measurement = {
        'Direction': direction,
        'Step': step,
        'V_VAR1': voltage_value_VAR1,
        'I_VAR1': current_value_VAR1,
    }

    # 根据传入的参数动态添加电压和电流数据
    if include_VAR2 and voltage_value_VAR2 is not None and current_value_VAR2 is not None:
        measurement['V_VAR2'] = voltage_value_VAR2
        measurement['I_VAR2'] = current_value_VAR2
    if include_const1 and voltage_CONST1 is not None and current_value_CONST1 is not None:
        measurement['V_CONST1'] = voltage_CONST1
        measurement['I_CONST1'] = current_value_CONST1
    if include_const2 and voltage_CONST2 is not None and current_value_CONST2 is not None:
        measurement['V_CONST2'] = voltage_CONST2
        measurement['I_CONST2'] = current_value_CONST2
    if include_const3 and voltage_CONST3 is not None and current_value_CONST3 is not None:
        measurement['V_CONST3'] = voltage_CONST3
        measurement['I_CONST3'] = current_value_CONST3

    return measurement

def send_measurement(data):
    value_data = data
    return value_data




