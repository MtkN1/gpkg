import platform


def get_machine() -> str:
    machine = platform.machine()
    if not machine:
        raise ValueError("Failed to get machine")
    return machine


def get_libcname() -> str:
    libcname, _ = platform.libc_ver()
    if not libcname:
        raise ValueError("Failed to get C library name")
    return libcname
