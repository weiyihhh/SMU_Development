import nidcpower
from measurements import MeasurementManager
from smu_config import SmuChannelConfig
from smu_config_get import config_get
import NiDcpower_SelfTest
from setup_smu import setup_smu_channel
from smu_measure import update_measurement
from smu_init import configure_smu
from csv_generate import csv_make
from smu_dict import smu_dict_set
#---------------------------------------constIV测量并记录---------------------------------------------------

#--------------------------------------------完成----------------------------------------------------------
#-------------------------------------在这里写入smu配置字典---------------------------------------------------

#---------------------------------------------完成---------------------------------------------------------


#------------------------------------------完成smu字典参数写入-------------------------------------------------
def smu_test_start(csv_save_path, csv_name, smu1_config_dict=None, smu2_config_dict=None, smu3_config_dict=None, smu4_config_dict=None):
    CSV_SAVE_PATH = csv_save_path
    CSV_NAME = csv_name
    VAR2_flag, CONST1_flag, CONST2_flag, CONST3_flag = 0, 0, 0, 0

    smu_configs = []

    # 直接判断是否传入了字典
    if smu1_config_dict is not None:
        smu_configs.append(smu1_config_dict)
    if smu2_config_dict is not None:
        smu_configs.append(smu2_config_dict)
    if smu3_config_dict is not None:
        smu_configs.append(smu3_config_dict)
    if smu4_config_dict is not None:
        smu_configs.append(smu4_config_dict)

    # 打印或使用 smu_configs 列表进行后续操作
    print(smu_configs)


    # 遍历每个 SMU 配置
    for smu_config in smu_configs:
        smu_channel = SmuChannelConfig(**smu_config)
        # 调用 config_get 函数，传递每个 SMU 配置
        data = config_get(smu_config)
        # 调用封装的函数来配置 SMU
        result = setup_smu_channel(smu_channel, data)
        if result is not None:
            # 获取返回的配置参数
            session = result[0]  # 会话对象
            params = result[1:]  # 其他参数
            # 根据 IV_flag 来分别处理返回的参数
            if data.get("IV_flag") in [1, 2]:
                sweep_mode_VAR1, num_points_VAR1, voltage_step_VAR1, voltage_max_VAR1, voltage_min_VAR1, IV_flag_VAR1 = params
                VAR1_session = session  # 保存会话对象
            elif data.get("IV_flag") in [3, 4]:
                sweep_mode_VAR1, num_points_VAR1, current_step_VAR1, current_max_VAR1, current_min_VAR1, IV_flag_VAR1 = params
                VAR1_session = session  # 保存会话对象
            elif data.get("IV_flag") in [5]:
                mode_VAR2, num_points_VAR2, voltage_step_VAR2, voltage_max_VAR2, voltage_min_VAR2, VAR2_flag = params
                VAR2_session = session  # 保存会话对象
            elif data.get("IV_flag") in [6]:
                mode_VAR2, num_points_VAR2, current_step_VAR2, current_max_VAR2, current_min_VAR2, VAR2_flag = params
                VAR2_session = session  # 保存会话对象
            elif data.get("IV_flag") in [7]:
                mode_CONST1, voltage_CONST1, CONST1_flag = params
                CONST1_session = session  # 保存会话对象
            elif data.get("IV_flag") in [8]:
                mode_CONST1, current_CONST1, CONST1_flag = params
                CONST1_session = session  # 保存会话对象
            elif data.get("IV_flag") in [9]:
                mode_CONST2, voltage_CONST2, CONST2_flag = params
                CONST2_session = session  # 保存会话对象
            elif data.get("IV_flag") in [10]:
                mode_CONST2, current_CONST2, CONST2_flag = params
                CONST2_session = session  # 保存会话对象
            elif data.get("IV_flag") in [11]:
                mode_CONST3, voltage_CONST3, CONST3_flag = params
                CONST3_session = session  # 保存会话对象
            elif data.get("IV_flag") in [12]:
                mode_CONST3, current_CONST3, CONST3_flag = params
                CONST3_session = session  # 保存会话对象
            else:
                print("----------Configure SMU ERROR!----------")
    # -----------------------------------------------完成---------------------------------------------------------
    def const_record(measurement):
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
            ('V_CONST2', voltage_value_CONST2, 'I_CONST2', current_value_CONST2)
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
            ('V_CONST3', voltage_value_CONST3, 'I_CONST3', current_value_CONST3)
        )
        return measurement
    # ------------------------------------------测试运行部分--------------------------------------------------------
    if 1 == VAR2_flag:  # 表明启用VAR2
        if mode_VAR2 == 'V':
            measurement_manager = MeasurementManager()
            for j in range(num_points_VAR2):
                VAR2_session.voltage_level = voltage_min_VAR2 + j * voltage_step_VAR2
                if IV_flag_VAR1 == 1:  # VAR1_V_single
                    for i in range(num_points_VAR1):
                        measurement = {}
                        Direction = "Forward"
                        VAR1_session.voltage_level = voltage_min_VAR1 + i * voltage_step_VAR1
                        # 测量开始
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
                            ('Direction', Direction),
                            ('V_VAR1', VAR1_session.voltage_level, 'I_VAR1', current_value_VAR1),
                            ('V_VAR2', VAR2_session.voltage_level, 'I_VAR2', current_value_VAR2),
                        )
                        measurement = const_record(measurement)
                        # 使用 add_measurement 添加数据
                        measurement_manager.add_measurement(measurement)
                        single_point_measurement = measurement_manager.get_measurements()  # 单点测得数据字典获取
                        # 打印VAR1和CONST的电压和电流值
                        print(
                            f"Direction: 'Forward' ,V_VAR1: {VAR1_session.voltage_level}, I_VAR1: {current_value_VAR1}, V_VAR2: {VAR2_session.voltage_level}, I_VAR2: {current_value_VAR2}, V_CONST1:{single_point_measurement['V_CONST1']},I_CONST1:{single_point_measurement['I_CONST1']},V_CONST2:{single_point_measurement['V_CONST2']},I_CONST2:{single_point_measurement['I_CONST2']},V_CONST3:{single_point_measurement['V_CONST3']},I_CONST3:{single_point_measurement['I_CONST3']}")
                elif IV_flag_VAR1 == 2:  # VAR1_V_double
                    # VAR1正向扫描
                    for i in range(num_points_VAR1):
                        measurement = {}
                        Direction = "Forward"
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
                            ('Direction', Direction),
                            ('V_VAR1', VAR1_session.voltage_level, 'I_VAR1', current_value_VAR1),
                            ('V_VAR2', VAR2_session.voltage_level, 'I_VAR2', current_value_VAR2),
                        )
                        measurement = const_record(measurement)
                        measurement_manager.add_measurement(measurement)
                        single_point_measurement = measurement_manager.get_measurements()  # 单点测得数据字典获取
                        # 打印VAR1和CONST的电压和电流值
                        print(
                            f"Direction: 'Forward' ,V_VAR1: {VAR1_session.voltage_level}, I_VAR1: {current_value_VAR1}, V_VAR2: {VAR2_session.voltage_level}, I_VAR2: {current_value_VAR2}, V_CONST1:{single_point_measurement['V_CONST1']},I_CONST1:{single_point_measurement['I_CONST1']},V_CONST2:{single_point_measurement['V_CONST2']},I_CONST2:{single_point_measurement['I_CONST2']},V_CONST3:{single_point_measurement['V_CONST3']},I_CONST3:{single_point_measurement['I_CONST3']}")
                    # VAR1反向扫描
                    for i in range(num_points_VAR1):
                        measurement = {}
                        Direction = "Reverse"
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
                            ('Direction', Direction),
                            ('V_VAR1', VAR1_session.voltage_level, 'I_VAR1', current_value_VAR1),
                            ('V_VAR2', VAR2_session.voltage_level, 'I_VAR2', current_value_VAR2),
                        )
                        measurement = const_record(measurement)
                        measurement_manager.add_measurement(measurement)
                        single_point_measurement = measurement_manager.get_measurements()  # 单点测得数据字典获取
                        # 打印VAR1和CONST的电压和电流值
                        print(
                            f"Direction: 'Reverse' ,V_VAR1: {VAR1_session.voltage_level}, I_VAR1: {current_value_VAR1}, V_VAR2: {VAR2_session.voltage_level}, I_VAR2: {current_value_VAR2} ,V_CONST1:{single_point_measurement['V_CONST1']},I_CONST1:{single_point_measurement['I_CONST1']},V_CONST2:{single_point_measurement['V_CONST2']},I_CONST2:{single_point_measurement['I_CONST2']},V_CONST3:{single_point_measurement['V_CONST3']},I_CONST3:{single_point_measurement['I_CONST3']}")
                elif IV_flag_VAR1 == 3:  ##VAR1_I_single
                    for i in range(num_points_VAR1):
                        Direction = "Forward"
                        measurement = {}
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
                            ('Direction', Direction),
                            ('V_VAR1', voltage_value_VAR1, 'I_VAR1', VAR1_session.current_level),
                            ('V_VAR2', VAR2_session.voltage_level, 'I_VAR2', current_value_VAR2),
                        )
                        measurement = const_record(measurement)
                        measurement_manager.add_measurement(measurement)
                        single_point_measurement = measurement_manager.get_measurements()  # 单点测得数据字典获取
                        print(
                            f"Direction: 'Forward' ,V_VAR1: {voltage_value_VAR1}, I_VAR1: {VAR1_session.current_level}, V_VAR2: {VAR2_session.voltage_level}, I_VAR2: {current_value_VAR2}, V_CONST1:{single_point_measurement['V_CONST1']},I_CONST1:{single_point_measurement['I_CONST1']},V_CONST2:{single_point_measurement['V_CONST2']},I_CONST2:{single_point_measurement['I_CONST2']},V_CONST3:{single_point_measurement['V_CONST3']},I_CONST3:{single_point_measurement['I_CONST3']}")
                elif IV_flag_VAR1 == 4:  # VAR1_I_double
                    # VAR1正向扫描
                    for i in range(num_points_VAR1):
                        measurement = {}
                        Direction = "Forward"
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
                            ('Direction', Direction),
                            ('V_VAR1', VAR1_session.current_level, 'I_VAR1', voltage_value_VAR1),
                            ('V_VAR2', VAR2_session.voltage_level, 'I_VAR2', current_value_VAR2),
                        )
                        measurement = const_record(measurement)
                        measurement_manager.add_measurement(measurement)
                        single_point_measurement = measurement_manager.get_measurements()  # 单点测得数据字典获取
                        print(
                            f"Direction: 'Forward' ,V_VAR1: {voltage_value_VAR1}, I_VAR1: {VAR1_session.current_level}, V_VAR2: {VAR2_session.voltage_level}, I_VAR2: {current_value_VAR2}, V_CONST1:{single_point_measurement['V_CONST1']},I_CONST1:{single_point_measurement['I_CONST1']},V_CONST2:{single_point_measurement['V_CONST2']},I_CONST2:{single_point_measurement['I_CONST2']},V_CONST3:{single_point_measurement['V_CONST3']},I_CONST3:{single_point_measurement['I_CONST3']}")
                    # VAR1反向扫描
                    for i in range(num_points_VAR1):
                        measurement = {}
                        Direction = "Reverse"
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
                            ('Direction', Direction),
                            ('V_VAR1', VAR1_session.current_level, 'I_VAR1', voltage_value_VAR1),
                            ('V_VAR2', VAR2_session.voltage_level, 'I_VAR2', current_value_VAR2),
                        )
                        measurement = const_record(measurement)
                        measurement_manager.add_measurement(measurement)
                        single_point_measurement = measurement_manager.get_measurements()  # 单点测得数据字典获取
                        print(
                            f"Direction: 'Reverse' ,V_VAR1: {voltage_value_VAR1}, I_VAR1: {VAR1_session.current_level}, V_VAR2: {VAR2_session.voltage_level}, I_VAR2: {current_value_VAR2}, V_CONST1:{single_point_measurement['V_CONST1']},I_CONST1:{single_point_measurement['I_CONST1']},V_CONST2:{single_point_measurement['V_CONST2']},I_CONST2:{single_point_measurement['I_CONST2']},V_CONST3:{single_point_measurement['V_CONST3']},I_CONST3:{single_point_measurement['I_CONST3']}")
            # 获取所有测量数据
            all_measurements = measurement_manager.measurements_data
            csv_make(measurement_manager.measurements_data, CSV_SAVE_PATH, CSV_NAME)
            return all_measurements
            #print(all_measurements)
        elif mode_VAR2 == 'I':
            measurement_manager = MeasurementManager()
            for j in range(num_points_VAR2):
                VAR2_session.current_level = current_min_VAR2 + j * current_step_VAR2
                if IV_flag_VAR1 == 1:
                    for i in range(num_points_VAR1):
                        measurement = {}
                        Direction = "Forward"
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
                            ('Direction', Direction),
                            ('V_VAR1', VAR1_session.voltage_level, 'I_VAR1', current_value_VAR1),
                            ('V_VAR2', voltage_value_VAR2, 'I_VAR2', VAR2_session.current_level),
                        )
                        measurement = const_record(measurement)
                        measurement_manager.add_measurement(measurement)
                        single_point_measurement = measurement_manager.get_measurements()  # 单点测得数据字典获取
                        # 打印VAR1和CONST的电压和电流值
                        print(
                            f"Direction: 'Forward' ,V_VAR1: {VAR1_session.voltage_level}, I_VAR1: {current_value_VAR1}, V_VAR2: {voltage_value_VAR2}, I_VAR2: {VAR2_session.current_level}, V_CONST1:{single_point_measurement['V_CONST1']},I_CONST1:{single_point_measurement['I_CONST1']},V_CONST2:{single_point_measurement['V_CONST2']},I_CONST2:{single_point_measurement['I_CONST2']},V_CONST3:{single_point_measurement['V_CONST3']},I_CONST3:{single_point_measurement['I_CONST3']}")
                elif IV_flag_VAR1 == 2:
                    # VAR1正向扫描
                    for i in range(num_points_VAR1):
                        measurement = {}
                        Direction = "Forward"
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
                            ('Direction', Direction),
                            ('V_VAR1', VAR1_session.voltage_level, 'I_VAR1', current_value_VAR1),
                            ('V_VAR2', voltage_value_VAR2, 'I_VAR2', VAR2_session.current_level),
                        )
                        measurement = const_record(measurement)
                        # 使用 add_measurement 添加数据
                        measurement_manager.add_measurement(measurement)
                        single_point_measurement = measurement_manager.get_measurements()  # 单点测得数据字典获取
                        # 打印VAR1和CONST的电压和电流值
                        print(
                            f"Direction: 'Forward' ,V_VAR1: {VAR1_session.voltage_level}, I_VAR1: {current_value_VAR1}, V_VAR2: {voltage_value_VAR2}, I_VAR2: {VAR2_session.current_level} ,V_CONST1:{single_point_measurement['V_CONST1']},I_CONST1:{single_point_measurement['I_CONST1']},V_CONST2:{single_point_measurement['V_CONST2']},I_CONST2:{single_point_measurement['I_CONST2']},V_CONST3:{single_point_measurement['V_CONST3']},I_CONST3:{single_point_measurement['I_CONST3']}")
                    # VAR1反向扫描
                    for i in range(num_points_VAR1):
                        measurement = {}
                        Direction = "Reverse"
                        VAR1_session.voltage_level = voltage_max_VAR1 - i * voltage_step_VAR1
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
                            ('Direction', Direction),
                            ('V_VAR1', VAR1_session.voltage_level, 'I_VAR1', current_value_VAR1),
                            ('V_VAR2', voltage_value_VAR2, 'I_VAR2', VAR2_session.current_level),
                        )
                        measurement = const_record(measurement)
                        # 使用 add_measurement 添加数据
                        measurement_manager.add_measurement(measurement)
                        single_point_measurement = measurement_manager.get_measurements()  # 单点测得数据字典获取
                        print(single_point_measurement)
                        # 打印VAR1和CONST的电压和电流值
                        print(
                            f"Direction: 'Reverse' ,V_VAR1: {VAR1_session.voltage_level}, I_VAR1: {current_value_VAR1}, V_VAR2: {voltage_value_VAR2}, I_VAR2: {VAR2_session.current_level},V_CONST1:{single_point_measurement['V_CONST1']},I_CONST1:{single_point_measurement['I_CONST1']},V_CONST2:{single_point_measurement['V_CONST2']},I_CONST2:{single_point_measurement['I_CONST2']},V_CONST3:{single_point_measurement['V_CONST3']},I_CONST3:{single_point_measurement['I_CONST3']}")
                elif IV_flag_VAR1 == 3:
                    for i in range(num_points_VAR1):
                        Direction = "Forward"
                        measurement = {}
                        VAR1_session.current_level = current_min_VAR1 + i * current_step_VAR1
                        VAR2_session.initiate()
                        VAR1_session.initiate()
                        # 进行 VAR1 测量
                        voltage_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                        VAR1_session.abort()
                        voltage_value_VAR2 = VAR2_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                        VAR2_session.abort()
                        # 将测量数据添加到字典中
                        measurement = update_measurement(
                            measurement,
                            ('Direction', Direction),
                            ('V_VAR1', voltage_value_VAR1, 'I_VAR1', VAR1_session.current_level),
                            ('V_VAR2', voltage_value_VAR2, 'I_VAR2', VAR2_session.current_level),
                        )
                        measurement = const_record(measurement)
                        # 使用 add_measurement 添加数据
                        measurement_manager.add_measurement(measurement)
                        single_point_measurement = measurement_manager.get_measurements()  # 单点测得数据字典获取
                        print(
                            f"Direction: 'Forward' ,V_VAR1: {voltage_value_VAR1}, I_VAR1: {VAR1_session.current_level}, V_VAR2: {voltage_value_VAR2}, I_VAR2: {VAR2_session.current_level},V_CONST1:{single_point_measurement['V_CONST1']},I_CONST1:{single_point_measurement['I_CONST1']},V_CONST2:{single_point_measurement['V_CONST2']},I_CONST2:{single_point_measurement['I_CONST2']},V_CONST3:{single_point_measurement['V_CONST3']},I_CONST3:{single_point_measurement['I_CONST3']}")
                elif IV_flag_VAR1 == 4:
                    # VAR1正向扫描
                    for i in range(num_points_VAR1):
                        measurement = {}
                        Direction = "Forward"
                        VAR1_session.current_level = current_min_VAR1 + i * current_step_VAR1
                        VAR2_session.initiate()
                        VAR1_session.initiate()
                        # 进行 VAR1 测量
                        voltage_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                        VAR1_session.abort()
                        voltage_value_VAR2 = VAR2_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                        VAR2_session.abort()
                        # 将测量数据添加到字典中
                        measurement = update_measurement(
                            measurement,
                            ('Direction', Direction),
                            ('V_VAR1', voltage_value_VAR1, 'I_VAR1', VAR1_session.current_level),
                            ('V_VAR2', voltage_value_VAR2, 'I_VAR2', VAR2_session.current_level),
                        )
                        measurement = const_record(measurement)
                        # 使用 add_measurement 添加数据
                        measurement_manager.add_measurement(measurement)
                        single_point_measurement = measurement_manager.get_measurements()  # 单点测得数据字典获取
                        print(
                            f"Direction: 'Forward' ,V_VAR1: {voltage_value_VAR1}, I_VAR1: {VAR1_session.current_level}, V_VAR2: {voltage_value_VAR2}, I_VAR2: {VAR2_session.current_level},V_CONST1:{single_point_measurement['V_CONST1']},I_CONST1:{single_point_measurement['I_CONST1']},V_CONST2:{single_point_measurement['V_CONST2']},I_CONST2:{single_point_measurement['I_CONST2']},V_CONST3:{single_point_measurement['V_CONST3']},I_CONST3:{single_point_measurement['I_CONST3']}")
                    # VAR1反向扫描
                    for i in range(num_points_VAR1):
                        measurement = {}
                        Direction = "Reverse"
                        VAR1_session.current_level = current_max_VAR1 - i * current_step_VAR1
                        VAR2_session.initiate()
                        VAR1_session.initiate()
                        voltage_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                        VAR1_session.abort()
                        voltage_value_VAR2 = VAR2_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                        VAR2_session.abort()
                        # 将测量数据添加到字典中
                        measurement = update_measurement(
                            measurement,
                            ('Direction', Direction),
                            ('V_VAR1', voltage_value_VAR1, 'I_VAR1', VAR1_session.current_level),
                            ('V_VAR2', voltage_value_VAR2, 'I_VAR2', VAR2_session.current_level),
                        )
                        measurement = const_record(measurement)
                        # 使用 add_measurement 添加数据
                        measurement_manager.add_measurement(measurement)
                        single_point_measurement = measurement_manager.get_measurements()  # 单点测得数据字典获取
                        print(
                            f"Direction: 'Reverse' ,V_VAR1: {voltage_value_VAR1}, I_VAR1: {VAR1_session.current_level}, V_VAR2: {voltage_value_VAR2}, I_VAR2: {VAR2_session.current_level},V_CONST1:{single_point_measurement['V_CONST1']},I_CONST1:{single_point_measurement['I_CONST1']},V_CONST2:{single_point_measurement['V_CONST2']},I_CONST2:{single_point_measurement['I_CONST2']},V_CONST3:{single_point_measurement['V_CONST3']},I_CONST3:{single_point_measurement['I_CONST3']}")
            all_measurements = measurement_manager.measurements_data
            csv_make(measurement_manager.measurements_data, CSV_SAVE_PATH, CSV_NAME)
            return all_measurements
    elif 0 == VAR2_flag:  # 表明未启用VAR2
        # 示例使用
        measurement_manager = MeasurementManager()
        if IV_flag_VAR1 == 1:
            for i in range(num_points_VAR1):
                Direction = "Forward"
                measurement = {}
                VAR1_session.voltage_level = voltage_min_VAR1 + i * voltage_step_VAR1
                VAR1_session.initiate()
                # 进行 VAR1 测量
                current_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.CURRENT)
                VAR1_session.abort()
                # 将测量数据添加到字典中
                measurement = update_measurement(
                    measurement,
                    ('Direction', Direction),
                    ('V_VAR1', VAR1_session.voltage_level, 'I_VAR1', current_value_VAR1),
                    ('V_VAR2', 0, 'I_VAR2', 0),
                )
                measurement = const_record(measurement)
                # 使用 add_measurement 添加数据
                measurement_manager.add_measurement(measurement)
                single_point_measurement = measurement_manager.get_measurements()  # 单点测得数据字典获取
                # 打印VAR1和CONST的电压和电流值
                print(
                    f"Direction: 'Forward' ,V_VAR1: {VAR1_session.voltage_level}, I_VAR1: {current_value_VAR1}, V_VAR2: 0, I_VAR2: 0,V_CONST1:{single_point_measurement['V_CONST1']},I_CONST1:{single_point_measurement['I_CONST1']},V_CONST2:{single_point_measurement['V_CONST2']},I_CONST2:{single_point_measurement['I_CONST2']},V_CONST3:{single_point_measurement['V_CONST3']},I_CONST3:{single_point_measurement['I_CONST3']}")
            all_measurements = measurement_manager.measurements_data
            csv_make(measurement_manager.measurements_data, CSV_SAVE_PATH,
                     CSV_NAME)
            return all_measurements
        elif IV_flag_VAR1 == 2:
            # VAR1正向扫描
            for i in range(num_points_VAR1):
                Direction = "Forward"
                measurement = {}
                VAR1_session.voltage_level = voltage_min_VAR1 + i * voltage_step_VAR1
                VAR1_session.initiate()
                # 进行 VAR1 测量
                current_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.CURRENT)
                VAR1_session.abort()
                measurement = const_record(measurement)
                # 将测量数据添加到字典中
                measurement = update_measurement(
                    measurement,
                    ('Direction', Direction),
                    ('V_VAR1', VAR1_session.voltage_level, 'I_VAR1', current_value_VAR1),
                    ('V_VAR2', 0, 'I_VAR2', 0),
                )
                # 使用 add_measurement 添加数据
                measurement_manager.add_measurement(measurement)
                single_point_measurement = measurement_manager.get_measurements()  # 单点测得数据字典获取
                # 打印VAR1和CONST的电压和电流值
                print(
                    f"Direction: 'Forward' ,V_VAR1: {VAR1_session.voltage_level}, I_VAR1: {current_value_VAR1}, V_VAR2: 0, I_VAR2: 0,V_CONST1:{single_point_measurement['V_CONST1']},I_CONST1:{single_point_measurement['I_CONST1']},V_CONST2:{single_point_measurement['V_CONST2']},I_CONST2:{single_point_measurement['I_CONST2']},V_CONST3:{single_point_measurement['V_CONST3']},I_CONST3:{single_point_measurement['I_CONST3']}")
            # VAR1反向扫描
            for i in range(num_points_VAR1):
                measurement = {}
                Direction = "Reverse"
                VAR1_session.voltage_level = voltage_max_VAR1 - i * voltage_step_VAR1
                VAR1_session.initiate()
                # 进行 VAR1 测量
                current_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.CURRENT)
                VAR1_session.abort()
                measurement = const_record(measurement)
                # 将测量数据添加到字典中
                measurement = update_measurement(
                    measurement,
                    ('Direction', Direction),
                    ('V_VAR1', VAR1_session.voltage_level, 'I_VAR1', current_value_VAR1),
                    ('V_VAR2', 0, 'I_VAR2', 0),
                )
                # 使用 add_measurement 添加数据
                measurement_manager.add_measurement(measurement)
                single_point_measurement = measurement_manager.get_measurements()  # 单点测得数据字典获取
                # 打印VAR1和CONST的电压和电流值
                print(
                    f"Direction: 'Reverse' ,V_VAR1: {VAR1_session.voltage_level}, I_VAR1: {current_value_VAR1}, V_VAR2: 0, I_VAR2: 0,V_CONST1:{single_point_measurement['V_CONST1']},I_CONST1:{single_point_measurement['I_CONST1']},V_CONST2:{single_point_measurement['V_CONST2']},I_CONST2:{single_point_measurement['I_CONST2']},V_CONST3:{single_point_measurement['V_CONST3']},I_CONST3:{single_point_measurement['I_CONST3']}")
            all_measurements = measurement_manager.measurements_data
            csv_make(measurement_manager.measurements_data, CSV_SAVE_PATH,
                     CSV_NAME)
            return all_measurements
        elif IV_flag_VAR1 == 3:
            for i in range(num_points_VAR1):
                Direction = "Forward"
                measurement = {}
                VAR1_session.current_level = current_min_VAR1 + i * current_step_VAR1
                VAR1_session.initiate()
                # 进行 VAR1 测量
                voltage_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                VAR1_session.abort()
                measurement = const_record(measurement)
                # 将测量数据添加到字典中
                measurement = update_measurement(
                    measurement,
                    ('Direction', Direction),
                    ('V_VAR1', voltage_value_VAR1, 'I_VAR1', VAR1_session.current_level),
                    ('V_VAR2', 0, 'I_VAR2', 0),
                )
                # 使用 add_measurement 添加数据
                measurement_manager.add_measurement(measurement)
                single_point_measurement = measurement_manager.get_measurements()  # 单点测得数据字典获取
                print(
                    f"Direction: 'Forward' ,V_VAR1: {voltage_value_VAR1}, I_VAR1: {VAR1_session.current_level}, V_VAR2: 0, I_VAR2: 0,V_CONST1:{single_point_measurement['V_CONST1']},I_CONST1:{single_point_measurement['I_CONST1']},V_CONST2:{single_point_measurement['V_CONST2']},I_CONST2:{single_point_measurement['I_CONST2']},V_CONST3:{single_point_measurement['V_CONST3']},I_CONST3:{single_point_measurement['I_CONST3']}")
            all_measurements = measurement_manager.measurements_data
            csv_make(measurement_manager.measurements_data, CSV_SAVE_PATH,
                     CSV_NAME)
            return all_measurements
        elif IV_flag_VAR1 == 4:
            # VAR1正向扫描
            for i in range(num_points_VAR1):
                Direction = "Forward"
                measurement = {}
                VAR1_session.current_level = current_min_VAR1 + i * current_step_VAR1
                VAR1_session.initiate()
                # 进行 VAR1 测量
                voltage_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                VAR1_session.abort()
                measurement = const_record(measurement)
                # 将测量数据添加到字典中
                measurement = update_measurement(
                    measurement,
                    ('Direction', Direction),
                    ('V_VAR1', voltage_value_VAR1, 'I_VAR1', VAR1_session.current_level),
                    ('V_VAR2', 0, 'I_VAR2', 0),
                )
                # 使用 add_measurement 添加数据
                measurement_manager.add_measurement(measurement)
                single_point_measurement = measurement_manager.get_measurements()  # 单点测得数据字典获取
                print(
                    f"Direction: 'Forward' ,V_VAR1: {voltage_value_VAR1}, I_VAR1: {VAR1_session.current_level}, V_VAR2: 0, I_VAR2: 0,V_CONST1:{single_point_measurement['V_CONST1']},I_CONST1:{single_point_measurement['I_CONST1']},V_CONST2:{single_point_measurement['V_CONST2']},I_CONST2:{single_point_measurement['I_CONST2']},V_CONST3:{single_point_measurement['V_CONST3']},I_CONST3:{single_point_measurement['I_CONST3']}")
            # VAR1反向扫描
            for i in range(num_points_VAR1):
                measurement = {}
                Direction = "Reverse"
                VAR1_session.current_level = current_max_VAR1 - i * current_step_VAR1
                VAR1_session.initiate()
                voltage_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                VAR1_session.abort()
                measurement = const_record(measurement)
                # 将测量数据添加到字典中
                measurement = update_measurement(
                    measurement,
                    ('Direction', Direction),
                    ('V_VAR1', voltage_value_VAR1, 'I_VAR1', VAR1_session.current_level),
                    ('V_VAR2', 0, 'I_VAR2', 0),
                )
                # 使用 add_measurement 添加数据
                measurement_manager.add_measurement(measurement)
                single_point_measurement = measurement_manager.get_measurements()  # 单点测得数据字典获取
                print(
                    f"Direction: 'Reverse' ,V_VAR1: {voltage_value_VAR1}, I_VAR1: {VAR1_session.current_level}, V_VAR2: 0, I_VAR2: 0,V_CONST1:{single_point_measurement['V_CONST1']},I_CONST1:{single_point_measurement['I_CONST1']},V_CONST2:{single_point_measurement['V_CONST2']},I_CONST2:{single_point_measurement['I_CONST2']},V_CONST3:{single_point_measurement['V_CONST3']},I_CONST3:{single_point_measurement['I_CONST3']}")
            all_measurements = measurement_manager.measurements_data
            csv_make(measurement_manager.measurements_data, CSV_SAVE_PATH,
                     CSV_NAME)
            return all_measurements

