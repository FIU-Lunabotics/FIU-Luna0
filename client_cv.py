import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import time

# defines pipeline
def gstreamer_pipeline(
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink drop=True"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


def connect_to_server(host='10.108.116.123', port=8089, max_attempts=5):
    attempt = 0
    while attempt < max_attempts:
        try:
            clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientsocket.settimeout(5)  # 5 second timeout
            clientsocket.connect((host, port))
            print(f"Connected to server at {host}:{port}")
            return clientsocket
        except socket.error as e:
            attempt += 1
            print(f"Connection attempt {attempt} failed: {e}")
            if attempt < max_attempts:
                print(f"Retrying in 2 seconds...")
                time.sleep(2)
    raise Exception("Failed to connect to server after multiple attempts")


def send_frame(clientsocket, frame):
    try:
        # Compress frame
        _, compressed_frame = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
        data = pickle.dumps(compressed_frame)
        
        # Pack the size of the data first (using struct to ensure proper byte format)
        message_size = struct.pack("!L", len(data))
        
        # Send size followed by data
        clientsocket.sendall(message_size)
        clientsocket.sendall(data)
        return True
    except (socket.error, ConnectionResetError) as e:
        print(f"Error sending frame: {e}")
        return False

def main():
    # Initialize video capture
    cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
    if not cap.isOpened():
        print("Error: Could not open video capture")
        return

    # Initial connection
    try:
        clientsocket = connect_to_server()
    except Exception as e:
        print(f"Failed to establish initial connection: {e}")
        cap.release()
        return

    while True:
        try:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                continue

            # Print frame info (optional)
            print(f"Frame size: {sys.getsizeof(frame)} bytes")
            
            # Send the frame
            if not send_frame(clientsocket, frame):
                print("Attempting to reconnect...")
                try:
                    clientsocket.close()
                    clientsocket = connect_to_server()
                except Exception as e:
                    print(f"Reconnection failed: {e}")
                    break

            # Optional: Add delay to control frame rate
            # time.sleep(0.03)  # Roughly 30 FPS

        except KeyboardInterrupt:
            print("\nStopping client...")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            break

    # Cleanup
    try:
        clientsocket.close()
    except:
        pass
    cap.release()

if __name__ == "__main__":
    main()
