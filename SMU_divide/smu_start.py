import nidcpower
from measurements import MeasurementManager
from smu_config import SmuChannelConfig
from smu_config_get import config_get
import NiDcpower_SelfTest
from setup_smu import setup_smu_channel
from smu_measure import update_measurement
from smu_init import configure_smu

#---------------------------------------constIV测量并记录----------------------------------------------
def const_record():
    if CONST1_flag == 1:
        if mode_CONST1 == 'V':
            CONST1_session.initiate()
            voltage_value_CONST1 = voltage_CONST1
            current_value_CONST1 = CONST1_session.measure(nidcpower.MeasurementTypes.CURRENT)
            CONST1_session.abort()
        elif mode_CONST1 == 'I':
            CONST1_session.initiate()
            voltage_value_CONST1 = CONST1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
            current_value_CONST1 = current_CONST1
            CONST1_session.abort()
        else:
            print("CONST1_MODE ERROR")
    else:
        voltage_value_CONST1 = 0
        current_value_CONST1 = 0
    measurement = update_measurement(
        measurement,
        ('V_CONST1', voltage_value_CONST1, 'I_CONST1', current_value_CONST1)
    )
    if CONST2_flag == 1:
        if mode_CONST2 == 'V':
            CONST2_session.initiate()
            voltage_value_CONST2 = voltage_CONST2
            current_value_CONST2 = CONST2_session.measure(nidcpower.MeasurementTypes.CURRENT)
            CONST2_session.abort()
        elif mode_CONST2 == 'I':
            CONST2_session.initiate()
            voltage_value_CONST2 = CONST2_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
            current_value_CONST2 = current_CONST2
            CONST2_session.abort()
        else:
            print("CONST2_MODE ERROR")
    else:
        voltage_value_CONST2 = 0
        current_value_CONST2 = 0
    measurement = update_measurement(
        measurement,
        ('V_CONST2', voltage_value_CONST1, 'I_CONST2', current_value_CONST1)
    )
    if CONST3_flag == 1:
        if mode_CONST3 == 'V':
            CONST3_session.initiate()
            voltage_value_CONST3 = voltage_CONST3
            current_value_CONST3 = CONST3_session.measure(nidcpower.MeasurementTypes.CURRENT)
            CONST3_session.abort()
        elif mode_CONST3 == 'I':
            CONST3_session.initiate()
            voltage_value_CONST3 = CONST3_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
            current_value_CONST3 = current_CONST3
            CONST3_session.abort()
        else:
            print("CONST3_MODE ERROR")
    else:
        voltage_value_CONST3 = 0
        current_value_CONST3 = 0
    measurement = update_measurement(
        measurement,
        ('V_CONST3', voltage_value_CONST1, 'I_CONST3', current_value_CONST1)
    )

#-------------------------------------在这里写入smu配置字典--------------------------------------------
smu1_config_dict = {
    'resource_name': "PXI1Slot3",
    'mode': "V",
    'function': "VAR1",
    'v_name': 'V1',
    'i_name': 'I1',
    'voltage_min_VAR1': 0,
    'voltage_max_VAR1': 5,
    'num_points_VAR1': 10,
    'current_limit_range_VAR1': 0.1,
    'current_limit_VAR1': 0.05,
    'VAR1_PLC': 1,
    'sweep_mode': "single"
}
smu2_config_dict = {
    'resource_name': "PXI1Slot2",
    'mode': "V",
    'function': "VAR2",
    'v_name': 'V2',
    'i_name': 'I2',
    'voltage_min_VAR2': 0,
    'voltage_max_VAR2': 1,
    'num_points_VAR2': 3,
    'current_limit_range_VAR2': 0.1,
    'current_limit_VAR2': 0.05,
    'VAR2_PLC': 1,
}

VAR2_flag, CONST1_flag, CONST2_flag, CONST3_flag = 0
#此处添加smu字典
smu_configs = [smu1_config_dict, smu2_config_dict]

#------------------------------------------完成smu字典参数写入-------------------------------------------------
configure_smu(smu_configs)

