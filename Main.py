import re
import logging
from logging.handlers import RotatingFileHandler
from pwinput import pwinput
from netmiko import ConnectHandler
from config import OLT_TYPES, commands, get_info_device
import subprocess
from io import StringIO
import pandas as pd
import os

def validate_ip(ip):
    """
    Validates the format of an IP address.

    Args:
        ip (str): The IP address to validate.

    Returns:
        bool: True if the IP address is valid and pingable, False otherwise.
    """
    if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
        return False
    
    try:
        result = subprocess.run(['ping', '-n', '1', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=2, universal_newlines=True)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False
    

def connect_to_device(device_info, secret):
    """
    Connects to the network device using Netmiko.

    Args:
        device_info (dict): A dictionary containing device connection details.

    Returns:
        netmiko.ConnectHandler: The connection handler object if successful, None otherwise.
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Connecting to device {device_info['ip']} with username {device_info['username']}")
    try:
        net_connect = ConnectHandler(**device_info)
        net_connect.exit_enable_mode()
        net_connect.enable()
        logger.info("Connection successful!")
        return net_connect
    
    except ConnectionError as e:
        logger.error(f"Error connecting to the device: {e}")
    except TimeoutError as e:
        logger.error(f"Connection timeout: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

    # Prompt for secret password again if enable mode activation fails
    while True:
        try:
            net_connect = ConnectHandler(**device_info)
            logger.info("Connection successful!")
            net_connect.exit_enable_mode()
            net_connect.enable()
            logger.info("Connection enable mode successful!")
            return net_connect
        except Exception as e:
            logger.error(f"Failed to authenticate. Please check your secret password.")
            secret = get_secret_password()
            device_info['secret'] = secret  # Update device_info with new secret password


def exit_device(connection):
    """
    Exits from the network device.

    Args:
        connection (netmiko.ConnectHandler): The connection handler object.
    """
    logger = logging.getLogger(__name__)
    try:
        logger.info("Exiting the device...")
        if connect_to_device: # Check if connection exists before disconnecting
            connection.disconnect()
            logger.info("Disconnected from the device.")
        else:
            logger.warning("No active connection to disconnect from.")
    except Exception as e:
        logger.error(f"Error while exiting the device: {str(e)}")

def get_ip_address():
    """
    Prompts the user to input the device IP address and validates its format.

    Returns:
        str: The validated IP address.
    """
    while True:
        ip = input('E.g., 172.30.20.41\nEnter the device IP address: ')
        if validate_ip(ip):
            return ip
        else:
            print("Invalid IP address format or is not pingable. Please try again.")

def get_olt_type():
    """
    Prompts the user to select the OLT type from available options.

    Returns:
        int: The selected OLT type code.
    """
    while True:
        print('Available OLT types:')
        for key, value in OLT_TYPES.items():
            print(f"{value} - {key}")
        choice = input('Enter the number corresponding to the OLT type: ')
        if choice.isdigit():
            olt_type = int(choice)
            if olt_type in OLT_TYPES.values():
                return olt_type
        print('Invalid option. Please choose a valid number.')

def get_password():
    """
    Prompts the user to input the OLT login password.

    Returns:
        str: The entered password.
    """
    while True:
        try:
            password = pwinput(prompt='Enter your password: ')
            if password:
                return password
            else:
                print("Password cannot be empty.")
        except KeyboardInterrupt:
            print("\nPassword input cancelled.")
            return None

def get_secret_password():
    """
    Prompts the user to input the OLT login secret password.

    Returns:
        str: The entered password.
    """
    while True:
        try:
            password = pwinput(prompt='Enter your secret password: ')
            if password:
                return password
            else:
                print("Password cannot be empty.")
        except KeyboardInterrupt:
            print("\nPassword input cancelled.")
            return None

def get_username():
    """
    Prompts the user to input the OLT login username.

    Returns:
        str: The entered username.
    """

    while True:
        try:
            username = input('Enter the OLT login: ')
            if username:
                return username
            else:
                print("Username cannot be empty.")
        except KeyboardInterrupt:
            print("\nUsername input cancelled.")
            return None

def main():
    """
    The main function to execute the program.
    """

    ip_address = get_ip_address()
    username = get_username()
    password = get_password()
    secret = get_secret_password()

    # Remove existing log file
    if os.path.exists('connection_log.log'):
        os.remove('connection_log.log')

    logging.basicConfig(level=logging.INFO)
    
    # Add a rotating file handler
    file_handler = RotatingFileHandler('connection_log.log', maxBytes=1024 * 1024, backupCount=5)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    # Add the file handler to the root logger
    logging.getLogger('').addHandler(file_handler)
    
    while password != None or username != None: # Check if username is also None
        device_info = get_info_device(ip_address, username, password, secret)
        try:
            device = connect_to_device(device_info, secret)
            device.send_command(commands['enter_config_mode']['command'], expect_string=commands['enter_config_mode']['expect'])
            break # If connection is successful, exit the loop
        except Exception as e:
            # Log the error
            logging.error("Connection error: %s", e)
            # If there's a connection error, prompt for username and password again
            print("Incorret password. Please enter with your username and password again or press Ctrl+C to exit.")
            username = get_username()
            password = get_password()

    # If username or password is None, just exit
    if password is None or username is None:
        return
    logger = logging.getLogger(__name__)
    try:
        # Iterate over all combinations of i and x
        output = device.send_command('show card') # Get card
        start_line = output.find("Shelf")
        if start_line != -1:
            # Extract and process the table
            df_show_card = pd.read_csv(StringIO(output[start_line:]), sep='\s+')
            df_show_card = df_show_card[df_show_card["Status"] == "INSERVICE"]
            df_show_card[['Shelf', 'Slot', 'Port']] = df_show_card[['Shelf', 'Slot', 'Port']].astype(int)
            df_show_card = df_show_card[df_show_card["Port"] > 0][["Shelf", "Slot", "Port"]].reset_index(drop=True)
            for _, row in df_show_card.iterrows():
                slot, port = row['Slot'], row['Port']
                if slot != 5 and slot != 6:
                    # Iterate over the commands and substitute {i} and {x} as necessary
                    for p in range(1, port + 1):
                        for cmd_name, cmd_info in commands.items():
                            if cmd_name != 'enter_config_mode':
                                command = cmd_info['command'].format(i=slot, x=p)
                                expect_string = cmd_info['expect'].format(i=slot, x=p)
                                device.send_command(command, expect_string=expect_string)
                                logger.info(command)
                        print('\n')
                    print('\n')
        else:
            print("String 'Shelf' not found in output.")
    except Exception as e:
        logging.error(f"Process error: {e}")
    finally:
        exit_device(device)

if __name__ == "__main__":
    main()
