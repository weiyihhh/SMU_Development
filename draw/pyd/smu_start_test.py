import smu_start
from smu_dict import smu_dict_set
from plot import extract_v_i
from plot import smu_plot
smu1 = smu_dict_set(
    resource_name="PXI1Slot4/0",
    mode="V",
    function="VAR1",
    v_name="V1",
    i_name="I1",
    voltage_min_VAR1=0,
    voltage_max_VAR1=5,
    num_points_VAR1=101,
    current_limit_range_VAR1=0.1,
    current_limit_VAR1=0.1,
    VAR1_PLC=1,
    sweep_mode="single"
)

smu2 = smu_dict_set(
    resource_name="PXI1Slot4/1",
    mode="V",
    function="VAR2",
    v_name="V2",
    i_name="I2",
    voltage_min_VAR2=0,
    voltage_max_VAR2=0.1,
    num_points_VAR2=5,
    current_limit_range_VAR2=0.1,
    current_limit_VAR2=0.1,
    VAR2_PLC=1
)

smu3 = smu_dict_set(
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

smu4 = smu_dict_set(
    resource_name="PXI1Slot4/3",
    mode="V",
    function="CONST2",
    v_name="V4",
    i_name="I4",
    voltage_CONST2=2,
    CONST2_PLC=1,
    current_limit_range_CONST2=0.1,
    current_limit_CONST2=0.1
)

measurement_data = smu_start.smu_test_start(smu1_config_dict=smu1, smu2_config_dict=smu2, smu3_config_dict=None, smu4_config_dict=None, csv_save_path='D:/user文件/mac备份/qq123/工作安排/第二十周/二代smu测试数据',csv_name='2')

# 提取测量数据
V_VAR1_values, I_VAR1_values, V_VAR2_values, I_VAR2_values, V_CONST1_values, I_CONST1_values, V_CONST2_values, I_CONST2_values, V_CONST3_values, I_CONST3_values = extract_v_i(measurement_data)

smu_plot(V_VAR1_values, V_VAR1_values)