#------------------------------------------测试运行部分--------------------------------------------------------
if 1 == VAR2_flag:#表明启用VAR2
    if mode_VAR2 == 'V':
        measurement_manager = MeasurementManager()
        for j in range(num_points_VAR2):
            VAR2_session.voltage_level = voltage_min_VAR2 + j * voltage_step_VAR2
            if IV_flag_VAR1 == 1:  #VAR1_V_single
                for i in range(num_points_VAR1):
                    measurement = {}
                    VAR1_session.voltage_level = voltage_min_VAR1 + i * voltage_step_VAR1
                    #测量开始
                    VAR2_session.initiate()
                    VAR1_session.initiate()
                    # 进行 VAR1 测量
                    current_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.CURRENT)
                    VAR1_session.abort()
                    current_value_VAR2 = VAR2_session.measure(nidcpower.MeasurementTypes.CURRENT)
                    VAR2_session.abort()
                    # 将测量数据添加到字典中
                    measurement = update_measurement(
                        measurement,
                        ('V_VAR1', VAR1_session.voltage_level, 'I_VAR1', current_value_VAR1),
                        ('V_VAR2', VAR2_session.voltage_level, 'I_VAR2', current_value_VAR2),
                    )
                    const_record()
                    # 使用 add_measurement 添加数据
                    measurement_manager.add_measurement(measurement)
                    # 打印VAR1和CONST的电压和电流值
                    print(f"Direction: 'Forward' ,V_VAR1: {VAR1_session.voltage_level}, I_VAR1: {current_value_VAR1}, V_VAR2: {VAR2_session.voltage_level}, I_VAR2: {current_value_VAR2}, V_CONST1:{voltage_value_CONST1},I_CONST1{current_value_CONST1},V_CONST2:{voltage_value_CONST2},I_CONST2{current_value_CONST2},V_CONST3:{voltage_value_CONST3},I_CONST3{current_value_CONST3}")
            elif IV_flag_VAR1 == 2: #VAR1_V_double
                #VAR1正向扫描
                for i in range(num_points_VAR1):
                    VAR1_session.voltage_level = voltage_min_VAR1 + i * voltage_step_VAR1
                    VAR2_session.initiate()
                    VAR1_session.initiate()
                    # 进行 VAR1 测量
                    current_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.CURRENT)
                    VAR1_session.abort()
                    current_value_VAR2 = VAR2_session.measure(nidcpower.MeasurementTypes.CURRENT)
                    VAR2_session.abort()
                    # 将测量数据添加到字典中
                    measurement = update_measurement(
                        measurement,
                        ('V_VAR1', VAR1_session.voltage_level, 'I_VAR1', current_value_VAR1),
                        ('V_VAR2', VAR2_session.voltage_level, 'I_VAR2', current_value_VAR2),
                    )
                    const_record()
                    measurement_manager.add_measurement(measurement)
                    # 打印VAR1和CONST的电压和电流值
                    print(f"Direction: 'Forward' ,V_VAR1: {VAR1_session.voltage_level}, I_VAR1: {current_value_VAR1}, V_VAR2: {VAR2_session.voltage_level}, I_VAR2: {current_value_VAR2}, V_CONST1:{voltage_value_CONST1},I_CONST1{current_value_CONST1},V_CONST2:{voltage_value_CONST2},I_CONST2{current_value_CONST2},V_CONST3:{voltage_value_CONST3},I_CONST3{current_value_CONST3}")
                #VAR1反向扫描
                for i in range(num_points_VAR1):
                    VAR1_session.voltage_level = voltage_max_VAR1 - i * voltage_step_VAR1
                    VAR2_session.initiate()
                    VAR1_session.initiate()
                    # 进行 VAR1 测量
                    current_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.CURRENT)
                    VAR1_session.abort()
                    current_value_VAR2 = VAR2_session.measure(nidcpower.MeasurementTypes.CURRENT)
                    VAR2_session.abort()
                    # 将测量数据添加到字典中
                    measurement = update_measurement(
                        measurement,
                        ('V_VAR1', VAR1_session.voltage_level, 'I_VAR1', current_value_VAR1),
                        ('V_VAR2', VAR2_session.voltage_level, 'I_VAR2', current_value_VAR2),
                    )
                    const_record()
                    measurement_manager.add_measurement(measurement)
                    # 打印VAR1和CONST的电压和电流值
                    print(f"Direction: 'Reverse' ,V_VAR1: {VAR1_session.voltage_level}, I_VAR1: {current_value_VAR1}, V_VAR2: {VAR2_session.voltage_level}, I_VAR2: {current_value_VAR2} ,V_CONST1:{voltage_value_CONST1},I_CONST1{current_value_CONST1},V_CONST2:{voltage_value_CONST2},I_CONST2{current_value_CONST2},V_CONST3:{voltage_value_CONST3},I_CONST3{current_value_CONST3}")
            elif IV_flag_VAR1 == 3:##VAR1_I_single
                for i in range(num_points_VAR1):
                    VAR1_session.current_level = current_min_VAR1 + i * current_step_VAR1
                    VAR2_session.initiate()
                    VAR1_session.initiate()
                    # 进行 VAR1 测量
                    voltage_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                    VAR1_session.abort()
                    current_value_VAR2 = VAR2_session.measure(nidcpower.MeasurementTypes.CURRENT)
                    VAR2_session.abort()
                    # 将测量数据添加到字典中
                    measurement = update_measurement(
                        measurement,
                        ('V_VAR1', voltage_value_VAR1, 'I_VAR1', VAR1_session.current_level),
                        ('V_VAR2', VAR2_session.voltage_level, 'I_VAR2', current_value_VAR2),
                    )
                    const_record()
                    measurement_manager.add_measurement(measurement)
                    print(f"Direction: 'Forward' ,V_VAR1: {voltage_value_VAR1}, I_VAR1: {VAR1_session.current_level}, V_VAR2: {VAR2_session.voltage_level}, I_VAR2: {current_value_VAR2}, V_CONST1:{voltage_value_CONST1},I_CONST1{current_value_CONST1},V_CONST2:{voltage_value_CONST2},I_CONST2{current_value_CONST2},V_CONST3:{voltage_value_CONST3},I_CONST3{current_value_CONST3}")
            elif IV_flag_VAR1 == 4:#VAR1_I_double
                # VAR1正向扫描
                for i in range(num_points_VAR1):
                    VAR1_session.current_level = current_min_VAR1 + i * current_step_VAR1
                    VAR2_session.initiate()
                    VAR1_session.initiate()
                    # 进行 VAR1 测量
                    voltage_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                    VAR1_session.abort()
                    current_value_VAR2 = VAR2_session.measure(nidcpower.MeasurementTypes.CURRENT)
                    VAR2_session.abort()
                    # 将测量数据添加到字典中
                    measurement = update_measurement(
                        measurement,
                        ('V_VAR1', VAR1_session.current_level, 'I_VAR1', voltage_value_VAR1),
                        ('V_VAR2', VAR2_session.voltage_level, 'I_VAR2', current_value_VAR2),
                    )
                    const_record()
                    measurement_manager.add_measurement(measurement)
                    print(f"Direction: 'Forward' ,V_VAR1: {voltage_value_VAR1}, I_VAR1: {VAR1_session.current_level}, V_VAR2: {VAR2_session.voltage_level}, I_VAR2: {current_value_VAR2}, V_CONST1:{voltage_value_CONST1},I_CONST1{current_value_CONST1},V_CONST2:{voltage_value_CONST2},I_CONST2{current_value_CONST2},V_CONST3:{voltage_value_CONST3},I_CONST3{current_value_CONST3}")
                # VAR1反向扫描
                for i in range(num_points_VAR1):
                    VAR1_session.current_level = current_max_VAR1 - i * current_step_VAR1
                    VAR2_session.initiate()
                    VAR1_session.initiate()
                    voltage_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                    VAR1_session.abort()
                    current_value_VAR2 = VAR2_session.measure(nidcpower.MeasurementTypes.CURRENT)
                    VAR2_session.abort()
                    # 将测量数据添加到字典中
                    measurement = update_measurement(
                        measurement,
                        ('V_VAR1', VAR1_session.current_level, 'I_VAR1', voltage_value_VAR1),
                        ('V_VAR2', VAR2_session.voltage_level, 'I_VAR2', current_value_VAR2),
                    )
                    const_record()
                    measurement_manager.add_measurement(measurement)
                    print(f"Direction: 'Reverse' ,V_VAR1: {voltage_value_VAR1}, I_VAR1: {VAR1_session.current_level}, V_VAR2: {VAR2_session.voltage_level}, I_VAR2: {current_value_VAR2}, V_CONST1:{voltage_value_CONST1},I_CONST1{current_value_CONST1},V_CONST2:{voltage_value_CONST2},I_CONST2{current_value_CONST2},V_CONST3:{voltage_value_CONST3},I_CONST3{current_value_CONST3}")
        # 获取所有测量数据
        all_measurements = measurement_manager.get_measurements()
        #print(all_measurements)
    elif mode_VAR2 == 'I':
        measurement_manager = MeasurementManager()
        for j in range(num_points_VAR2):
            VAR2_session.current_level = current_min_VAR2 + j * current_step_VAR2
            if IV_flag_VAR1 == 1:
                for i in range(num_points_VAR1):
                    VAR1_session.voltage_level = voltage_min_VAR1 + i * voltage_step_VAR1
                    VAR2_session.initiate()
                    VAR1_session.initiate()
                    # 进行 VAR1 测量
                    current_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.CURRENT)
                    VAR1_session.abort()
                    voltage_value_VAR2 = VAR2_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                    VAR2_session.abort()
                    # 将测量数据添加到字典中
                    measurement = update_measurement(
                        measurement,
                        ('V_VAR1', VAR1_session.voltage_level, 'I_VAR1', current_value_VAR1),
                        ('V_VAR2', voltage_value_VAR2, 'I_VAR2', VAR2_session.current_level),
                    )
                    const_record()
                    measurement_manager.add_measurement(measurement)
                    # 打印VAR1和CONST的电压和电流值
                    print(f"Direction: 'Forward' ,V_VAR1: {VAR1_session.voltage_level}, I_VAR1: {current_value_VAR1}, V_VAR2: {voltage_value_VAR2}, I_VAR2: {VAR2_session.current_level}, V_CONST1:{voltage_value_CONST1},I_CONST1{current_value_CONST1},V_CONST2:{voltage_value_CONST2},I_CONST2{current_value_CONST2},V_CONST3:{voltage_value_CONST3},I_CONST3{current_value_CONST3}")
            elif IV_flag_VAR1 == 2:
                #VAR1正向扫描
                for i in range(num_points_VAR1):
                    VAR1_session.voltage_level = voltage_min_VAR1 + i * voltage_step_VAR1
                    VAR2_session.initiate()
                    VAR1_session.initiate()
                    # 进行 VAR1 测量
                    current_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.CURRENT)
                    VAR1_session.abort()
                    voltage_value_VAR2 = VAR2_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                    VAR2_session.abort()
                    const_record()
                    # 使用 add_measurement 添加数据
                    measurement_manager.add_measurement(measurement)
                    # 打印VAR1和CONST的电压和电流值
                    print(f"Direction: 'Forward' ,V_VAR1: {VAR1_session.voltage_level}, I_VAR1: {current_value_VAR1}, V_VAR2: {voltage_value_VAR2}, I_VAR2: {VAR2_session.current_level} ,V_CONST1:{voltage_value_CONST1},I_CONST1{current_value_CONST1},V_CONST2:{voltage_value_CONST2},I_CONST2{current_value_CONST2},V_CONST3:{voltage_value_CONST3},I_CONST3{current_value_CONST3}")
                #VAR1反向扫描
                for i in range(num_points_VAR1):
                    VAR1_session.voltage_level = voltage_max_VAR1 - i * voltage_step_VAR1
                    VAR2_session.initiate()
                    VAR1_session.initiate()
                    # 进行 VAR1 测量
                    current_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.CURRENT)
                    VAR1_session.abort()
                    voltage_value_VAR2 = VAR2_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                    VAR2_session.abort()
                    const_record()
                    # 使用 add_measurement 添加数据
                    measurement_manager.add_measurement(measurement)
                    # 打印VAR1和CONST的电压和电流值
                    print(f"Direction: 'Reverse' ,V_VAR1: {VAR1_session.voltage_level}, I_VAR1: {current_value_VAR1}, V_VAR2: {voltage_value_VAR2}, I_VAR2: {VAR2_session.current_level},V_CONST1:{voltage_value_CONST1},I_CONST1{current_value_CONST1},V_CONST2:{voltage_value_CONST2},I_CONST2{current_value_CONST2},V_CONST3:{voltage_value_CONST3},I_CONST3{current_value_CONST3}")
            elif IV_flag_VAR1 == 3:
                for i in range(num_points_VAR1):
                    VAR1_session.current_level = current_min_VAR1 + i * current_step_VAR1
                    VAR2_session.initiate()
                    VAR1_session.initiate()
                    # 进行 VAR1 测量
                    voltage_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                    VAR1_session.abort()
                    voltage_value_VAR2 = VAR2_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                    VAR2_session.abort()
                    const_record()
                    # 使用 add_measurement 添加数据
                    measurement_manager.add_measurement(measurement)
                    print(f"Direction: 'Forward' ,V_VAR1: {voltage_value_VAR1}, I_VAR1: {VAR1_session.current_level}, V_VAR2: {voltage_value_VAR2}, I_VAR2: {VAR2_session.current_level},V_CONST1:{voltage_value_CONST1},I_CONST1{current_value_CONST1},V_CONST2:{voltage_value_CONST2},I_CONST2{current_value_CONST2},V_CONST3:{voltage_value_CONST3},I_CONST3{current_value_CONST3}")
            elif IV_flag_VAR1 == 4:
                # VAR1正向扫描
                for i in range(num_points_VAR1):
                    VAR1_session.current_level = current_min_VAR1 + i * current_step_VAR1
                    VAR2_session.initiate()
                    VAR1_session.initiate()
                    # 进行 VAR1 测量
                    voltage_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                    VAR1_session.abort()
                    voltage_value_VAR2 = VAR2_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                    VAR2_session.abort()
                    const_record()
                    # 使用 add_measurement 添加数据
                    measurement_manager.add_measurement(measurement)
                    print(f"Direction: 'Forward' ,V_VAR1: {voltage_value_VAR1}, I_VAR1: {VAR1_session.current_level}, V_VAR2: {voltage_value_VAR2}, I_VAR2: {VAR2_session.current_level},V_CONST1:{voltage_value_CONST1},I_CONST1{current_value_CONST1},V_CONST2:{voltage_value_CONST2},I_CONST2{current_value_CONST2},V_CONST3:{voltage_value_CONST3},I_CONST3{current_value_CONST3}")
                # VAR1反向扫描
                for i in range(num_points_VAR1):
                    VAR1_session.current_level = current_max_VAR1 - i * current_step_VAR1
                    VAR2_session.initiate()
                    VAR1_session.initiate()
                    voltage_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                    VAR1_session.abort()
                    voltage_value_VAR2 = VAR2_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                    VAR2_session.abort()
                    const_record()
                    # 使用 add_measurement 添加数据
                    measurement_manager.add_measurement(measurement)
                    print(f"Direction: 'Reverse' ,V_VAR1: {voltage_value_VAR1}, I_VAR1: {VAR1_session.current_level}, V_VAR2: {voltage_value_VAR2}, I_VAR2: {VAR2_session.current_level},V_CONST1:{voltage_value_CONST1},I_CONST1{current_value_CONST1},V_CONST2:{voltage_value_CONST2},I_CONST2{current_value_CONST2},V_CONST3:{voltage_value_CONST3},I_CONST3{current_value_CONST3}")
