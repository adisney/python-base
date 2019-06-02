from asynctest import patch


def start_patch(testcase, patch_on=None, to_patch=None, *, target=None, **kwargs):
    if not(target):
        target = f"{patch_on.__module__}.{to_patch.__name__}"
    p = patch(target, **kwargs)
    testcase.addCleanup(p.stop)
    return p.start()
