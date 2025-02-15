import numpy as np
import matplotlib.pyplot as plt


class MOSFETMeasurement:
    def __init__(self, Vg_values, Id_values, Is_values):
        '''初始化 MOSFET 测量数据'''
        self.Vg_values = Vg_values
        self.Id_values = Id_values
        self.Is_values = Is_values

        # 设置图形窗口
        self.fig, self.ax = plt.subplots(figsize=(20, 12), facecolor='lightgray')
        self.ax.set_title("MOSFET Id-Vg Curve with Is", fontsize=20, fontweight='bold')
        self.ax.set_xlabel("Gate-Source Voltage (V)", fontsize=14)
        self.ax.set_ylabel("Drain Current (Id) (A)", fontsize=14)

        # 创建右侧y轴
        self.ax2 = self.ax.twinx()
        self.ax2.set_ylabel("Source Current (Is) (A)", fontsize=14)

        # 设置网格和坐标轴样式
        self.ax.grid(True, which='both', axis='both', color='lightgray', linestyle='-', linewidth=0.7)
        self.ax.set_facecolor('white')
        self.ax.tick_params(axis='both', which='major', labelsize=12)
        self.ax2.tick_params(axis='both', which='major', labelsize=12)

        # 初始化数据
        self.x_data = []
        self.y_data_id = []
        self.y_data_is = []

        # 初始化图形线条，颜色改为橘色和绿色
        self.line_id, = self.ax.plot([], [], linestyle='-', color='orange', linewidth=1.5)
        self.line_is, = self.ax2.plot([], [], linestyle='-', color='blue', linewidth=1.5)

        # 启动交互式绘图
        plt.ion()

    def update_data(self):
        '''实时更新数据并绘制图形'''
        for Vg, Id, Is in zip(self.Vg_values, self.Id_values, self.Is_values):
            # 更新数据
            self.x_data.append(Vg)
            self.y_data_id.append(Id)
            self.y_data_is.append(Is)

            # 更新图形数据
            self.line_id.set_data(self.x_data, self.y_data_id)
            self.line_is.set_data(self.x_data, self.y_data_is)

            # 动态调整X轴和Y轴范围
            self.ax.set_xlim(min(self.Vg_values), max(self.Vg_values))
            self.ax.set_ylim(min(self.y_data_id) * 1.1, max(self.y_data_id) * 1.1)
            self.ax2.set_ylim(min(self.y_data_is) * 1.1, max(self.y_data_is) * 1.1)

            # 刷新图形
            plt.draw()
            plt.pause(0.1)

    def show_plot(self):
        '''显示最终图形'''
        self.update_data()
        plt.ioff()
        plt.show()


# 使用示例
Vg_values = [0, 0.1, 0.2, 0.3, 0.4]
Id_values = [1e-6, 2e-6, 3e-6, 4e-6, 5e-6]
Is_values = [0.5e-6, 1e-6, 1.5e-6, 2e-6, 2.5e-6]

# 创建 MOSFETMeasurement 实例并显示图形
measurement = MOSFETMeasurement(Vg_values, Id_values, Is_values)
measurement.show_plot()
