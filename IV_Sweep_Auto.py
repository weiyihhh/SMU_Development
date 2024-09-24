"""
 需要设定Unit、V Name、I Name、Mode（I、V、common）、Function（VAR1、VAR2、CONST）
 4140有四个smu模块
 新增Double模式

"""

import nidcpower
import time
import csv
import tkinter as tk
from tkinter import simpledialog

def configure_smu(session, source_mode, output_function, voltage_level=None, current_limit=None):
    session.source_mode = source_mode
    session.output_function = output_function
    if voltage_level is not None:
        session.voltage_level = voltage_level
    if current_limit is not None:
        session.current_limit = current_limit

def IV_Sweep_Single(VAR1, VAR2, CONST, num_points_VAR1, voltage_min_VAR1, voltage_max_VAR1,
             num_points_VAR2, voltage_min_VAR2, voltage_max_VAR2, voltage_CONST, current_limit_VAR1,current_limit_VAR2, current_limit_CONST,
             VAR1_PLC, VAR2_PLC, CONST_PLC):
    #弹出对话框获取文件名
    root = tk.Tk()
    root.withdraw() #隐藏主窗口

    #请求用户输入文件名
    output_file = simpledialog.askstring("输入文件名", "请输入文件名（不包含扩展名）:")
    if output_file is None:
        print("未输入文件名，程序退出。")
        return

    #添加CSV扩展名
    output_file += '.csv'
    output_path = 'C:/Users/25092/Desktop/Yi.Wei_Data/'

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
                csv_writer.writerow(['Step', 'V_VAR1', 'V_VAR2', 'V_CONST', 'I_VAR1', 'I_VAR2', 'I_CONST'])

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
                        with nidcpower.Session(resource_name=CONST) as session_CONST:
                            session_CONST.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                            session_CONST.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                            session_CONST.voltage_level = voltage_CONST  # 设CONST端的电压
                            session_CONST.current_limit = current_limit_CONST
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
                            print('{:<10} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}'.format('Step', 'V_VAR1', 'V_VAR2',
                                                                                           'V_CONST', 'I_VAR1',
                                                                                           'I_VAR2', 'I_CONST'))

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
                                current_value_CONST = session_CONST.measure(nidcpower.MeasurementTypes.CURRENT)

                                # 写入CSV文件
                                csv_writer.writerow([i + 1, voltage_value_VAR1, voltage_value_VAR2, voltage_CONST,
                                                     current_value_VAR1, current_value_VAR2, current_value_CONST])

                                # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                print('{:<10} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format(
                                    i + 1,
                                    voltage_value_VAR1,
                                    voltage_value_VAR2,
                                    voltage_CONST,
                                    current_value_VAR1,
                                    current_value_VAR2,
                                    current_value_CONST))

        else:
            # 计算VAR2步进电压
            voltage_step_VAR2 = round((voltage_max_VAR2 - voltage_min_VAR2) / (num_points_VAR2 - 1), 8)
            session_VAR2.initiate()

            with open(output_path + output_file, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['Direction', 'Step', 'V_VAR1', 'V_VAR2', 'V_CONST', 'I_VAR1', 'I_VAR2', 'I_CONST'])

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
                        with nidcpower.Session(resource_name=CONST) as session_CONST:
                            session_CONST.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                            session_CONST.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                            session_CONST.voltage_level = voltage_CONST  # 设CONST端的电压
                            session_CONST.current_limit = current_limit_CONST
                            session_CONST.current_limit_autorange = True

                            # 设置CONST.PLC
                            session_CONST.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                            session_CONST.aperture_time = CONST_PLC

                            # 计算VAR1步进电压
                            voltage_step_VAR1 = round((voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)

                            # 启动所有会话
                            session_VAR1.initiate()
                            session_CONST.initiate()

                            # 打印表头
                            print('{:<10} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}'.format('Direction', 'Step',
                                                                                                   'V_VAR1', 'V_VAR2',
                                                                                                   'V_CONST', 'I_VAR1',
                                                                                                   'I_VAR2', 'I_CONST'))

                            #扫描VAR1：逐步设置VAR1电压并测量VAR1、VAR2、CONST的电流
                            for i in range(num_points_VAR1):
                                voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                # 执行测量VAR1电流
                                current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)

                                # 执行测量VAR2电流
                                current_value_VAR2 = session_VAR2.measure(nidcpower.MeasurementTypes.CURRENT)

                                # 执行测量CONST电流
                                current_value_CONST = session_CONST.measure(nidcpower.MeasurementTypes.CURRENT)

                                # 写入CSV文件
                                csv_writer.writerow(['Forward', i + 1, voltage_value_VAR1, voltage_value_VAR2,
                                                     voltage_CONST, current_value_VAR1, current_value_VAR2,
                                                     current_value_CONST])

                                # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                print(
                                    '{:<10} {:<15} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format(
                                        'Forward', i + 1,
                                        voltage_value_VAR1,
                                        voltage_value_VAR2,
                                        voltage_CONST,
                                        current_value_VAR1,
                                        current_value_VAR2,
                                        current_value_CONST))

        print(f"Data saved to {output_path + output_file }")

