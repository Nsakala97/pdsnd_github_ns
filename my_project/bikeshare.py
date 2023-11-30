import time
import pandas as pd
from statistics import mode
from datetime import datetime

city_data = {'chicago': 'chicago.csv', 'new york': 'new_york_city.csv', 'washington': 'washington.csv'}
acceptable_months = ["all", "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
acceptable_days = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
acceptable_cities = ["all", "chicago", "new york", "washington"]
#This function gets user input to be used as filters

def get_filters():
    user_input_city = user_input_month = user_input_day = None  # Initialize variable
   

    while True:
        try:
            user_input_city = input("Hello! Let's explore some US bikeshare data\n What city would you like to look at? ").lower()

            if user_input_city not in acceptable_cities:
                raise ValueError("City input must be an acceptable city. This dataset includes chicago, new york, and washington.")
            elif user_input_city == "all":
                user_input_city = "all"
            break
        except ValueError as e:
            print(f"Error: {e}")

    while True:
        try:
            user_input_month = input("What month would you like to look at? ").lower()
           

            if user_input_month not in acceptable_months:
                raise ValueError("Month input must be an acceptable month of the year.")

            if user_input_month == "all":
                user_input_month = "all"
            break
        except ValueError as e:
            print(f"Error: {e}")

    while True:
        try:
            user_input_day = input("What day would you like to look at? ").lower()
            

            if user_input_day not in acceptable_days:
                raise ValueError("Day input must be an acceptable day of the week.")

            if user_input_day == "all":
                user_input_day = "all"
            break
        except ValueError as e:
            print(f"Error: {e}")

    return user_input_city, user_input_month, user_input_day


#This function loads data based on the filters provided
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (list) acceptable_months - list of acceptable months
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    if city != 'all':
        city_data_path = city_data[city]
        df = pd.read_csv(city_data_path)
        df['Start Time'] = pd.to_datetime(df['Start Time'])
       
    else:
        df = pd.DataFrame()
        for city_name, city_path in city_data.items():
            city_df = pd.read_csv(city_path)
            city_df['Start Time'] = pd.to_datetime(city_df['Start Time'])
            df = pd.concat([df, city_df], ignore_index=True)

    if month != 'all':
        
        month_index = acceptable_months.index(month) 
        
        
        df = df[df['Start Time'].dt.month == month_index]
        

    if day != 'all':
        # Assuming day is an integer (1 for Monday, 2 for Tuesday, ..., 7 for Sunday)
       day_index = acceptable_days.index(day) 
       df = df[df['Start Time'].dt.dayofweek == (day_index - 1)]
        

    return df
#This function displays time statistics based on the data loaded
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    if df.empty:
        print("No data to analyze.")
        return

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month_name'] = df['Start Time'].dt.strftime('%B')
    popular_month = mode(df['month_name'])
    
    print(f"The most common month is: {popular_month}")
    df['weekday_name'] = df['Start Time'].dt.strftime('%A')

    popular_day = mode(df['weekday_name'])
    print(f"The most common day of the week is: {popular_day}")

    popular_hour = mode(df['Start Time'].dt.hour)
    print(f"The most common start hour is: {popular_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    if df.empty:
        print("No data to analyze.")
        return

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station.
    # Count for each of the start stations.
    start_station_count = df['Start Station'].value_counts()
    # Max station is the station with the highest count
    max_start_station = start_station_count.idxmax()
    print(f"The station with the highest count is: {max_start_station}")

    # TO DO: display most commonly used end station.
    # Count for each of the stations.
    end_station_count = df['End Station'].value_counts()
    # Max station is the station with the highest count.
    max_end_station = end_station_count.idxmax()
    print(f"The end station with the highest count is: {max_end_station}")

    # TO DO: display most frequent combination of start station and end station trip.
    # Combines start and end station to come up with a new column.
    df['Start_and_End_Station'] = df['Start Station'] + ' - ' + df['End Station']
    start_end_count = df['Start_and_End_Station'].value_counts()
    max_start_end_station = start_end_count.idxmax()
    print(f"The start_end station with the highest count is: {max_start_end_station}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    if df.empty:
        print("No data to analyze.")
        return
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time.
    total_travel_time = df['Trip Duration'].sum()
    print(f"The total travel time for this period is: {total_travel_time}")

    # TO DO: display mean travel time.
    mean_travel_time = df['Trip Duration'].mean()
    print(f"The average travel time for this period is: {mean_travel_time}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    
    if df.empty:
        print("No data to analyze.")
        return

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types.
    # This shows the distinct user types and their count.
    user_type = df['User Type'].value_counts()
    print(f"User Type : \nThe different usertypes in the data requested are :\n {user_type}")

    # TO DO: Display counts of.
    # Check if the column exists in the dataset.
    if 'Gender' in df.columns:
        user_gender = df['Gender'].value_counts()
        print(f"Gender:\n The different genders in the data requested are:\n {user_gender}")
    else:
        print("This column does not exist in this dataset. Kindly select a different city for analysis of gender")

    # TO DO: Display earliest, most recent, and most common year of birth.
    # This calculates minimum birth year.
    if 'Birth Year' in df.columns:
        earliest_birth_year = int(df['Birth Year'].min())
        print("Birth year:\n The earliest birth year in this dataset is: {}".format(earliest_birth_year))

        # This calculates the most recent birth year.
        most_recent_birth_year = int(df['Birth Year'].max())
        print("Birth year: \nThe most recent birth year in this dataset is: {}".format(most_recent_birth_year))

        # Calculate the most common year of birth.
        birth_year_count = df['Birth Year']
        max_birth_year_count = int(birth_year_count.value_counts().idxmax())

        print("The most common year of birth in this dataset is: {}".format(max_birth_year_count))
    else:
        print("This column does not exist in this dataset. Kindly select a different city for analysis of birth year")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

#This is for raw data upon user request.

def raw_data_request_function(df):
    start_at = 0
    df_size = 5

    if df.empty:
        print("No data to analyze.")
        return

    while start_at < len(df):
        end_at = start_at + df_size
        print(df.iloc[start_at:end_at])

        more_data = input('\nWould you like to see more data? Enter yes or no.\n').lower()
        if more_data == 'no':
            break

        start_at += df_size





# Run this script.
def main():
    while True:
        user_city, user_month, user_day = get_filters()
        df = load_data(user_city, user_month, user_day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        raw_data_request = input('\nWould you like to see the raw data output? Enter yes or no.\n')
        if raw_data_request.lower() == 'yes':
           
           raw_data_request_function(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
