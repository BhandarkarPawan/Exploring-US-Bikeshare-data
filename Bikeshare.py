import time
import pandas as pd


# Declaration area
CITY_DATA = {'Chicago': 'chicago.csv',
             'New York City': 'new_york_city.csv',
             'Washington': 'washington.csv'}

INDEX = {'1': 'Chicago',
         '2': 'New York City',
         '3': 'Washington'}


MONTHS = {1: 'January',
          2: 'February',
          3: 'March',
          4: 'April',
          5: 'May',
          6: 'June',
          7: 'July',
          8: 'August',
          9: 'September',
          10: 'October',
          11: 'November',
          12: 'December'}

DAYS = {'Mon': 'Monday',
        'Tue': 'Tuesday',
        'Wed': 'Wednesday',
        'Thu': 'Thursday',
        'Fri': 'Friday',
        'Sat': 'Saturday',
        'Sun': 'Sunday'}


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    start_time = time.time()
    print('-'*80)  # ----------------------------------------------------------
    print('\n THE MOST FREQUENT TIMES OF TRAVEL\n')
    print('-'*80)  # ----------------------------------------------------------

    # display the most common month
    print("\nMost popular month: " + df['Month'].mode()[0])
    # display the most common day of week
    print("\nMost popular day of the week: " + str(df['Day of week'].mode()[0]))
    # display the most common start hour
    print("\nMost popular hour of the day: " + str(df['Hour'].mode()[0]))

    print("\nThis took %s seconds.\n" % round((time.time() - start_time), 3))


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    start_time = time.time()
    print('-'*80)  # ----------------------------------------------------------
    print('\nMOST POPULAR STATIONS AND TRIP\n')
    print('-'*80)  # ----------------------------------------------------------

    # Find the most common path taken and store the start and end stations
    paths = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False)
    path_start, path_end = paths.index[0]

    # display most commonly used start station
    print("\nMost popular Start Station: " + str(df['Start Station'].mode()[0]))
    # display most commonly used end station
    print("\nMost popular End Station: " + str(df['End Station'].mode()[0]))
    # display most frequent combination of start station and end station trip
    print("\nMost popular path: From " + path_start + " to " + path_end)

    print("\nThis took %s seconds.\n" % round((time.time() - start_time), 3))


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    start_time = time.time()
    print('-'*80)  # ----------------------------------------------------------
    print('\nTRIP DURATION\n')
    print('-'*80)  # ----------------------------------------------------------

    # display mean travel time
    print("\nAverage time taken per trip(mins): " + str(round(df['Trip Duration'].mean(), 2)))
    # display total travel time
    print("\nTotal time travelled(mins): " + str(df['Trip Duration'].sum()))

    print("\nThis took %s seconds.\n" % round((time.time() - start_time), 3))


def user_stats(df):
    """Displays statistics on bikeshare users."""

    start_time = time.time()
    print('-'*80)  # ----------------------------------------------------------
    print('\nUSER STATISTICS\n')
    print('-'*80)  # ----------------------------------------------------------

    # Calculate the number of customers and subscribers
    subscribers = df[df['User Type'] == 'Subscriber'].shape[0]
    customers = df[df['User Type'] == 'Customer'].shape[0]

    # Display counts of user types
    print("\nNumber of Subcribers: " + str(subscribers))
    print("\nNumber of Customers: " + str(customers))

    # Gender and Birth Year are available only for Chicago and NYC
    if('Gender' in df.keys()):
        male = df[df['Gender'] == 'Male'].shape[0]
        female = df[df['Gender'] == 'Female'].shape[0]

        # Display counts of gender
        print("\nNumber of Males: " + str(male))
        print("\nNumber of Females: " + str(female))

    if('Birth Year' in df.keys()):
        common_year = int(df["Birth Year"].mode())
        recent_year = df['Birth Year'].max()
        earliest_year = df['Birth Year'].min()

        # Display earliest, most recent, and most common year of birth
        print("\nMost common birth year: " + str(common_year))
        print("\nMost recent birth year: " + str(recent_year))
        print("\nEarliest birth year: " + str(earliest_year))

    print("\nThis took %s seconds.\n" % round((time.time() - start_time), 3))


def get_city():
    """
    Called from the user interface to initialize city data.

    Returns:
    (DataFrame) df - contains the data frame of the selected city.
    """

    print('-'*80)  # ----------------------------------------------------------
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    print('-'*80)  # ----------------------------------------------------------

    # Choosing a city to explore
    while True:
        option = input("\nChoose a city to explore:\n\
            1.Chicago\n\
            2.New york city\n\
            3.Washington\n").strip()
        if option in ['1', '2', '3']:
            city = INDEX[option].title()
            confirm = input("Explore {}? (y/n): ".format(city)).strip()
            if(confirm.upper() == 'Y'):
                break
        print("\nInvalid input! Please try again.")

    start_time = time.time()
    print(city + " is loading.... Please stand by.\n")
    # Load the CSV file into a DataFrame df for use
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Add columns for faster access
    df['Day of week'] = df['Start Time'].dt.weekday_name
    df['Hour'] = df['Start Time'].dt.hour
    df['Month'] = df['Start Time'].dt.month.map(MONTHS)
    df['Date'] = df['Start Time'].dt.day

    print("\nThat took %s seconds.\n" % round((time.time() - start_time), 3))
    print("Thank you for your patience!".format(city))

    return df


def search_by_date(df):
    """
    Called when the user decides to look up information from a certain date
    """

    while True:
        try:
            month = int(input("\nEnter the month (1-6): ").strip())
        except ValueError:
            print("Invalid input. Please try again!")
        else:
            if month not in range(1, 7):
                print("Invalid input. Please try again!")
                continue
            try:
                date = int(input("\nEnter the date (1-31): ").strip())
            except ValueError:
                print("Invalid input. Please try again!")
            else:
                if date in range(1, 32):
                    break
                print("Invalid input. Please try again!")

    month = MONTHS[month]

    df = df[df['Date'] == date]
    df = df[df['Month'] == month]

    if df.shape[0] == 0:
        print("Looks like there are no entries that match your requests.")
    else:
        display_info(df)


