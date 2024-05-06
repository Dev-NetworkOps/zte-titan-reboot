# ZTE C650 Optical Line Terminal Port Reboot Tool

This Python script provides a convenient way to reboot ports on the ZTE C650 Optical Line Terminal (OLT) using SSH connectivity. It focuses on enabling users to reboot individual ports through a command-line interface, leveraging the Netmiko library for seamless interaction with the device.

## Features

- **IP Address Validation and Pingability Check:** Ensures the validity of the IP address and verifies its pingability before initiating a connection to the ZTE C650 OLT.
  
- **Connection Establishment:** Establishes a secure SSH connection to the ZTE C650 OLT, allowing users to interact with the device remotely.
  
- **Interactive User Input:** Prompts users to input essential details such as the device IP address, username, password, and secret password (if required), ensuring secure access to the ZTE C650 OLT.
  
- **Logging and Error Handling:** Implements comprehensive logging functionality to record connection attempts, errors, and important events throughout the port reboot process. Handles various exceptions gracefully, providing informative error messages to assist users in troubleshooting potential issues.
  
- **Port Reboot Functionality:** Executes predefined commands tailored specifically for the ZTE C650 OLT to reboot individual ports, facilitating targeted troubleshooting and maintenance tasks.
  
- **Dynamic Configuration Execution:** Adapts configuration commands based on the unique requirements of the ZTE C650 OLT, ensuring precise and efficient execution of port reboot tasks.
  
- **Clean Exit and Resource Management:** Ensures proper disconnection from the ZTE C650 OLT upon completion of the port reboot process or in case of errors, maintaining system integrity and resource efficiency.

## Usage

1. **Clone the Repository:** Clone this repository to your local machine to access the Python script and associated files.

2. **Install Dependencies:** Install the required dependencies by running:
   ```
   pip install -r requirements.txt
   ```

3. **Run the Script:** Execute the `main()` function in the Python script to initiate the ZTE C650 OLT port reboot tool. Follow the interactive prompts to input the necessary details and select the ports for rebooting.

4. **Review Logs:** Check the generated log files for detailed information about the port reboot tasks and any encountered errors.

5. **Customization and Expansion:** Customize the script further by modifying reboot commands or adding new features to meet specific requirements of the ZTE C650 OLT environment.

## Notes

- This tool is tailored specifically for rebooting ports on the ZTE C650 Optical Line Terminal.
- Ensure proper authentication credentials and permissions are provided to access and reboot ports on the ZTE C650 OLT.
- Exercise caution when initiating port reboots, as they may disrupt network connectivity and services for connected devices.
