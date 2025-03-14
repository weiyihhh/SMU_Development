import IV_Sweep_Auto
import NiDcpower_SelfTest
import nidcpower

"""smu模块选择"""
smu1 = 'PXI1Slot2/0'
smu2 = 'PXI1Slot3/0'



#设置common端的smu通道：
smu_common_list = []
# 创建参数字典
params = {
    'VAR1': smu1,
    'VAR2': None,
    'CONST1': smu2, #CONST1的优先级是最高的，使用CONST的话，第一个开始使用CONST1，用两个的话，用CONST1和CONST2，三个才是CONST1、CONST2、CONST3
    'CONST2': None,
    'CONST3': None,
    'num_points_VAR1': 101,
    'voltage_min_VAR1': -1,
    'voltage_max_VAR1': 4,
    'current_limit_VAR1': 0.1,
    'VAR1_PLC': 1,

    'num_points_VAR2': 2,
    'voltage_min_VAR2': 0.5,
    'voltage_max_VAR2': 0.6,
    'current_limit_VAR2': 0.1,
    'VAR2_PLC': 1,

    'voltage_CONST1': 0,
    'current_limit_CONST1': 0.1,
    'CONST1_PLC': 1,

    'voltage_CONST2': 0,
    'current_limit_CONST2': 0.1,
    'CONST2_PLC': 1,

    'voltage_CONST3': 0,
    'current_limit_CONST3': 0.1,
    'CONST3_PLC': 1,

    'file_name': '1',
    'file_path': 'D:/user文件/mac备份/qq123/other/smu测试数据保存',

    'sweep_mode': 'double',
}

def main():
    # 自检测部分参数设置
    device_name = "PXI1Slot3"
    max_retries = 300  # 最大重复次数
    retry_count = 0  # 当前重复次数
    reset_num = 1
    selftest_num = 1
    selfcal_num = 0

    NiDcpower_SelfTest.SelfTest(device_name, max_retries, retry_count, reset_num, selftest_num, selfcal_num)

    retry_count = 0
    while retry_count < max_retries:
        try:
            IV_Sweep_Auto.choose_sweep_mode(**params)
            break
        except nidcpower.Error as e:
            print(f"Error happening: {e}")
            retry_count += 1
            if retry_count < max_retries:
                print(f"Retrying....({retry_count}/{max_retries})")
            else:
                print("Reached maximum number of retries. Mission failed.")

if __name__ == '__main__':
    main()
