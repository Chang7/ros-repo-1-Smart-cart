"""YOLO single-model webcam smoke test.

This script is intended for quick local validation of an obstacle detection
model. It opens webcam index 0, runs one YOLO model, draws bounding boxes, and
shows the result in an OpenCV window.

Example:
    python ai_server/test_webcam.py --model ai_server/models/obstacle.pt --conf 0.5
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import cv2

try:
    from ultralytics import YOLO
except ImportError:
    print("ultralytics is not installed.")
    print("Install command: pip install ultralytics")
    sys.exit(1)


class SingleModelWebcamTest:
    """Run one YOLO model against the default webcam."""

    def __init__(self, model_path: str, camera_index: int = 0):
        self.model_path = Path(model_path)
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found: {self.model_path}")

        print(f"Loading YOLO model: {self.model_path}")
        self.model = YOLO(str(self.model_path))

        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open webcam index {camera_index}")

        self.box_color = (0, 0, 255)

    def draw_detections(self, frame, results, color):
        """Draw YOLO bounding boxes on a frame."""
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                class_name = result.names[class_id]
                label = f"{class_name} {confidence:.2f}"

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                (text_width, text_height), _ = cv2.getTextSize(
                    label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2
                )
                cv2.rectangle(
                    frame,
                    (x1, y1 - text_height - 10),
                    (x1 + text_width, y1),
                    color,
                    -1,
                )
                cv2.putText(
                    frame,
                    label,
                    (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    2,
                )
        return frame

    def run(self, confidence_threshold: float = 0.5):
        print("\n" + "=" * 60)
        print("YOLO webcam test started")
        print("=" * 60)
        print(f"Model: {self.model_path.name}")
        print(f"Confidence threshold: {confidence_threshold}")
        print("Controls: q/ESC = quit, s = save screenshot")
        print("=" * 60 + "\n")

        frame_count = 0
        screenshot_count = 0

        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("Failed to read a frame from webcam.")
                    break

                frame_count += 1
                results = self.model(frame, conf=confidence_threshold, verbose=False)
                frame = self.draw_detections(frame, results, self.box_color)

                object_count = sum(len(r.boxes) for r in results)
                cv2.putText(
                    frame,
                    f"Frame: {frame_count}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2,
                )
                cv2.putText(
                    frame,
                    f"Objects: {object_count}",
                    (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2,
                )

                cv2.imshow("YOLO Webcam Test - Press Q to quit", frame)
                key = cv2.waitKey(1) & 0xFF
                if key in {ord("q"), 27}:
                    break
                if key == ord("s"):
                    screenshot_count += 1
                    filename = f"screenshot_{screenshot_count}.jpg"
                    cv2.imwrite(filename, frame)
                    print(f"Saved screenshot: {filename}")
        except KeyboardInterrupt:
            print("Interrupted by user.")
        finally:
            self.cap.release()
            cv2.destroyAllWindows()
            print(f"Processed frames: {frame_count}")


def main():
    parser = argparse.ArgumentParser(description="YOLO webcam single-model test")
    parser.add_argument(
        "--model",
        default="ai_server/models/obstacle.pt",
        help="Path to YOLO model file",
    )
    parser.add_argument("--camera", type=int, default=0, help="Webcam index")
    parser.add_argument("--conf", type=float, default=0.5, help="Confidence threshold")
    args = parser.parse_args()

    tester = SingleModelWebcamTest(args.model, camera_index=args.camera)
    tester.run(confidence_threshold=args.conf)


if __name__ == "__main__":
    main()
