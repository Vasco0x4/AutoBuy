import time
import asyncio
import colorama
from loguru import logger
from .client import Client  
from .config_controller import ConfigController  
from .order_bitget import open_market_order 
from .order_bitget import close_position
from auto.config_controller import close_position_delay


SYMBOL_SIZE_MAPPING = {
    "BTC": {"symbol":"BTCUSDT","size":0.00729182},
    "ETH": {"symbol":"ETHUSDT","size":0.14270384},
    "USDT": {"symbol":"USDTUSDT","size":501.25263032},
    "BNB": {"symbol":"BNBUSDT","size":0.88440789},
    "SOL": {"symbol":"SOLUSDT","size":2.7499725},
}


class Duplicator:
    def __init__(self):
        self.config = ConfigController.get_config()
        self.client = Client(self.config)

    async def start(self):
        await self.client.start()
        await self.duplicate()

    async def duplicate(self):
        logger.info("Parsing conversation account list")
        self.groups = await self.client.get_groups()

        while True:
            logger.debug("Running cycle")

            for group in self.groups:
                logger.debug(f"Processing '{group['name']}' group")
                for source_channel in group["sources"]:
                    if not source_channel:
                        continue

                    messages_history = await self.client.get_last_messages(
                        source_channel, min_id=self._calc_channel_min_id(source_channel)
                    )

                    new_messages = self._filter_old_messages(
                        source_channel, messages_history
                    )

                    for msg in new_messages:
                        # si le message contient 🟢 ou test
                        if all(emoji in msg.message for emoji in ["🟢"]) and "test" in msg.message.upper(): ## changé cette partie en fonction du type de message target
                            logger.info(colorama.Fore.LIGHTGREEN_EX + f"New message detected in '{source_channel}': {msg.message}")
                            for key, mapping in SYMBOL_SIZE_MAPPING.items():
                                if key in msg.message.upper():
                                    symbol = mapping["symbol"]
                                    size = mapping["size"]
                                    side = "buy" 
                                    response = open_market_order(symbol=symbol, side=side, size=size, product_type="usdt-futures", margin_mode="isolated", order_type="market")
                                    logger.info(f"Order response: {response}")
                                    time.sleep(close_position_delay)
                                    close_position(symbol, productType="usdt-futures", holdSide="long")
                                    logger.info(f"Close order response: {response}")
                                    break

                        else:
                            logger.debug(colorama.Fore.LIGHTYELLOW_EX + f"Message ignored due to missing required. message = {msg.message}")

            await asyncio.sleep(self.config["delay"])

    def _calc_channel_min_id(self, source_channel):
        channel_last_id = source_channel.last_message_id()
        if not channel_last_id:
            channel_last_id = 0
        min_id = channel_last_id - self.config["edit_message_checker_limit"]
        if min_id < 0:
            min_id = 0
        return min_id

    @staticmethod
    def _filter_old_messages(source_channel, messages):
        if source_channel.last_message_id() == 0:
            if messages:
                source_channel.set_last_message_id(messages[-1].id)
            logger.debug("Skipping first cycle")
            return []

        new_messages = [m for m in messages if m.id > source_channel.last_message_id()]
        if new_messages:
            source_channel.set_last_message_id(new_messages[-1].id)
        return new_messages
