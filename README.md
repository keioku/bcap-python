# b-CAP client library

## Sample code

```python
from bcap import BCapClient

# Select the protocol. The protocols that can be selected are tcp or udp.
client = BCapClient("tcp")

try:
    # Connect to b-CAP server.
    client.connect("192.168.0.1", 3.0)
    # Start b-CAP communication.
    client.service_start("WDT=400")
    # Execute AddController to connect RC8.
    controller_handle = client.controller_connect(
        "Controller0", "CaoProv.DENSO.RC8", "", "@IfNotMember"
    )
    # Execute AddRobot to control the robot.
    robot_handle = client.controller_get_robot(controller_handle, "Arm0", "@IfNotMember")
    # Motor off.
    client.controller_execute(controller_handle, "Motor", False)
    # AddVariable.
    lock_variable_handle = client.controller_get_variable(controller_handle, "@LOCK")
    # Get machine lock status.
    is_lock = client.variable_get_value(lock_variable_handle)
    # Enable machine lock.
    client.variable_put_value(lock_variable_handle, True)
    # TakeArm.
    client.robot_execute(robot_handle, "TakeArm")
    # Set external the speed to 10%.
    client.robot_execute(robot_handle, "ExtSpeed", 10)
    # Move the robot with NEXT option.
    client.robot_move(robot_handle, 1, [[0, 0, 90, 0, 0, 0], "J", "@P"], "NEXT")
    # Move the robot.
    client.robot_move(robot_handle, 1, [[0, 45, 90, 0, 45, 0], "J", "@P"], "")
    # GiveArm.
    client.robot_execute(robot_handle, "GiveArm")
    # Reset lock status.
    client.variable_put_value(lock_variable_handle, is_lock)
    # Release the robot resource.
    client.robot_release(robot_handle)
    # Release variable resource.
    client.variable_release(lock_variable_handle)
    # Release controller resource.
    client.controller_disconnect(controller_handle)
    # Stop b-CAP communication.
    client.service_stop()
finally:
    # Disconnect from b-CAP server.
    client.disconnect()
```
