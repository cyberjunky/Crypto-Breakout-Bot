import telegram
import util
import strategy
from datetime import datetime


# TODO notify also how strong is the breakout


class CryptoBreakoutBot:
    def __init__(self, token, chat_id):
        self.bot = telegram.Bot(token=token)
        self.chat_id = chat_id
        self.foundSymbols = {} # maps found symbols to the timestamp when they are found. Used to avoid signaling the same symbol again before some time has passed

    def start(self):
        allSymbols = util.get_all_symbols()
        print(allSymbols)
        
        while (True):
            for fsym in allSymbols[:10]:
                # ignore if already found this symbol
                if self.alreadyFound(fsym):
                    continue

                isConsolidating, isPumping = strategy.check_status(fsym)
                print(f"{fsym} is consolidating: {isConsolidating} is breaking out: {isPumping}")

                if isConsolidating and isPumping:
                    self.bot.sendMessage(chat_id=self.chat_id, text=f"{fsym} is breaking out")
                    self.foundSymbols[fsym] = datetime.timestamp(datetime.now()) # add the symbol to the found dict with the corresponding timestamp

    def alreadyFound(self, fsym):
        if fsym not in self.foundSymbols:
            return False
        lastTimestamp = self.foundSymbols[fsym] # last time this symbol was found
        timestampNow = datetime.timestamp(datetime.now())
        dt = timestampNow - lastTimestamp # seconds that have passed since this symbol was found
        return dt < 3600 # do not notify if already found in the last hour


if __name__ == '__main__':
    with open("private.txt", 'r') as f:
        token = f.readline().strip()
        chat_id = f.readline()

    bot = CryptoBreakoutBot(token, chat_id)
    bot.start()