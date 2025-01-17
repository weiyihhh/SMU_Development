import nidcpower
import time
VAR1 = 'PXI1Slot2'
current_limit_VAR1= 0.1
current_limit_range_VAR1=0.1
VAR1_PLC=1
num_points_VAR1= 101
voltage_min_VAR1= 0
voltage_max_VAR1 = 4
voltage_step_VAR1 = round((voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)
with nidcpower.Session(resource_name=VAR1) as session_VAR1:
    session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
    session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出1
    session_VAR1.current_limit = current_limit_VAR1  # 设置VAR1端的电流限制
    session_VAR1.current_limit_range = current_limit_range_VAR1

    # 设置VAR1.PLC
    session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
    session_VAR1.aperture_time = VAR1_PLC

    # 逐步设置VAR1电压并测量VAR1、VAR2、CONST的电流
    for i in range(num_points_VAR1):
        voltage_value_VAR1 = voltage_min_VAR1 + i * voltage_step_VAR1  # 计算当前步进的VAR1电压值
        session_VAR1.voltage_level = voltage_value_VAR1  # 设置VAR1端的电压输出
        session_VAR1.initiate()
        # 执行测量VAR1电流
        current_value_VAR1 = session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)
        print(f"V_VAR1: {voltage_value_VAR1}, I_VAR1: {current_value_VAR1}")
        session_VAR1.abort()
        # 执行测量VAR2电流
        #current_value_VAR2 = session_VAR2.measure(nidcpower.MeasurementTypes.CURRENT)


    for j in range(num_points_VAR2):
        VAR2_session.voltage_level = voltage_min_VAR2 + j * voltage_step_VAR2
        VAR2_session.initiate()
        if sweep_mode_VAR1 == 'single' :
            # 继续判断是V还是I
            if 1 == mode_VAR1:  # 表明是V模式
                smu1_config = smu1.config_data
                voltage_step_VAR1 = smu1_config.get("voltage_step_VAR1", 0)
                #NiDcpower_SelfTest.SelfTest(device_name=smu1.resource_name, max_retries=300, retry_count=0, reset_num=1, selftest_num=10, selfcal_num=0)
                for i in range(smu1.num_points_VAR1):
                    smu1.session_VAR1.voltage_level = smu1.voltage_min_VAR1 + i * voltage_step_VAR1
                    smu1.session_VAR1.initiate()
                    # 进行 VAR1 测量
                    current_value_VAR1 = smu1.session_VAR1.measure(nidcpower.MeasurementTypes.CURRENT)
                    smu1.session_VAR1.abort()
                    current_value_VAR2= smu2.session_VAR2.measure(nidcpower.MeasurementTypes.CURRENT)
                    # 打印VAR1和CONST的电压和电流值
                    print(f"V_VAR1: {smu1.session_VAR1.voltage_level}, I_VAR1: {current_value_VAR1}, V_VAR2: {smu2.session_VAR2.voltage_level}, I_VAR2: {current_value_VAR2}")

            elif 0 == mode_VAR1:  # 标明是I模式
                print("1")
            elif 2 == mode_VAR1:
                print("ERROR: Output function must be constant for the unit_VAR1 in common mode.")

        elif sweep_mode_VAR1 == 'double':
            print("2")
        smu2.session_VAR2.abort()
        print("\n\n\n\n888888888888888888888888888888888888888888888\n\n\n\n\n\n\n\n")