import matplotlib.pyplot as plt

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



# 设置网格和坐标轴样式
ax.grid(True, which='both', axis='both', color='lightgray', linestyle='-', linewidth=0.7)  # 密集网格
ax.set_facecolor('white')  # 背景为白色
ax.tick_params(axis='both', which='major', labelsize=12)


# 调用 smu_plot 多次，添加新的线条
x_values1 = [1, 2, 3, 4, 5]
y_values1 = [1, 4, 9, 16, 25]
line_id1, = ax.plot([], [], linestyle='-', color='orange', linewidth=1.5, label="Drain Current (Id)")  # Id的橘色线条
smu_plot(x_values1, y_values1, line_id1)

x_values2 = [1, 2, 3, 4, 5]
y_values2 = [1, 21, 31, 4, 5]
line_id2, = ax.plot([], [], linestyle='-', color='green', linewidth=1.5, label="New Line")  # 绿色线条
smu_plot(x_values2, y_values2, line_id2)

x_values3 = [1, 2, 3, 4, 5]
y_values3 = [5, 4, 3, 2, 1]
line_id3, = ax.plot([], [], linestyle='-', color='purple', linewidth=1.5, label="Third Line")  # 紫色线条
smu_plot(x_values3, y_values3, line_id3)

# 最终显示图形
plt.show()
