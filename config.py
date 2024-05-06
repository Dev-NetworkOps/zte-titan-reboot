# Dictionary containing the commands and their respective expect strings
commands = {
    'enter_config_mode': {
        'command': r'configure terminal',
        'expect': r'\(config\)#'
        
    },
    'interface_config': {
        'command': r'interface gpon_olt-1/{i}/{x}',
        'expect': r'\(config-if-gpon_olt-1/{i}/{x}\)'
    },
    'onu_reboot': {
        'command': r'onu-action omci-reboot',
        'expect': r'\(config-if-gpon_olt-1/{i}/{x}\)'
    },
    'exit_config_mode': {
        'command': r'exit',
        'expect': r'\(config\)#'
    }
}
def get_info_device(ip_address, username, password, secret):
  device_info = {
    'device_type': 'zte_zxros',
    'ip': ip_address,
    'username': username,
    'password': password,
    'secret': secret,
    'timeout': 15,
    'conn_timeout': 20,
  }
  return device_info