import IV_Sweep_Auto
import NiDcpower_SelfTest
import nidcpower

"""smu模块选择"""
smu0 = 'PXI1Slot5/0'
smu1 = 'PXI1Slot5/1'
smu2 = 'PXI1Slot5/2'
smu3 = 'PXI1Slot5/3'

def main():
    # 自检测部分参数设置
    device_name = "PXI1Slot5"
    file_name = '1'
    file_path = 'C:/Users/Administrator/Desktop/Yi.Wei_Data/'
    max_retries = 300  # 最大重复次数
    retry_count = 0  # 当前重复次数
    reset_num = 1
    selftest_num = 1
    selfcal_num = 1

    NiDcpower_SelfTest.SelfTest(device_name, max_retries, retry_count, reset_num, selftest_num, selfcal_num)
    VAR1 = smu0
    VAR2 = None
    CONST1 = None
    CONST2 = None
    smu_common_list = [smu1, smu2, smu3]

    voltage_min_VAR1 = -1
    voltage_max_VAR1 = 4
    num_points_VAR1 = 101
    current_limit_VAR1 = 0.1  # 单位为A


    voltage_min_VAR2 = 0.5
    voltage_max_VAR2 = 0.6
    num_points_VAR2 = 2
    current_limit_VAR2 = 0.1  # 单位为A


    voltage_CONST1 = 0
    voltage_CONST2 = 0
    current_limit_CONST1 = 0.1 # 单位为A
    current_limit_CONST2 = 0.1

    VAR1_PLC = 1
    VAR2_PLC = 1
    CONST1_PLC = 1
    CONST2_PLC = 1
    sweep_mode = 'double' #设置扫描模式
    while retry_count < max_retries:
        try:
            IV_Sweep_Auto.choose_sweep_mode(sweep_mode, VAR1, VAR2, CONST1, CONST2, num_points_VAR1, voltage_min_VAR1,
                                            voltage_max_VAR1,
                                            num_points_VAR2, voltage_min_VAR2, voltage_max_VAR2, voltage_CONST1,voltage_CONST2,
                                            current_limit_VAR1,
                                            current_limit_VAR2, current_limit_CONST1, current_limit_CONST2, VAR1_PLC, VAR2_PLC, CONST1_PLC, CONST2_PLC, smu_common_list, file_name, file_path)
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