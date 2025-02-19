class MeasurementManager:
    def __init__(self):
        '''初始化测量数据列表'''
        self.measurements_data = []

    def add_measurement(self, data):
        '''将测量数据添加到 measurements_data 列表中'''
        self.measurements_data.append(data)

    def get_measurements(self):
        '''返回所有测量数据'''
        return self.measurements_data

    def clear_measurements(self):
        '''清空所有测量数据'''
        self.measurements_data = []

