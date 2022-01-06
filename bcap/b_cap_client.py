from typing import Union, Optional
from .b_cap_tcp import BCapTcp
from .b_cap_udp import BCapUdp


class BCapClient:
    def __init__(self, protocol: str, should_return_hr: bool = False):
        _protocol = protocol.lower()
        if _protocol == "tcp":
            self._b_cap_socket = BCapTcp(should_return_hr)
        elif _protocol == "udp":
            self._b_cap_socket = BCapUdp(should_return_hr)
        else:
            raise NotImplementedError()

    def __del__(self):
        self.disconnect()

    def connect(self, endpoint: str, timeout: float, retry=1) -> None:
        self._b_cap_socket.connect(endpoint, timeout, retry)

    def disconnect(self) -> None:
        try:
            self.service_stop()
        except Exception:
            pass
        
        self._b_cap_socket.disconnect()

    def set_timeout(self, timeout: float) -> None:
        self._b_cap_socket.set_timeout(timeout)

    def get_timeout(self) -> float:
        return self._b_cap_socket.get_timeout()

    def set_compression(self, enable: bool, level: int = -1) -> None:
        self._b_cap_socket.set_compression(enable, level)

    def service_start(self, option="") -> Optional[int]:
        return self._b_cap_socket.request(1, [option])

    def service_stop(self) -> Optional[int]:
        return self._b_cap_socket.request(2, [])

    def controller_connect(
        self, name: str, provider: str, machine: str, option: str
    ) -> Union[int, any]:
        return self._b_cap_socket.request(3, [name, provider, machine, option])

    def controller_disconnect(self, handle: int) -> Optional[int]:
        return self._b_cap_socket.request(4, [handle])

    def controller_get_extension(
        self, handle: int, name: str, option=""
    ) -> Union[int, any]:
        return self._b_cap_socket.request(5, [handle, name, option])

    def controller_get_file(self, handle: int, name: str, option="") -> Union[int, any]:
        return self._b_cap_socket.request(6, [handle, name, option])

    def controller_get_robot(
        self, handle: int, name: str, option=""
    ) -> Union[int, any]:
        return self._b_cap_socket.request(7, [handle, name, option])

    def controller_get_task(self, handle: int, name: str, option="") -> Union[int, any]:
        return self._b_cap_socket.request(8, [handle, name, option])

    def controller_get_variable(
        self, handle: int, name: str, option=""
    ) -> Union[int, any]:
        return self._b_cap_socket.request(9, [handle, name, option])

    def controller_get_command(
        self, handle: int, name: str, option=""
    ) -> Union[int, any]:
        return self._b_cap_socket.request(10, [handle, name, option])

    def controller_get_extension_names(self, handle: int, option="") -> any:
        return self._b_cap_socket.request(11, [handle, option])

    def controller_get_file_names(self, handle: int, option="") -> any:
        return self._b_cap_socket.request(12, [handle, option])

    def controller_get_robot_names(self, handle: int, option="") -> any:
        return self._b_cap_socket.request(13, [handle, option])

    def controller_get_task_names(self, handle: int, option="") -> any:
        return self._b_cap_socket.request(14, [handle, option])

    def controller_get_variable_names(self, handle: int, option="") -> any:
        return self._b_cap_socket.request(15, [handle, option])

    def controller_get_command_names(self, handle: int, option="") -> any:
        return self._b_cap_socket.request(16, [handle, option])

    def controller_execute(self, handle: int, command: str, param=None) -> any:
        return self._b_cap_socket.request(17, [handle, command, param])

    def controller_get_message(self, handle: int) -> Union[str, any]:
        return self._b_cap_socket.request(18, [handle])

    def controller_get_attribute(self, handle: int) -> any:
        return self._b_cap_socket.request(19, [handle])

    def controller_get_help(self, handle: int) -> any:
        return self._b_cap_socket.request(20, [handle])

    def controller_get_name(self, handle: int) -> Union[str, any]:
        return self._b_cap_socket.request(21, [handle])

    def controller_get_tag(self, handle: int) -> any:
        return self._b_cap_socket.request(22, [handle])

    def controller_put_tag(self, handle: int, new_val) -> any:
        return self._b_cap_socket.request(23, [handle, new_val])

    def controller_get_id(self, handle: int) -> any:
        return self._b_cap_socket.request(24, [handle])

    def controller_put_id(self, handle: int, new_val) -> any:
        return self._b_cap_socket.request(25, [handle, new_val])

    def extension_get_variable(
        self, handle: int, name: str, option=""
    ) -> Union[int, any]:
        return self._b_cap_socket.request(26, [handle, name, option])

    def extension_get_variable_names(self, handle: int, option="") -> any:
        return self._b_cap_socket.request(27, [handle, option])

    def extension_execute(self, handle: int, command: str, param=None) -> any:
        return self._b_cap_socket.request(28, [handle, command, param])

    def extension_get_attribute(self, handle: int) -> any:
        return self._b_cap_socket.request(29, [handle])

    def extension_get_help(self, handle: int) -> any:
        return self._b_cap_socket.request(30, [handle])

    def extension_get_name(self, handle: int) -> Union[str, any]:
        return self._b_cap_socket.request(31, [handle])

    def extension_get_tag(self, handle: int) -> any:
        return self._b_cap_socket.request(32, [handle])

    def extension_put_tag(self, handle: int, new_val) -> any:
        return self._b_cap_socket.request(33, [handle, new_val])

    def extension_get_id(self, handle: int) -> any:
        return self._b_cap_socket.request(34, [handle])

    def extension_put_id(self, handle: int, new_val) -> any:
        return self._b_cap_socket.request(35, [handle, new_val])

    def extension_release(self, handle: int) -> Optional[any]:
        return self._b_cap_socket.request(36, [handle])

    def file_get_file(self, handle: int, name: str, option="") -> Union[int, any]:
        return self._b_cap_socket.request(37, [handle, name, option])

    def file_get_variable(self, handle: int, name: str, option="") -> Union[int, any]:
        return self._b_cap_socket.request(38, [handle, name, option])

    def file_get_file_names(self, handle: int, option="") -> any:
        return self._b_cap_socket.request(39, [handle, option])

    def file_get_variable_names(self, handle: int, option="") -> any:
        return self._b_cap_socket.request(40, [handle, option])

    def file_execute(self, handle: int, command: str, param=None) -> any:
        return self._b_cap_socket.request(41, [handle, command, param])

    def file_copy(self, handle: int, name: str, option="") -> Optional[any]:
        return self._b_cap_socket.request(42, [handle, name, option])

    def file_delete(self, handle: int, option="") -> Optional[any]:
        return self._b_cap_socket.request(43, [handle, option])

    def file_move(self, handle: int, name: str, option="") -> Optional[any]:
        return self._b_cap_socket.request(44, [handle, name, option])

    def file_run(self, handle: int, option="") -> any:
        return self._b_cap_socket.request(45, [handle, option])

    def file_get_date_created(self, handle: int) -> any:
        return self._b_cap_socket.request(46, [handle])

    def file_get_date_last_accessed(self, handle: int) -> any:
        return self._b_cap_socket.request(47, [handle])

    def file_get_date_last_modified(self, handle: int) -> any:
        return self._b_cap_socket.request(48, [handle])

    def file_get_path(self, handle: int) -> any:
        return self._b_cap_socket.request(49, [handle])

    def file_get_size(self, handle: int) -> any:
        return self._b_cap_socket.request(50, [handle])

    def file_get_type(self, handle: int) -> any:
        return self._b_cap_socket.request(51, [handle])

    def file_get_value(self, handle: int) -> any:
        return self._b_cap_socket.request(52, [handle])

    def file_put_value(self, handle: int, new_val) -> Optional[any]:
        return self._b_cap_socket.request(53, [handle, new_val])

    def file_get_attribute(self, handle: int) -> any:
        return self._b_cap_socket.request(54, [handle])

    def file_get_help(self, handle: int) -> any:
        return self._b_cap_socket.request(55, [handle])

    def file_get_name(self, handle: int) -> any:
        return self._b_cap_socket.request(56, [handle])

    def file_get_tag(self, handle: int) -> any:
        return self._b_cap_socket.request(57, [handle])

    def file_put_tag(self, handle: int, new_val) -> Optional[any]:
        return self._b_cap_socket.request(58, [handle, new_val])

    def file_get_id(self, handle: int) -> any:
        return self._b_cap_socket.request(59, [handle])

    def file_put_id(self, handle: int, new_val) -> Optional[any]:
        return self._b_cap_socket.request(60, [handle, new_val])

    def file_release(self, handle: int) -> Optional[any]:
        return self._b_cap_socket.request(61, [handle])

    def robot_get_variable(self, handle: int, name: str, option="") -> Union[int, any]:
        return self._b_cap_socket.request(62, [handle, name, option])

    def robot_get_variable_names(self, handle: int, option="") -> any:
        return self._b_cap_socket.request(63, [handle, option])

    def robot_execute(self, handle: int, command: str, param=None) -> any:
        return self._b_cap_socket.request(64, [handle, command, param])

    def robot_accelerate(
        self, handle: int, axis: int, accel: float, decel: float
    ) -> Optional[any]:
        return self._b_cap_socket.request(65, [handle, axis, accel, decel])

    def robot_change(self, handle: int, name: str) -> Optional[any]:
        return self._b_cap_socket.request(66, [handle, name])

    def robot_chuck(self, handle: int, option="") -> Optional[any]:
        return self._b_cap_socket.request(67, [handle, option])

    def robot_drive(
        self, handle: int, axis: int, mov: float, option=""
    ) -> Optional[any]:
        return self._b_cap_socket.request(68, [handle, axis, mov, option])

    def robot_go_home(self, handle: int) -> Optional[any]:
        return self._b_cap_socket.request(69, [handle])

    def robot_halt(self, handle: int, option="") -> Optional[any]:
        return self._b_cap_socket.request(70, [handle, option])

    def robot_hold(self, handle: int, option="") -> Optional[any]:
        return self._b_cap_socket.request(71, [handle, option])

    def robot_move(self, handle: int, comp: int, pose: any, option="") -> Optional[any]:
        return self._b_cap_socket.request(72, [handle, comp, pose, option])

    def robot_rotate(
        self, handle: int, rotation_surface: any, degree: float, pivot: any, option=""
    ) -> Optional[any]:
        return self._b_cap_socket.request(
            73, [handle, rotation_surface, degree, pivot, option]
        )

    def robot_speed(self, handle: int, axis: int, speed: float) -> Optional[any]:
        return self._b_cap_socket.request(74, [handle, axis, speed])

    def robot_unchuck(self, handle: int, option="") -> Optional[any]:
        return self._b_cap_socket.request(75, [handle, option])

    def robot_unhold(self, handle: int, option="") -> Optional[any]:
        return self._b_cap_socket.request(76, [handle, option])

    def robot_get_attribute(self, handle: int) -> any:
        return self._b_cap_socket.request(77, [handle])

    def robot_get_help(self, handle: int) -> any:
        return self._b_cap_socket.request(78, [handle])

    def robot_get_name(self, handle: int) -> any:
        return self._b_cap_socket.request(79, [handle])

    def robot_get_tag(self, handle: int) -> any:
        return self._b_cap_socket.request(80, [handle])

    def robot_put_tag(self, handle: int, new_val) -> Optional[any]:
        return self._b_cap_socket.request(81, [handle, new_val])

    def robot_get_id(self, handle: int) -> any:
        return self._b_cap_socket.request(82, [handle])

    def robot_put_id(self, handle: int, new_val) -> Optional[any]:
        return self._b_cap_socket.request(83, [handle, new_val])

    def robot_release(self, handle: int) -> Optional[any]:
        return self._b_cap_socket.request(84, [handle])

    def task_get_variable(self, handle: int, name: str, option="") -> Union[int, any]:
        return self._b_cap_socket.request(85, [handle, name, option])

    def task_get_variable_names(self, handle: int, option="") -> any:
        return self._b_cap_socket.request(86, [handle, option])

    def task_execute(self, handle: int, command: str, param=None) -> any:
        return self._b_cap_socket.request(87, [handle, command, param])

    def task_start(self, handle: int, mode, option="") -> Optional[any]:
        return self._b_cap_socket.request(88, [handle, mode, option])

    def task_stop(self, handle: int, mode, option="") -> Optional[any]:
        return self._b_cap_socket.request(89, [handle, mode, option])

    def task_delete(self, handle: int, option="") -> any:
        return self._b_cap_socket.request(90, [handle, option])

    def task_get_file_name(self, handle: int) -> any:
        return self._b_cap_socket.request(91, [handle])

    def task_get_attribute(self, handle: int) -> any:
        return self._b_cap_socket.request(92, [handle])

    def task_get_help(self, handle: int) -> any:
        return self._b_cap_socket.request(93, [handle])

    def task_get_name(self, handle: int) -> any:
        return self._b_cap_socket.request(94, [handle])

    def task_get_tag(self, handle: int) -> any:
        return self._b_cap_socket.request(95, [handle])

    def task_put_tag(self, handle: int, new_val) -> Optional[any]:
        return self._b_cap_socket.request(96, [handle, new_val])

    def task_get_id(self, handle: int) -> any:
        return self._b_cap_socket.request(97, [handle])

    def task_put_id(self, handle: int, new_val) -> Optional[any]:
        return self._b_cap_socket.request(98, [handle, new_val])

    def task_release(self, handle: int) -> Optional[any]:
        return self._b_cap_socket.request(99, [handle])

    def variable_get_date_time(self, handle: int) -> any:
        return self._b_cap_socket.request(100, [handle])

    def variable_get_value(self, handle: int) -> Union[int, any]:
        return self._b_cap_socket.request(101, [handle])

    def variable_put_value(self, handle: int, new_val) -> Optional[any]:
        return self._b_cap_socket.request(102, [handle, new_val])

    def variable_get_attribute(self, handle: int) -> any:
        return self._b_cap_socket.request(103, [handle])

    def variable_get_help(self, handle: int) -> any:
        return self._b_cap_socket.request(104, [handle])

    def variable_get_name(self, handle: int) -> any:
        return self._b_cap_socket.request(105, [handle])

    def variable_get_tag(self, handle: int) -> any:
        return self._b_cap_socket.request(106, [handle])

    def variable_put_tag(self, handle: int, new_val) -> Optional[any]:
        return self._b_cap_socket.request(107, [handle, new_val])

    def variable_get_id(self, handle: int) -> any:
        return self._b_cap_socket.request(108, [handle])

    def variable_put_id(self, handle: int, new_val) -> Optional[any]:
        return self._b_cap_socket.request(109, [handle, new_val])

    def variable_get_microsecond(self, handle: int) -> any:
        return self._b_cap_socket.request(110, [handle])

    def variable_release(self, handle: int) -> Optional[any]:
        return self._b_cap_socket.request(111, [handle])

    def command_execute(self, handle: int, mode) -> Optional[any]:
        return self._b_cap_socket.request(112, [handle, mode])

    def command_cancel(self, handle: int) -> Optional[any]:
        return self._b_cap_socket.request(113, [handle])

    def command_get_timeout(self, handle: int) -> any:
        return self._b_cap_socket.request(114, [handle])

    def command_put_timeout(self, handle: int, new_val) -> Optional[any]:
        return self._b_cap_socket.request(115, [handle, new_val])

    def command_get_state(self, handle: int) -> any:
        return self._b_cap_socket.request(116, [handle])

    def command_get_parameters(self, handle: int) -> any:
        return self._b_cap_socket.request(117, [handle])

    def command_put_parameters(self, handle: int, new_val) -> Optional[any]:
        return self._b_cap_socket.request(118, [handle, new_val])

    def command_get_result(self, handle: int) -> any:
        return self._b_cap_socket.request(119, [handle])

    def command_get_attribute(self, handle: int) -> any:
        return self._b_cap_socket.request(120, [handle])

    def command_get_help(self, handle: int) -> any:
        return self._b_cap_socket.request(121, [handle])

    def command_get_name(self, handle: int) -> any:
        return self._b_cap_socket.request(122, [handle])

    def command_get_tag(self, handle: int) -> any:
        return self._b_cap_socket.request(123, [handle])

    def command_put_tag(self, handle: int, new_val) -> Optional[any]:
        return self._b_cap_socket.request(124, [handle, new_val])

    def command_get_id(self, handle: int) -> any:
        return self._b_cap_socket.request(125, [handle])

    def command_put_id(self, handle: int, new_val) -> Optional[any]:
        return self._b_cap_socket.request(126, [handle, new_val])

    def command_release(self, handle: int) -> Optional[any]:
        return self._b_cap_socket.request(127, [handle])

    def message_reply(self, handle: int, data) -> Optional[any]:
        return self._b_cap_socket.request(128, [handle, data])

    def message_clear(self, handle: int) -> Optional[any]:
        return self._b_cap_socket.request(129, [handle])

    def message_get_date_time(self, handle: int) -> any:
        return self._b_cap_socket.request(130, [handle])

    def message_get_description(self, handle: int) -> any:
        return self._b_cap_socket.request(131, [handle])

    def message_get_destination(self, handle: int) -> any:
        return self._b_cap_socket.request(132, [handle])

    def message_get_number(self, handle: int) -> any:
        return self._b_cap_socket.request(133, [handle])

    def message_get_serial_number(self, handle: int) -> any:
        return self._b_cap_socket.request(134, [handle])

    def message_get_source(self, handle: int) -> any:
        return self._b_cap_socket.request(135, [handle])

    def message_get_value(self, handle: int) -> any:
        return self._b_cap_socket.request(136, [handle])

    def message_release(self, handle: int) -> Optional[any]:
        return self._b_cap_socket.request(137, [handle])
