import nidcpower
import hightime


def create_session(resource_name="PXI1Slot2", source_mode=nidcpower.SourceMode.SEQUENCE, voltage_level_autorange=True,
                   current_limit_autorange=True, source_delay_seconds=0.1):
    """
    创建并初始化 SMU 会话
    :param resource_name: 设备资源名称
    :param source_mode: 源模式（默认使用 SEQUENCE）
    :param voltage_level_autorange: 是否自动调节电压
    :param current_limit_autorange: 是否自动调节电流
    :param source_delay_seconds: 源延迟时间（单位：秒）
    :return: 返回创建的 SMU 会话对象
    """
    session = nidcpower.Session(resource_name=resource_name)
    session.source_mode = source_mode
    session.voltage_level_autorange = voltage_level_autorange
    session.current_limit_autorange = current_limit_autorange
    session.source_delay = hightime.timedelta(seconds=source_delay_seconds)

    return session


def create_sequence(session, sequence_name='my_sequence', properties_used=None, set_as_active_sequence=True):
    """
    创建并设置高级序列
    :param session: SMU 会话对象
    :param sequence_name: 序列的名称
    :param properties_used: 序列属性
    :param set_as_active_sequence: 是否将该序列设置为活动序列
    """
    if properties_used is None:
        properties_used = ['output_function', 'voltage_level']

    session.create_advanced_sequence(sequence_name=sequence_name, property_names=properties_used,
                                     set_as_active_sequence=set_as_active_sequence)


def calculate_voltage_step(voltage_max, voltage_min, num_points):
    """
    计算电压步进
    :param voltage_max: 电压最大值
    :param voltage_min: 电压最小值
    :param num_points: 测量点数
    :return: 电压步进值
    """
    return round((voltage_max - voltage_min) / (num_points - 1), 8)


def test(voltage_max_VAR1, voltage_min_VAR1, num_points_VAR1, source_delay):
    """
    执行 SMU 测量过程
    :param voltage_max_VAR1: 电压最大值
    :param voltage_min_VAR1: 电压最小值
    :param num_points_VAR1: 测量点数
    :param source_delay: 源延迟时间
    """
    # 创建 SMU 会话
    session_VAR1 = create_session(resource_name="PXI1Slot2", source_delay_seconds=source_delay)

    # 创建并设置高级序列
    create_sequence(session_VAR1)

    # 计算电压步进
    voltage_step_VAR1 = calculate_voltage_step(voltage_max_VAR1, voltage_min_VAR1, num_points_VAR1)

    # 添加测量步骤
    for i in range(num_points_VAR1):
        session_VAR1.create_advanced_sequence_step(set_as_active_step=False)
        session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE
        session_VAR1.voltage_level = voltage_min_VAR1 + i * voltage_step_VAR1

    aperture_time = session_VAR1.aperture_time  # 获取每次测量的窗口时间（采样时间）
    total_points = num_points_VAR1  # 总的测量点数
    timeout = hightime.timedelta(seconds=((source_delay + aperture_time) * total_points + 1.0))  # 计算超时时间

    # 启动测量
    with session_VAR1.initiate():
        channel_indices = f'0-{session_VAR1.channel_count - 1}'
        channels = session_VAR1.get_channel_names(channel_indices)
        measurement_group = [session_VAR1.channels[name].fetch_multiple(total_points, timeout=timeout) for name in
                             channels]

    # 删除序列并打印结果
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

    # 关闭会话
    session_VAR1.close()


# 调用函数执行测试
test(voltage_max_VAR1=-0.9, voltage_min_VAR1=0.05, num_points_VAR1=101, source_delay=0.1)
