'''
This is my submitted project in a Udacity data analysis nanodegree program, I used Python to explore data 
related to bike share systems for three major cities in the United States—Chicago, New York City, and Washington. 
I wrote code to import the data and answer interesting questions about it by computing descriptive statistics, 
in addition,script that takes in raw input to create an interactive experience 
in the terminal to present these statistics.
'''
import calendar #I'll use this module in time_stats function to convert number of month into names
import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago':  'chicago.csv',
              'new york city':'new_york_city.csv',
              'washington': 'washington.csv'}

# Filter a city,month and day.
def get_filters():

    name = input("Enter your name: ") #To break the ice :D
    print('\nHello {}! Let\'s explore some US bikeshare data!'.format(name).title())

    #Filter the cities.
    for city in CITY_DATA :
        city = input("\nFirst pick a city (chicago, washington, new york city):  ").lower()
        if city not in CITY_DATA:
            print("\nInvalid Value/ city is not included")
        else:
            print('\n{} ! nice choice, {}'.format(city,name))
            break

    #Filter the months.
    while True :
        month = input("\nwrite a month from January to June or type 'all' to explore the data:  ").lower()
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        if month not in months and month != 'all':
            print("\nInvalid Value or Spelling Mistake")
        else:
            break

    #Filter the days.
    while True :
        day = input("\nInsert a day or type 'all' for the whole week to explore the data:  ").lower()
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']
        if day not in days and day != 'all':
            print("\nInvalid Value or Spelling Mistake") 
        else:
            break

    print('-'*40)
    return city, month, day

#Loads data for the specified city and filters by month and day if applicable    
def load_data(city, month, day):

    # load data file into a dataframe
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


#Displays statistics on the most frequent times of travel.
def time_stats(df):

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most frequent month
    frequent_month_num = df['month'].mode()[0] # display months in numbers
    frequent_month = calendar.month_name[frequent_month_num] # converts (months in numbers) to (months in names)
    print('\nThe most frequent month is: ', frequent_month)

    # display the most frequent day of week
    frequent_day = df['day_of_week'].mode()[0] 
    print('\nThe most frequent day of the week is: ', frequent_day)

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most frequent start hour
    frequent_hour = df['hour'].mode()[0]
    print('\nThe most frequent start hour is: ', frequent_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#Displays statistics on the most popular stations and trip.
def station_stats(df):
    
    print('\nCalculating The Most Frequent Stations and Trip...\n')
    start_time = time.time()

    # display most frequently used start station
    frequent_start = df['Start Station'].mode()[0]
    print('\nThe most frequent start station is: ', frequent_start)

    # display most frequently used end station
    frequent_end = df['End Station'].mode()[0]
    print('\nThe most frequent end station is: ', frequent_end)

    # display most frequent combination of start station and end station trip
    combination = df['Start Station'] + " --> " + df['End Station']
    frequent_combination = combination.mode()[0]
    print("\nThe most frequent combination of start station and end station trip is: ",frequent_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#Displays statistics on the total and average trip duration.
def trip_duration_stats(df):
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time in hours
    total = df['Trip Duration'].sum()
    total_in_hr = total / 3600
    print('\nTotal trip duration is:  ', total_in_hr, ' hrs')

    # display mean travel time in hours
    mean = df['Trip Duration'].mean()
    mean_in_hr = mean / 3600
    print('\nAverage trip duration is:  ', mean_in_hr, ' hrs')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#Displays statistics on bikeshare users.
def user_stats(df):
    
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of user types are:\n ',user_types)

    # Display counts of gender.
    # Since Washigton doesn't have gender in its data, if statement is added to avoid errors.
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print('Counts of gender are:\n ', gender)

    # Display earliest, most recent, and most frequent year of birth.
    # Since Washigton doesn't have bith year in its data, if statement is added to avoid errors
    if 'Birth Year' in df:
        # Display earliest birth year(BY)
        earliest_BY = int(df['Birth Year'].min())
        print('\n The earliest birth day is  ', earliest_BY)

        # Display most recent birth year
        recent_BY = int(df['Birth Year'].max())
        print('\n The recent birth day is  ', recent_BY)

        # Display most frequent birth year
        frequent_BY = int(df['Birth Year'].mode()[0])
        print('\n The most frequent birth day is  ', frequent_BY)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def get_raw_data (df):

    result = input('\n Would you like to see 5 rows of the data ? please enter yes or no : \n').lower()
    i = 0
   
    while True:
        if result != 'yes':
            print("Thank you !")
            break
        print(df.iloc[i:i+5])
        result = input('\n Would you like to see 5 more rows of the data? please enter yes or no : \n').lower()
        i += 5
        

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        get_raw_data (df) 

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()