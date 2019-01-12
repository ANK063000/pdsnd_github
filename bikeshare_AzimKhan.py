import time
import pandas as pd
import numpy as np
import calendar as clr
from datetime import date


city_list = ('chicago','new york city','washington')
month_list = ('all','january','february','march','april','may','june','july','august','september','october','november','december')
day_list = ('all','monday','tuesday','wednesday','thursday','friday','saturday','sunday')
options_list = ('month','day','both','neither')

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
    print('\nHello! Let\'s explore some US bikeshare data!')

    # 1 get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Select one of the following cities to review: Chicago, New York City or Washington? \n').lower()

    while city not in city_list:
        city = input('Please try again and specify the city you are interested in. Type "Chicago", "New York City" or "Washington".\n').lower()

    # 2 get decision on whether user wants to filter by Month, Day, both or not at all
    option2 = input('\nWould you like to filter on month, day, both or neither?\n').lower()

    while option2 not in options_list:
        option2 = input('\nPlease try again and specify your filters by typing "month", "day", "both" or "neither".\n')

    if option2 == 'both':
        # get user input for month (all, january, february, ... , june)
        month = input('\nWhich month? January, February, March, April, May or June?\n').lower()

        while month not in month_list:
            month = input('\nPlease try again and specify the month you are interested in.  Type "January", "February", "March", "April", "May" or "June".\n').lower()

        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input('\nWhat day? Monday, Tuesday, ... Sunday?\n').lower()

        while day not in day_list:
            print('\nPlease try again and specify the day of the week.  Type "Monday", "Tuesday", "Wednesday" ... "Sunday".\n').lower()

    elif option2 == 'month':
        day = 'all'
        # get user input for month (all, january, february, ... , june)
        month = input('\nWhich month? January, February, March, April, May or June?\n').lower()

        while month not in month_list:
            month = input('\nPlease try again and specify the month you are interested in.  Type "January", "February", "March", "April", "May" or "June".\n').lower()

    elif option2 == 'day':
        month = 'all'
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input('\nWhat day? Monday, Tuesday, ... Sunday?\n').lower()

        while day not in day_list:
            print('\nPlease try again and specify the day of the week.  Type "Monday", "Tuesday", "Wednesday" ... "Sunday".\n').lower()

    elif option2 == 'neither':
        month = 'all'
        day = 'all'

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
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicables
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january','february','march','april','may','june','july','august','september','october','november','december']
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

    # changes Start Time from string
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # display the most common month
    common_mo = df['month'].mode()[0]
    print('Most Common Month: ', clr.month_name[common_mo])

    # display the most common day of week
    common_wk = df['day_of_week'].mode()[0]
    print('Most Common Day of the Week: ', common_wk)

    # display the most common start hour
    common_hr = df['hour'].mode()[0]
    print('Most Common Hour: ', common_hr)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    st_station = df['Start Station'].mode()[0]
    print("Most common Start Station: ", st_station)

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print("Most common End Station: ", end_station)

    # display most frequent combination of start station and end station trip
    df['combo'] = df['Start Station'] + ' to ' + df['End Station']
    combination = df['combo'].mode()[0]
    print("Most traveled route: ",combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #df['Start Time'] = pd.to_datetime(df['Start Time'])
    #df['End Time'] = pd.to_datetime(df['End Time'])

    # display total travel time
    # total_time = (df['End Time'] - df['Start Time']).sum()
    tvl_time = df['Trip Duration'].sum() // 60
    print("Total travel time: ",tvl_time," minutes")

    # display mean travel time
    avg_time = df['Trip Duration'].mean() // 60
    print("Average travel time: ",avg_time," minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    today = date.today()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("User Types: ")
    print(user_types)

    # Display counts of gender
    # washington.csv does not contain Gender information
    if 'Gender' in df.columns:
        gender = df['Gender'].fillna('Undisclosed').value_counts()
        print("\nGender:")
        print(gender)
    else:
        print("\nNo gender information available.")

    # Display earliest, most recent, and most common year of birth
    # washington.csv does not contain Birth Year information
    if 'Birth Year' in df.columns:
        earliest_birth = df['Birth Year'].min()
        print("\nOldest age of customer:", today.year - int(earliest_birth))

        recent_birth = df['Birth Year'].max()
        print("Youngest age of customer:", today.year - int(recent_birth))

        birth_year = df['Birth Year'].mode()[0]
        print("Average age of customer: ", today.year - int(birth_year))

    else:
        print("\nNo birth year information available.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def individual_stats(df):
    """Displays statistics on bikeshare users."""

    # Prompt user if they want to see invdividual stats
    ind_prompt1 = input('Would you like to see stats at an individual level?  Y/N\n')

    x = 0
    y = 5

    while ind_prompt1.lower() == 'y':
        #Im sure there is a better was to do this with a loop...using brute force here, sorry!
        #I dont like seeing the data as a DataFrame and prefer a Series
        print('\n',df.loc[x])
        x += 1
        print('-'*40)

        print('\n',df.loc[x])
        x += 1
        print('-'*40)

        print('\n',df.loc[x])
        x += 1
        print('-'*40)

        print('\n',df.loc[x])
        x += 1
        print('-'*40)

        print('\n',df.loc[x])
        x += 1
        print('-'*40)

        ind_promt2 = input('\nWould you like to see the next 5?  Y/N\n')

        if ind_promt2.lower() != 'y':
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        individual_stats(df)

        restart = input('\nWould you like to restart? Y/N.\n')
        if restart.lower() != 'y':
            break

if __name__ == "__main__":
	main()
