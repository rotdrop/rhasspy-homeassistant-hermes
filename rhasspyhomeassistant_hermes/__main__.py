"""Hermes MQTT service for rhasspy homeassistant"""
import argparse
import asyncio
import logging

import paho.mqtt.client as mqtt
import rhasspyhermes.cli as hermes_cli

from . import HomeAssistantHermesMqtt

_LOGGER = logging.getLogger("rhasspyhomeassistant_hermes")

# -----------------------------------------------------------------------------


def main():
    """Main method."""
    parser = argparse.ArgumentParser(prog="rhasspy-homeassistant-hermes")
    parser.add_argument("--url", required=True, help="URL of Home Assistant server")
    parser.add_argument(
        "--access-token", help="Long-lived access token (Authorization)"
    )
    parser.add_argument("--api-password", help="API password (X-HA-Access, deprecated)")
    parser.add_argument(
        "--handle-type",
        choices=["event", "intent"],
        default="event",
        help="Use Home Assistant events or intent API",
    )
    parser.add_argument(
        "--event-type-format",
        default="rhasspy_{0}",
        help="Format string for event types",
    )
    parser.add_argument("--certfile", help="SSL certificate file")
    parser.add_argument("--keyfile", help="SSL private key file (optional)")

    hermes_cli.add_hermes_args(parser)
    args = parser.parse_args()

    hermes_cli.setup_logging(args)
    _LOGGER.debug(args)

    try:
        loop = asyncio.get_event_loop()

        # Listen for messages
        client = mqtt.Client()
        hermes = HomeAssistantHermesMqtt(
            client,
            url=args.url,
            access_token=args.access_token,
            api_password=args.api_password,
            event_type_format=args.event_type_format,
            certfile=args.certfile,
            keyfile=args.keyfile,
            handle_type=args.handle_type,
            siteIds=args.siteId,
            loop=loop,
        )

        _LOGGER.debug("Connecting to %s:%s", args.host, args.port)
        hermes_cli.connect(client, args)
        client.loop_start()

        # Run event loop
        hermes.loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        _LOGGER.debug("Shutting down")


# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
