import uvicorn
import argparse
import sys
import signal
import asyncio
import platform
import os


def handle_shutdown(signum, frame):
    print("Shutting down...")
    sys.exit(0)


signal.signal(signal.SIGINT, handle_shutdown)
signal.signal(signal.SIGTERM, handle_shutdown)

if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    env_port = int(os.environ.get("PORT", 8000))

    env_host = "0.0.0.0" if os.environ.get("RENDER") else "localhost"

    parser = argparse.ArgumentParser(description="Run the RAGCHAT server")

    parser.add_argument(
        "--host",
        type=str,
        default=env_host,
        help=f"host bind the server to (default: {env_host})"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=env_port,
        help=f"port bind the server to (default: {env_port})"
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
        choices=["critical", "error", "warning",
                 "debug", "info"],
        help="log level (default: info)"
    )

    args = parser.parse_args()

    try:
        print(f"Starting server on {args.host}:{args.port}")
        uvicorn.run(
            "src.main:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
            log_level=args.log_level
        )
    except Exception as e:
        print(f"Error occurred: {e}")
        sys.exit(1)
