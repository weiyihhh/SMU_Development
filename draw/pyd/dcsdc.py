import matplotlib.pyplot as plt
import numpy as np

def smu_plot(x_values, y_values, line_id):
    # 更新数据
    line_id.set_data(x_values, y_values)  # 更新电流数据的线条

    # 动态调整X轴和Y轴范围
    ax.set_xlim(min(x_values), max(x_values))  # 保证X轴显示整个范围
    ax.set_ylim(min(y_values) * 1.1, max(y_values) * 1.1)  # 动态调整左侧y轴范围

    # 刷新图形
    plt.draw()
    plt.pause(0.1)

# 在外部创建图形窗口
fig, ax = plt.subplots(figsize=(20, 12), facecolor='lightgray')

# 创建右侧y轴（仅创建一次）
ax2 = ax.twinx()

# 设置网格和坐标轴样式
ax.grid(True, which='both', axis='both', color='lightgray', linestyle='-', linewidth=0.7)  # 密集网格
ax.set_facecolor('white')  # 背景为白色
ax.tick_params(axis='both', which='major', labelsize=12)
ax2.tick_params(axis='both', which='major', labelsize=12)

# 初始化图例
ax.legend(loc='upper left')
ax2.legend(loc='upper right')

# 数据集和对应的标签
data_sets = [
    ([1, 2, 3, 4, 5], [1, 4, 9, 16, 25], 'Drain Current (Id)'),
    ([1, 2, 3, 4, 5], [1, 21, 31, 4, 5], 'New Line'),
    ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1], 'Third Line')
    # 添加更多的数据集
]

# 通过 `plt.cm` 获取 1000 个颜色
colors = plt.cm.viridis(np.linspace(0, 1, len(data_sets)))

# 循环创建和绘制每条线，自动为每条线设置不同的颜色
for idx, (x_values, y_values, label) in enumerate(data_sets):
    line_id, = ax.plot([], [], linestyle='-', color=colors[idx], linewidth=1.5, label=label)  # 自动设置颜色
    smu_plot(x_values, y_values, line_id)

# 最终显示图形
plt.show()
