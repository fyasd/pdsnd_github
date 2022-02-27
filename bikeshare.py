import time
import pandas as pd
import matplotlib.pyplot as plt

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Use a cascade of streamlined questions to prompt the user to specify a
    city, month, and day to be analyzed.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no
        month filter
        (str) day - name of the day of week to filter by, or "all" to apply no
        day filter
    """
    print('Right on! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    # use a while loop to handle invalid inputs
    while True:
        city = input('Do you want to explore data on Chicago, New York City,'
                     ' or Washington?\n').lower()
        if city not in (CITY_DATA.keys()):
            print('Please enter Chicago, New York City, or Washington.')
            continue
        else:
            break

    # set user input for month & day of week to 'all' -or-
    # set filter params to the specified month or day with filter funcs

    while True:
        filter_yes_no = input('Do you want to filter the data?'
                              ' (yes or no)\n').lower()
        if filter_yes_no == 'no':
            month = 'all'
            day = 'all'
            break
        elif filter_yes_no == 'yes':
            # note: contents excised to safeguard against invalid user input
            break
        else:
            print('Please enter yes or no.')
            continue

    def filter_month():
        """Return the month to be filtered, as specified by the user."""
        while True:
            month = input('Please specify a month between January and'
                          ' June.\n').lower()
            if month not in ('january', 'february', 'march', 'april', 'may',
                             'june'):
                print('Please enter January, February, March, April, May, or'
                      ' June.')
                continue
            else:
                break
        return month

    def filter_day():
        """Return the day to be filtered, as specified by the user."""
        while True:
            day = input('Please specify the day of the week.\n').lower()
            if day not in ('monday', 'tuesday', 'wednesday', 'thursday',
                           'friday', 'saturday', 'sunday'):
                print('Please enter Monday, Tuesday, Wednesday, Thursday,'
                      ' Friday, Saturday, or Sunday.')
                continue
            else:
                break
        return day

    # note: from here, triggering an 'else' won't cause the script to continue
    # all the way back to "Do you want to filter the data?" like it would have
    # were it still nested in the while loop above
    while filter_yes_no == 'yes':
        filter_param = input('Do you want to filter by month, day, or'
                             ' both?\n').lower()
        if filter_param == 'month':
            month = filter_month()
            day = 'all'
            break
        elif filter_param == 'day':
            month = 'all'
            day = filter_day()
            break
        elif filter_param == 'both':
            month = filter_month()
            day = filter_day()
            break
        else:
            print('Please enter \'month\' or \'day\' or \'both\''
                  ' (without the quotes).')
            continue

    print('\u2015'*39)
    return city, month, day


def load_data(city, month, day):
    """
    Load data for the specified city and filter by month and day if
    applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no
        month filter
        (str) day - name of the day of week to filter by, or "all" to apply no
        day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, month, day):
    """Display statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel\u2026\n')
    start_time = time.time()

    # display the most common month unless filtering by month
    if month == 'all':
        print('The most common month is', df['month'].mode()[0])
    else:
        print('You filtered by month:', month.title())

    # display the most common day of week unless filtering by month
    if day == 'all':
        print('The most common day of week is', df['day_of_week'].mode()[0])
    else:
        print('You filtered by day:', day.title())

    # display the most common start hour
    hour_str = str(df['Start Time'].dt.hour.mode()[0])
    hour_time = time.strptime(hour_str, "%H")

    print('The most common start hour is',
          time.strftime("%I %p", hour_time).lstrip("0"))

    print(f'\nThis took {time.time() - start_time} seconds.')
    print('\u2015'*39)


def station_stats(df):
    """Display statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip\u2026\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station is',
          df['Start Station'].mode()[0])

    # display most commonly used end station
    print('The most commonly used end station is',
          df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    trip = df['Start Station'] + ' to ' + df['End Station']

    print('The most commonly occurring trip is\u2025\n'
          'from', trip.mode()[0])

    print(f'\nThis took {time.time() - start_time} seconds.')
    print('\u2015'*39)


def trip_duration_stats(df):
    """Display statistics on the total and average (median) trip duration."""

    print('\nCalculating Trip Duration\u2026\n')
    start_time = time.time()

    # display total travel time in a human-readable format
    tot_dur = df['Trip Duration'].sum()

    print(f'The total travel time is about {round(tot_dur / 3600)}'
          f' hours\u2012\nthat amounts to more than {int(tot_dur // 604800)}'
          ' weeks-worth of cycling!')

    # display median travel time in a human-readable format
    # note: median is more suitable than mean for skewed data
    median_dur = df['Trip Duration'].median()
    mins, secs = divmod(median_dur, 60)

    print(f'The median travel time is {int(mins)} minutes and {int(secs)}'
          ' seconds')

    print(f'\nThis took {time.time() - start_time} seconds.')
    print('\u2015'*39)


def user_stats(df):
    """Display statistics on bikeshare users."""

    print('\nCalculating User Stats\u2026\n')
    start_time = time.time()

    # display counts of user types
    subscriber_trips = df['User Type'].value_counts()[0]
    customer_trips = df['User Type'].value_counts()[1]

    print(f'Of the trips taken, {subscriber_trips} were by subscribers\u2012\n'
          f'and {customer_trips} were by unsubscribed customers\n')

    # display counts of gender if available
    if 'Gender' in df:
        male_trips = df['Gender'].value_counts()[0]
        female_trips = df['Gender'].value_counts()[1]
        unspecified_gender_trips = len(df) - df['Gender'].count()

        print('Of the trips taken\u2012for which gender was specified:\n'
              f'\u2043 {male_trips} trips were taken by males\n'
              f'\u2043 {female_trips} trips were taken by females\n'
              f'Note: {unspecified_gender_trips} trips were taken by people of'
              ' unspecified gender\n')

    # display earliest, most recent, and most common year of birth if available
    if 'Birth Year' in df:
        S = df['Birth Year']
        # get the deviation from the mean for each value-in absolute terms
        # index values within 3 standard deviations
        birth_year_sans_outlier = S[(S-S.mean()).abs() <= 3 * S.std()]
        mode_year = int(df['Birth Year'].mode())
        min_year = int(df['Birth Year'].min())
        max_year = int(df['Birth Year'].max())
        int_year_sans_outlier = int(birth_year_sans_outlier.min())
        unspecified_year_trips = int(len(df) - df['Birth Year'].count())

        print('Of the trips taken\u2012for which birth year was specified:\n'
              f'\u2043 {mode_year} was the most common year of birth\n'
              f'\u2043 {min_year} was the earliest year of birth\n'
              f'\u2043 {max_year} was the latest year of birth\n'
              f'Note: {int_year_sans_outlier} was the earliest year of birth'
              ' \u2012sans outliers\u2012\n'
              f'Note: {unspecified_year_trips} trips were taken by people of'
              ' unspecified birth year')

    print(f'\nThis took {time.time() - start_time} seconds.')
    print('\u2015'*39)


def show_vis(df, city):
    """Display visualizations describing the data."""

    while True:
        vis_yes_no = input('Do you want to see a boxplot describing the data'
                           '\u2012sans outliers?\nNote: The script will pause'
                           ' until the visualizer is closed.\n(yes or no)\n'
                           ).lower()
        if vis_yes_no == 'yes':
            dur_mins = df['Trip Duration'] / 60
            if city != 'washington':
                fig, axs = plt.subplots(1, 2, figsize=(8, 4))
                dur_mins.plot.box(showfliers=False, ax=axs[0],
                                  ylabel='Minutes', title='Distribution of'
                                                          ' Trip Durations')
                df['Birth Year'].plot.box(showfliers=False, ax=axs[1],
                                          title='Distribution of Birth Years')
            else:
                dur_mins.plot.box(showfliers=False, ylabel='Minutes',
                                  title='Distribution of Trip Durations')
            plt.show()
            break
        elif vis_yes_no == 'no':
            break
        else:
            print('Please enter yes or no.')
            continue

    print('\u2015'*39)


def show_data(df):
    """Display the raw data for the specified city, month and day."""

    while True:
        data_yes_no = input('Do you want to take a peek at the raw data?'
                            ' (yes or no)\n').lower()
        if data_yes_no == 'yes':
            print(df.head())
            break
        elif data_yes_no == 'no':
            break
        else:
            print('Please enter yes or no.')
            continue

    cur_row = 5

    while data_yes_no == 'yes':
        scroll_yes_no = input('Do you want to see some more?'
                              ' (yes or no)\n').lower()
        if scroll_yes_no == 'yes':
            print(df.iloc[cur_row:cur_row + 5])
            cur_row += 5
            if cur_row > len(df):
                print('There is no more data to display.')
                break
            continue
        elif scroll_yes_no == 'no':
            break
        else:
            print('Please enter yes or no.')
            continue


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_vis(df, city)
        show_data(df)

        restart = input('Do you want to keep exploring? (yes or no)\n')
        if restart.lower() != 'yes':
            print('Goodbye!')
            break


if __name__ == "__main__":
    main()
