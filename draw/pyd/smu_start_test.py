import smu_start
from smu_dict import smu_dict_set
from plot import extract_v_i
from plot import smu_plot
from plot import plot_fig
from plot import line_color
from smu_slide import data_slice
smu1 = smu_dict_set(
    resource_name="PXI1Slot4/0",
    mode="V",
    function="VAR1",
    v_name="V1",
    i_name="I1",
    voltage_min_VAR1=0,
    voltage_max_VAR1=5,
    num_points_VAR1=11,
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

measurement_data, line_num_points ,line_nums = smu_start.smu_test_start(smu1_config_dict=smu1, smu2_config_dict=smu2, smu3_config_dict=None, smu4_config_dict=None, csv_save_path='D:/user文件/mac备份/qq123/工作安排/第二十周/二代smu测试数据',csv_name='2')
# 提取测量数据
V_VAR1_values, I_VAR1_values, V_VAR2_values, I_VAR2_values, V_CONST1_values, I_CONST1_values, V_CONST2_values, I_CONST2_values, V_CONST3_values, I_CONST3_values = extract_v_i(measurement_data)

fig , ax = plot_fig()

data_slices = data_slice("V_VAR1",V_VAR1_values, line_num_points, line_nums )
print(data_slices)
"""#画图部分的函数smu_plot()

if line_nums == 1:
    # 如果只有一条线，则不需要循环
    V_VAR1_slide = V_VAR1_values
else:
    V_VAR1_slide = []
    I_VAR1_slide = []
    V_VAR2_slide = []
    I_VAR2_slide = []
    V_CONST1_slide = []
    I_CONST1_slide = []
    V_CONST2_slide = []
    I_CONST2_slide = []
    V_CONST3_slide = []
    I_CONST3_slide = []

    line_ids, colors= line_color(line_nums, ax)

    for i in range(line_nums):
        # 为每条线分配不同的颜色，并创建一个空的线条（没有数据）
        line_id, = ax.plot([], [], linestyle='-', color=colors[i], linewidth=1.5, label=f"Line {i + 1}")
        # 计算当前切片的起始和结束索引
        start_idx = i * line_num_points
        end_idx = start_idx + line_num_points
        # 获取切片
        V_VAR1_slice = V_VAR1_values[start_idx:end_idx]
        I_VAR1_slice = I_VAR1_values[start_idx:end_idx]
        V_VAR2_slice = V_VAR2_values[start_idx:end_idx]
        I_VAR2_slice = I_VAR2_values[start_idx:end_idx]
        V_CONST1_slice = V_CONST1_values[start_idx:end_idx]
        I_CONST1_slice = I_CONST1_values[start_idx:end_idx]
        V_CONST2_slice = V_CONST2_values[start_idx:end_idx]
        I_CONST2_slice = I_CONST2_values[start_idx:end_idx]
        V_CONST3_slice = V_CONST3_values[start_idx:end_idx]
        I_CONST3_slice = I_CONST3_values[start_idx:end_idx]

        smu_plot(V_VAR1_slice, V_VAR2_slice, line_id, ax, fig)
        # 将切片添加到 V_VAR1_slide 列表
        V_VAR1_slide.append(V_VAR1_slice)
        I_VAR1_slide.append(I_VAR1_slice)
        V_VAR2_slide.append(V_VAR2_slice)
        I_VAR2_slide.append(I_VAR2_slice)
        print(V_VAR1_slice)
        print(I_VAR1_slide)
#print(V_VAR1_slide)
"""