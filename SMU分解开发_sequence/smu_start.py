import smu_config
import nidcpower
import hightime
import smu_measure

# 实例化 SmuChannelConfig 并调用 open_session()
smu1 = smu_config.SmuChannelConfig(
    resource_name="PXI1Slot2",  # 设置 SMU 设备的资源名称
    mode="V",  # 设置为电压模式
    function="VAR1",  # 设置功能为 VAR1
    voltage_min_VAR1=0.0,  # 设置 VAR1 的最小电压
    voltage_max_VAR1=10.0,  # 设置 VAR1 的最大电压
    num_points_VAR1=101,  # 设置 VAR1 的测量点数
    current_limit_range_VAR1=0.1,  # 设置 VAR1 的电流限制范围
    current_limit_VAR1=0.05,  # 设置 VAR1 的电流限制
    VAR1_PLC=1,  # 设置 VAR1 的 PLC 时间
    sweep_mode="single"  # 设置扫描模式为 single
)

smu2 = smu_config.SmuChannelConfig(
    resource_name="PXI1Slot3",  # 设置 SMU 设备的资源名称
    mode="V",  # 设置为电压模式
    function="CONST1",  # 设置功能为 CONST1
    voltage_CONST1=0.0,  # 设置 CONST1 的电压
    current_limit_range_CONST1=0.1,  # 设置 CONST1 的电流限制范围
    current_limit_CONST1=0.05,  # 设置 CONST1 的电流限制
    CONST1_PLC=1,  # 设置 VAR1 的 PLC 时间
)

mode_VAR1 = smu1.mode_select()

# 设置扫描模式
sweep_mode_VAR1 = 'single'

if sweep_mode_VAR1 == 'single':
    # 继续判断是V还是I
    if 1 == mode_VAR1:  # 表明是V模式
        smu1.create_session()
        smu1_config = smu1.config_data
        voltage_step_VAR1 = smu1_config.get("voltage_step_VAR1", 0)

        # 设置测量条件
        smu1.session_VAR1.measure_when = nidcpower.MeasureWhen.ON_DEMAND  # 设置为按需测量

        smu1.create_sequence()
        # 循环进行测量
        for i in range(smu1.num_points_VAR1):
            smu1.session_VAR1.create_advanced_sequence_step(set_as_active_step=False)
            smu1.session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE
            smu1.session_VAR1.voltage_level = smu1.voltage_min_VAR1 + i * voltage_step_VAR1

            # 这里将调用CONST的测量
            smu_measure.smu_const_measure(smu2)  # 直接调用smu_const_measure进行测量

            # 打印每次的电压和电流值（VAR1的电压）
            print(f"V_VAR1: {smu1.session_VAR1.voltage_level}")

            # 打印CONST的电压和电流值
            voltage_value_CONST1 = smu_measure.smu_const_measure(smu2).get("voltage_value_CONST1")
            current_value_CONST1 = smu_measure.smu_const_measure(smu2).get("current_value_CONST1")
            print(f"V_CONST1: {voltage_value_CONST1}, I_CONST1: {current_value_CONST1}")

        aperture_time = smu1.session_VAR1.aperture_time  # 获取每次测量的窗口时间（采样时间）
        total_points = smu1.num_points_VAR1  # 总的测量点数。这里假设一次是电压扫描和一次电流扫描。
        timeout = hightime.timedelta(seconds=((0.0166 + aperture_time) * total_points + 1.0))  # 计算超时时间
        with smu1.session_VAR1.initiate():
            channel_indices = f'0-{smu1.session_VAR1.channel_count - 1}'
            channels = smu1.session_VAR1.get_channel_names(channel_indices)
            measurement_group = [smu1.session_VAR1.channels[name].fetch_multiple(total_points, timeout=timeout) for name in
                                 channels]
    elif 0 == mode_VAR1:  # 标明是I模式
        print("1")
    elif 2 == mode_VAR1:
        print("ERROR: Output function must be constant for the unit_VAR1 in common mode.")

elif sweep_mode_VAR1 == 'double':
    print("2")
