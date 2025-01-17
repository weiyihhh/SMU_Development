import nidcpower
import time


device_name = "PXI1Slot2"
max_retries = 30  # 最大重复次数
retry_count = 0  # 当前重复次数
reset_num = 1
selftest_num = 5
selfcal_num = 1
def SelfTest(device_name, max_retries, retry_count, reset_num, selftest_num, selfcal_num):
    while retry_count < max_retries:
        try:
            for i in range(reset_num):
                with nidcpower.Session(resource_name=device_name) as session_SMU:
                    session_SMU.reset_device()
                    print(f"{device_name} self_reset completed for {i + 1}.")
                    time.sleep(0.2)
            print("_______Finished Self_Reset_______\n")
            time.sleep(0.1)
            # 如果整个for循环完成而没有引发异常，则退出while循环
            break
        except nidcpower.Error as e:
            print(f"NI-DCPower error during Self_Reset: {e}")
            retry_count += 1  # 增加重复次数
            if retry_count < max_retries:
                print(f"Retrying self_reset... ({retry_count}/{max_retries})")
                time.sleep(2)  # 在重试之前等待一段时间
            else:
                print("Reached maximum number of retries. SelfReset failed.")
    # 注意：如果while循环因为达到最大重复次数而退出，则下面的代码将执行
    # 但如果因为for循环成功完成而没有异常而退出，则下面的代码也将执行
    print("SelfReset process completed (either successfully or after retries).")

    while retry_count < max_retries:
        try:
            for i in range(selftest_num):
                with nidcpower.Session(resource_name=device_name) as session_SMU:
                    session_SMU.self_test()
                    print(f"{device_name} self_test completed for {i + 1}.")
                    time.sleep(0.2)
            print("_______Finished Self_Test_______\n")
            time.sleep(0.1)
            # 如果整个for循环完成而没有引发异常，则退出while循环
            break
        except nidcpower.Error as e:
            print(f"NI-DCPower error during SelfTest: {e}")
            retry_count += 1  # 增加重复次数
            if retry_count < max_retries:
                print(f"Retrying self_test... ({retry_count}/{max_retries})")
                time.sleep(1)  # 在重试之前等待一段时间
            else:
                print("Reached maximum number of retries. SelfTest failed.")
    # 注意：如果while循环因为达到最大重复次数而退出，则下面的代码将执行
    # 但如果因为for循环成功完成而没有异常而退出，则下面的代码也将执行
    print("SelfTest process completed (either successfully or after retries).")

    while retry_count < max_retries:
        try:
            for i in range(selfcal_num):
                with nidcpower.Session(resource_name=device_name) as session_SMU:
                    session_SMU.self_cal()
                    print(f"{device_name} self_cal completed for {i + 1}.")
                    time.sleep(0.2)
            print("_______Finished Self_Cal_______\n")
            time.sleep(0.1)
            # 如果整个for循环完成而没有引发异常，则退出while循环
            break
        except nidcpower.Error as e:
            print(f"NI-DCPower error during SelfCal: {e}")
            retry_count += 1  # 增加重复次数
            if retry_count < max_retries:
                print(f"Retrying self_cal... ({retry_count}/{max_retries})")
                time.sleep(1)  # 在重试之前等待一段时间
            else:
                print("Reached maximum number of retries. SelfCal failed.")
    # 注意：如果while循环因为达到最大重复次数而退出，则下面的代码将执行
    # 但如果因为for循环成功完成而没有异常而退出，则下面的代码也将执行
    print("SelfCal process completed (either successfully or after retries).")
    print("\n\n\n____________________Successfully prepared for testing!____________________\n\n\n")

    #结束会话
    nidcpower.Session(resource_name=device_name).abort()


if __name__ == "__main__":
    # 调用函数开始执行
    SelfTest(device_name, max_retries, retry_count, reset_num, selftest_num, selfcal_num)