def IV_Sweep_Double(VAR1, VAR2, CONST, num_points_VAR1, voltage_min_VAR1, voltage_max_VAR1,
                    num_points_VAR2, voltage_min_VAR2, voltage_max_VAR2, voltage_CONST, current_limit_VAR1,current_limit_VAR2,
                    current_limit_CONST, VAR1_PLC, VAR2_PLC, CONST_PLC):
    # 弹出对话框获取文件名
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    # 请求用户输入文件名
    output_file = simpledialog.askstring("输入文件名", "请输入文件名（不包含扩展名）:")
    if output_file is None:
        print("未输入文件名，程序退出。")
        return

    # 添加CSV扩展名
    output_file += '.csv'
    output_path = 'C:/Users/25092/Desktop/Yi.Wei_Data/'

    # 创建VAR2测量的会话并设置参数
    with nidcpower.Session(resource_name=VAR2) as session_VAR2:
        session_VAR2.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
        session_VAR2.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
        session_VAR2.current_limit = current_limit_VAR2  # 设置VAR2端的电流限制
        session_VAR2.current_limit = current_limit_VAR2
        session_VAR2.current_limit_autorange = True

        # 设置VAR2.PLC
        session_VAR2.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
        session_VAR2.aperture_time = VAR2_PLC

        #增添if语句，当VAR2只有一个点时，执行一次double测量
        if voltage_max_VAR2 == voltage_min_VAR2:
            session_VAR2.initiate()

            with open(output_path + output_file, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['Direction', 'Step', 'V_VAR1', 'V_VAR2', 'V_CONST', 'I_VAR1', 'I_VAR2', 'I_CONST'])




                for j in range(num_points_VAR2):

                    #设置VAR端输出参数
                    voltage_value_VAR2 = voltage_min_VAR2
                    session_VAR2.voltage_level = voltage_value_VAR2  # 设置VAR2端的电压输出

                    # 创建VAR1控制的会话并设置参数
                    with nidcpower.Session(resource_name=VAR1) as session_VAR1:
                        session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                        session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                        session_VAR1.current_limit = current_limit_VAR1  # 设置VAR1端的电流限制
                        session_VAR1.current_limit = current_limit_VAR1
                        session_VAR1.current_limit_autorange = True

                        # 设置VAR1.PLC
                        session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                        session_VAR1.aperture_time = VAR1_PLC

                        # 创建CONST控制的会话并设置参数
                        with nidcpower.Session(resource_name=CONST) as session_CONST:
                            session_CONST.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                            session_CONST.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                            session_CONST.voltage_level = voltage_CONST  # 设CONST端的电压
                            session_CONST.current_limit = current_limit_CONST
                            session_CONST.current_limit_autorange = True

                            # 设置CONST.PLC
                            session_CONST.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                            session_CONST.aperture_time = CONST_PLC

                            # 计算VAR1步进电压
                            voltage_step_VAR1 = round((voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)

                            # 启动所有会话
                            session_VAR1.initiate()
                            session_CONST.initiate()

                            # 打印表头
                            print('{:<10} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}'.format('Direction', 'Step', 'V_VAR1',
                                                                                        'V_VAR2', 'V_CONST', 'I_VAR1', 'I_VAR2', 'I_CONST'))

                            # 正向扫描VAR1：逐步设置VAR1电压并测量VAR1、VAR2、CONST的电流
                            for i in range(num_points_VAR1):
                                voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                # 执行测量VAR1电流
                                current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)


                                # 执行测量VAR2电流
                                current_value_VAR2 = session_VAR2.measure(nidcpower.MeasurementTypes.CURRENT)


                                # 执行测量CONST电流
                                current_value_CONST = session_CONST.measure(nidcpower.MeasurementTypes.CURRENT)

                                # 写入CSV文件
                                csv_writer.writerow(['Forward', i + 1, voltage_value_VAR1, voltage_value_VAR2,
                                                    voltage_CONST, current_value_VAR1, current_value_VAR2,
                                                    current_value_CONST])

                                # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                print('{:<10} {:<15} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format(
                                    'Forward', i + 1, voltage_value_VAR1, voltage_value_VAR2, voltage_CONST,
                                        current_value_VAR1, current_value_VAR2, current_value_CONST))

                            # 反向扫描VAR1
                            for i in range(num_points_VAR1 - 1, -1, -1):
                                voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                # 执行测量VAR1电流
                                current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)


                                # 执行测量VAR2电流
                                current_value_VAR2 = session_VAR2.measure(nidcpower.MeasurementTypes.CURRENT)


                                # 执行测量CONST电流
                                current_value_CONST = session_CONST.measure(nidcpower.MeasurementTypes.CURRENT)

                                # 写入CSV文件
                                csv_writer.writerow(['Reverse', i + 1, voltage_value_VAR1, voltage_value_VAR2,
                                                    voltage_CONST, current_value_VAR1, current_value_VAR2,
                                                    current_value_CONST])

                                # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                print('{:<10} {:<15} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format('Reverse',
                                                                                                                i + 1, voltage_value_VAR1,
                                                                                                                voltage_value_VAR2,
                                                                                                                voltage_CONST,
                                                                                                                current_value_VAR1,
                                                                                                                current_value_VAR2,
                                                                                                                current_value_CONST))
        else:

            # 计算VAR2步进电压
            voltage_step_VAR2 = round((voltage_max_VAR2 - voltage_min_VAR2) / (num_points_VAR2 - 1), 8)
            session_VAR2.initiate()

            with open(output_path + output_file, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['Direction', 'Step', 'V_VAR1', 'V_VAR2', 'V_CONST', 'I_VAR1', 'I_VAR2', 'I_CONST'])

                # 正向扫描和反向扫描
                for j in range(num_points_VAR2):
                    # 正向扫描VAR2
                    voltage_value_VAR2 = voltage_min_VAR2 + j * voltage_step_VAR2  # 计算当前步进的VAR2电压值
                    session_VAR2.voltage_level = voltage_value_VAR2  # 设置VAR2端的电压输出

                    # 创建VAR1控制的会话并设置参数
                    with nidcpower.Session(resource_name=VAR1) as session_VAR1:
                        session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                        session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                        session_VAR1.current_limit = current_limit_VAR1  # 设置VAR1端的电流限制
                        session_VAR1.current_limit = current_limit_VAR1
                        session_VAR1.current_limit_autorange = True

                        # 设置VAR1.PLC
                        session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                        session_VAR1.aperture_time = VAR1_PLC

                        # 创建CONST控制的会话并设置参数
                        with nidcpower.Session(resource_name=CONST) as session_CONST:
                            session_CONST.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
                            session_CONST.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                            session_CONST.voltage_level = voltage_CONST  # 设CONST端的电压
                            session_CONST.current_limit = current_limit_CONST
                            session_CONST.current_limit_autorange = True


                            # 设置CONST.PLC
                            session_CONST.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                            session_CONST.aperture_time = CONST_PLC

                            # 计算VAR1步进电压
                            voltage_step_VAR1 = round((voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)

                            # 启动所有会话
                            session_VAR1.initiate()
                            session_CONST.initiate()

                            # 打印表头
                            print('{:<10} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}'.format('Direction', 'Step', 'V_VAR1', 'V_VAR2', 'V_CONST', 'I_VAR1', 'I_VAR2', 'I_CONST'))

                            # 正向扫描VAR1：逐步设置VAR1电压并测量VAR1、VAR2、CONST的电流
                            for i in range(num_points_VAR1):
                                voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                # 执行测量VAR1电流
                                current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)

                                # 执行测量VAR2电流
                                current_value_VAR2 = session_VAR2.measure(nidcpower.MeasurementTypes.CURRENT)

                                # 执行测量CONST电流
                                current_value_CONST = session_CONST.measure(nidcpower.MeasurementTypes.CURRENT)

                                # 写入CSV文件
                                csv_writer.writerow(['Forward', i + 1, voltage_value_VAR1, voltage_value_VAR2,
                                                 voltage_CONST, current_value_VAR1, current_value_VAR2, current_value_CONST])


                                # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                print('{:<10} {:<15} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format('Forward', i + 1,
                                                                                                                voltage_value_VAR1,
                                                                                                                voltage_value_VAR2,
                                                                                                                voltage_CONST,
                                                                                                                current_value_VAR1,
                                                                                                                current_value_VAR2,
                                                                                                                current_value_CONST))

                            # 反向扫描VAR1
                            for i in range(num_points_VAR1 - 1, -1, -1):
                                voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
                                session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
                                time.sleep(0.001)  # 暂停0.001秒，等待稳定

                                # 执行测量VAR1电流
                                current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)

                                # 执行测量VAR2电流
                                current_value_VAR2 = session_VAR2.measure(nidcpower.MeasurementTypes.CURRENT)

                                # 执行测量CONST电流
                                current_value_CONST = session_CONST.measure(nidcpower.MeasurementTypes.CURRENT)

                                # 写入CSV文件
                                csv_writer.writerow(['Reverse', i + 1, voltage_value_VAR1, voltage_value_VAR2,
                                                    voltage_CONST, current_value_VAR1, current_value_VAR2, current_value_CONST])

                                # 打印步数、VAR1、VAR2、CONST电压和IVAR1、IVAR2、CONST电流值
                                print('{:<10} {:<15} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f} {:<15.15f}'.format('Reverse', i + 1,
                                                                                                                voltage_value_VAR1,
                                                                                                                voltage_value_VAR2,
                                                                                                                voltage_CONST,
                                                                                                                current_value_VAR1,
                                                                                                                current_value_VAR2,
                                                                                                                current_value_CONST))

        print(f"Data saved to {output_path + output_file }")

