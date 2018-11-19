import unittest
from mock import patch, MagicMock, Mock
import asynctest

def create_patch(test_case, patch_str, patch_obj=None, return_value=None, *args, **kwargs):
    patcher = None
    if patch_obj:
        patcher = patch(patch_str, new=patch_obj, *args, **kwargs)
    else:
        patcher = patch(patch_str, return_value=return_value, *args, **kwargs)
    test_case.addCleanup(patcher.stop)
    return patcher.start()



def create_async_patch(test_case, patch_str, patch_obj=None, return_value=None, *args, **kwargs):
    patcher = None
    if patch_obj:
        patcher = asynctest.patch(patch_str, new=patch_obj, *args, **kwargs)
    else:
        patcher = asynctest.patch(patch_str, return_value=return_value, *args, **kwargs)
    test_case.addCleanup(patcher.stop)
    return patcher.start()
