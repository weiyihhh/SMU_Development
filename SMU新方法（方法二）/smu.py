import nidcpower
import time
import csv

def smu_common_mode(smu_common_list):
    for smu_resource in smu_common_list:
        try:
            with nidcpower.Session(resource_name=smu_resource) as session:
                session.source_mode = nidcpower.SourceMode.SINGLE_POINT
                session.output_function = nidcpower.OutputFunction.DC_VOLTAGE
                session.current_limit_autorange = True
                session.voltage_level = 0
                print(f"Successfully configured SMU-COMMON: {smu_resource}")
        except Exception as e:
            print(f"Failed to configure SMU-COMMON: {smu_resource}. Error: {e}")


def CONST_SETTING(smu_const_mode):
    with nidcpower.Session(resource_name=smu_const_mode) as session_CONST:
        session_CONST.source_mode = nidcpower.SourceMode.SINGLE_POINT  # 设置为单点输出模式
        session_CONST.output_function = nidcpower.OutputFunction.DC_VOLTAGE  # 设置为直流电压输出
        session_CONST.voltage_level = voltage_CONST  # 设CONST端的电压
        session_CONST.current_limit = current_limit_CONST
        session_CONST.current_limit_autorange = True

        # 设置CONST1.PLC
        session_CONST.aperture_time_units = nidcpower.ApertureTimeUnits.POWER_LINE_CYCLES
        session_CONST.aperture_time = CONST_PLC


with open(output_path + output_file, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Step', 'V_VAR1', 'V_VAR2', 'V_CONST', 'I_VAR1', 'I_VAR2', 'I_CONST'])