# TCP Socket Serial Passthrough Test Tool

A simple TCP client tool for communication testing with serial passthrough modules (e.g., VONETS VM300).

## Features

- Connect to specified IP address and port
- Independent thread for receiving data with real-time display
- Automatically appends `\r\n` line endings to commands
- Interactive command input
- Comprehensive error handling and crash prevention

## Usage

### Requirements

- Python 3.6+

### Run

```bash
python tcp_socket_test.py
```

Follow the prompts to enter:
1. IP address of the serial passthrough module
2. Serial passthrough service port

### Example

```
Enter serial passthrough module IP: 192.168.1.100
Enter serial passthrough service port: 6011
[System] Connecting to 192.168.1.100:6011 ...
[System] -> Connected! You can now enter commands.

[Enter AT command (auto appends "\r\n")] -> AT
[Serial RX] <- OK
```

Type `exit` to quit the program.

## Use Cases

- VONETS WiFi serial passthrough module debugging
- General TCP socket communication testing
- AT command send/receive testing

## License

MIT License
