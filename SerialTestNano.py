"""
#!/usr/bin/python3
import serial
import time

arduino = with serial.Serial(
port = "/dev/ttyTHS1",
baudrate = 115200,
bytesize = serial.EIGHTBITS,
parity = serial.PARITY_NONE,
stopbits = serial.STOPBITS_ONE,
timeout = 5,
xonxoff = False,
rtscts = False,
dsrdtr = False,
writeTimeout = 2
)

with serial.Serial('/dev/ttyTHS1', 9600, timeout=10) as ser:
    while True:
        try:
            ser.write("Command from Jetson|".encode())
            data = ser.readLine()
            if data:
                print(data)
                time.sleep(1)
        except Exception as e:
            print(e)
            ser.close()
""" 

#!/usr/bin/python3
import serial
import time
import sys
import traceback

def connect_to_arduino(port='/dev/ttyACM0', baudrate=115200, timeout=5):
    """
    Establish a connection with Arduino with robust error handling.
    
    Args:
        port (str): Serial port to connect to
        baudrate (int): Communication speed
        timeout (int): Connection timeout
    
    Returns:
        serial.Serial: Connected serial object
    """
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=timeout,
            write_timeout=2
        )
        # Give the Arduino time to reset
        time.sleep(2)
        print("Connected to Arduino")
        return ser
    except serial.SerialException as e:
        print(f"Error connecting to Arduino: {e}")
        sys.exit(1)

def send_command(ser, command):
    """
    Send a command to Arduino and handle encoding.
    
    Args:
        ser (serial.Serial): Serial connection
        command (str): Command to send
    """
    try:
        ser.write(f"{command}\n".encode('utf-8'))
    except serial.SerialTimeoutException:
        print("Write timeout occurred")
    except Exception as e:
        print(f"Error sending command: {e}")

def read_arduino_data(ser):
    """
    Read data from Arduino with error handling.
    
    Args:
        ser (serial.Serial): Serial connection
    
    Returns:
        str or None: Decoded data or None
    """
    try:
        # Use readline() instead of readLine()
        data = ser.readline().decode('utf-8').strip()
        return data if data else None
    except UnicodeDecodeError:
        print("Could not decode incoming data")
    except Exception as e:
        print(f"Error reading data: {e}")
    return None

def main():
    """
    Main function to handle Arduino communication.
    """
    ser = None
    try:
        ser = connect_to_arduino()
        
        while True:
            # Send a command
            send_command(ser, input())
            
            # Read response
            data = read_arduino_data(ser)
            if data:
                print(f"Received: {data}")
            
            # Wait before next iteration
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()
    
    finally:
        # Ensure serial connection is closed
        if ser and ser.is_open:
            ser.close()
            print("Serial connection closed.")

if __name__ == "__main__":
    main()
