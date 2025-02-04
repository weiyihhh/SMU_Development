
import nidcpower

from smu_config import SmuChannelConfig
from smu_config_get import config_get
import NiDcpower_SelfTest

smu1_config_dict = {
    'resource_name': "PXI1Slot3",
    'mode': "V",
    'function': "VAR1",
    'v_name': 'V1',
    'i_name': 'I1',
    'voltage_min_VAR1': 0.0,
    'voltage_max_VAR1': 0.9,
    'num_points_VAR1': 101,
    'current_limit_range_VAR1': 0.1,
    'current_limit_VAR1': 0.05,
    'VAR1_PLC': 0,
    'sweep_mode': "single"
}

smu2_config_dict = {
    "resource_name": "PXI1Slot2",
    "mode": "V",
    "function": "VAR2",
    "v_name": "V2",
    "i_name": "I2",
    "voltage_min_VAR2": 0.0,
    "voltage_max_VAR2": 3,
    "num_points_VAR2": 3,
    "VAR2_PLC": 0,
    "current_limit_range_VAR2": 0.1,  # 设置 VAR2 的电流限制范围
    "current_limit_VAR2": 0.05,  # 设置 VAR2 的电流限制
}
VAR2_flag = 0
# 配置字典列表
smu_configs = [smu1_config_dict, smu2_config_dict]

# 遍历每个 SMU 配置
for smu_config in smu_configs:
    smu_channel = SmuChannelConfig(**smu_config)
    # 调用 config_get 函数，传递每个 SMU 配置
    data = config_get(smu_config)
    if  data.get("IV_flag") == 1 :
        sweep_mode_VAR1 = 'single'
        num_points_VAR1 = data.get("points")
        voltage_step_VAR1 = data.get("step")
        voltage_max_VAR1 = data.get("voltage_max_VAR1")
        voltage_min_VAR1 = data.get("voltage_min_VAR1")
        VAR1_session = smu_channel.create_session()
        IV_flag = 1
    elif data.get("IV_flag") == 2:
        sweep_mode_VAR1 = 'double'
        num_points_VAR1 = data.get("points")
        voltage_step_VAR1 = data.get("step")
        voltage_max_VAR1 = data.get("voltage_max_VAR1")
        voltage_min_VAR1 = data.get("voltage_min_VAR1")
        VAR1_session = smu_channel.create_session()
        IV_flag = 2
    elif data.get("IV_flag") == 3:
        sweep_mode_VAR1 = 'single'
        num_points_VAR1 = data.get("points")
        current_step_VAR1 = data.get("step")
        current_max_VAR1 = data.get("current_max_VAR1")
        current_min_VAR1 = data.get("current_min_VAR1")
        VAR1_session = smu_channel.create_session()
        IV_flag = 3
    elif data.get("IV_flag") == 4:
        sweep_mode_VAR1 = 'double'
        num_points_VAR1 = data.get("points")
        current_step_VAR1 = data.get("step")
        current_max_VAR1 = data.get("current_max_VAR1")
        current_min_VAR1 = data.get("current_min_VAR1")
        VAR1_session = smu_channel.create_session()
        IV_flag = 4
    elif data.get("IV_flag") == 5:
        mode_VAR2 = 'V'
        num_points_VAR2 = data.get("points")
        voltage_step_VAR2 = data.get("step")
        voltage_max_VAR2 = data.get("voltage_max_VAR2")
        voltage_min_VAR2 = data.get("voltage_min_VAR2")
        VAR2_session = smu_channel.create_session()
        VAR2_flag = 1
    elif data.get("IV_flag") == 6:
        mode_VAR2 = 'I'
        num_points_VAR2 = data.get("points")
        current_step_VAR2 = data.get("step")
        current_max_VAR2 = data.get("current_max_VAR2")
        current_min_VAR2 = data.get("current_min_VAR2")
        VAR2_session = smu_channel.create_session()
        VAR2_flag = 1
    elif data.get("IV_flag") == 7:
        mode_CONST1 = 'V'
        CONST1_flag = 1
        voltage_CONST1 = data.get("voltage_CONST1")
        CONST1_session = smu_channel.create_session()
    elif data.get("IV_flag") == 8:
        mode_CONST1 = 'I'
        CONST1_flag = 1
        current_CONST1 = data.get("current_CONST1")
        CONST1_session = smu_channel.create_session()
    elif data.get("IV_flag") == 9:
        mode_CONST2 = 'V'
        CONST2_flag = 1
        voltage_CONST2 = data.get("voltage_CONST2")
        CONST2_session = smu_channel.create_session()
    elif data.get("IV_flag") == 10:
        mode_CONST2 = 'I'
        CONST2_flag = 1
        current_CONST2 = data.get("current_CONST2")
        CONST2_session = smu_channel.create_session()
    elif data.get("IV_flag") == 11:
        mode_CONST3 = 'V'
        CONST3_flag = 1
        voltage_CONST3 = data.get("voltage_CONST3")
        CONST3_session = smu_channel.create_session()
    elif data.get("IV_flag") == 12:
        mode_CONST3 = 'I'
        CONST3_flag = 1
        current_CONST3 = data.get("current_CONST3")
        CONST3_session = smu_channel.create_session()

