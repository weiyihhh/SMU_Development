import nidcpower
import hightime
class SmuChannelConfig:
    def __init__(self, resource_name, mode, function,
                    num_points_VAR1=None, voltage_min_VAR1=None, voltage_max_VAR1=None, current_limit_range_VAR1=None,
                    voltage_limit_range_VAR1=None,current_max_VAR1=None,current_min_VAR1=None,voltage_limit_VAR1=None,
                    current_limit_range_CONST1=None, current_limit_range_CONST2=None, current_limit_range_CONST3=None,
                    num_points_VAR2=None, voltage_min_VAR2=None, voltage_max_VAR2=None, voltage_CONST1=None,current_CONST1=None,current_CONST2=None,
                    current_CONST3=None,voltage_limit_CONST1=None,voltage_limit_CONST2=None,voltage_limit_CONST3=None,voltage_limit_range_CONST1=None,
                    voltage_limit_range_CONST2=None,voltage_limit_range_CONST3=None,
                    voltage_CONST2=None, voltage_CONST3=None, current_limit_VAR1=None, current_limit_VAR2=None,voltage_limit_range_VAR2=None,
                    current_limit_range_VAR2=None, current_limit_CONST1=None, current_limit_CONST2=None,voltage_limit_VAR2=None,
                    current_limit_CONST3=None, VAR1_PLC=None, VAR2_PLC=None, CONST1_PLC=None, CONST2_PLC=None,
                    CONST3_PLC=None, sweep_mode=None,current_max_VAR2=None,current_min_VAR2=None):
        """
            初始化通道配置
            :param resource_name: SMU设备的资源名称
            :param mode: 模式（V、I、COMMON）
            :param function: 功能（VAR1、VAR2、CONST1、CONST2、CONST3）
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
        self.current_limit_range_CONST3 = current_limit_range_CONST3
        self.num_points_VAR2 = num_points_VAR2
        self.voltage_min_VAR2 = voltage_min_VAR2
        self.voltage_max_VAR2 = voltage_max_VAR2
        self.current_max_VAR2 = current_max_VAR2
        self.current_min_VAR2 = current_min_VAR2
        self.voltage_CONST1 = voltage_CONST1
        self.voltage_CONST2 = voltage_CONST2
        self.voltage_CONST3 = voltage_CONST3
        self.current_limit_VAR1 = current_limit_VAR1
        self.current_limit_VAR2 = current_limit_VAR2
        self.current_limit_range_VAR2 = current_limit_range_VAR2
        self.voltage_limit_range_VAR2 = voltage_limit_range_VAR2
        self.current_limit_CONST1 = current_limit_CONST1
        self.current_limit_CONST2 = current_limit_CONST2
        self.current_limit_CONST3 = current_limit_CONST3
        self.voltage_limit_range_VAR1 = voltage_limit_range_VAR1
        self.voltage_limit_VAR1 = voltage_limit_VAR1
        self.voltage_limit_VAR2 = voltage_limit_VAR2
        self.VAR1_PLC = VAR1_PLC
        self.VAR2_PLC = VAR2_PLC
        self.CONST1_PLC = CONST1_PLC
        self.CONST2_PLC = CONST2_PLC
        self.CONST3_PLC = CONST3_PLC
        self.sweep_mode = sweep_mode
        self.current_max_VAR1 = current_max_VAR1
        self.current_min_VAR1 = current_min_VAR1
        self.voltage_CONST2 = voltage_CONST2
        self.voltage_CONST3 = voltage_CONST3
        self.voltage_limit_CONST1 = voltage_limit_CONST1
        self.voltage_limit_CONST2 = voltage_limit_CONST2
        self.voltage_limit_CONST3 = voltage_limit_CONST3
        self.voltage_limit_range_CONST1 = voltage_limit_range_CONST1
        self.voltage_limit_range_CONST2 = voltage_limit_range_CONST2
        self.voltage_limit_range_CONST3 = voltage_limit_range_CONST3
        self.current_CONST1 = current_CONST1
        self.current_CONST2 = current_CONST2
        self.current_CONST3 = current_CONST3

    def mode_select(self):
        if self.mode == 'V':
            return 1
        elif self.mode == 'I':
            return 0
        elif self.mode == 'COMMON':
            return None

    def CONST_select(self):
        if self.function == 'CONST1':
            return {"CONST": 1}
        elif self.function == 'CONST2':
            return {"CONST": 2}
        elif self.function == 'CONST3':
            return {"CONST": 3}
        else:
            return {"CONST": 0} #表示未用CONST

    def open_session(self):
        # 根据function选择VAR1、VAR2或CONST
        if self.function == 'VAR1':
            if self.mode == 'COMMON':
                self.session_VAR1 = nidcpower.Session(self.resource_name, reset=True)
                self.session_VAR1.source_mode = nidcpower.SourceMode.SINGLE_POINT
                self.session_VAR1.output_function = nidcpower.OutputFunction.DC_VOLTAGE
                self.session_VAR1.current_limit_autorange = True
                self.session_VAR1.voltage_level = 0
                print(f"Successfully configured SMU-COMMON: {self.resource_name}\n\n")
            else:
                self.session_VAR1 = nidcpower.Session(self.resource_name, reset=True)
                self.session_VAR1.source_mode = nidcpower.SourceMode.SEQUENCE
                # 设置VAR1.PLC
                self.session_VAR1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                self.session_VAR1.aperture_time = self.VAR1_PLC
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
                        return {"sweep_mode":'single',
                                "voltage_step_VAR1": voltage_step_VAR1}
                    elif self.sweep_mode == 'double':
                        return {"sweep_mode":'double',
                                "voltage_step_VAR1": voltage_step_VAR1}
                    else:
                        print("Invalid sweep mode")

                    #----------------------------------到这一步完成了VAR1的会话的初始化设置，接下来是session的for来开始执行测量-----------------------------------------
                elif self.mode == 'I':
                    """SMU会话配置"""
                    self.session_VAR1.current_level_autorange = True
                    self.session_VAR1.voltage_limit_range = self.voltage_limit_range_VAR1
                    self.session_VAR1.voltage_limit = self.voltage_limit_VAR1
                    current_step_VAR1 = round((self.current_max_VAR1 - self.current_min_VAR1) / (self.num_points_VAR1 - 1),8)
                    if self.sweep_mode == 'single':
                        return {"sweep_mode":'single'}
                    elif self.sweep_mode == 'double':
                        return {"sweep_mode": 'double'}
                    else:
                        print("Invalid sweep mode")
                    # ----------------------------------到这一步完成了VAR1的会话的初始化设置，接下来是session的for来开始执行测量-----------------------------------------
        elif self.function == 'VAR2':
            if self.mode == 'COMMON':
                self.session_VAR2 = nidcpower.Session(self.resource_name, reset=True)
                self.session_VAR2.source_mode = nidcpower.SourceMode.SINGLE_POINT
                self.session_VAR2.output_function = nidcpower.OutputFunction.DC_VOLTAGE
                self.session_VAR2.current_limit_autorange = True
                self.session_VAR2.voltage_level = 0
                print(f"Successfully configured SMU-COMMON: {self.resource_name}\n\n")
            else:
                self.session_VAR2 = nidcpower.Session(self.resource_name, reset=True)
                self.session_VAR2.source_mode = nidcpower.SourceMode.SINGLE_POINT
                # 设置VAR2.PLC
                self.session_VAR2.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                self.session_VAR2.aperture_time = self.VAR2_PLC
                # 设置通道模式
                if self.mode == 'V':
                    self.session_VAR2.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
                    self.session_VAR2.current_limit = self.current_limit_VAR2  # 设置VAR2端的电流限制
                    self.session_VAR2.current_limit_range = self.current_limit_range_VAR2
                    # 计算VAR2步进电压
                    voltage_step_VAR2 = round((self.voltage_max_VAR2 - self.voltage_min_VAR2) / (self.num_points_VAR2 - 1), 8)
                    return {
                        "voltage_step_VAR2": voltage_step_VAR2,
                        "voltage_max_VAR2": self.voltage_max_VAR2,
                        "volatge_min_VAR2": self.voltage_min_VAR2,
                    }

                elif self.mode == 'I':
                    self.session_VAR2.output_function = nidcpower.OutputFunction.DC_CURRENT  # 设置为直流电压输出
                    self.session_VAR2.voltage_limit = self.voltage_limit_VAR2  # 设置VAR2端的电流限制
                    self.session_VAR2.voltage_limit_range = self.voltage_limit_range_VAR2
                    # 计算VAR2步进电流
                    current_step_VAR2 = round((self.current_max_VAR2 - self.current_min_VAR2) / (self.num_points_VAR2 - 1),8)
                    return {
                        "current_step_VAR2": current_step_VAR2,
                        "current_max_VAR2": self.voltage_max_VAR2,
                        "current_min_VAR2": self.voltage_min_VAR2,
                    }
        elif self.function == 'CONST1':
            if self.mode == 'COMMON':
                self.session_CONST1 = nidcpower.Session(self.resource_name, reset=True)
                self.session_CONST1.source_mode = nidcpower.SourceMode.SINGLE_POINT
                self.session_CONST1.output_function = nidcpower.OutputFunction.DC_VOLTAGE
                self.session_CONST1.current_limit_autorange = True
                self.session_CONST1.voltage_level = 0
                print(f"Successfully configured SMU-COMMON: {self.resource_name}\n\n")
            else:
                self.session_CONST1 = nidcpower.Session(self.resource_name, reset=True)
                self.session_CONST1.source_mode = nidcpower.SourceMode.SINGLE_POINT
                # 设置CONST1.PLC
                self.session_CONST1.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                self.session_CONST1.aperture_time = self.CONST1_PLC
                # 设置通道模式
                if self.mode == 'V':
                    self.session_CONST1.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置输出为电压模式
                    self.session_CONST1.voltage_level = self.voltage_CONST1  # 设CONST1端的电压
                    self.session_CONST1.current_limit = self.current_limit_CONST1
                    self.session_CONST1.current_limit_range = self.current_limit_range_CONST1
                elif self.mode == 'I':
                    self.session_CONST1.output_function = nidcpower.OutputFunction.DC_CURRENT  # 设置输出为电流模式
                    self.session_CONST1.current_level = self.current_CONST1  # 设CONST1端的电流
                    self.session_CONST1.voltage_limit = self.voltage_limit_CONST1
                    self.session_CONST1.voltage_limit_range = self.voltage_limit_range_CONST1
        elif self.function == 'CONST2':
            if self.mode == 'COMMON':
                self.session_CONST2 = nidcpower.Session(self.resource_name, reset=True)
                self.session_CONST2.source_mode = nidcpower.SourceMode.SINGLE_POINT
                self.session_CONST2.output_function = nidcpower.OutputFunction.DC_VOLTAGE
                self.session_CONST2.current_limit_autorange = True
                self.session_CONST2.voltage_level = 0
                print(f"Successfully configured SMU-COMMON: {self.resource_name}\n\n")
            else:
                self.session_CONST2 = nidcpower.Session(self.resource_name, reset=True)
                self.session_CONST2.source_mode = nidcpower.SourceMode.SINGLE_POINT
                # 设置CONST2.PLC
                self.session_CONST2.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                self.session_CONST2.aperture_time = self.CONST2_PLC
                # 设置通道模式
                if self.mode == 'V':
                    self.session_CONST2.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置输出为电压模式
                    self.session_CONST2.voltage_level = self.voltage_CONST2  # 设CONST2端的电压
                    self.session_CONST2.current_limit = self.current_limit_CONST2
                    self.session_CONST2.current_limit_range = self.current_limit_range_CONST2
                elif self.mode == 'I':
                    self.session_CONST2.output_function = nidcpower.OutputFunction.DC_CURRENT  # 设置输出为电流模式
                    self.session_CONST2.current_level = self.current_CONST2  # 设CONST2端的电流
                    self.session_CONST2.voltage_limit = self.voltage_limit_CONST2
                    self.session_CONST2.voltage_limit_range = self.voltage_limit_range_CONST2
        elif self.function == 'CONST3':
            if self.mode == 'COMMON':
                self.session_CONST3 = nidcpower.Session(self.resource_name, reset=True)
                self.session_CONST3.source_mode = nidcpower.SourceMode.SINGLE_POINT
                self.session_CONST3.output_function = nidcpower.OutputFunction.DC_VOLTAGE
                self.session_CONST3.current_limit_autorange = True
                self.session_CONST3.voltage_level = 0
                print(f"Successfully configured SMU-COMMON: {self.resource_name}\n\n")
            else:
                self.session_CONST3 = nidcpower.Session(self.resource_name, reset=True)
                self.session_CONST3.source_mode = nidcpower.SourceMode.SINGLE_POINT
                # 设置CONST3.PLC
                self.session_CONST3.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
                self.session_CONST3.aperture_time = self.CONST3_PLC
                # 设置通道模式
                if self.mode == 'V':
                    self.session_CONST3.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置输出为电压模式
                    self.session_CONST3.voltage_level = self.voltage_CONST3  # 设CONST3端的电压
                    self.session_CONST3.current_limit = self.current_limit_CONST3
                    self.session_CONST3.current_limit_range = self.current_limit_range_CONST3
                elif self.mode == 'I':
                    self.session_CONST3.output_function = nidcpower.OutputFunction.DC_CURRENT  # 设置输出为电流模式
                    self.session_CONST3.current_level = self.current_CONST3  # 设CONST3端的电流
                    self.session_CONST3.voltage_limit = self.voltage_limit_CONST3
                    self.session_CONST3.voltage_limit_range = self.voltage_limit_range_CONST3
    def close_session(self):
        """关闭会话"""
        if self.session:
            self.session.close()
        else:
            raise RuntimeError("Session not open.")


