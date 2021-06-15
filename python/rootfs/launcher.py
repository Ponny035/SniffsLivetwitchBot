from src import TwitchBot, UserFunction, automod, EventTrigger
import sys

def main(environment, dryrun):
    bot = TwitchBot(environment, dryrun, UserFunction, automod, EventTrigger)
    bot.run()

if __name__ == "__main__":
    environment = sys.argv[1]
    try:
        if((environment == "dev") or (environment == "prod")):
            if environment == "dev":
                try:
                    dryrun = sys.argv[2]
                except IndexError:
                    dryrun = "msgon"
            else: dryrun = "msgon"
            main(environment, dryrun)
        else:
            raise TypeError("Only 2 types are allow (dev/production)")

    except Exception as msg:
        print(msg)