if 1 == VAR2_flag:#表明启用VAR2
    if mode_VAR2 == 'V':
        for j in range(num_points_VAR2):
            VAR2_session.voltage_level = voltage_min_VAR2 + j * voltage_step_VAR2
            if IV_flag == 1:
                for i in range(num_points_VAR1):
                    VAR1_session.voltage_level = voltage_min_VAR1 + i * voltage_step_VAR1
                    VAR2_session.initiate()
                    VAR1_session.initiate()
                    # 进行 VAR1 测量
                    current_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.CURRENT)
                    VAR1_session.abort()
                    current_value_VAR2 = VAR2_session.measure(nidcpower.MeasurementTypes.CURRENT)
                    VAR2_session.abort()
                    if CONST1_flag ==1:
                        if mode_CONST1 == 'V':
                            CONST1_session.initiate()
                            voltage_value_CONST1 = voltage_CONST1
                            current_value_CONST1 = CONST1_session.measure(nidcpower.MeasurementTypes.CURRENT)
                            CONST1_session.abort()
                        elif mode_CONST1== 'I':
                            CONST1_session.initiate()
                            voltage_value_CONST1 = CONST1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                            current_value_CONST1 = current_CONST1
                            CONST1_session.abort()
                        else:
                            pass
                    else:
                        pass
                    if CONST2_flag ==1:
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
                            pass
                    else:
                        pass
                    if CONST3_flag ==1:
                        if mode_CONST3 == 'V':
                            CONST3_session.initiate()
                            voltage_value_CONST3 = voltage_CONST3
                            current_value_CONST3 = CONST3_session.measure(nidcpower.MeasurementTypes.CURRENT)
                            CONST3_session.abort()
                        elif mode_CONST3== 'I':
                            CONST3_session.initiate()
                            voltage_value_CONST3 = CONST3_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                            current_value_CONST3 = current_CONST3
                            CONST3_session.abort()
                        else:
                            pass
                    else:
                        pass
                    # 打印VAR1和CONST的电压和电流值
                    print(f"Direction: 'Forward' ,V_VAR1: {VAR1_session.voltage_level}, I_VAR1: {current_value_VAR1}, V_VAR2: {VAR2_session.voltage_level}, I_VAR2: {current_value_VAR2}, V_CONST1:{voltage_value_CONST1},I_CONST1{current_value_CONST1},V_CONST2:{voltage_value_CONST2},I_CONST2{current_value_CONST2},V_CONST3:{voltage_value_CONST3},I_CONST3{current_value_CONST3}")
            elif IV_flag == 2:
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
                    if CONST1_flag ==1:
                        if mode_CONST1 == 'V':
                            CONST1_session.initiate()
                            voltage_value_CONST1 = voltage_CONST1
                            current_value_CONST1 = CONST1_session.measure(nidcpower.MeasurementTypes.CURRENT)
                            CONST1_session.abort()
                        elif mode_CONST1== 'I':
                            CONST1_session.initiate()
                            voltage_value_CONST1 = CONST1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                            current_value_CONST1 = current_CONST1
                            CONST1_session.abort()
                        else:
                            pass
                    else:
                        pass
                    if CONST2_flag ==1:
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
                            pass
                    else:
                        pass
                    if CONST3_flag ==1:
                        if mode_CONST3 == 'V':
                            CONST3_session.initiate()
                            voltage_value_CONST3 = voltage_CONST3
                            current_value_CONST3 = CONST3_session.measure(nidcpower.MeasurementTypes.CURRENT)
                            CONST3_session.abort()
                        elif mode_CONST3== 'I':
                            CONST3_session.initiate()
                            voltage_value_CONST3 = CONST3_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                            current_value_CONST3 = current_CONST3
                            CONST3_session.abort()
                        else:
                            pass
                    else:
                        pass
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
                    if CONST1_flag ==1:
                        if mode_CONST1 == 'V':
                            CONST1_session.initiate()
                            voltage_value_CONST1 = voltage_CONST1
                            current_value_CONST1 = CONST1_session.measure(nidcpower.MeasurementTypes.CURRENT)
                            CONST1_session.abort()
                        elif mode_CONST1== 'I':
                            CONST1_session.initiate()
                            voltage_value_CONST1 = CONST1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                            current_value_CONST1 = current_CONST1
                            CONST1_session.abort()
                        else:
                            pass
                    else:
                        pass
                    if CONST2_flag ==1:
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
                            pass
                    else:
                        pass
                    if CONST3_flag ==1:
                        if mode_CONST3 == 'V':
                            CONST3_session.initiate()
                            voltage_value_CONST3 = voltage_CONST3
                            current_value_CONST3 = CONST3_session.measure(nidcpower.MeasurementTypes.CURRENT)
                            CONST3_session.abort()
                        elif mode_CONST3== 'I':
                            CONST3_session.initiate()
                            voltage_value_CONST3 = CONST3_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                            current_value_CONST3 = current_CONST3
                            CONST3_session.abort()
                        else:
                            pass
                    else:
                        pass
                    # 打印VAR1和CONST的电压和电流值
                    print(f"Direction: 'Reverse' ,V_VAR1: {VAR1_session.voltage_level}, I_VAR1: {current_value_VAR1}, V_VAR2: {VAR2_session.voltage_level}, I_VAR2: {current_value_VAR2} ,V_CONST1:{voltage_value_CONST1},I_CONST1{current_value_CONST1},V_CONST2:{voltage_value_CONST2},I_CONST2{current_value_CONST2},V_CONST3:{voltage_value_CONST3},I_CONST3{current_value_CONST3}")
            elif IV_flag == 3:
                for i in range(num_points_VAR1):
                    VAR1_session.current_level = current_min_VAR1 + i * current_step_VAR1
                    VAR2_session.initiate()
                    VAR1_session.initiate()
                    # 进行 VAR1 测量
                    voltage_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                    VAR1_session.abort()
                    current_value_VAR2 = VAR2_session.measure(nidcpower.MeasurementTypes.CURRENT)
                    VAR2_session.abort()
                    if CONST1_flag ==1:
                        if mode_CONST1 == 'V':
                            CONST1_session.initiate()
                            voltage_value_CONST1 = voltage_CONST1
                            current_value_CONST1 = CONST1_session.measure(nidcpower.MeasurementTypes.CURRENT)
                            CONST1_session.abort()
                        elif mode_CONST1== 'I':
                            CONST1_session.initiate()
                            voltage_value_CONST1 = CONST1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                            current_value_CONST1 = current_CONST1
                            CONST1_session.abort()
                        else:
                            pass
                    else:
                        pass
                    if CONST2_flag ==1:
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
                            pass
                    else:
                        pass
                    if CONST3_flag ==1:
                        if mode_CONST3 == 'V':
                            CONST3_session.initiate()
                            voltage_value_CONST3 = voltage_CONST3
                            current_value_CONST3 = CONST3_session.measure(nidcpower.MeasurementTypes.CURRENT)
                            CONST3_session.abort()
                        elif mode_CONST3== 'I':
                            CONST3_session.initiate()
                            voltage_value_CONST3 = CONST3_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                            current_value_CONST3 = current_CONST3
                            CONST3_session.abort()
                        else:
                            pass
                    else:
                        pass
                    print(f"Direction: 'Forward' ,V_VAR1: {voltage_value_VAR1}, I_VAR1: {VAR1_session.current_level}, V_VAR2: {VAR2_session.voltage_level}, I_VAR2: {current_value_VAR2}, V_CONST1:{voltage_value_CONST1},I_CONST1{current_value_CONST1},V_CONST2:{voltage_value_CONST2},I_CONST2{current_value_CONST2},V_CONST3:{voltage_value_CONST3},I_CONST3{current_value_CONST3}")
            elif IV_flag == 4:
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
                    if CONST1_flag ==1:
                        if mode_CONST1 == 'V':
                            CONST1_session.initiate()
                            voltage_value_CONST1 = voltage_CONST1
                            current_value_CONST1 = CONST1_session.measure(nidcpower.MeasurementTypes.CURRENT)
                            CONST1_session.abort()
                        elif mode_CONST1== 'I':
                            CONST1_session.initiate()
                            voltage_value_CONST1 = CONST1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                            current_value_CONST1 = current_CONST1
                            CONST1_session.abort()
                        else:
                            pass
                    else:
                        pass
                    if CONST2_flag ==1:
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
                            pass
                    else:
                        pass
                    if CONST3_flag ==1:
                        if mode_CONST3 == 'V':
                            CONST3_session.initiate()
                            voltage_value_CONST3 = voltage_CONST3
                            current_value_CONST3 = CONST3_session.measure(nidcpower.MeasurementTypes.CURRENT)
                            CONST3_session.abort()
                        elif mode_CONST3== 'I':
                            CONST3_session.initiate()
                            voltage_value_CONST3 = CONST3_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                            current_value_CONST3 = current_CONST3
                            CONST3_session.abort()
                        else:
                            pass
                    else:
                        pass
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
                    if CONST1_flag ==1:
                        if mode_CONST1 == 'V':
                            CONST1_session.initiate()
                            voltage_value_CONST1 = voltage_CONST1
                            current_value_CONST1 = CONST1_session.measure(nidcpower.MeasurementTypes.CURRENT)
                            CONST1_session.abort()
                        elif mode_CONST1== 'I':
                            CONST1_session.initiate()
                            voltage_value_CONST1 = CONST1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                            current_value_CONST1 = current_CONST1
                            CONST1_session.abort()
                        else:
                            pass
                    else:
                        pass
                    if CONST2_flag ==1:
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
                            pass
                    else:
                        pass
                    if CONST3_flag ==1:
                        if mode_CONST3 == 'V':
                            CONST3_session.initiate()
                            voltage_value_CONST3 = voltage_CONST3
                            current_value_CONST3 = CONST3_session.measure(nidcpower.MeasurementTypes.CURRENT)
                            CONST3_session.abort()
                        elif mode_CONST3== 'I':
                            CONST3_session.initiate()
                            voltage_value_CONST3 = CONST3_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                            current_value_CONST3 = current_CONST3
                            CONST3_session.abort()
                        else:
                            pass
                    else:
                        pass
                    print(f"Direction: 'Reverse' ,V_VAR1: {voltage_value_VAR1}, I_VAR1: {VAR1_session.current_level}, V_VAR2: {VAR2_session.voltage_level}, I_VAR2: {current_value_VAR2}, V_CONST1:{voltage_value_CONST1},I_CONST1{current_value_CONST1},V_CONST2:{voltage_value_CONST2},I_CONST2{current_value_CONST2},V_CONST3:{voltage_value_CONST3},I_CONST3{current_value_CONST3}")
    elif mode_VAR2 == 'I':
        for j in range(num_points_VAR2):
            VAR2_session.current_level = current_min_VAR2 + j * current_step_VAR2
            if IV_flag == 1:
                for i in range(num_points_VAR1):
                    VAR1_session.voltage_level = voltage_min_VAR1 + i * voltage_step_VAR1
                    VAR2_session.initiate()
                    VAR1_session.initiate()
                    # 进行 VAR1 测量
                    current_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.CURRENT)
                    VAR1_session.abort()
                    voltage_value_VAR2 = VAR2_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                    VAR2_session.abort()
                    if CONST1_flag ==1:
                        if mode_CONST1 == 'V':
                            CONST1_session.initiate()
                            voltage_value_CONST1 = voltage_CONST1
                            current_value_CONST1 = CONST1_session.measure(nidcpower.MeasurementTypes.CURRENT)
                            CONST1_session.abort()
                        elif mode_CONST1== 'I':
                            CONST1_session.initiate()
                            voltage_value_CONST1 = CONST1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                            current_value_CONST1 = current_CONST1
                            CONST1_session.abort()
                        else:
                            pass
                    else:
                        pass
                    if CONST2_flag ==1:
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
                            pass
                    else:
                        pass
                    if CONST3_flag ==1:
                        if mode_CONST3 == 'V':
                            CONST3_session.initiate()
                            voltage_value_CONST3 = voltage_CONST3
                            current_value_CONST3 = CONST3_session.measure(nidcpower.MeasurementTypes.CURRENT)
                            CONST3_session.abort()
                        elif mode_CONST3== 'I':
                            CONST3_session.initiate()
                            voltage_value_CONST3 = CONST3_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                            current_value_CONST3 = current_CONST3
                            CONST3_session.abort()
                        else:
                            pass
                    else:
                        pass
                    # 打印VAR1和CONST的电压和电流值
                    print(f"Direction: 'Forward' ,V_VAR1: {VAR1_session.voltage_level}, I_VAR1: {current_value_VAR1}, V_VAR2: {voltage_value_VAR2}, I_VAR2: {VAR2_session.current_level}, V_CONST1:{voltage_value_CONST1},I_CONST1{current_value_CONST1},V_CONST2:{voltage_value_CONST2},I_CONST2{current_value_CONST2},V_CONST3:{voltage_value_CONST3},I_CONST3{current_value_CONST3}")
            elif IV_flag == 2:
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
                    if CONST1_flag ==1:
                        if mode_CONST1 == 'V':
                            CONST1_session.initiate()
                            voltage_value_CONST1 = voltage_CONST1
                            current_value_CONST1 = CONST1_session.measure(nidcpower.MeasurementTypes.CURRENT)
                            CONST1_session.abort()
                        elif mode_CONST1== 'I':
                            CONST1_session.initiate()
                            voltage_value_CONST1 = CONST1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                            current_value_CONST1 = current_CONST1
                            CONST1_session.abort()
                        else:
                            pass
                    else:
                        pass
                    if CONST2_flag ==1:
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
                            pass
                    else:
                        pass
                    if CONST3_flag ==1:
                        if mode_CONST3 == 'V':
                            CONST3_session.initiate()
                            voltage_value_CONST3 = voltage_CONST3
                            current_value_CONST3 = CONST3_session.measure(nidcpower.MeasurementTypes.CURRENT)
                            CONST3_session.abort()
                        elif mode_CONST3== 'I':
                            CONST3_session.initiate()
                            voltage_value_CONST3 = CONST3_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                            current_value_CONST3 = current_CONST3
                            CONST3_session.abort()
                        else:
                            pass
                    else:
                        pass
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
                    if CONST1_flag ==1:
                        if mode_CONST1 == 'V':
                            CONST1_session.initiate()
                            voltage_value_CONST1 = voltage_CONST1
                            current_value_CONST1 = CONST1_session.measure(nidcpower.MeasurementTypes.CURRENT)
                            CONST1_session.abort()
                        elif mode_CONST1== 'I':
                            CONST1_session.initiate()
                            voltage_value_CONST1 = CONST1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                            current_value_CONST1 = current_CONST1
                            CONST1_session.abort()
                        else:
                            pass
                    else:
                        pass
                    if CONST2_flag ==1:
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
                            pass
                    else:
                        pass
                    if CONST3_flag ==1:
                        if mode_CONST3 == 'V':
                            CONST3_session.initiate()
                            voltage_value_CONST3 = voltage_CONST3
                            current_value_CONST3 = CONST3_session.measure(nidcpower.MeasurementTypes.CURRENT)
                            CONST3_session.abort()
                        elif mode_CONST3== 'I':
                            CONST3_session.initiate()
                            voltage_value_CONST3 = CONST3_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                            current_value_CONST3 = current_CONST3
                            CONST3_session.abort()
                        else:
                            pass
                    else:
                        pass
                    # 打印VAR1和CONST的电压和电流值
                    print(f"Direction: 'Reverse' ,V_VAR1: {VAR1_session.voltage_level}, I_VAR1: {current_value_VAR1}, V_VAR2: {voltage_value_VAR2}, I_VAR2: {VAR2_session.current_level},V_CONST1:{voltage_value_CONST1},I_CONST1{current_value_CONST1},V_CONST2:{voltage_value_CONST2},I_CONST2{current_value_CONST2},V_CONST3:{voltage_value_CONST3},I_CONST3{current_value_CONST3}")
            elif IV_flag == 3:
                for i in range(num_points_VAR1):
                    VAR1_session.current_level = current_min_VAR1 + i * current_step_VAR1
                    VAR2_session.initiate()
                    VAR1_session.initiate()
                    # 进行 VAR1 测量
                    voltage_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                    VAR1_session.abort()
                    voltage_value_VAR2 = VAR2_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                    VAR2_session.abort()
                    if CONST1_flag ==1:
                        if mode_CONST1 == 'V':
                            CONST1_session.initiate()
                            voltage_value_CONST1 = voltage_CONST1
                            current_value_CONST1 = CONST1_session.measure(nidcpower.MeasurementTypes.CURRENT)
                            CONST1_session.abort()
                        elif mode_CONST1== 'I':
                            CONST1_session.initiate()
                            voltage_value_CONST1 = CONST1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                            current_value_CONST1 = current_CONST1
                            CONST1_session.abort()
                        else:
                            pass
                    else:
                        pass
                    if CONST2_flag ==1:
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
                            pass
                    else:
                        pass
                    if CONST3_flag ==1:
                        if mode_CONST3 == 'V':
                            CONST3_session.initiate()
                            voltage_value_CONST3 = voltage_CONST3
                            current_value_CONST3 = CONST3_session.measure(nidcpower.MeasurementTypes.CURRENT)
                            CONST3_session.abort()
                        elif mode_CONST3== 'I':
                            CONST3_session.initiate()
                            voltage_value_CONST3 = CONST3_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                            current_value_CONST3 = current_CONST3
                            CONST3_session.abort()
                        else:
                            pass
                    else:
                        pass
                    print(f"Direction: 'Forward' ,V_VAR1: {voltage_value_VAR1}, I_VAR1: {VAR1_session.current_level}, V_VAR2: {voltage_value_VAR2}, I_VAR2: {VAR2_session.current_level},V_CONST1:{voltage_value_CONST1},I_CONST1{current_value_CONST1},V_CONST2:{voltage_value_CONST2},I_CONST2{current_value_CONST2},V_CONST3:{voltage_value_CONST3},I_CONST3{current_value_CONST3}")
            elif IV_flag == 4:
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
                    if CONST1_flag ==1:
                        if mode_CONST1 == 'V':
                            CONST1_session.initiate()
                            voltage_value_CONST1 = voltage_CONST1
                            current_value_CONST1 = CONST1_session.measure(nidcpower.MeasurementTypes.CURRENT)
                            CONST1_session.abort()
                        elif mode_CONST1== 'I':
                            CONST1_session.initiate()
                            voltage_value_CONST1 = CONST1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                            current_value_CONST1 = current_CONST1
                            CONST1_session.abort()
                        else:
                            pass
                    else:
                        pass
                    if CONST2_flag ==1:
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
                            pass
                    else:
                        pass
                    if CONST3_flag ==1:
                        if mode_CONST3 == 'V':
                            CONST3_session.initiate()
                            voltage_value_CONST3 = voltage_CONST3
                            current_value_CONST3 = CONST3_session.measure(nidcpower.MeasurementTypes.CURRENT)
                            CONST3_session.abort()
                        elif mode_CONST3== 'I':
                            CONST3_session.initiate()
                            voltage_value_CONST3 = CONST3_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                            current_value_CONST3 = current_CONST3
                            CONST3_session.abort()
                        else:
                            pass
                    else:
                        pass
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
                    if CONST1_flag ==1:
                        if mode_CONST1 == 'V':
                            CONST1_session.initiate()
                            voltage_value_CONST1 = voltage_CONST1
                            current_value_CONST1 = CONST1_session.measure(nidcpower.MeasurementTypes.CURRENT)
                            CONST1_session.abort()
                        elif mode_CONST1== 'I':
                            CONST1_session.initiate()
                            voltage_value_CONST1 = CONST1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                            current_value_CONST1 = current_CONST1
                            CONST1_session.abort()
                        else:
                            pass
                    else:
                        pass
                    if CONST2_flag ==1:
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
                            pass
                    else:
                        pass
                    if CONST3_flag ==1:
                        if mode_CONST3 == 'V':
                            CONST3_session.initiate()
                            voltage_value_CONST3 = voltage_CONST3
                            current_value_CONST3 = CONST3_session.measure(nidcpower.MeasurementTypes.CURRENT)
                            CONST3_session.abort()
                        elif mode_CONST3== 'I':
                            CONST3_session.initiate()
                            voltage_value_CONST3 = CONST3_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
                            current_value_CONST3 = current_CONST3
                            CONST3_session.abort()
                        else:
                            pass
                    else:
                        pass
                    print(f"Direction: 'Reverse' ,V_VAR1: {voltage_value_VAR1}, I_VAR1: {VAR1_session.current_level}, V_VAR2: {voltage_value_VAR2}, I_VAR2: {VAR2_session.current_level},V_CONST1:{voltage_value_CONST1},I_CONST1{current_value_CONST1},V_CONST2:{voltage_value_CONST2},I_CONST2{current_value_CONST2},V_CONST3:{voltage_value_CONST3},I_CONST3{current_value_CONST3}")
