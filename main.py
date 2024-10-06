from face_tracking import FaceTracker
from game import FlappyFaceGame

def main():
    face_tracker = FaceTracker()
    game = FlappyFaceGame()

    try:
        while True:
            game.run(face_tracker)
    except KeyboardInterrupt:
        print("Exiting the game...")
    finally:
        face_tracker.release()

if __name__ == "__main__":
    main()
