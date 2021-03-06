import argparse
import ipaddress
import sys


_IPTABLES_COMMAND_TEMPLATE = (
    'iptables -t nat -A prerouting_wan_rule -s {src_address} -p {protocol} -m {protocol} '
    '--dport {src_port} -j DNAT --to-destination {dest_address}:{dest_port}'
)
_IPTABLES_COMMAND_COMMENT_TEMPLATE = (
    "iptables -t nat -A prerouting_wan_rule -s {src_address} -p {protocol} -m {protocol} --dport {src_port} "
    "-m comment --comment '{comment}' -j DNAT --to-destination {dest_address}:{dest_port}"
)


def format_command_raw(src_address, src_port, protocol, dest_address, dest_port=None, comment=None):
    if dest_port is None:
        dest_port = src_port
    if comment is None:
        return _IPTABLES_COMMAND_TEMPLATE.format(
            src_address=src_address,
            protocol=protocol,
            src_port=src_port,
            dest_address=dest_address,
            dest_port=dest_port
        )
    return _IPTABLES_COMMAND_COMMENT_TEMPLATE.format(
        src_address=src_address,
        protocol=protocol,
        src_port=src_port,
        comment=comment,
        dest_address=dest_address,
        dest_port=dest_port
    )


def format_commands(
    src_addresses,
    src_port,
    protocols,
    dest_address,
    dest_port=None,
    comment=None,
    format_comment=False
):
    dest_address = ipaddress.IPv4Address(dest_address).compressed
    result = []
    for raw_src_address in src_addresses:
        src_address = ipaddress.IPv4Network(raw_src_address).compressed
        for protocol in protocols:
            if format_comment and comment is not None:
                comment = comment.format(
                    src_address=src_address,
                    src_port=src_port,
                    protocol=protocol,
                    dest_address=dest_address,
                    dest_port=dest_port
                )
            command = format_command_raw(
                src_address,
                src_port,
                protocol,
                dest_address,
                dest_port,
                comment
            )
            result.append(command)
    return result


def _cli():

    def error(message=None, exception=None):
        if message is not None:
            print(f'Error: {message}', file=sys.stderr)
        elif exception is not None:
            if str(exception):
                print(f'{type(exception).__name__}: {exception}', file=sys.stderr)
            else:
                print(type(exception).__name__, file=sys.stderr)
        else:
            raise ValueError("Argument 'message' or 'exception' is required")
        sys.exit(1)

    class HelpFormatter(argparse.HelpFormatter):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, max_help_position=32, **kwargs)

        def _format_action_invocation(self, action):
            if not action.option_strings or action.nargs == 0:
                return super()._format_action_invocation(action)
            default = self._get_default_metavar_for_optional(action)
            args_string = self._format_args(action, default)
            return f'{", ".join(action.option_strings)} {args_string}'

    parser = argparse.ArgumentParser(formatter_class=HelpFormatter)
    del HelpFormatter

    src_group = parser.add_mutually_exclusive_group(required=True)
    src_group.add_argument(
        '-a',
        '--src-address',
        help="Comma-separated list of source addresses (or '--src-file')",
        metavar='<src address>'
    )
    src_group.add_argument(
        '-f',
        '--src-file',
        help="Newline-separated list of source addresses from file or stdin (or '--src-address')",
        metavar='<src file>'
    )
    parser.add_argument(
        '-p',
        '--src-port',
        type=int,
        required=True,
        help='Source port',
        metavar='<src port>'
    )
    parser.add_argument(
        '-t',
        '--protocol',
        required=True,
        help='Comma-separated list of protocols (values: tcp, udp)',
        metavar='<protocol>'
    )
    parser.add_argument(
        '-A',
        '--dest-address',
        required=True,
        help='Destination address',
        metavar='<dest address>'
    )
    parser.add_argument(
        '-P',
        '--dest-port',
        type=int,
        help="Destination port (optional; default: same as '--src-port')",
        metavar='<dest port>'
    )
    parser.add_argument(
        '-c',
        '--comment',
        help='Comment in iptables command (optional)',
        metavar='<comment>'
    )
    parser.add_argument(
        '-k',
        '--format-comment',
        action='store_true',
        help='Enable replacing placeholders in comment (optional)'
    )
    args = parser.parse_args()

    if not 0 < args.src_port < 65536:
        error(f"Invalid source port '{args.src_port}'")

    if args.dest_port is None:
        args.dest_port = args.src_port
    elif not 0 < args.dest_port < 65536:
        error(f"Invalid destination port '{args.src_port}'")

    protocols = args.protocol.split(',')
    if not set(protocols).issubset({'tcp', 'udp'}):
        error(f"Invalid protocol '{args.protocol}'")


    if args.src_address is not None:
        # Comma-separated list
        src_addresses = args.src_address.split(',')
    elif args.src_file == '-':
        # Newline-separated from stdin
        src_addresses = [line.strip() for line in sys.stdin.readlines()]
    else:
        # Newline-separated from file
        try:
            with open(args.src_file, 'r', encoding='utf-8') as f:
                src_addresses = [line.strip() for line in f.readlines()]
        except (OSError, UnicodeError) as e:
            error(exception=e)

    try:
        commands = format_commands(
            src_addresses,
            args.src_port,
            protocols,
            args.dest_address,
            args.dest_port,
            args.comment,
            args.format_comment
        )
    except ValueError as e:
        error(exception=e)
    print(*commands, sep='\n')


def _main():
    try:
        _cli()
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
        sys.exit(1)


if __name__ == '__main__':
    _main()
