import os
import platform
from argparse import ArgumentParser
from crontab import CronTab

# NB: this script probably won't work on Windows - works great on Raspbian Linux though


CRONJOB_COMMENT = "Scrapy daily job"

# the cron command will look like "python ~/Documents/go_festival/scraper/festival/festival/spiders/festivals/py"
# this starts the crawler process
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
CRON_COMMAND = "python " + os.path.join(CURRENT_PATH, "festival", "festival", "spiders", "festivals.py")


def add_to_crontab(cron):
    remove_from_crontab(cron)  # remove it first if it's already there, to prevent duplicates
    job = cron.new(command=CRON_COMMAND, comment=CRONJOB_COMMENT)
    job.day.every(1)
    cron.write()


def remove_from_crontab(cron):
    cron.remove_all(comment=CRONJOB_COMMENT)
    cron.write()


def get_command_line_arguments():
    parser = ArgumentParser(description="Manage whether the scheduled scraping job is run daily, or not")
    group = parser.add_mutually_exclusive_group()  # cannot start and stop the cron job at the same time!
    group.add_argument("--start", action="store_true", help="Add the scraping job to the crontab")
    group.add_argument("--stop", action="store_true", help="Remove the scraping job from the crontab")
    return parser.parse_args()


def main():
    # the server runs Raspbian so this script was not designed to work with Windows
    if platform.system() == "Windows":
        print("Sorry, this script only works on Unix based systems")
        return


    cron = CronTab(user=True)  # current user's cron

    args = get_command_line_arguments()
    if args.start:  # --start was supplied as a cmd line arg
        add_to_crontab(cron)
        print("Scrapy job added to crontab")

    elif args.stop:  # --stop was supplied as a cmd line arg
        remove_from_crontab(cron)
        print("Scrapy job removed from crontab")

    else:
        print("Either supply --start or --stop to control whether the scraping job is added or removed from the crontab")



if __name__ == "__main__":
    main()
