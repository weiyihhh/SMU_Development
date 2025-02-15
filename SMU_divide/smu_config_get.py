import smu_config
"""
IV-flag 解释：  =1：VAR1 V single
               =2: VAR1 V double
               =3: VAR1 I single
               =4: VAR1 I double
               =5: VAR2 V 
               =6: VAR2 I
               =7: CONST1 V
               =8: CONST1 I
               =9: CONST2 V
               =10: CONST2 I
               =11: CONST3 V
               =12: CONST3 I
"""
def config_get(smu):
    smu_params = smu_config.SmuChannelConfig(**smu)
    if smu_params.function == 'VAR1':
        if smu_params.mode == 'V':
            if smu_params.sweep_mode == 'single':
                voltage_step_VAR1 = round((smu_params.voltage_max_VAR1 - smu_params.voltage_min_VAR1) / (smu_params.num_points_VAR1 - 1), 8)
                num_points_VAR1 = smu_params.num_points_VAR1
                voltage_max_VAR1 = smu_params.voltage_max_VAR1
                voltage_min_VAR1 = smu_params.voltage_min_VAR1
                return {'step':voltage_step_VAR1,'points': num_points_VAR1,'IV_flag' : 1, 'voltage_max_VAR1':voltage_max_VAR1,'voltage_min_VAR1':voltage_min_VAR1}
            elif smu_params.sweep_mode == 'double':
                voltage_step_VAR1 = round((smu_params.voltage_max_VAR1 - smu_params.voltage_min_VAR1) / (smu_params.num_points_VAR1 - 1), 8)
                num_points_VAR1 = smu_params.num_points_VAR1
                voltage_max_VAR1 = smu_params.voltage_max_VAR1
                voltage_min_VAR1 = smu_params.voltage_min_VAR1
                return {'step': voltage_step_VAR1, 'points': num_points_VAR1, 'IV_flag' : 2, 'voltage_max_VAR1':voltage_max_VAR1,'voltage_min_VAR1':voltage_min_VAR1}
        elif smu_params.mode == 'I':
            if smu_params.sweep_mode == 'single':
                current_step_VAR1 = round((smu_params.current_max_VAR1 - smu_params.current_min_VAR1) / (smu_params.num_points_VAR1 - 1),8)
                num_points_VAR1 = smu_params.num_points_VAR1
                current_max_VAR1 = smu_params.current_max_VAR1
                current_min_VAR1 = smu_params.current_min_VAR1
                return {'step': current_step_VAR1, 'points': num_points_VAR1, 'IV_flag': 3,  'current_max_VAR1':current_max_VAR1,'current_min_VAR1':current_min_VAR1}
            elif smu_params.sweep_mode == 'double':
                current_step_VAR1 = round((smu_params.current_max_VAR1 - smu_params.current_min_VAR1) / (smu_params.num_points_VAR1 - 1), 8)
                num_points_VAR1 = smu_params.num_points_VAR1
                current_max_VAR1 = smu_params.current_max_VAR1
                current_min_VAR1 = smu_params.current_min_VAR1
                return {'step': current_step_VAR1,  'points': num_points_VAR1, 'IV_flag': 4, 'current_max_VAR1':current_max_VAR1,'current_min_VAR1':current_min_VAR1}
        else:
            print("Error:SMU function error!")
    elif smu_params.function == 'VAR2':
        if smu_params.mode == 'V':
            voltage_step_VAR2 = round((smu_params.voltage_max_VAR2 - smu_params.voltage_min_VAR2) / (smu_params.num_points_VAR2 - 1), 8)
            num_points_VAR2 = smu_params.num_points_VAR2
            voltage_max_VAR2 = smu_params.voltage_max_VAR2
            voltage_min_VAR2 = smu_params.voltage_min_VAR2
            return {'step': voltage_step_VAR2, 'points': num_points_VAR2, 'IV_flag': 5, 'voltage_max_VAR2':voltage_max_VAR2,'voltage_min_VAR2':voltage_min_VAR2}
        elif smu_params.mode == 'I':
            current_step_VAR2 = round((smu_params.current_max_VAR2 - smu_params.current_min_VAR2) / (smu_params.num_points_VAR2 - 1), 8)
            num_points_VAR2 = smu_params.num_points_VAR2
            current_max_VAR2 = smu_params.current_max_VAR2
            current_min_VAR2 = smu_params.current_min_VAR2
            return {'step': current_step_VAR2, 'points': num_points_VAR2, 'IV_flag': 6,'current_max_VAR2':current_max_VAR2,'current_min_VAR2':current_min_VAR2}
        else:
            print("Error:SMU function error!")
        print()
    elif smu_params.function == 'CONST1':
        if smu_params.mode == 'V':
            voltage_CONST1 = smu_params.voltage_CONST1
            return {'level': voltage_CONST1, 'IV_flag': 7}
        elif smu_params.mode == 'I':
            current_CONST1 = smu_params.current_CONST1
            return {'level': current_CONST1, 'IV_flag': 8}
    elif smu_params.function == 'CONST2':
        if smu_params.mode == 'V':
            voltage_CONST2 = smu_params.voltage_CONST2
            return {'level': voltage_CONST2, 'IV_flag': 9}
        elif smu_params.mode == 'I':
            current_CONST2 = smu_params.current_CONST2
            return {'level': current_CONST2, 'IV_flag': 10}
    elif smu_params.function == 'CONST3':
        if smu_params.mode == 'V':
            voltage_CONST3 = smu_params.voltage_CONST3
            return {'level': voltage_CONST3, 'IV_flag': 11}
        elif smu_params.mode == 'I':
            current_CONST3 = smu_params.current_CONST3
            return {'level': current_CONST3, 'IV_flag': 12}