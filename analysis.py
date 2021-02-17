import strategy
from datetime import datetime

# Run this as main to check the status of a symbol between 2 dates

if __name__ == '__main__':
    startDate = datetime(2021, 2, 15, 12, 30, 0) # Y, M, D, h, m, s
    endDate = datetime(2021, 2, 17, 10, 15, 0)
    fsym = 'BNB'
    isConsolidating, isPumping = strategy.check_status_between_dates(fsym, startDate, endDate)
    print(f"{fsym} is consolidating: {isConsolidating} is breaking out: {isPumping}")