import nidcpower

with nidcpower.Session(resource_name="PXI1Slot2") as session_VAR1:
    session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
    session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
    session_VAR1.voltage_level = 0
    session_VAR1.abort()