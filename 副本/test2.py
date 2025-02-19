smu1_config_dict = {
    'resource_name': "PXI1Slot3",
    'mode': "V",
    'function': "VAR1",
    'v_name': 'V1',
    'i_name': 'I1',
    'voltage_min_VAR1': 0,
    'voltage_max_VAR1': 5,
    'num_points_VAR1': 101,
    'current_limit_range_VAR1': 0.1,
    'current_limit_VAR1': 0.05,
    'VAR1_PLC': 1,
    'sweep_mode': "single"
}
smu2_config_dict = {
    "resource_name": "PXI1Slot2",
    "mode": "V",
    "function": "CONST1",
    "v_name": "V2",
    "i_name": "I2",
    "voltage_CONST1": 1,
    "CONST1_PLC": 1,
    "current_limit_range_CONST1": 0.1,  # 设置 VAR2 的电流限制范围
    "current_limit_CONST1": 0.05,  # 设置 VAR2 的电流限制
}