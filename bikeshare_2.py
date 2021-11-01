import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Enter city name between (chicago, new york city, washington)").lower()
    while city != 'chicago' and city != 'new york city' and city != 'washington':
        city = input("Enter city name between (chicago, new york city, washington)").lower()

    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = input("Enter month name between (all, january, february, ... , june)").lower()
    while month != 'all' and month not in months:
        month = input("Enter month name between (all, january, february, ... , june)").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'saturday', 'sunday']
    day = input("Enter day of the week between (all, monday, tuesday, ... sunday)").lower()
    while day != 'all' and day not in days_week:
        day = input("Enter day of the week between (all, monday, tuesday, ... sunday)").lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('The most common month is: ', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('The most common day of week is: \n', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour =df['hour'].mode()[0]
    print('The most common hour is: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def five_rows_displays(df):
    """
    Displays five rows from the dataframe receive into a argument.

    Args:
        (pandas df) df - Pandas DataFrame containing city data filtered by month and day
    Returns:
        Five rows displayed
    """
    view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?")
    start_loc = 0
    while (view_data=='yes'):
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most common Start Station is: \n', format(common_start_station))

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most common End Station is: \n', format(common_end_station))

    # display most frequent combination of start station and end station trip
    df['start_end_station'] = df['Start Station'] + ' - ' + df['End Station']
    common_start_end_station = df['start_end_station'].mode()[0]
    print('The most frequent combination of start station and end station is: \n', format(common_start_end_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print('The total travel time is: \n', format(total_time))

    # display mean travel time
    total_time = df['Trip Duration'].mean()
    print('The mean travel time is: \n', format(total_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of user types: \n', user_types)

    # Display counts of gender
    try:
        gender_user_counts = df['Gender'].value_counts()
        print('Counts of gender: \n', gender_user_counts)
    except Exception as e:
        print('Gender field not exist')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()
        print('Earliest, most recent, and most common year of birth: \n', earliest, most_recent, most_common)
    except Exception as e:
        print('Birth Year field not exist')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        print(city, month, day)
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        five_rows_displays(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