def choose_sweep_mode(sweep_mode, VAR1, VAR2, CONST, num_points_VAR1, voltage_min_VAR1, voltage_max_VAR1,
                      num_points_VAR2, voltage_min_VAR2, voltage_max_VAR2, voltage_CONST, current_limit_VAR1, current_limit_VAR2, current_limit_CONST,
                      VAR1_PLC, VAR2_PLC, CONST_PLC):
    if sweep_mode == 'single':
        IV_Sweep_Single(VAR1, VAR2, CONST, num_points_VAR1, voltage_min_VAR1, voltage_max_VAR1,
                                 num_points_VAR2, voltage_min_VAR2, voltage_max_VAR2, voltage_CONST, current_limit_VAR1, current_limit_VAR2,
                                 current_limit_CONST,
                                 VAR1_PLC, VAR2_PLC, CONST_PLC)
    elif sweep_mode == 'double':
        IV_Sweep_Double(VAR1, VAR2, CONST, num_points_VAR1, voltage_min_VAR1, voltage_max_VAR1,
                                 num_points_VAR2, voltage_min_VAR2, voltage_max_VAR2, voltage_CONST, current_limit_VAR1, current_limit_VAR2,
                                 current_limit_CONST,
                                 VAR1_PLC, VAR2_PLC, CONST_PLC)
    else:
        print("无效的扫描模式选择。")


