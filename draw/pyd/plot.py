import numpy as np
import matplotlib.pyplot as plt

#解包函数
def extract_v_i(measurement_data):
    """
    从 SMU 测量数据中提取指定的

    :param measurement_data: list, 包含多个测量数据字典
    :return: Vg_values, Id_values, Is_values（如果 I_VAR2 存在）
    """
    V_VAR1_values = []
    I_VAR1_values = []
    V_VAR2_values = []
    I_VAR2_values = []
    V_CONST1_values = []
    I_CONST1_values = []
    V_CONST2_values = []
    I_CONST2_values = []
    V_CONST3_values = []
    I_CONST3_values = []
    for entry in measurement_data:
        # 提取电压和电流
        if "V_VAR1" in entry and "I_VAR1" in entry:
            V_VAR1_values.append(entry["V_VAR1"])
            I_VAR1_values.append(entry["I_VAR1"])

        if "V_VAR2" in entry and "I_VAR2" in entry:
            V_VAR2_values.append(entry["V_VAR2"])
            I_VAR2_values.append(entry["I_VAR2"])

        if "V_CONST1" in entry and "I_CONST1" in entry:
            V_CONST1_values.append(entry["V_CONST1"])
            I_CONST1_values.append(entry["I_CONST1"])

        if "V_CONST2" in entry and "I_CONST2" in entry:
            V_CONST2_values.append(entry["V_CONST2"])
            I_CONST2_values.append(entry["I_CONST2"])

        if "V_CONST3" in entry and "I_CONST3" in entry:
            V_CONST3_values.append(entry["V_CONST3"])
            I_CONST3_values.append(entry["I_CONST3"])

    return V_VAR1_values, I_VAR1_values, V_VAR2_values, I_VAR2_values, V_CONST1_values, I_CONST1_values, V_CONST2_values, I_CONST2_values, V_CONST3_values, I_CONST3_values





def smu_plot(x_values, y_values):

    # 设置图形窗口
    fig, ax = plt.subplots(figsize=(20, 12), facecolor='lightgray')  # 背景色为浅灰色
    ax.set_title("SMU Test Curve", fontsize=20, fontweight='bold')
    ax.set_xlabel("-----x-------", fontsize=14)
    ax.set_ylabel("-----y-------", fontsize=14)

    # 创建右侧y轴
    ax2 = ax.twinx()

    # 设置网格和坐标轴样式
    ax.grid(True, which='both', axis='both', color='lightgray', linestyle='-', linewidth=0.7)  # 密集网格
    ax.set_facecolor('white')  # 背景为白色
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax2.tick_params(axis='both', which='major', labelsize=12)

    # 初始化数据
    x_data = []
    y_data = []  # 用于Id数据


    # 初始化图形线条，颜色改为橘色和绿色
    line_id, = ax.plot([], [], linestyle='-', color='orange', linewidth=1.5, label="Drain Current (Id)")  # Id的橘色线条
    line_is, = ax2.plot([], [], linestyle='-', color='blue', linewidth=1.5, label="Source Current (Is)")  # Is的蓝色线条

    # 启动交互式绘图
    plt.ion()

    # 模拟实时数据更新并绘图
    def simulate_measurement():
        for i, (x, y) in enumerate(zip(x_values, y_values)):
            # 更新数据
            x_data.append(x)
            y_data.append(y)

            # 更新图形数据
            line_id.set_data(x_data, y_data)

            # 动态调整X轴和Y轴范围
            ax.set_xlim(min(x_values), max(x_values))  # 保证X轴显示整个范围
            ax.set_ylim(min(y_data) * 1.1, max(y_data) * 1.1)  # 动态调整左侧y轴范围

            # 刷新图形
            plt.draw()
            plt.pause(0.1)

        # 添加图例
        ax.legend(loc='upper left')
        ax2.legend(loc='upper right')

    simulate_measurement()

    # 关闭交互模式
    plt.ioff()
    plt.show()
