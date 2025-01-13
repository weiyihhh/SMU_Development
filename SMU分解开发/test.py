import nidcpower
import hightime
# 创建会话
def test(voltage_max_VAR1,voltage_min_VAR1,num_points_VAR1,source_delay):
    session_VAR1 = nidcpower.Session(resource_name="PXI1Slot2")
    session_VAR1.source_mode = nidcpower.SourceMode.SEQUENCE
    session_VAR1.voltage_level_autorange = True
    session_VAR1.current_limit_autorange = True
    session_VAR1.source_delay = hightime.timedelta(seconds=source_delay)
    properties_used = ['output_function', 'voltage_level']
    session_VAR1.create_advanced_sequence(sequence_name='my_sequence', property_names=properties_used,
                                          set_as_active_sequence=True)

    voltage_step_VAR1 = round((voltage_max_VAR1 - voltage_min_VAR1) / (num_points_VAR1 - 1), 8)
    for i in range(num_points_VAR1):
        session_VAR1.create_advanced_sequence_step(set_as_active_step=False)
        session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE
        session_VAR1.voltage_level = voltage_min_VAR1 + i * voltage_step_VAR1

    aperture_time = session_VAR1.aperture_time  # 获取每次测量的窗口时间（采样时间）
    total_points = num_points_VAR1 # 总的测量点数。这里假设一次是电压扫描和一次电流扫描。
    timeout = hightime.timedelta(seconds=((source_delay + aperture_time) * total_points + 1.0))  # 计算超时时间
    with session_VAR1.initiate():
        channel_indices = f'0-{session_VAR1.channel_count - 1}'
        channels = session_VAR1.get_channel_names(channel_indices)
        measurement_group = [session_VAR1.channels[name].fetch_multiple(total_points, timeout=timeout) for name in channels]

    session_VAR1.delete_advanced_sequence(sequence_name='my_sequence')
    line_format = '{:<15} {:<4} {:<10} {:<10} {:<6}'
    print(line_format.format('Channel', 'Num', 'Voltage', 'Current', 'In Compliance'))
    for i, measurements in enumerate(measurement_group):
        num = 0
        channel_name = channels[i].strip()
        for measurement in measurements:
            print(line_format.format(channel_name, num, measurement.voltage, measurement.current,
                                     str(measurement.in_compliance)))
            num += 1
    # 手动关闭会话
    session_VAR1.close()

test(voltage_max_VAR1=-0.9,voltage_min_VAR1=0.05,num_points_VAR1=101,source_delay=0.1)