def search_by_filters(df):
    """
    Called when the user decides to look up information using filters.
    User can choose to filter by month, day of the week or both.
    """

    day = month = "all"
    while True:
        filter = input("\nWould you like to filter by month, day or both?").strip()
        if filter.lower() in ['month', 'day', 'both']:
            break
        print("\nInvalid input! Please try again.")

    print("\nYou chose to filter by " + filter)

    # User chose to filter by day of the week
    if filter == "day":
        while True:
            day = input(
                "\nEnter a day of the week to filter by: Mon, Tue, Wed, Thu, Fri, Sat, Sun: ").strip()
            if day.title() in DAYS.keys():
                day = DAYS[day.title()]
                break
            print("\nInvalid input! Please try again.")

    # User chose to filter by a particular month
    elif filter == 'month':
        while True:
            try:
                month = int(input(
                    "\nEnter a month to filter by (1 - 6): ").strip())
            except ValueError:
                print("Invalid input. Please try again!")
            else:
                if(month in range(1, 7)):
                    month = MONTHS[month]
                    break
                print("\nInvalid input! Please try again.")

    # User chose to filter by a day of the week in a particular month
    elif filter == 'both':
        while True:
            try:
                month = int(input(
                    "\nEnter a month to filter by (1 - 6): "))
            except ValueError:
                print("Invalid input. Please try again!")
            else:
                if(month not in range(1, 7)):
                    print("\nInvalid input! Please try again.")
                else:
                    month = MONTHS[month]
                    while True:
                        day = input(
                            "\nEnter a day of the week to filter by: Mon, Tue, Wed, Thu, Fri, Sat, Sun: ").strip()
                        if day.title() in DAYS.keys():
                            day = DAYS[day.title()]
                            break
                        print("\nInvalid input! Please try again.")
                    break

    if day != "all":
        df = df[df['Day of week'] == day]
    if month != "all":
        df = df[df['Month'] == month]

    if df.shape[0] == 0:
        print("Looks like there are no entries that match your requests.")
    else:
        display_info(df)


def display_info(df):
    print("\nHeres the data you asked for:\n")
    time_stats(df)
    station_stats(df)
    trip_duration_stats(df)
    user_stats(df)


def display_data(df):
    """
    Function that enables the user to parse the data set either from the
    beginning or from a certain point in the data, displaying a certain number
    of rows at a time (determined by the value of step)

    """
    df.drop(['Day of week', 'Month', 'Hour', 'Date'], axis=1, inplace=True)
    start = 0
    while True:
        choice = input("\nHow would you like to search?: \
        \n1. From a certain point \
        \n2. From the start\n").strip()

        if(choice not in ['1', '2']):
            print("\nInvalid input! Please try again.")
            continue
        break

    if(choice == '1'):
        while True:
            try:
                start, step = map(int, input("\nEnter start and step values: ").split())
            except ValueError:
                print("\nInvalid input! Please try again.")
                continue
            else:
                end = start + step
                if end > df.shape[0]:
                    print("\n--Out of bounds--\n")
                    break
                print(df.iloc[start: end, :])
                while True:
                    choice = input(
                        "\nWould you like to see %d more lines of data?(y/n): " % step).strip()
                    if choice.upper() not in ['Y', 'N']:
                        print("\nInvalid input! Please try again.")
                    elif(choice.upper() == 'Y'):
                        start = start + step
                        end = end + step
                        print(df.iloc[start: end, :])
                    else:
                        break
                break

    elif(choice == '2'):
        while True:
            try:
                step = int(input("\nEnter a value to increment by: "))
            except ValueError:
                print("\nPlease enter a non negative integer.")
                continue
            else:
                if step < 0:
                    print("\nPlease enter a non negative integer.")
                    continue
                else:
                    end = start + step
                    if end > df.shape[0]:
                        print("\n--Out of bounds--\n")
                        break
                    print(df.iloc[start: end, :])
                    while True:
                        choice = input(
                            "\nWould you like to see %d more lines of data?(y/n): " % step).strip()
                        if choice.upper() not in ['Y', 'N']:
                            print("\nInvalid input! Please try again.")
                        elif(choice.upper() == 'Y'):
                            start = start + step
                            end = end + step
                            print(df.iloc[start: end, :])
                        else:
                            break
                    break
            break
    else:
        print("\nInvalid input! Please try again.")


def user_interface(df):

    while True:
        print("\nWhat would you like to do today?:\
        \n1. Explore the data on my own (raw data).\
        \n2. Look at the entries for a specific date.\
        \n3. Filter the data (by month/day/both).\
        \n4. Get some general information (no filters).\
        \n5. I'm done for now. (exit)")

        try:
            choice = int(input())
        except ValueError:
            print("Invalid input. Please try again!")
        else:
            if choice in range(1, 6):
                break
            print("\nInvalid input! Please try again.")

    if choice == 1:
        display_data(df)
    elif choice == 2:
        search_by_date(df)
    elif choice == 3:
        search_by_filters(df)
    elif choice == 4:
        display_info(df)
    else:
        print('-'*80)  # ------------------------------------------------------
        print("\n Goodbye!\n")
        print('-'*80)  # ------------------------------------------------------
        exit()


def main():
    while True:
        df = get_city()
        user_interface(df)

        print('-'*80)  # ------------------------------------------------------
        restart = input('\nWould you like to restart? Enter yes or no.\n').strip()
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
