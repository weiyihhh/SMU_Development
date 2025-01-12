import nidcpower

class SmuSessionConfig:
    def __init__(self, resources):
        """
        初始化时传入资源字典，字典中每个设备的配置，包括电压、电流限制、PLC等信息
        :param resources: 设备资源配置字典
        """
        self.resources = resources  # 设备配置字典
        self.sessions = {}  # 存储每个设备的会话对象

    def open_sessions(self):
        """打开每个设备的会话并配置相关参数"""
        for device_name, config in self.resources.items():
            session = nidcpower.Session(device_name)
            self.configure_session(session, config)
            self.sessions[device_name] = session

    def configure_session(self, session, config):
        """为每个会话设备配置通用参数"""
        session.source_mode = nidcpower.SourceMode.SINGLE_POINT
        session.output_function = nidcpower.OutputFunction.DC_VOLTAGE
        session.current_limit = config['current_limit']
        session.voltage_level = config['voltage_limit']
        session.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
        session.aperture_time = config['aperture_time']

    def initiate_sessions(self):
        """启动所有设备的会话"""
        for session in self.sessions.values():
            session.initiate()

    def close_sessions(self):
        """关闭所有设备的会话"""
        for session in self.sessions.values():
            session.close()

    def measure_current(self, session_name):
        """测量指定设备的电流"""
        if session_name in self.sessions:
            session = self.sessions[session_name]
            return session.measure(nidcpower.MeasurementTypes.CURRENT)
        else:
            raise RuntimeError(f"Session {session_name} not open.")
