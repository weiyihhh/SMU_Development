import nidcpower
import hightime
class SmuChannelConfig:
    def __init__(self, resource_name, mode, function,
                    num_points_VAR1=None, voltage_min_VAR1=None, voltage_max_VAR1=None, current_limit_range_VAR1=None,
                    voltage_limit_range_VAR1=None,current_max_VAR1=None,current_min_VAR1=None,voltage_limit_VAR1=None,
                    current_limit_range_CONST1=None, current_limit_range_CONST2=None, current_limit_range_CONST3=None,
                    num_points_VAR2=None, voltage_min_VAR2=None, voltage_max_VAR2=None, voltage_CONST1=None,
                    voltage_CONST2=None, voltage_CONST3=None, current_limit_VAR1=None, current_limit_VAR2=None,
                    current_limit_range_VAR2=None, current_limit_CONST1=None, current_limit_CONST2=None,
                    current_limit_CONST3=None, VAR1_PLC=None, VAR2_PLC=None, CONST1_PLC=None, CONST2_PLC=None,
                    CONST3_PLC=None, sweep_mode=None):
        """
            初始化通道配置
            :param resource_name: SMU设备的资源名称
            :param mode: 模式（V、I、IPULSE、VPULSE）
            :param function: 功能（VAR1、VAR2、CONST）
            :param num_points_VAR1: VAR1模式下的测量点数
            :param voltage_min_VAR1: VAR1模式下的最小电压
            :param voltage_max_VAR1: VAR1模式下的最大电压
            :param current_limit_range_VAR1: VAR1模式下的电流限制范围
            :param current_limit_range_CONST1: CONST1模式下的电流限制范围
            :param current_limit_range_CONST2: CONST2模式下的电流限制范围
            :param current_limit_range_CONST3: CONST3模式下的电流限制范围
            :param num_points_VAR2: VAR2模式下的测量点数
            :param voltage_min_VAR2: VAR2模式下的最小电压
            :param voltage_max_VAR2: VAR2模式下的最大电压
            :param voltage_CONST1: CONST1模式下的电压值
            :param voltage_CONST2: CONST2模式下的电压值
            :param voltage_CONST3: CONST3模式下的电压值
            :param current_limit_VAR1: VAR1模式下的电流限制值
            :param current_limit_VAR2: VAR2模式下的电流限制值
            :param current_limit_range_VAR2: VAR2模式下的电流限制范围
            :param current_limit_CONST1: CONST1模式下的电流限制值
            :param current_limit_CONST2: CONST2模式下的电流限制值
            :param current_limit_CONST3: CONST3模式下的电流限制值
            :param VAR1_PLC: VAR1模式下的PLC值
            :param VAR2_PLC: VAR2模式下的PLC值
            :param CONST1_PLC: CONST1模式下的PLC值
            :param CONST2_PLC: CONST2模式下的PLC值
            :param CONST3_PLC: CONST3模式下的PLC值
            """
        # 初始化参数
        self.resource_name = resource_name
        self.mode = mode
        self.function = function
        self.num_points_VAR1 = num_points_VAR1
        self.voltage_min_VAR1 = voltage_min_VAR1
        self.voltage_max_VAR1 = voltage_max_VAR1
        self.current_limit_range_VAR1 = current_limit_range_VAR1
        self.current_limit_range_CONST1 = current_limit_range_CONST1
        self.current_limit_range_CONST2 = current_limit_range_CONST2
        self.num_points_VAR2 = num_points_VAR2
        self.voltage_min_VAR2 = voltage_min_VAR2
        self.voltage_max_VAR2 = voltage_max_VAR2
        self.voltage_CONST1 = voltage_CONST1
        self.voltage_CONST2 = voltage_CONST2
        self.voltage_CONST3 = voltage_CONST3
        self.current_limit_VAR1 = current_limit_VAR1
        self.current_limit_VAR2 = current_limit_VAR2
        self.current_limit_range_VAR2 = current_limit_range_VAR2
        self.current_limit_CONST1 = current_limit_CONST1
        self.current_limit_CONST2 = current_limit_CONST2
        self.current_limit_CONST3 = current_limit_CONST3
        self.voltage_limit_range_VAR1 = voltage_limit_range_VAR1
        self.voltage_limit_VAR1 = voltage_limit_VAR1
        self.VAR1_PLC = VAR1_PLC
        self.VAR2_PLC = VAR2_PLC
        self.CONST1_PLC = CONST1_PLC
        self.CONST2_PLC = CONST2_PLC
        self.CONST3_PLC = CONST3_PLC
        self.sweep_mode = sweep_mode
        self.current_max_VAR1 = current_max_VAR1
        self.current_min_VAR1 = current_min_VAR1
    def open_session(self):
        # 根据function选择VAR1、VAR2或CONST
        if self.function == 'VAR1':
            self.session_VAR1 = nidcpower.Session(self.resource_name, reset=True)
            self.session_VAR1.source_mode = nidcpower.SourceMode.SEQUENCE
            properties_used = ['output_function', 'voltage_level', 'current_level']
            self.session_VAR1.create_advanced_sequence(sequence_name='my_sequence_VAR1', property_names=properties_used,
                                                        set_as_active_sequence=True)
            # 设置通道模式
            if self.mode == 'V': #此时的session被设置为VAR1的V输出
                """SMU会话配置"""
                self.session_VAR1.voltage_level_autorange = True
                self.session_VAR1.current_limit_range = self.current_limit_range_VAR1
                self.session_VAR1.current_limit = self.current_limit_VAR1  #限流设置
                voltage_step_VAR1 = round((self.voltage_max_VAR1 - self.voltage_min_VAR1) / (self.num_points_VAR1 - 1), 8)
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
            elif self.mode == 'I':
                """SMU会话配置"""
                self.session_VAR1.current_level_autorange = True
                self.session_VAR1.voltage_limit_range = self.voltage_limit_range_VAR1
                self.session_VAR1.voltage_limit = self.voltage_limit_VAR1
                current_step_VAR1 = round((self.current_max_VAR1 - self.current_min_VAR1) / (self.num_points_VAR1 - 1),8)
                if self.sweep_mode == 'single':
                    for i in range(self.num_points_VAR1):
                        self.session_VAR1.create_advanced_sequence_step(set_as_active_step=False)
                        self.session_VAR1.output_function = nidcpower.OutputFunction.DC_CURRENT
                        self.session_VAR1.current_level = self.current_min_VAR1 + i * current_step_VAR1
                elif self.sweep_mode == 'double':
                    # 正向扫描
                    for i in range(self.num_points_VAR1):
                        self.session_VAR1.create_advanced_sequence_step(set_as_active_step=False)
                        self.session_VAR1.output_function = nidcpower.OutputFunction.DC_CURRENT
                        self.session_VAR1.current_level = self.current_min_VAR1 + i * current_step_VAR1

                    # 反向扫描
                    for i in range(self.num_points_VAR1):
                        self.session_VAR1.create_advanced_sequence_step(set_as_active_step=False)
                        self.session_VAR1.output_function = nidcpower.OutputFunction.DC_CURRENT
                        self.session_VAR1.current_level = self.current_max_VAR1 - i * current_step_VAR1
                else:
                    print("Invalid sweep mode")
                aperture_time = self.session_VAR1.aperture_time  # 获取每次测量的窗口时间（采样时间）
                total_points = self.num_points_VAR1  # 总的测量点数。这里假设一次是电压扫描和一次电流扫描。
                timeout = hightime.timedelta(seconds=((self.session_VAR1.source_delay + aperture_time) * total_points + 1.0))  # 计算超时时间
                # ----------------------------------到这一步完成了VAR1的会话的初始化设置，接下来是session的initiate()来开始执行测量-----------------------------------------
            elif self.mode == 'VPULSE':
                """
                self.session_VAR1.output_function = nidcpower.OutputFunction.PULSE_VOLTAGE  # 设置为电压脉冲输出
                self.session_VAR1.pulse_voltage_level_range = self.voltage_limit_range_VAR1  # 设置电压脉冲范围
                self.session_VAR1.pulse_voltage_level = self.voltage_max_VAR1  # 设置脉冲的最大电压
                self.session_VAR1.current_limit_range = self.current_limit_range_VAR1
                self.session_VAR1.current_limit = self.voltage_limit_VAR1

                # 配置脉冲参数
                self.session_VAR1.pulse_on_time = 0.01  # 设置脉冲开启时间
                self.session_VAR1.pulse_off_time = 0.01  # 设置脉冲关闭时间
                self.session_VAR1.pulse_bias_voltage = 0  # 设置偏置电压（如果需要）
                self.session_VAR1.pulse_current_limit = self.current_limit_VAR1  # 设置电流限制
                self.session_VAR1.pulse_current_limit_range = self.current_limit_range_VAR1  # 设置电流限制范围

                # 创建脉冲序列步骤
                voltage_step_VAR1 = round((self.voltage_max_VAR1 - self.voltage_min_VAR1) / (self.num_points_VAR1 - 1),
                                          8)

                if self.sweep_mode == 'single':
                    for i in range(self.num_points_VAR1):
                        self.session_VAR1.create_advanced_sequence_step(set_as_active_step=False)
                        self.session_VAR1.voltage_level = self.voltage_min_VAR1 + i * voltage_step_VAR1
                elif self.sweep_mode == 'double':
                    # 正向扫描
                    for i in range(self.num_points_VAR1):
                        self.session_VAR1.create_advanced_sequence_step(set_as_active_step=False)
                        self.session_VAR1.voltage_level = self.voltage_min_VAR1 + i * voltage_step_VAR1

                    # 反向扫描
                    for i in range(self.num_points_VAR1):
                        self.session_VAR1.create_advanced_sequence_step(set_as_active_step=False)
                        self.session_VAR1.voltage_level = self.voltage_max_VAR1 - i * voltage_step_VAR1
                else:
                    print("Invalid sweep mode")

                aperture_time = self.session_VAR1.aperture_time  # 获取每次测量的窗口时间（采样时间）
                total_points = self.num_points_VAR1  # 总的测量点数
                timeout = hightime.timedelta(
                    seconds=((self.session_VAR1.source_delay + aperture_time) * total_points + 1.0))  # 计算超时时间"""
            elif self.mode == 'IPULSE':

        elif self.function == 'VAR2':
            self.session_VAR2 = nidcpower.Session(self.resource_name, reset=True)
            self.session_VAR2.source_mode = nidcpower.SourceMode.SINGLE_POINT

            # 设置通道模式
            if self.mode == 'V':


            elif self.mode == 'I':


            elif self.mode == 'IPULSE':
            elif self.mode == 'VPULSE':


        elif self.function == 'CONST':
            # 设置通道模式
            if self.mode == 'V':


            elif self.mode == 'I':


            elif self.mode == 'IPULSE':


            elif self.mode == 'VPULSE':

        self.session.initiate()

    def close_session(self):
        """关闭会话"""
        if self.session:
            self.session.close()
        else:
            raise RuntimeError("Session not open.")


