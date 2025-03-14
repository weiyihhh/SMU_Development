def smu_dict_set(
    resource_name=None, mode=None, function=None, v_name=None, i_name=None, sweep_mode=None,
    voltage_min_VAR1=None, voltage_max_VAR1=None, num_points_VAR1=None,
    current_limit_range_VAR1=None, current_limit_VAR1=None, VAR1_PLC=None,
    voltage_min_VAR2=None, voltage_max_VAR2=None, num_points_VAR2=None,
    current_limit_range_VAR2=None, current_limit_VAR2=None, VAR2_PLC=None,
    voltage_CONST1=None, CONST1_PLC=None, current_limit_range_CONST1=None, current_limit_CONST1=None,
    voltage_CONST2=None, CONST2_PLC=None, current_limit_range_CONST2=None, current_limit_CONST2=None,
    voltage_CONST3=None, CONST3_PLC=None, current_limit_range_CONST3=None, current_limit_CONST3=None
):
    return {
        "resource_name": resource_name, "mode": mode, "function": function,
        "v_name": v_name, "i_name": i_name, "sweep_mode": sweep_mode,
        "voltage_min_VAR1": voltage_min_VAR1, "voltage_max_VAR1": voltage_max_VAR1,
        "num_points_VAR1": num_points_VAR1, "current_limit_range_VAR1": current_limit_range_VAR1,
        "current_limit_VAR1": current_limit_VAR1, "VAR1_PLC": VAR1_PLC,
        "voltage_min_VAR2": voltage_min_VAR2, "voltage_max_VAR2": voltage_max_VAR2,
        "num_points_VAR2": num_points_VAR2, "current_limit_range_VAR2": current_limit_range_VAR2,
        "current_limit_VAR2": current_limit_VAR2, "VAR2_PLC": VAR2_PLC,
        "voltage_CONST1": voltage_CONST1, "CONST1_PLC": CONST1_PLC,
        "current_limit_range_CONST1": current_limit_range_CONST1, "current_limit_CONST1": current_limit_CONST1,
        "voltage_CONST2": voltage_CONST2, "CONST2_PLC": CONST2_PLC,
        "current_limit_range_CONST2": current_limit_range_CONST2, "current_limit_CONST2": current_limit_CONST2,
        "voltage_CONST3": voltage_CONST3, "CONST3_PLC": CONST3_PLC,
        "current_limit_range_CONST3": current_limit_range_CONST3, "current_limit_CONST3": current_limit_CONST3
    }

# 示例调用（只传部分参数，其他默认为 None）

smu1_config_dict = smu_dict_set(
    resource_name="PXI1Slot4/0",
    mode="V",
    function="VAR1",
    v_name="V1",
    i_name="I1",
    voltage_min_VAR1=0,
    voltage_max_VAR1=5,
    num_points_VAR1=10,
    current_limit_range_VAR1=0.1,
    current_limit_VAR1=0.05,
    VAR1_PLC=1,
    sweep_mode="single"
)

smu2_config_dict = smu_dict_set(
    resource_name="PXI1Slot4/1",
    mode="V",
    function="VAR2",
    v_name="V2",
    i_name="I2",
    voltage_min_VAR2=0,
    voltage_max_VAR2=1,
    num_points_VAR2=3,
    current_limit_range_VAR2=0.1,
    current_limit_VAR2=0.05,
    VAR2_PLC=1
)

smu3_config_dict = smu_dict_set(
    resource_name="PXI1Slot4/2",
    mode="V",
    function="CONST1",
    v_name="V3",
    i_name="I3",
    voltage_CONST1=1,
    CONST1_PLC=1,
    current_limit_range_CONST1=0.1,
    current_limit_CONST1=0.05
)

smu4_config_dict = smu_dict_set(
    resource_name="PXI1Slot4/3",
    mode="V",
    function="CONST2",
    v_name="V4",
    i_name="I4",
    voltage_CONST2=2,
    CONST2_PLC=1,
    current_limit_range_CONST2=0.1,
    current_limit_CONST2=0.05
)
print(smu3_config_dict)