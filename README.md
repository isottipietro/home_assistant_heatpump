This is a HACS custom integration for a cheap heatpump without any connection except for an internal serial bus. The same cheap heatpump is marketed as:
* Cosmogas ECOTwin (Italy)
* Neoheat EKO II (Poland)
* ES AWH (Sweden)
* HEIKO Thermal CH + DHW (Poland)
* Attack TCI (Slovakia)
... and many others

# Installation

1. Open the cheap Serial-Wifi converter USR W600 or W610 (username and password: admin)
2. Set WiFi in STA Mode and connect to lan
3. Serial port
    1. Baudrate: 115200 bps
    2. Data bits: 8 bit
    3. Parity: none
    4. Stopbits: 1 bit
4. Network setting: Transparent mode
5. Socket
    1. TCP Server
    2. set preferred IP and port
6. Add to configuration.yaml address and port