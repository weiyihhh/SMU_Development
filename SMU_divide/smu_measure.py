import nidcpower
import smu_config
def smu_const_measure(smu_const):
    const_flag = smu_const.create_session().get("CONST_FLAG")
    if const_flag == 1:
        # 执行测量CONST1电流
        current_value_CONST1 = smu_const.session_CONST1.measure(nidcpower.MeasurementTypes.CURRENT)
        voltage_value_CONST1 = 0
        return {
            "current_value_CONST1":current_value_CONST1,
            "voltage_value_CONST1": 0
        }
    elif const_flag == 2:
        # 执行测量CONST1电流
        current_value_CONST1 = smu_const.session_CONST1.measure(nidcpower.MeasurementTypes.CURRENT)
        voltage_value_CONST1 = smu_const.voltage_CONST1
        return {
            "current_value_CONST1": current_value_CONST1,
            "voltage_value_CONST1": voltage_value_CONST1
        }
    elif const_flag == 3: #'I'模式
        # 执行测量CONST1电压
        voltage_value_CONST1 = smu_const.session_CONST1.measure(nidcpower.MeasurementTypes.VOLTAGE)
        current_value_CONST1 = smu_const.current_CONST1
        return {
            "current_value_CONST1": current_value_CONST1,
            "voltage_value_CONST1": voltage_value_CONST1
        }
    elif const_flag == 4:
        # 执行测量CONST2电流
        current_value_CONST2 = smu_const.session_CONST2.measure(nidcpower.MeasurementTypes.CURRENT)
        voltage_value_CONST2 = 0
        return {
            "current_value_CONST2": current_value_CONST2,
            "voltage_value_CONST2": voltage_value_CONST2
        }
    elif const_flag == 5:
        # 执行测量CONST2电流
        current_value_CONST2 = smu_const.session_CONST2.measure(nidcpower.MeasurementTypes.CURRENT)
        voltage_value_CONST2 = smu_const.voltage_CONST2
        return {
            "current_value_CONST2": current_value_CONST2,
            "voltage_value_CONST2": voltage_value_CONST2
        }
    elif const_flag == 6:
        # 执行测量CONST2电压
        voltage_value_CONST2 = smu_const.session_CONST2.measure(nidcpower.MeasurementTypes.VOLTAGE)
        current_value_CONST2 = smu_const.current_CONST2
        return {
            "current_value_CONST2": current_value_CONST2,
            "voltage_value_CONST2": voltage_value_CONST2
        }
    elif const_flag == 7:
        # 执行测量CONST3电流
        current_value_CONST3 = smu_const.session_CONST3.measure(nidcpower.MeasurementTypes.CURRENT)
        voltage_value_CONST3 = 0
        return {
            "current_value_CONST3": current_value_CONST3,
            "voltage_value_CONST3": voltage_value_CONST3
        }
    elif const_flag == 8:
        # 执行测量CONST3电流
        current_value_CONST3 = smu_const.session_CONST3.measure(nidcpower.MeasurementTypes.CURRENT)
        voltage_value_CONST3 = smu_const.voltage_CONST3
        return {
            "current_value_CONST3": current_value_CONST3,
            "voltage_value_CONST3": voltage_value_CONST3
        }
    elif const_flag == 9:
        # 执行测量CONST3电压
        voltage_value_CONST3 = smu_const.session_CONST3.measure(nidcpower.MeasurementTypes.VOLTAGE)
        current_value_CONST3 = smu_const.current_CONST3
        return {
            "current_value_CONST3": current_value_CONST3,
            "voltage_value_CONST3": voltage_value_CONST3
        }