elif 0 == VAR2_flag:#表明未启用VAR2
    if IV_flag == 1:
        for i in range(num_points_VAR1):
            VAR1_session.voltage_level = voltage_min_VAR1 + i * voltage_step_VAR1
            VAR2_session.initiate()
            VAR1_session.initiate()
            # 进行 VAR1 测量
            current_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.CURRENT)
            VAR1_session.abort()
            current_value_VAR2 = VAR2_session.measure(nidcpower.MeasurementTypes.CURRENT)
            VAR2_session.abort()
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
                    pass
            else:
                pass
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
                    pass
            else:
                pass
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
                    pass
            else:
                pass
            # 打印VAR1和CONST的电压和电流值
            print(f"Direction: 'Forward' ,V_VAR1: {VAR1_session.voltage_level}, I_VAR1: {current_value_VAR1}, V_VAR2: 0, I_VAR2: 0,V_CONST1:{voltage_value_CONST1},I_CONST1{current_value_CONST1},V_CONST2:{voltage_value_CONST2},I_CONST2{current_value_CONST2},V_CONST3:{voltage_value_CONST3},I_CONST3{current_value_CONST3}")
    elif IV_flag == 2:
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
                    pass
            else:
                pass
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
                    pass
            else:
                pass
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
                    pass
            else:
                pass
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
            # 打印VAR1和CONST的电压和电流值
            print(
                f"Direction: 'Reverse' ,V_VAR1: {VAR1_session.voltage_level}, I_VAR1: {current_value_VAR1}, V_VAR2: 0, I_VAR2: 0,V_CONST1:{voltage_value_CONST1},I_CONST1{current_value_CONST1},V_CONST2:{voltage_value_CONST2},I_CONST2{current_value_CONST2},V_CONST3:{voltage_value_CONST3},I_CONST3{current_value_CONST3}")
    elif IV_flag == 3:
        for i in range(num_points_VAR1):
            VAR1_session.current_level = current_min_VAR1 + i * current_step_VAR1
            VAR2_session.initiate()
            VAR1_session.initiate()
            # 进行 VAR1 测量
            voltage_value_VAR1 = VAR1_session.measure(nidcpower.MeasurementTypes.VOLTAGE)
            VAR1_session.abort()
            current_value_VAR2 = VAR2_session.measure(nidcpower.MeasurementTypes.CURRENT)
            VAR2_session.abort()
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
                    pass
            else:
                pass
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
                    pass
            else:
                pass
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
                    pass
            else:
                pass
            print(f"Direction: 'Forward' ,V_VAR1: {voltage_value_VAR1}, I_VAR1: {VAR1_session.current_level}, V_VAR2: 0, I_VAR2: 0,V_CONST1:{voltage_value_CONST1},I_CONST1{current_value_CONST1},V_CONST2:{voltage_value_CONST2},I_CONST2{current_value_CONST2},V_CONST3:{voltage_value_CONST3},I_CONST3{current_value_CONST3}")
    elif IV_flag == 4:
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
                    pass
            else:
                pass
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
                    pass
            else:
                pass
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
                    pass
            else:
                pass
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
                    pass
            else:
                pass
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
                    pass
            else:
                pass
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
                    pass
            else:
                pass
            print(f"Direction: 'Reverse' ,V_VAR1: {voltage_value_VAR1}, I_VAR1: {VAR1_session.current_level}, V_VAR2: 0, I_VAR2: 0,V_CONST1:{voltage_value_CONST1},I_CONST1{current_value_CONST1},V_CONST2:{voltage_value_CONST2},I_CONST2{current_value_CONST2},V_CONST3:{voltage_value_CONST3},I_CONST3{current_value_CONST3}")

