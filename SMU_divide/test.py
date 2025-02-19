import nidcpower

with nidcpower.Session(resource_name='PXI1Slot3') as session_VAR2:
    session_VAR2.reset_device()
    session_VAR2.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
    session_VAR2.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
    session_VAR2.current_limit = 0.1  # 设置VAR2端的电流限制
    session_VAR2.current_limit_range = 0.1
    session_VAR2.voltage_level = 0.1  # 设置VAR2端的电压输出
    session_VAR2.initiate()
