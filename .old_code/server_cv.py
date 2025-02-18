#!/usr/bin/env python3
from typing import Optional, Union, Tuple
import socket
import sys
import cv2
import pickle
import numpy as np
import struct
from numpy.typing import NDArray

def recv_all(conn: socket.socket, n: int) -> Optional[bytes]:
    """
    Helper function to receive exactly n bytes from a connection.
    
    Args:
        conn: Network socket connection
        n: Number of bytes to receive
        
    Returns:
        bytes or None if connection closed
    """
    data = bytearray()
    while len(data) < n:
        try:
            packet = conn.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        except socket.error as e:
            print(f"Socket error while receiving: {e}")
            return None
    return bytes(data)

def receive_frame(conn: socket.socket) -> Optional[NDArray]:
    """
    Reliably receive a compressed video frame over a network connection.
    
    Args:
        conn: Network socket connection
        
    Returns:
        numpy array representing the frame or None if error
    """
    try:
        # Get the message size first (4 bytes)
        size_data = recv_all(conn, 4)
        if size_data is None:
            return None
            
        size = struct.unpack('!L', size_data)[0]
        
        # Now get the actual frame data
        frame_data = recv_all(conn, size)
        if frame_data is None:
            return None
            
        # Deserialize the compressed frame
        compressed_frame = pickle.loads(frame_data)
        
        # Decompress the frame
        frame = cv2.imdecode(compressed_frame, cv2.IMREAD_COLOR)
        if frame is None:
            print("Error: Could not decompress frame")
            return None
            
        return frame
        
    except (socket.error, pickle.UnpicklingError) as e:
        print(f"Error receiving frame: {e}")
        return None

def create_server_socket(host: str, port: int) -> Tuple[socket.socket, Tuple[str, int]]:
    """
    Create and set up the server socket
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    print('Socket created')
    
    server_socket.bind((host, port))
    print('Socket bind complete')
    
    server_socket.listen(10)
    print('Socket now listening')
    
    print(f'Waiting for connection on {host}:{port}...')
    conn, addr = server_socket.accept()
    print(f'Connected to {addr}')
    
    return conn, addr

def main() -> None:
    # Connection settings
    HOST: str = '10.0.0.74'
    PORT: int = 8089
    
    try:
        # Create and set up server socket
        conn, addr = create_server_socket(HOST, PORT)
        
        # Create window for display
        cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
        
        while True:
            # Receive frame
            frame = receive_frame(conn)
            
            if frame is None:
                print("No frame received, connection might be closed")
                break
            
            # Display the frame
            cv2.imshow('Frame', frame)
            
            # Break loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Quit command received")
                break
                
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up
        print("Cleaning up...")
        try:
            conn.close()
        except NameError:
            pass  # Connection wasn't established
        cv2.destroyAllWindows()
        print("Cleanup complete")

if __name__ == "__main__":
    main()
