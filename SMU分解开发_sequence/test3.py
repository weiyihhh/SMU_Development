import smu_config

# 实例化 SmuChannelConfig 并调用 open_session()
smu_VAR1 = smu_config.SmuChannelConfig(
    resource_name="PXI1Slot2",  # 设置 SMU 设备的资源名称
    mode="V",  # 设置为电压模式
    function="VAR1",  # 设置功能为 VAR1
    voltage_min_VAR1=0.0,  # 设置 VAR1 的最小电压
    voltage_max_VAR1=10.0,  # 设置 VAR1 的最大电压
    num_points_VAR1=101,  # 设置 VAR1 的测量点数
    current_limit_range_VAR1=0.1,  # 设置 VAR1 的电流限制范围
    current_limit_VAR1=0.05,  # 设置 VAR1 的电流限制
    VAR1_PLC=10,  # 设置 VAR1 的 PLC 时间
    sweep_mode="single"  # 设置扫描模式为 single
)
sweep_mode_VAR1 = smu_VAR1.open_session().get("sweep_mode") #这时候是'single'或'double'
if sweep_mode_VAR1 == 'single':

elif sweep_mode_VAR1 == 'double':