elif 0 == VAR2_flag:#表明未启用VAR2
    # 示例使用
    measurement_manager = MeasurementManager()
    if IV_flag_VAR1 == 1:
        for i in range(num_points_VAR1):
            measurement = {}
            VAR1_session.voltage_level = voltage_min_VAR1 + i * voltage_step_VAR1
            VAR1_session.initiate()
            # 进行 VAR1 测量
            current_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.CURRENT)
            VAR1_session.abort()
            # 将测量数据添加到字典中
            measurement['V_VAR1'] = VAR1_session.voltage_level
            measurement['I_VAR1'] = current_value_VAR1
            measurement['V_VAR2'] = 0  # 固定值，假设为0
            measurement['I_VAR2'] = 0  # 固定值，假设为0
            const_record()
            # 使用 add_measurement 添加数据
            measurement_manager.add_measurement(measurement)
            # 打印VAR1和CONST的电压和电流值
            print(f"Direction: 'Forward' ,V_VAR1: {VAR1_session.voltage_level}, I_VAR1: {current_value_VAR1}, V_VAR2: 0, I_VAR2: 0,V_CONST1:{voltage_value_CONST1},I_CONST1{current_value_CONST1},V_CONST2:{voltage_value_CONST2},I_CONST2{current_value_CONST2},V_CONST3:{voltage_value_CONST3},I_CONST3{current_value_CONST3}")
    elif IV_flag_VAR1 == 2:
        # VAR1正向扫描
        for i in range(num_points_VAR1):
            VAR1_session.voltage_level = voltage_min_VAR1 + i * voltage_step_VAR1
            VAR2_session.initiate()
            VAR1_session.initiate()
            # 进行 VAR1 测量
            current_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.CURRENT)
            VAR1_session.abort()
            current_value_VAR2 = VAR2_session.measure(nidcpower.MeasurementTypes.CURRENT)
            VAR2_session.abort()
            const_record()
            # 使用 add_measurement 添加数据
            measurement_manager.add_measurement(measurement)
            # 打印VAR1和CONST的电压和电流值
            print(f"Direction: 'Forward' ,V_VAR1: {VAR1_session.voltage_level}, I_VAR1: {current_value_VAR1}, V_VAR2: 0, I_VAR2: 0,V_CONST1:{voltage_value_CONST1},I_CONST1{current_value_CONST1},V_CONST2:{voltage_value_CONST2},I_CONST2{current_value_CONST2},V_CONST3:{voltage_value_CONST3},I_CONST3{current_value_CONST3}")
        # VAR1反向扫描
        for i in range(num_points_VAR1):
            VAR1_session.voltage_level = voltage_max_VAR1 - i * voltage_step_VAR1
            VAR2_session.initiate()
            VAR1_session.initiate()
            # 进行 VAR1 测量
            current_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.CURRENT)
            VAR1_session.abort()
            current_value_VAR2 = VAR2_session.measure(nidcpower.MeasurementTypes.CURRENT)
            VAR2_session.abort()
            const_record()
            # 使用 add_measurement 添加数据
            measurement_manager.add_measurement(measurement)
            # 打印VAR1和CONST的电压和电流值
            print(
                f"Direction: 'Reverse' ,V_VAR1: {VAR1_session.voltage_level}, I_VAR1: {current_value_VAR1}, V_VAR2: 0, I_VAR2: 0,V_CONST1:{voltage_value_CONST1},I_CONST1{current_value_CONST1},V_CONST2:{voltage_value_CONST2},I_CONST2{current_value_CONST2},V_CONST3:{voltage_value_CONST3},I_CONST3{current_value_CONST3}")
    elif IV_flag_VAR1 == 3:
        for i in range(num_points_VAR1):
            VAR1_session.current_level = current_min_VAR1 + i * current_step_VAR1
            VAR2_session.initiate()
            VAR1_session.initiate()
            # 进行 VAR1 测量
            voltage_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
            VAR1_session.abort()
            current_value_VAR2 = VAR2_session.measure(nidcpower.MeasurementTypes.CURRENT)
            VAR2_session.abort()
            const_record()
            # 使用 add_measurement 添加数据
            measurement_manager.add_measurement(measurement)
            print(f"Direction: 'Forward' ,V_VAR1: {voltage_value_VAR1}, I_VAR1: {VAR1_session.current_level}, V_VAR2: 0, I_VAR2: 0,V_CONST1:{voltage_value_CONST1},I_CONST1{current_value_CONST1},V_CONST2:{voltage_value_CONST2},I_CONST2{current_value_CONST2},V_CONST3:{voltage_value_CONST3},I_CONST3{current_value_CONST3}")
    elif IV_flag_VAR1 == 4:
        # VAR1正向扫描
        for i in range(num_points_VAR1):
            VAR1_session.current_level = current_min_VAR1 + i * current_step_VAR1
            VAR2_session.initiate()
            VAR1_session.initiate()
            # 进行 VAR1 测量
            voltage_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
            VAR1_session.abort()
            current_value_VAR2 = VAR2_session.measure(nidcpower.MeasurementTypes.CURRENT)
            VAR2_session.abort()
            const_record()
            # 使用 add_measurement 添加数据
            measurement_manager.add_measurement(measurement)
            print(f"Direction: 'Forward' ,V_VAR1: {voltage_value_VAR1}, I_VAR1: {VAR1_session.current_level}, V_VAR2: 0, I_VAR2: 0,V_CONST1:{voltage_value_CONST1},I_CONST1{current_value_CONST1},V_CONST2:{voltage_value_CONST2},I_CONST2{current_value_CONST2},V_CONST3:{voltage_value_CONST3},I_CONST3{current_value_CONST3}")
        # VAR1反向扫描
        for i in range(num_points_VAR1):
            VAR1_session.current_level = current_max_VAR1 - i * current_step_VAR1
            VAR2_session.initiate()
            VAR1_session.initiate()
            voltage_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
            VAR1_session.abort()
            current_value_VAR2 = VAR2_session.measure(nidcpower.MeasurementTypes.CURRENT)
            VAR2_session.abort()
            const_record()
            # 使用 add_measurement 添加数据
            measurement_manager.add_measurement(measurement)
            print(f"Direction: 'Reverse' ,V_VAR1: {voltage_value_VAR1}, I_VAR1: {VAR1_session.current_level}, V_VAR2: 0, I_VAR2: 0,V_CONST1:{voltage_value_CONST1},I_CONST1{current_value_CONST1},V_CONST2:{voltage_value_CONST2},I_CONST2{current_value_CONST2},V_CONST3:{voltage_value_CONST3},I_CONST3{current_value_CONST3}")


