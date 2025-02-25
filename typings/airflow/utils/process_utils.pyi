"""
This type stub file was generated by pyright.
"""

import signal
from collections.abc import Generator
from contextlib import contextmanager

from airflow.utils.platform import IS_WINDOWS

"""Utilities for running or stopping processes."""
if not IS_WINDOWS: ...
log = ...
DEFAULT_TIME_TO_WAIT_AFTER_SIGTERM = ...

def reap_process_group(
    process_group_id: int, logger, sig: signal.Signals = ..., timeout: int = ...
) -> dict[int, int]:
    """
    Send sig (SIGTERM) to the process group of pid.

    Tries really hard to terminate all processes in the group (including grandchildren). Will send
    sig (SIGTERM) to the process group of pid. If any process is alive after timeout
    a SIGKILL will be send.

    :param process_group_id: process group id to kill.
           The process that wants to create the group should run
           `airflow.utils.process_utils.set_new_process_group()` as the first command
           it executes which will set group id = process_id. Effectively the process that is the
           "root" of the group has pid = gid and all other processes in the group have different
           pids but the same gid (equal the pid of the root process)
    :param logger: log handler
    :param sig: signal type
    :param timeout: how much time a process has to terminate
    """
    ...

def execute_in_subprocess(
    cmd: list[str], cwd: str | None = ..., env: dict | None = ...
) -> None:
    """
    Execute a process and stream output to logger.

    :param cmd: command and arguments to run
    :param cwd: Current working directory passed to the Popen constructor
    :param env: Additional environment variables to set for the subprocess. If None,
        the subprocess will inherit the current environment variables of the parent process
        (``os.environ``)
    """
    ...

def execute_in_subprocess_with_kwargs(cmd: list[str], **kwargs) -> None:
    """
    Execute a process and stream output to logger.

    :param cmd: command and arguments to run

    All other keyword args will be passed directly to subprocess.Popen
    """
    ...

def execute_interactive(cmd: list[str], **kwargs) -> None:
    """
    Run the new command as a subprocess.

    Runs the new command as a subprocess and ensures that the terminal's state is restored to its original
    state after the process is completed e.g. if the subprocess hides the cursor, it will be restored after
    the process is completed.
    """
    ...

def kill_child_processes_by_pids(pids_to_kill: list[int], timeout: int = ...) -> None:
    """
    Kills child processes for the current process.

    First, it sends the SIGTERM signal, and after the time specified by the `timeout` parameter, sends
    the SIGKILL signal, if the process is still alive.

    :param pids_to_kill: List of PID to be killed.
    :param timeout: The time to wait before sending the SIGKILL signal.
    """
    ...

@contextmanager
def patch_environ(new_env_variables: dict[str, str]) -> Generator[None, None, None]:
    """
    Set environment variables in context.

    After leaving the context, it restores its original state.
    :param new_env_variables: Environment variables to set
    """
    ...

def check_if_pidfile_process_is_running(pid_file: str, process_name: str):  # -> None:
    """
    Check if a pidfile already exists and process is still running.

    If process is dead then pidfile is removed.

    :param pid_file: path to the pidfile
    :param process_name: name used in exception if process is up and
        running
    """
    ...

def set_new_process_group() -> None:
    """
    Try to set current process to a new process group.

    That makes it easy to kill all sub-process of this at the OS-level,
    rather than having to iterate the child processes.

    If current process was spawned by system call ``exec()``, the current
    process group is kept.
    """
    ...
