from __future__ import annotations

import time
from typing import Any, Callable, Dict, List

from main_server.infrastructure.robot_bridge.robot_communicator import IRobotCommunicator


class MockRobotCommunicator(IRobotCommunicator):
    """In-memory robot communicator for local simulation and tests.

    The mock keeps every published command/event in lists so a test can assert
    the server generated the expected robot payloads without requiring ROS,
    rosbridge, or a physical robot.
    """

    def __init__(self, host: str = "localhost", port: int = 6000):
        self.host = host
        self.port = port
        self.is_connected = False
        self.action_sequences: list[dict[str, Any]] = []
        self.obstacle_messages: list[dict[str, Any]] = []
        self.employee_messages: list[dict[str, Any]] = []
        self.cancelled_tasks: list[str] = []
        self._status_callbacks: dict[str, Callable[[dict[str, Any]], Any]] = {}
        print(f"Mock Robot Communicator: {host}:{port} simulation mode.")

    def connect(self):
        self.is_connected = True
        print("Mock Robot Communicator connected.")

    def disconnect(self):
        self.is_connected = False
        print("Mock Robot Communicator disconnected.")

    def send_action_sequence(
        self,
        robot_name: str,
        actions: List[Dict[str, Any]],
        task_id: int | None = None,
    ):
        if not self.is_connected:
            raise RuntimeError("MockRobotCommunicator is not connected")

        record = {
            "robot_name": robot_name,
            "task_id": task_id,
            "actions": actions,
            "timestamp": time.time(),
        }
        self.action_sequences.append(record)
        print(f"--- [Mock] '{robot_name}' Action Sequence ---")
        for action in actions:
            print(f"  - {action}")
        print("------------------------------------------")

    def publish_obstacle_info(self, robot_name: str, obstacle_data: Dict[str, Any]):
        self.obstacle_messages.append(
            {
                "robot_name": robot_name,
                "payload": obstacle_data,
                "timestamp": time.time(),
            }
        )

    def publish_employee_result(self, robot_name: str, result_data: Dict[str, Any]):
        self.employee_messages.append(
            {
                "robot_name": robot_name,
                "payload": result_data,
                "timestamp": time.time(),
            }
        )

    def listen_for_status(self, callback: Any):
        self._status_callbacks["*"] = callback
        print("[Mock] Waiting for robot status...")

    def listen_for_robot_status(self, robot_name: str, callback: Any):
        self._status_callbacks[robot_name] = callback
        print(f"[Mock] Waiting for robot status: {robot_name}")

    def emit_status(self, robot_name: str, status: str = "IDLE", **extra: Any):
        """Inject a fake robot status event into registered callbacks."""
        message = {
            "robot_name": robot_name,
            "status": status,
            "battery": extra.pop("battery", 100.0),
            "location": extra.pop("location", [0.0, 0.0]),
            "timestamp": time.time(),
            **extra,
        }
        callback = self._status_callbacks.get(robot_name) or self._status_callbacks.get("*")
        if callback:
            callback(message)
        return message

    def cancel_robot_task(self, robot_name: str):
        self.cancelled_tasks.append(robot_name)
