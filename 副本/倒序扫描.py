if self.sweep_mode == 'single':
    # 正序扫描
    if self.scan_direction == 'forward':  # 可以使用自定义的 scan_direction 来控制方向
        for i in range(self.num_points_VAR1):
            self.session_VAR1.create_advanced_sequence_step(set_as_active_step=False)
            self.session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE
            self.session_VAR1.voltage_level = self.voltage_min_VAR1 + i * voltage_step_VAR1
    # 倒序扫描
    elif self.scan_direction == 'reverse':
        for i in range(self.num_points_VAR1):
            self.session_VAR1.create_advanced_sequence_step(set_as_active_step=False)
            self.session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE
            self.session_VAR1.voltage_level = self.voltage_max_VAR1 - i * voltage_step_VAR1
    else:
        raise ValueError("Invalid scan direction. Use 'forward' or 'reverse'.")




"""  # 这里将调用CONST的测量
            const_measurement = smu_measure.smu_const_measure(smu2)  # 直接调用smu_const_measure进行测量
            voltage_value_CONST1 = const_measurement.get("voltage_value_CONST1")
            current_value_CONST1 = const_measurement.get("current_value_CONST1")"""


smu2 = smu_config.SmuChannelConfig(
    resource_name="PXI1Slot3",  # 设置 SMU 设备的资源名称
    mode="V",  # 设置为电压模式
    function="CONST1",  # 设置功能为 CONST1
    voltage_CONST1=0.0,  # 设置 CONST1 的电压
    current_limit_range_CONST1=0.1,  # 设置 CONST1 的电流限制范围
    current_limit_CONST1=0.05,  # 设置 CONST1 的电流限制
    CONST1_PLC=1,  # 设置 VAR1 的 PLC 时间
)
