from ultralytics import YOLO
import numpy as np

class VisionService:
    """
    Handles object detection using a YOLO model.
    This service is responsible for processing image frames.
    """
    def __init__(self, model_path: str = 'yolov8n.pt'):
        """
        Initializes the VisionService by loading the YOLO model.
        Args:
            model_path: The path to the YOLO model file.
        """
        self.model = YOLO(model_path)

    def detect_objects(self, frame: np.ndarray) -> tuple[np.ndarray, list[str]]:
        """
        Performs object detection on a single frame.
        Args:
            frame: The image frame (as a numpy array) to process.
        Returns:
            A tuple containing:
            - The annotated frame with bounding boxes.
            - A list of unique detected object names.
        """
        # Perform inference
        results = self.model(frame)

        # Assuming one result object for a single frame
        r = results[0]

        # Draw annotations on the frame
        annotated_frame = r.plot()

        # Extract unique object names with confidence > 0.5
        detected_objects = []
        for box in r.boxes:
            confidence = float(box.conf[0])
            if confidence > 0.5:
                class_name = r.names[int(box.cls[0])]
                if class_name not in detected_objects:
                    detected_objects.append(class_name)

        return annotated_frame, detected_objects
