from main_server.infrastructure.robot_bridge.mock_communicator import MockRobotCommunicator


def test_mock_robot_communicator_records_and_emits_status():
    events = []
    communicator = MockRobotCommunicator()

    communicator.connect()
    communicator.listen_for_robot_status("robot01", events.append)
    communicator.send_action_sequence("robot01", [{"command": "goto", "target": "lobby"}])
    communicator.publish_obstacle_info("robot01", {"level": "CAUTION"})
    communicator.publish_employee_result("robot01", {"employee_id": "E001"})
    status = communicator.emit_status("robot01", "MOVING", battery=88.0)
    communicator.cancel_robot_task("robot01")
    communicator.disconnect()

    assert communicator.is_connected is False
    assert len(communicator.action_sequences) == 1
    assert communicator.action_sequences[0]["robot_name"] == "robot01"
    assert len(communicator.obstacle_messages) == 1
    assert len(communicator.employee_messages) == 1
    assert events == [status]
    assert communicator.cancelled_tasks == ["robot01"]
