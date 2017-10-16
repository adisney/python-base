import unittest
from mock import patch, MagicMock, Mock

def create_patch(test_case, patch_str, patch_obj=None, return_value=None):
    patcher = None
    if patch_obj:
        patcher = patch(patch_str, new=patch_obj)
    else:
        patcher = patch(patch_str, return_value=return_value)
    test_case.addCleanup(patcher.stop)
    return patcher.start()
