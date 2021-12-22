import time
from datetime import datetime
import pandas as pd
import numpy as np
import calendar as cd
pd.set_option("display.precision", 4)
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv',
             'c': 'chicago.csv',
             'n': 'new_york_city.csv',
             'w': 'washington.csv'}
months = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4,
          'may': 5, 'jun': 6, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, 'all': 'all'}
days = {'fri': 'Friday', 'thu': 'Thursday', 'wedn': 'Wednesday',
        'mon': 'Monday', 'tue': 'Tuesday', 'sat': 'Saturday', 'sun': 'Sunday', 'all': 'all'}

# gets user input for filters  to pass them to the next function


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
    while True:
        city = input(
            'Enter either the name of your desired city or just the character chicago(c),New York(n) or Washington(w) ').lower()
        if city in CITY_DATA:
            break
    # get user input for month (all, january, february, ... , june)
    while True:
        month = str(input(
            'Enter the month you want to filter with(jan,feb,mar,apr,may,jun) or as nmerical value enter all to apply no filter ')).lower()
        # checks if use input is a valid input or not
        if month in months:
            break
        # if no input is valid function continue to prompt user to input valid data

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = str(input(
            'Enter the day you want to filter with(Fri,Thu,Wedn,Mon,Tue,Sat,Sun) or enter all to apply no filter ').lower())
        # checks if use input is a valid input or not
        if day in days:
            break
        # if no input is valid function continue to prompt user to input valid data

    print('-'*40)
    return city, month, day


# loads the specified city data with the filter passed from the previous function


def load_data(city, month, day):
    if month != 'all':
        month = int(month)
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load file of choosen city in a df
    city_file = pd.read_csv(city)
    # converts start time and end time column to datetime format
    city_file['Start Time'] = pd.to_datetime(city_file['Start Time'])
    city_file['End Time'] = pd.to_datetime(city_file['End Time'])
    # create columns for month ,day and hour for the start time column
    city_file['month_start'] = city_file['Start Time'].dt.month
    city_file['day_start'] = city_file['Start Time'].dt.day_name()
    city_file['hour_start'] = city_file['Start Time'].dt.hour
    city_file['trip'] = city_file['Start Station']+'|'+city_file['End Station']
    # assign the city file df to df variable
    df = city_file
    # checks if month and day == all
    # filter by month
    if month != 'all':
        df = df[df['month_start'] == month]
    # filter by day
    if day != 'all':
        df = df[df['day_start'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    Args:
        (Data frame) df --> data frame passd on from load data function with the desired city data filtered
    outputs:
        most common month
        most common day of week
        most common start hour

    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df.month_start.mode(dropna=True)[0]
    print("Most common month is "+cd.month_name[most_common_month])
    # display the most common day of week
    most_common_day = df.day_start.mode(dropna=True)[0]
    print("Most common day is "+most_common_day)
    # display the most common start hour
    most_common_hour = datetime.strptime(str(
        df.hour_start.mode(dropna=True)[0]), "%H").strftime("%I %p")

    print("Most common hour is : "+str(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
      Args:
        (Data frame) df --> data frame passd on from load data function with the desired city data filtered
    outputs:
        most common used start station
        most common used end station
        most common trip
        """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_used_start_station = df['Start Station'].mode(dropna=True)[0]
    print('Most commonly used start station is '+(most_used_start_station))
    # display most commonly used end station
    most_used_end_station = df['End Station'].mode(dropna=True)[0]
    print('Most commonly used end station is '+most_used_end_station)

    # display most frequent combination of start station and end station trip
    # to get the most commong trip a coulmn 'trip' was added that contains the combination of start and end stations

    most_common_trip = df['trip'].mode(dropna=True)[0]
    # to get the start trip in the most common trip we split at '|' that is already added and get the first part
    start_station = most_common_trip.split('|')[0]
    end_station = most_common_trip.split('|')[1]

    print('Most frequent combination of start station and end station trip is : ' +
          start_station + ' and '+end_station)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
        Args:
        (Data frame) df --> data frame passd on from load data function with the desired city data filtered
    outputs:
        Total number of travel time
        Mean travel time


    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # converts column data type to numeric(float)
    df['Trip Duration'] = pd.to_numeric(df['Trip Duration'])
    # get sum  of all travel time
    total_travel_time = df['Trip Duration'].sum()  # in seconds
    # converts total time to different time units
    time_count = float(total_travel_time)
    day = time_count // (24 * 3600)
    time_count = time_count % (24 * 3600)
    hour = time_count // 3600
    time_count %= 3600
    minutes = time_count // 60
    time_count %= 60
    seconds = time_count
    print("Total travel time is : %d day:%d hour:%d minute :%d seconds" %
          (day, hour, minutes, seconds))
    # display total travel time
    # get mean of travel time
    average_travel_time = df['Trip Duration'].mean()  # display in seconds
    time_count = float(average_travel_time)
    day = time_count // (24 * 3600)
    time_count = time_count % (24 * 3600)
    hour = time_count // 3600
    time_count %= 3600
    minutes = time_count // 60
    time_count %= 60
    seconds = time_count
    # display mean travel time
    print("Average travel time is : %d day:%d hour:%d minute :%d seconds" %
          (day, hour, minutes, seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users.
       Args:
        (Data frame) df --> data frame passd on from load data function with the desired city data filtered
        (str) city --> to determine if the city is washington so that we don't calculate gender
    outputs:
        count if user types(customer OR subscriber)
        earliest year of user
        most recent year of user
        most common year of birh

    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    # value.counts() --> counts how many value found for each unique element in the column
    count_of_user_types = df['User Type'].value_counts()
    print('User types are {}'.format(count_of_user_types))
    # Skip count of gender and age stats if city is washington
    if city == 'washington.csv':
        print('Gender counts and age stats not available in Washington')
    else:
        # Display counts of gender
        df['Gender'].fillna('Not Defined', inplace=True)
        count_of_user_gender = df['Gender'].value_counts()
        print('User genders are')
        print(count_of_user_gender)
        # Display earliest, most recent, and most common year of birth
        # convert values in column to numeric(float)
        df['Birth Year'] = pd.to_numeric(df['Birth Year'])
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_bd = int(df['Birth Year'].mode(dropna=True)[0])
        print('Earliest year is :{}'.format(earliest_year))
        print('Most recent year is :{}'.format(most_recent_year))
        print('Most common year of Birth :{}'.format(most_common_bd))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(city):
    """Displays raw data from the file
    Args:
        city:city which the user specified at first
    returns:
        if user choose to display sample it returns a set raw data from the file
    """
    city_file = pd.read_csv(city)
    decision = input('Do you want to see a sample of data?(y,n)')
    # if user wants to see raw data from file
    if decision.lower() == 'y':
        print(city_file.sample(5))
        # re-ask if user wants to see some more sample
        display_raw_data(city)


def main():
    while True:
        c, m, d = get_filters()
        city = CITY_DATA[c]
        month = months[m]
        day = days[d]

        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(city)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() not in['yes', 'y']:
            break


if __name__ == "__main__":
    main()
