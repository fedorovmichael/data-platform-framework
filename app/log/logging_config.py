import logging


def configure_logging(level=logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(name)s:%(lineno)-3d %(levelname)-7s - %(message)s",
    )

    logging.getLogger("py4j").setLevel(logging.WARNING)
