
def extract_v_i_names(*smu_configs):
    extracted_names = []

    for smu in smu_configs:
        if smu is None:
            continue

        function = smu.get("function")
        v_name = smu.get("v_name")
        i_name = smu.get("i_name")

        if function and v_name and i_name:
            extracted_names[function] = {"V": v_name, "I": i_name}

    return extracted_names