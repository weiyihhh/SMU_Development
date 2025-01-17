import IV_Sweep
smu0 = 'PXI1Slot3/0'
smu1 = 'PXI1Slot2/0'
smu2 = 'PXI1Slot5/2'
smu3 = 'PXI1Slot5/3'

def main():

    VAR1 = smu0
    VAR2 = None
    CONST = smu1


    voltage_min_VAR1 = 0.05
    voltage_max_VAR1 = -0.9
    num_points_VAR1 = 101
    current_limit_VAR1 = 0.00010  # 单位为A
    current_limit_range_VAR1 = 0.00010  # 单位为A，uA为0.000001A， 有10uA、100uA、1mA、10mA、100mA可供选择


    voltage_min_VAR2 = -0.05
    voltage_max_VAR2 = -0.55
    num_points_VAR2 = 3
    current_limit_VAR2 = 0.000010  # 单位为A
    current_limit_range_VAR2 = 0.000010  # 单位为A，uA为0.000001A， 有10uA、100uA、1mA、10mA、100mA可供选择

    voltage_CONST = 0
    current_limit_CONST = 0.001 # 单位为A
    current_limit_range_CONST = 0.001 # 单位为A，uA为0.000001A， 有10uA、100uA、1mA、10mA、100mA可供选择

    VAR1_PLC = 1
    VAR2_PLC = 1
    CONST_PLC = 1

    sweep_mode = 'single' #设置扫描模式

    IV_Sweep.choose_sweep_mode(sweep_mode, VAR1, VAR2, CONST, num_points_VAR1, voltage_min_VAR1, voltage_max_VAR1,
                               num_points_VAR2, voltage_min_VAR2, voltage_max_VAR2, voltage_CONST, current_limit_VAR1,
                               current_limit_VAR2, current_limit_CONST, current_limit_range_VAR1,
                               current_limit_range_VAR2, current_limit_range_CONST, VAR1_PLC, VAR2_PLC, CONST_PLC)



if __name__ == '__main__':
    main()