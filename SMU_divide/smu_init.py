from smu_config import SmuChannelConfig
from smu_config_get import config_get
from setup_smu import setup_smu_channel

def configure_smu(smu_configs):
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
                return sweep_mode_VAR1, num_points_VAR1, voltage_step_VAR1, voltage_max_VAR1, voltage_min_VAR1, IV_flag_VAR1,VAR1_session
            elif data.get("IV_flag") in [3, 4]:
                sweep_mode_VAR1, num_points_VAR1, current_step_VAR1, current_max_VAR1, current_min_VAR1, IV_flag_VAR1 = params
                VAR1_session = session  # 保存会话对象
                return sweep_mode_VAR1, num_points_VAR1, current_step_VAR1, current_max_VAR1, current_min_VAR1, IV_flag_VAR1, VAR1_session
            elif data.get("IV_flag") in [5]:
                mode_VAR2, num_points_VAR2, voltage_step_VAR2, voltage_max_VAR2, voltage_min_VAR2, VAR2_flag = params
                VAR2_session = session  # 保存会话对象
                return mode_VAR2, num_points_VAR2, voltage_step_VAR2, voltage_max_VAR2, voltage_min_VAR2, VAR2_flag,VAR2_session
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