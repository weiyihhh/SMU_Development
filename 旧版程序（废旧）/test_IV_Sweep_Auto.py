import IV_Sweep_Auto
"""smu模块选择"""
smu0 = 'PXI1Slot4/0'
smu1 = 'PXI1Slot4/1'
smu2 = 'PXI1Slot4/2'
smu3 = 'PXI1Slot4/3'

def main():

    VAR1 = smu0
    VAR2 = smu1
    CONST = smu2


    voltage_min_VAR1 = 0.5
    voltage_max_VAR1 = -1
    num_points_VAR1 = 101
    current_limit_VAR1 = 0.10  # 单位为A


    voltage_min_VAR2 = -0.1
    voltage_max_VAR2 = -0.6
    num_points_VAR2 = 2
    current_limit_VAR2 = 0.00003  # 单位为A


    voltage_CONST = 0
    current_limit_CONST = 0.1 # 单位为A


    VAR1_PLC = 5
    VAR2_PLC = 5
    CONST_PLC = 5

    sweep_mode = 'single' #设置扫描模式

    IV_Sweep_Auto.choose_sweep_mode(sweep_mode, VAR1, VAR2, CONST, num_points_VAR1, voltage_min_VAR1, voltage_max_VAR1,
                                    num_points_VAR2, voltage_min_VAR2, voltage_max_VAR2, voltage_CONST, current_limit_VAR1,
                                    current_limit_VAR2, current_limit_CONST, VAR1_PLC, VAR2_PLC, CONST_PLC)



if __name__ == '__main__':
    main()