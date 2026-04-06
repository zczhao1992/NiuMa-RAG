import uvicorn
import argparse
import sys
import signal
import asyncio
import platform


def handle_shutdown(signum, frame):
    print("shut down...")
    sys.exit(0)


signal.signal(signal.SIGINT, handle_shutdown)
signal.signal(signal.SIGTERM, handle_shutdown)


if __name__ == "__main__":

    if platform.system() == "Windows":
        # 1. 强制设置策略为 Selector
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    parser = argparse.ArgumentParser(description="Run the RAGCHAT server")

    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="host bind the server to(default: localhost)"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="host bind the server to(default: 8000)"
    )

    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload"
    )

    parser.add_argument(
        "--log-level",
        type=str,
        default="info",
        choices=["critical", "error", "warning", "debug"],
        help="log level (default: info)"
    )

    args = parser.parse_args()

    reload = False
    if args.reload:
        reload = True

    try:
        uvicorn.run("src.main:app", host=args.host,
                    port=args.port, reload=reload, log_level=args.log_level, loop="asyncio")
    except Exception as e:
        print(e)
        sys.exit(1)
