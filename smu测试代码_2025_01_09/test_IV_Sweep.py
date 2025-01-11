
import NiDcpower_SelfTest
import nidcpower

smu1 = 'PXI1Slot5/0'
smu2 = 'PXI1Slot5/1'
smu3 = 'PXI1Slot5/2'
smu4 = 'PXI1Slot5/3'
# 创建参数字典
def get_params(VAR1 = 'PXI1Slot5/0',VAR2 = None, CONST1 = None, CONST2 = None, CONST3 = None, num_points_VAR1 = 101,voltage_min_VAR1=-1,voltage_max_VAR1 = 4,
               current_limit_VAR1 = 0.1, current_limit_range_VAR1 = 0.1, VAR1_PLC=1,num_points_VAR2=2,voltage_min_VAR2=0.5,voltage_max_VAR2=0.6,current_limit_VAR2=0.1,
               current_limit_range_VAR2 =0.1, VAR2_PLC=1, voltage_CONST1 = 0, current_limit_CONST1 = 0.1,current_limit_range_CONST1=0.1,CONST1_PLC =1,
               voltage_CONST2 = 0,current_limit_CONST2=0.1,current_limit_range_CONST2 =0.1,CONST2_PLC =1,voltage_CONST3 = 0,CONST3_PLC =1,current_limit_CONST3= 0.1,
               current_limit_range_CONST3 = 0.3,smu_common = ['PXI1Slot5/1','PXI1Slot5/2','PXI1Slot5/3'],file_name = '1',
               file_path = 'C:/Users/Administrator/Desktop/Yi.Wei_Data/',sweep_mode = 'double'):
    params = {
        'VAR1': VAR1,
        'VAR2': VAR2,
        'CONST1': CONST1, #CONST1的优先级是最高的，使用CONST的话，第一个开始使用CONST1，用两个的话，用CONST1和CONST2，三个才是CONST1、CONST2、CONST3
        'CONST2': CONST2,
        'CONST3': CONST3,
        'num_points_VAR1': num_points_VAR1,
        'voltage_min_VAR1': voltage_min_VAR1,
        'voltage_max_VAR1': voltage_max_VAR1,
        'current_limit_VAR1': current_limit_VAR1,
        'current_limit_range_VAR1':current_limit_range_VAR1,
        'VAR1_PLC': VAR1_PLC,

        'num_points_VAR2': num_points_VAR2,
        'voltage_min_VAR2': voltage_min_VAR2,
        'voltage_max_VAR2': voltage_max_VAR2,
        'current_limit_VAR2': current_limit_VAR2,
        'current_limit_range_VAR2': current_limit_range_VAR2,
        'VAR2_PLC': VAR2_PLC,

        'voltage_CONST1': voltage_CONST1,
        'current_limit_CONST1': current_limit_CONST1,
        'current_limit_range_CONST1': current_limit_range_CONST1,
        'CONST1_PLC': CONST1_PLC,

        'voltage_CONST2':voltage_CONST2,
        'current_limit_CONST2':current_limit_CONST2,
        'current_limit_range_CONST2': current_limit_range_CONST2,
        'CONST2_PLC': CONST2_PLC,

        'voltage_CONST3':voltage_CONST3,
        'current_limit_CONST3': current_limit_CONST3,
        'current_limit_range_CONST3':current_limit_range_CONST3,
        'CONST3_PLC': CONST3_PLC,

        #设置common端的smu通道：
        'smu_common': smu_common,
        'file_name': file_name,
        'file_path': file_path,

        'sweep_mode': sweep_mode,
    }
    return params
def test_begin(device_name = "PXI1Slot5",max_retries = 300, retry_count = 0 , reset_num = 1, selftest_num = 1, selfcal_num = 1,):
    # 自检测部分参数设置
    params = get_params()
    NiDcpower_SelfTest.SelfTest(device_name, max_retries, retry_count, reset_num, selftest_num, selfcal_num)
    retry_count = 0
    while retry_count < max_retries:
        try:
            from IV_Sweep import choose_sweep_mode
            choose_sweep_mode(**params)
            break
        except nidcpower.Error as e:
            print(f"Error happening: {e}")
            retry_count += 1
            if retry_count < max_retries:
                print(f"Retrying....({retry_count}/{max_retries})")
            else:
                print("Reached maximum number of retries. Mission failed.")

