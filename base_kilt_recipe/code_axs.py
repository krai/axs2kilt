from distutils.version import LooseVersion as V

def stringify_version(version_list):
    return  V('.'.join([str(item) for item in version_list]))

def compare_sdk_versions(qaic_sdk_version, qaic_sdk_version_reference):
    if qaic_sdk_version:
        this_version = stringify_version(qaic_sdk_version)
        reference_version = stringify_version(qaic_sdk_version_reference)
        
        if this_version > reference_version:
            return 1
        elif this_version < reference_version: 
            return -1
        else:
            return 0
    else:
        return None
        
