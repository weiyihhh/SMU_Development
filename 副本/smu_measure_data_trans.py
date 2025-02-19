import smu_config
#至多有4个smu通道
#传递数据字典：'{smu1.v_name}': ,'{smu1.i_name}': ,
# 假设这些是你为每个SMU通道设置的电压和电流名称
smu1 = smu_config.SmuChannelConfig(v_name="V1", i_name="I1")
smu2 = smu_config.SmuChannelConfig(v_name="V2", i_name="I2")
smu3 = smu_config.SmuChannelConfig(v_name="V3", i_name="I3")
smu4 = smu_config.SmuChannelConfig(v_name="V4", i_name="I4")

# 假设每个SMU通道都有一些测量数据
smu1_v_value = 3.0  # 例如，电压值为 3.0V
smu1_i_value = 0.01  # 例如，电流值为 0.01A

smu2_v_value = 2.8
smu2_i_value = 0.02

smu3_v_value = 3.5
smu3_i_value = 0.015

smu4_v_value = 3.2
smu4_i_value = 0.018

# 构建字典
smu_data = {
    f'{smu1.v_name}': smu1_v_value,
    f'{smu1.i_name}': smu1_i_value,
    f'{smu2.v_name}': smu2_v_value,
    f'{smu2.i_name}': smu2_i_value,
    f'{smu3.v_name}': smu3_v_value,
    f'{smu3.i_name}': smu3_i_value,
    f'{smu4.v_name}': smu4_v_value,
    f'{smu4.i_name}': smu4_i_value,
}

print(smu_data)
