from datetime import datetime
import csv
import strategy

# Run this file as main to test a database of breakouts
# The test data is in a csv file in the format: startDate, endDate, symbol
# The test data should satisfy the criteria under which the movement is classified as a breakout


if __name__ == '__main__':
    with open('test_data/test.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            # parse file
            startDate = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
            endDate = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
            fsym = row[2]

            # check status
            isConsolidating, isPumping = strategy.check_status_between_dates(fsym, startDate, endDate, debug=True)
            assert isPumping == True
            assert isConsolidating == True

    print("\nTest run successfully")