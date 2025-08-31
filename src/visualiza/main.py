# This is the main entry point of the application.
# It follows the Composition Root pattern, where all dependencies are
# instantiated and wired together.

import sys
import os

# This is a common pattern to make sure the 'src' directory is in the python path
# especially when running scripts from a subdirectory.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.visualiza.application.services.user_service import UserApplicationService
from src.visualiza.infrastructure.persistence.sqlite_repository import SQLiteUserRepository
from src.visualiza.infrastructure.services.voice_service import VoiceService
from src.visualiza.infrastructure.services.vision_service import VisionService
from src.visualiza.infrastructure.ui.main_window import MainWindow

def main():
    """
    Composition Root: Initializes and injects all dependencies.
    """
    # 1. Create Repository instance
    user_repository = SQLiteUserRepository()

    # 2. Create Service instances
    user_service = UserApplicationService(user_repository)
    voice_service = VoiceService()
    vision_service = VisionService(model_path="yolov8n.pt") # Ensure the model is in the root

    # 3. Create UI instance and inject services
    app = MainWindow(
        user_service=user_service,
        voice_service=voice_service,
        vision_service=vision_service,
    )

    # 4. Start the application
    app.start()

if __name__ == "__main__":
    main()