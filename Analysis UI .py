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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("In which city chicago, new york city, or washington: ").lower()
    while city not in CITY_DATA.keys():
        print ("Error! this city in not available")
        city = input("In which city chicago, new york city, or washington: ").lower()


    # TO DO: get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input("Which month form january to june or all of them? ").lower()
        if month in months:
            break
        else:
            print("Error! this month in not available")
            
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input("Which day of the week or all of them? ").lower()
        if day in days:
            break
        else:
            print("Error! this day in not correct")


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
    '''
    load data file into a dataframe 
    and convert the Start Time to datetime
    the extracting month, day, hour into columns
    '''
    df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    #month filter if the user asked
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    #day filter if the user asked
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    '''
    TO DO:
    display the most common month
    and the most common day of week
    and the most common start hour
    '''
    popular_month = df['month'].mode()[0]
    print("The Most Popular Month:", popular_month)

    popular_day_of_week = df['day_of_week'].mode()[0]
    print("The Most Day Of Week:", popular_day_of_week)

    popular_common_start_hour = df['hour'].mode()[0]
    print("The Most Common Start Hour:", popular_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    '''
    TO DO: 
    display most commonly used start station
    and most commonly used end station
    and most frequent combination of start station and end station trip
    '''
    popular_start_station = df['Start Station'].mode()[0]
    print("The Most Start Station:", popular_start_station)

    popular_end_station = df['End Station'].mode()[0]
    print("The Most End Station:", popular_end_station)

    group_field=df.groupby(['Start Station','End Station'])
    popular_combination_station = group_field.size().sort_values(ascending=False).head(1)
    print("The Most frequent combination of Start and End Station trip:\n" , popular_combination_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    '''
    TO DO:
    display total travel time
    and mean travel time
    '''
    total_travel_time = df['Trip Duration'].sum()
    print("The Total of Travel Time:", total_travel_time)

    mean_travel_time = df['Trip Duration'].mean()
    print("The Mean of Travel Time:", mean_travel_time)

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_type = df['User Type'].value_counts()
    print("User Type Count:"+" "+ str(count_user_type) +"\n")
        
    # Not all the cities have the “Gender” column
    if 'Gender' in df.columns:
        print("users types are \n", df['Gender'].value_counts())

    # Display counts of gender
    print("Stats of Gender :")
    print(df['Gender'].value_counts())
        
    # Display earliest, most recent, and most common year of birth
    print("Stats of Birth Year :")
        
    most_common_year = df['Birth Year'].mode()[0]
    print(" The Most Common Birth Year:" ,most_common_year)
        
    most_recent_year = df['Birth Year'].max()
    print("The Most Recent Birth Year:" ,most_recent_year)
        
    earliest_year = df['Birth Year'].min()
    print("The Earliest Birth Year:" ,earliest_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?")
        start_loc = 0
        keep_asking = True
        while (keep_asking):
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
            view_display = input("Do you wish to continue?: ").lower()
            if view_display == "no": 
                keep_asking = False

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
