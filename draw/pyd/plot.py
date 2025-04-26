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

def plot_fig():
    # 如果没有传入fig和ax，创建一个新的图形窗口
    fig, ax = plt.subplots(figsize=(20, 12), facecolor='lightgray')
    ax.set_title("SMU Test Curve", fontsize=20, fontweight='bold')
    ax.set_xlabel("-----x-------", fontsize=14)
    ax.set_ylabel("-----y-------", fontsize=14)

    # 设置网格和坐标轴样式
    ax.grid(True, which='both', axis='both', color='lightgray', linestyle='-', linewidth=0.7)  # 密集网格
    ax.set_facecolor('white')  # 背景为白色
    ax.tick_params(axis='both', which='major', labelsize=12)
    return fig, ax


def line_color(line_nums, ax):
    # 使用 'viridis' 颜色映射，根据线条数量生成对应数量的颜色
    colors = plt.cm.viridis(np.linspace(0, 1, line_nums))  # 使用 'viridis' 颜色映射

    # 创建空的线条对象
    line_ids = []  # 用于存储每条线的 id
    for idx in range(line_nums):
        # 为每条线分配不同的颜色，并创建一个空的线条（没有数据）
        line_id, = ax.plot([], [], linestyle='-', color=colors[idx], linewidth=1.5, label=f"Line {idx + 1}")
        line_ids.append(line_id)

    return line_ids, colors  # 返回所有线条的 id 和颜色

def smu_plot(x_values, y_values, line_id, ax, fig):

    # 初始化数据
    x_data = []  # x轴数据
    y_data = []  # y轴数据

    # 更新数据
    line_id.set_data(x_values, y_values)  # 更新电流数据的线条

    # 动态调整X轴和Y轴范围
    ax.set_xlim(min(x_values), max(x_values))  # 保证X轴显示整个范围
    ax.set_ylim(min(y_values) * 1.1, max(y_values) * 1.1)  # 动态调整左侧y轴范围

    # 刷新图形
    plt.draw()
    plt.pause(0.1)

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

    simulate_measurement()

    # 关闭交互模式
    plt.ioff()
    plt.show()

    return fig, ax  # 返回fig和ax以便后续使用

"""# 示例调用：
# 初次调用，创建图形
fig, ax = smu_plot(x_values, y_values)

# 后续调用，更新图形
fig, ax = smu_plot(new_x_values, new_y_values, fig, ax)
"""