
def setup_smu_channel(smu_channel, data):
    IV_flag = data.get("IV_flag")

    if IV_flag == 1 or IV_flag == 2:
        # 电压扫描配置
        sweep_mode_VAR1 = 'single' if IV_flag == 1 else 'double'
        num_points_VAR1 = data.get("points")
        voltage_step_VAR1 = data.get("step")
        voltage_max_VAR1 = data.get("voltage_max_VAR1")
        voltage_min_VAR1 = data.get("voltage_min_VAR1")
        VAR1_session = smu_channel.create_session()
        return VAR1_session, sweep_mode_VAR1, num_points_VAR1, voltage_step_VAR1, voltage_max_VAR1, voltage_min_VAR1, IV_flag

    elif IV_flag == 3 or IV_flag == 4:
        # 电流扫描配置
        sweep_mode_VAR1 = 'single' if IV_flag == 3 else 'double'
        num_points_VAR1 = data.get("points")
        current_step_VAR1 = data.get("step")
        current_max_VAR1 = data.get("current_max_VAR1")
        current_min_VAR1 = data.get("current_min_VAR1")
        VAR1_session = smu_channel.create_session()
        return VAR1_session, sweep_mode_VAR1, num_points_VAR1, current_step_VAR1, current_max_VAR1, current_min_VAR1, IV_flag

    elif IV_flag == 5:
        # VAR2 V配置
        mode_VAR2 = 'V'
        num_points_VAR2 = data.get("points")
        voltage_step_VAR2 = data.get("step")
        voltage_max_VAR2 = data.get("voltage_max_VAR2")
        voltage_min_VAR2 = data.get("voltage_min_VAR2")
        VAR2_session = smu_channel.create_session()
        VAR2_flag = 1
        return VAR2_session, mode_VAR2, num_points_VAR2, voltage_step_VAR2, voltage_max_VAR2, voltage_min_VAR2, VAR2_flag
    elif IV_flag == 6:
        # VAR2 I配置
        mode_VAR2 = 'I'
        num_points_VAR2 = data.get("points")
        current_step_VAR2 = data.get("step")
        current_max_VAR2 = data.get("current_max_VAR2")
        current_min_VAR2 = data.get("current_min_VAR2")
        VAR2_session = smu_channel.create_session()
        VAR2_flag = 1
        return VAR2_session, mode_VAR2, num_points_VAR2, current_step_VAR2, current_max_VAR2, current_min_VAR2, VAR2_flag
    elif IV_flag == 7:
        mode_CONST1 = 'V'
        CONST1_flag = 1
        voltage_CONST1 = data.get("voltage_CONST1")
        CONST1_session = smu_channel.create_session()
        return CONST1_session, mode_CONST1, voltage_CONST1, CONST1_flag
    elif IV_flag == 8:
        mode_CONST1 = 'I'
        CONST1_flag = 1
        current_CONST1 = data.get("current_CONST1")
        CONST1_session = smu_channel.create_session()
        return CONST1_session, mode_CONST1, current_CONST1, CONST1_flag
    elif IV_flag == 9:
        mode_CONST2 = 'V'
        CONST2_flag = 1
        voltage_CONST2 = data.get("voltage_CONST2")
        CONST2_session = smu_channel.create_session()
        return CONST2_session, mode_CONST2, voltage_CONST2, CONST2_flag
    elif IV_flag == 10:
        mode_CONST2 = 'I'
        CONST2_flag = 1
        current_CONST2 = data.get("current_CONST2")
        CONST2_session = smu_channel.create_session()
        return CONST2_session, mode_CONST2, current_CONST2, CONST2_flag
    elif IV_flag == 11:
        mode_CONST3 = 'V'
        CONST3_flag = 1
        voltage_CONST3 = data.get("voltage_CONST3")
        CONST3_session = smu_channel.create_session()
        return CONST3_session, mode_CONST3, voltage_CONST3, CONST3_flag
    return None  # 如果 IV_flag 不符合任何条件
