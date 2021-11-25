# iptables Forwarding Helper

Generate iptables commands for OpenWrt firewall custom port forwarding rules.
Intended for adding or updating source addresses in batch for a single rule.

## Usage

```
python ifh.py [-h] [-v] (-a <src address> | -f <src file>) -p <src port> -t <protocol> -A <dest address> [-P <dest port>] [-c <comment>] [-k]
```

## CLI Arguments

| Argument             | Type | Value                           | Default              | Required                 | Description                                          |
|----------------------|------|---------------------------------|----------------------|--------------------------|------------------------------------------------------|
| -a, --src-address    | str  | IPv4 address with optional mask |                      | Yes (or `--src-file`)    | Comma-separated list of source addresses             |
| -f, --src-file       | str  | filename                        |                      | Yes (or `--src-address`) | Newline-separated list of source addresses from file |
| -p, --src-port       | int  | 1-65535                         |                      | Yes                      | Source port                                          |
| -t, --protocol       | str  | `tcp`, `udp`                    |                      | Yes                      | Comma-separated list of protocols                    |
| -A, --dest-address   | str  | IPv4 address                    |                      | Yes                      | Destination address                                  |
| -P, --dest-port      | int  | 1-65535                         | Same as `--src-port` | No                       | Destination port                                     |
| -c, --comment        | str  |                                 |                      | No                       | Comment in iptables command                          |
| -k, --format-comment | bool |                                 |                      | No                       | Enable replacing placeholders in comment             |

Placeholders in comments surrounded by `{}` will be replaced with the corresponding values

| Placeholder  | Value                                                   |
|--------------|---------------------------------------------------------|
| src_address  | Source address with netmask length for the current rule |
| src_port     | Source port                                             |
| protocol     | Protocol for the current rule                           |
| dest_address | Destination address                                     |
| dest_port    | Destination port                                        |

## License

MIT license. See [LICENSE][license] for more information.

[license]: https://github.com/alexitx/iptables-forwarding-helper/blob/master/LICENSE
