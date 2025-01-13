#测量部份的for循环单独拿出来写
"""
                if self.sweep_mode == 'single':
                    for i in range(self.num_points_VAR1):
                        self.session_VAR1.create_advanced_sequence_step(set_as_active_step=False)
                        self.session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE
                        self.session_VAR1.voltage_level = self.voltage_min_VAR1 + i * voltage_step_VAR1
                elif self.sweep_mode == 'double':
                    # 正向扫描
                    for i in range(self.num_points_VAR1):
                        self.session_VAR1.create_advanced_sequence_step(set_as_active_step=False)
                        self.session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE
                        self.session_VAR1.voltage_level = self.voltage_min_VAR1 + i * voltage_step_VAR1

                    # 反向扫描
                    for i in range(self.num_points_VAR1):
                        self.session_VAR1.create_advanced_sequence_step(set_as_active_step=False)
                        self.session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE
                        self.session_VAR1.voltage_level = self.voltage_max_VAR1 - i * voltage_step_VAR1
                else:
                    print("Invalid sweep mode")
                aperture_time = self.session_VAR1.aperture_time  # 获取每次测量的窗口时间（采样时间）
                total_points = self.num_points_VAR1  # 总的测量点数。这里假设一次是电压扫描和一次电流扫描。
                timeout = hightime.timedelta(seconds=((self.session_VAR1.source_delay + aperture_time) * total_points + 1.0))  # 计算超时时间
                #----------------------------------到这一步完成了VAR1的会话的初始化设置，接下来是session的initiate()来开始执行测量-----------------------------------------




"""