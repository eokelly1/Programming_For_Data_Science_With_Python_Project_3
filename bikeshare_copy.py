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
    #identifies the valid values for city, month, and day
    valid_cities = ['chicago', 'new york city', 'washington']
    valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

    # gets user input for city (chicago, new york city, washington).
    while True:
        city = input("Please select a city (Chicago, New York City, Washington): ").lower()
        if city in valid_cities:
            break
        #invalid input response
        else:
            print("Please select a valid city.")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Please select a month (All, January, February, March, April, May, June): ").lower()
        if month in valid_months:
            break
        #invalid input response
        else:
            print("Please select a valid month.")

    #gets user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Please select a day (All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday): ").lower()
        if day in valid_days:
            break
        #invalid input response
        else:
            print("Please select a valid day.")

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
    #load datafile into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    #convert state time to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #extract month and day
    df['month'] = df['Start Time'].dt.month
    df['day_in_week'] = df['Start Time'].dt.weekday

     #filter for month input of dataset
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    #filter for day input of dataset
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)
        df = df[df['day_in_week'] == day]

    return df


def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # determines the most common month
    most_common_month = df['month'].value_counts().idxmax()
    # when selection is all
    if month == 'all':
        print('The most common month in ',str(city),' is', str(most_common_month))
    # when selection is a month
    else:
        print('You have selected ',str(month),'so the most common month will be your selection')

    # display the most common day of week
    most_common_day = df['day_in_week'].value_counts().idxmax()
    # when selection is all
    if day == 'all':
        print('The most common day in ', str(city),' is', str(most_common_day))
    # when selection is a day
    else:
        print('You have selected ', str(day),'so the most common day will be your selection')

    # display the most common start hour
    #this will extract the hour from the Start Time column
    df['Start Hour'] = df['Start Time'].dt.hour
    #Identify the most common start hour and print
    most_common_starthour = df['Start Hour'].value_counts().idxmax()
    print('The most common hour for start time from your selection is', str(most_common_starthour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station for your selection is:',
            df['Start Station'].value_counts().idxmax())

    # display most commonly used end station
    print('The most commonly used end station for your selection is:',
            df['End Station'].value_counts().idxmax())

    # display most frequent combination of start station and end station trip
    #Create new column with start and end stations combined
    df['Station Combination'] = df['Start Station'] + ' (start) and ' + df['End Station'] + ' (end)'
    #print station compination
    print('The most frequent combination of start and end station trip is:', df['Station Combination'].value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    #Print total and transform from seconds to hours
    print('Total travel time is:', round(df['Trip Duration'].sum()/ 60 / 60 ,0), 'hours')

    # display mean travel time
    #Print Mean and transform from seconds to hours
    print('Mean travel time is:', round(df['Trip Duration'].mean()/ 60 ,0), 'minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns:
        print(df['User Type'].value_counts())

    # Display counts of gender
    #identify if gender is in selection
    if 'Gender' in df.columns:
        print(df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        #Print the earliest year from the selection
        print('The earliest year of birth is:', int(df['Birth Year'].min()))
        #Print the most recent year from the selection
        print('The most recent year of birth is:', int(df['Birth Year'].max()))
        #Print the most common year from the selection by using mode
        print('The most common year of birth is:', int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#New function which allows for user to see raw data
def raw_data(df):
    #Displays 5 lines of raw data at a time when yes is selected.
    # define index i, start at line 1
    i = 1
    while True:
        r_data = input('Would you like to see 5 lines of raw data? Enter yes or no.')
        if r_data.lower() == 'yes':
            # print current 5 lines
            print(df[i:i+5])

            # increase index by 5 to print next 5 lines
            i = i+5

        else:
            # when no is selected break
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, city, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        # additonal function to display raw data
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Thank you and have a good day')
            break


if __name__ == "__main__":
	main()

#Recources

#Udacity Course and Practice Questions
#https://learn.udacity.com/nanodegrees/nd104/parts/cd0024/lessons/ls1727/concepts/6e3bdeed-dd42-44d8-9865-57b1f679fdc4?tab=lesson
#https://learn.udacity.com/nanodegrees/nd104/parts/cd0024/lessons/ls1727/concepts/7e54db42-a52e-47d4-b422-96d9368910ea?tab=lesson
#https://learn.udacity.com/nanodegrees/nd104/parts/cd0024/lessons/ls1727/concepts/2d64a03d-e921-4c75-92f8-b188611ee3cf?tab=lesson
