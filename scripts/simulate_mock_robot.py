"""Run a local mock robot communication simulation.

This script validates the server-to-robot payload flow without ROS, rosbridge,
or a physical robot.

Usage:
    python scripts/simulate_mock_robot.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from main_server.infrastructure.robot_bridge.mock_communicator import (  # noqa: E402
    MockRobotCommunicator,
)


def main() -> int:
    events: list[dict] = []

    communicator = MockRobotCommunicator()
    communicator.connect()
    communicator.listen_for_robot_status("robot01", events.append)

    actions = [
        {"command": "goto", "target": "pantry"},
        {"command": "pickup", "item": "snack"},
        {"command": "goto", "target": "desk_a"},
        {"command": "dropoff", "item": "snack"},
    ]
    communicator.send_action_sequence("robot01", actions, task_id=101)
    communicator.publish_obstacle_info("robot01", {"level": "CAUTION", "distance_m": 0.8})
    communicator.publish_employee_result("robot01", {"employee_id": "E001", "confidence": 0.97})
    communicator.emit_status("robot01", "MOVING", location=[1.2, 3.4], battery=87.5)
    communicator.cancel_robot_task("robot01")
    communicator.disconnect()

    result = {
        "connected_after_disconnect": communicator.is_connected,
        "action_sequences": len(communicator.action_sequences),
        "obstacle_messages": len(communicator.obstacle_messages),
        "employee_messages": len(communicator.employee_messages),
        "status_events": len(events),
        "cancelled_tasks": communicator.cancelled_tasks,
        "last_status": events[-1] if events else None,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

    ok = (
        result["connected_after_disconnect"] is False
        and result["action_sequences"] == 1
        and result["obstacle_messages"] == 1
        and result["employee_messages"] == 1
        and result["status_events"] == 1
        and result["cancelled_tasks"] == ["robot01"]
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
