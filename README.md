# iptables Forwarding Helper

Generate iptables commands for OpenWrt firewall custom port forwarding rules.
Intended for adding or updating source addresses in batch for a single rule.

## Usage

```
python ifh.py [-h] [-v] (-a <src address> | -f <src file>) -p <src port> -t <protocol> -A <dest address> [-P <dest port>] [-c <comment>] [-k]
```

## License

MIT license. See [LICENSE][license] for more information.

[license]: https://github.com/alexitx/iptables-forwarding-helper/blob/master/LICENSE
