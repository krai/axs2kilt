import xml.etree.ElementTree as ET

def detect_qaic_api_version(path_to_platform, sdk_version_list):
    sdk_version_list_str = []
    sdk_version_part_1 = sdk_version_list[0]
    sdk_version_part_2 = sdk_version_list[1]
    sdk_version_list.pop(3)

    sdk_version_list_str = [str(item) for item in sdk_version_list]
    sdk_version_list_str[2] = "X"
    separator = "_"
    sdk_qaic_sdk_version = separator.join(sdk_version_list_str)
    
    if sdk_version_part_1 == 1:
       if sdk_version_part_2 >= 11:
           sdk_qaic_sdk_version = "1_11_X"
    elif sdk_version_part_1 > 1:
        sdk_qaic_sdk_version = "1_11_X"
    return sdk_qaic_sdk_version
