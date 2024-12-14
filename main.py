import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def ma(combined_dataFrame):

  combined_dataFrame['date'] = pd.to_datetime(combined_dataFrame[['year', 'month', 'day', 'hour']])
  combined_dataFrame.set_index('date', inplace=True)
  combined_dataFrame['wd'] = combined_dataFrame['wd'].astype(str)
  combined_dataFrame['year'] = combined_dataFrame.index.year
  combined_dataFrame['month'] = combined_dataFrame.index.month
  combined_dataFrame['day'] = combined_dataFrame.index.day
  combined_dataFrame['hour'] = combined_dataFrame.index.hour

  winter_index=[12, 1, 2]
  spring_index=[3, 4, 5]
  summer_index=[6, 7, 8]
  autumn_index=[9, 10, 11]

  def seasen_detection(month):
    if month in winter_index:
      season ='Winter'
    elif month in spring_index:
      season = 'Spring'
    elif month in summer_index:
      season ='Summer'
    elif month in autumn_index:
      season = 'Autumn'
    return season

  combined_dataFrame['season'] = combined_dataFrame['month'].apply(seasen_detection)

  st.header("General insight about the data")

  information=['Number of rows and columns','Data types','Data Overview','Basic Statistics','Number of missing values','All information']
  selected_info = st.multiselect('What information would you like to see about the data?',information,default=information[:1])

  if 'All information' in selected_info:
    st.subheader('Number of rows and columns')
    st.write(combined_dataFrame.shape)
    st.subheader('Data types')
    st.write(combined_dataFrame.dtypes)
    st.subheader("Data Overview")
    st.write(combined_dataFrame.head(10))
    st.subheader('Basic Statistics')
    st.write(combined_dataFrame.describe())
    st.subheader('Number of missing values')
    st.write(combined_dataFrame.isnull().sum())
  else:

    if 'Number of rows and columns' in selected_info:
      st.subheader('Number of rows and columns')
      st.write(combined_dataFrame.shape)

    if 'Data types' in selected_info:
      st.subheader('Data types')
      st.write(combined_dataFrame.dtypes)

    if 'Data Overview' in selected_info:
      st.subheader("Data Overview")
      st.write(combined_dataFrame.head(10))
    if 'Basic Statistics' in selected_info:
      st.subheader('Basic Statistics')
      st.write(combined_dataFrame.describe())

    if 'Number of missing values' in selected_info:
      st.subheader('Number of missing values')
      st.write(combined_dataFrame.isnull().sum())

  st.title("Air Quality Data Visualization")

  plot_mode = st.radio("What would you like to visualize?", ('Plot pollutant levels over time', 'Plot weather conditions over time','Plot pollutant levels and weather conditions at the same time'))
  pollutants=['PM2.5','PM10','SO2','NO2','CO','O3']
  weather_conditions=['TEMP','PRES','DEWP','RAIN','WSPM']
  plot_yearwise_overall=st.radio('Select the type of visualization you would like to view:',('Year-wise Visualization','Overal Visualization'))

  if (plot_mode == 'Plot pollutant levels over time') & (plot_yearwise_overall=='Year-wise Visualization'):
    selected_pollutants = st.multiselect('Which pollutant would you like to track over time??',pollutants,default=pollutants[:1])
    tab1, tab2, tab3 , tab4 = st.tabs(["Year-wise Hourly visualization","Year-wise Daily Average visualization", "Year-wise Monthly Average visualization", "Year-wise Seasonal Average visualization"])
    with tab1:
      st.header("Year-wise Hourly visualization")
      for item in pollutants:
        if item in selected_pollutants:
          st.subheader(f"{item} Year-wise Hourly visualization")
          plt.figure(figsize=(30, 6))
          plt.plot(combined_dataFrame.index, combined_dataFrame[item],marker='.', alpha=0.5, linestyle='None', label=item)
          plt.xlabel('Date')
          plt.ylabel(item)
          plt.legend()
          st.pyplot(plt.gcf())

    with tab2:
      st.header("Year-wise Daily Average visualization")
      daily_average = combined_dataFrame.groupby(['year', 'month', 'day'])[pollutants].mean().reset_index()
      daily_average['Date'] = pd.to_datetime(daily_average[['year', 'month', 'day']])
      for item in selected_pollutants:
        st.subheader(f"{item} Year-wise Daily Average visualization")
        plt.figure(figsize=(30, 6))
        plt.plot(daily_average['Date'], daily_average[item], marker='.', alpha=0.7, linestyle='-', label=item)
        plt.xlabel('Date')
        plt.ylabel(item)
        plt.title(f'{item} Daily Average Concentration Over Time')
        plt.legend()
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())

    with tab3:
      st.header("Year-wise Monthly Average visualization")
      monthly_avrage = combined_dataFrame.groupby(['year', 'month'])[pollutants].mean().reset_index()
      monthly_avrage['Date'] = pd.to_datetime(monthly_avrage[['year', 'month']].assign(DAY=1))
      for item in selected_pollutants:
        st.subheader(f"{item} Year-wise Monthly Average visualization")
        plt.figure(figsize=(30, 6))
        plt.plot(monthly_avrage['Date'], monthly_avrage[item], marker='.', alpha=0.7, linestyle='-', label=item)
        plt.xlabel('Date')
        plt.ylabel(item)
        plt.title(f'{item} Monthly Average Concentration Over Time')
        plt.legend()
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())



      with tab4:
        st.header("Year-wise Seasonal Average Visualization")
        seasonal_avrage = combined_dataFrame.groupby(['year', 'season'])[pollutants].mean().reset_index()
        for item in selected_pollutants:
          st.subheader(f"{item} Year-wise Seasonal Average Visualization")
          plt.figure(figsize=(30, 6))
          seasonal= seasonal_avrage.pivot(index='year', columns='season', values=item)
          seasonal.plot(kind='bar', figsize=(14, 6), alpha=0.7)
          plt.xlabel('Year')
          plt.ylabel(item)
          plt.title(f'{item} Seasonal Average Concentration Over Time')
          plt.legend(title='Season')
          plt.xticks(rotation=45)
          st.pyplot(plt.gcf())


  elif (plot_mode == 'Plot pollutant levels over time')&(plot_yearwise_overall=='Overal Visualization'):
    selected_pollutants = st.multiselect('Which pollutant would you like to track over time??',pollutants,default=pollutants[:1])
    tab1, tab2, tab3 , tab4 = st.tabs(["Overall Hourly visualization","Overall Daily Average visualization", "Overall Monthly Average visualization", "Overall Seasonal Average visualization"])
    with tab1:
      st.header("Overal Hourly visualization")
      hourly_avrage_overall = combined_dataFrame.groupby('hour')[pollutants].mean().reset_index()
      for item in pollutants:
        if item in selected_pollutants:
          st.subheader(f"{item} Overall Hourly visualization")
          plt.figure(figsize=(30, 6))
          plt.plot(hourly_avrage_overall['hour'], hourly_avrage_overall[item], marker='.', alpha=0.5, linestyle='-', label=item)
          plt.xlabel('Date')
          plt.ylabel(item)
          plt.legend()
          st.pyplot(plt.gcf())

    with tab2:
      st.header("Overall Daily Average visualization")
      daily_average_overall = combined_dataFrame.groupby('day')[pollutants].mean().reset_index()
      for item in selected_pollutants:
        st.subheader(f"{item} Overal Daily Average Visualization")
        plt.figure(figsize=(30, 6))
        plt.plot(daily_average_overall['day'], daily_average_overall[item], marker='.', alpha=0.7, linestyle='-', label=item)
        plt.xlabel('Day')
        plt.ylabel(item)
        plt.title(f'{item} Daily Average Concentration Over Time')
        plt.legend()
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())

    with tab3:
      st.header("Overal Monthly Average visualization")
      months=['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
      monthly_avrage_overall = combined_dataFrame.groupby('month')[pollutants].mean().reset_index()
      for item in selected_pollutants:
        st.subheader(f"{item} Overal Monthly Average Visualization")
        plt.figure(figsize=(30, 6))
        plt.plot(months, monthly_avrage_overall[item], marker='o', linestyle='-', color='blue', alpha=0.7, label='Monthly Average')
        plt.xlabel('Months')
        plt.ylabel(item)
        plt.title(f'{item} Monthly Average Concentration Over Time')
        plt.legend()
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())

      with tab4:
        st.header("Overall Seasonal Average Visualization")
        seasonal_avrage_overall = combined_dataFrame.groupby(['season'])[pollutants].mean().reset_index()
        for item in selected_pollutants:
          st.subheader(f"{item} Overall Seasonal Average Visualization")
          plt.figure(figsize=(14, 6))
          plt.plot(seasonal_avrage_overall['season'], seasonal_avrage_overall[item], marker='.', alpha=0.7, linestyle='-', label=item)
          plt.xlabel('Season')
          plt.ylabel(item)
          plt.title(f'{item} Overall Seasonal Average Concentration')
          plt.legend(title='Season')
          plt.xticks(rotation=45)
          st.pyplot(plt.gcf())


  elif (plot_mode == 'Plot weather conditions over time')&(plot_yearwise_overall=='Year-wise Visualization'):
    selected_weather_conditions = st.multiselect('Which weather condition would you like to track over time??',weather_conditions,default=weather_conditions[:1])
    tab1, tab2, tab3 , tab4 = st.tabs(["Year-wise Hourly visualization","Year-wise Daily Average visualization", "Year-wise Monthly Average visualization", "Year-wise Seasonal Average visualization"])
    with tab1:
      st.header("Year-wise Hourly visualization")
      for item in weather_conditions:
        if item in selected_weather_conditions:
          st.subheader(f"{item} Year-wise Hourly visualization")
          plt.figure(figsize=(30, 6))
          plt.plot(combined_dataFrame.index, combined_dataFrame[item],marker='.', alpha=0.5, linestyle='None', label=item)
          plt.xlabel('Date')
          plt.ylabel(item)
          plt.legend()
          st.pyplot(plt.gcf())

    with tab2:
      st.header("Year-wise Daily Average visualization")
      daily_average_w = combined_dataFrame.groupby(['year', 'month', 'day'])[weather_conditions].mean().reset_index()
      daily_average_w['Date'] = pd.to_datetime(daily_average_w[['year', 'month', 'day']])
      for item in selected_weather_conditions:
        st.subheader(f"{item} Year-wise Daily Average visualization")
        plt.figure(figsize=(30, 6))
        plt.plot(daily_average_w['Date'], daily_average_w[item], marker='.', alpha=0.7, linestyle='-', label=item)
        plt.xlabel('Date')
        plt.ylabel(item)
        plt.title(f'{item} Daily Average Concentration Over Time')
        plt.legend()
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())


    with tab3:
      st.header("Year-wise Monthly Average visualization")
      monthly_avrage_w = combined_dataFrame.groupby(['year', 'month'])[weather_conditions].mean().reset_index()
      monthly_avrage_w['Date'] = pd.to_datetime(monthly_avrage_w[['year', 'month']].assign(DAY=1))
      for item in selected_weather_conditions:
        st.subheader(f"{item} Year-wise Monthly Average visualization")
        plt.figure(figsize=(30, 6))
        plt.plot(monthly_avrage_w['Date'], monthly_avrage_w[item], marker='.', alpha=0.7, linestyle='-', label=item)
        plt.xlabel('Date')
        plt.ylabel(item)
        plt.title(f'{item} Monthly Average Concentration Over Time')
        plt.legend()
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())

      with tab4:
        st.header("Year-wise Seasonal Average Visualization")
        seasonal_avrage_w = combined_dataFrame.groupby(['year', 'season'])[weather_conditions].mean().reset_index()
        for item in selected_weather_conditions:
          st.subheader(f"{item} Year-wise Seasonal Average Visualization")
          plt.figure(figsize=(30, 6))
          seasonal= seasonal_avrage_w.pivot(index='year', columns='season', values=item)
          seasonal.plot(kind='bar', figsize=(14, 6), alpha=0.7)
          plt.xlabel('Year')
          plt.ylabel(item)
          plt.title(f'{item} Seasonal Average Concentration Over Time')
          plt.legend(title='Season')
          plt.xticks(rotation=45)
          st.pyplot(plt.gcf())










  elif (plot_mode == 'Plot weather conditions over time')&(plot_yearwise_overall=='Overal Visualization'):
    selected_weather_conditions = st.multiselect('Which weather condirion would you like to track ??',weather_conditions,default=weather_conditions[:1])
    tab1, tab2, tab3 , tab4 = st.tabs(["Overall Hourly Average visualization","Overall Daily Average visualization", "Overall Monthly Average visualization", "Overall Seasonal Average visualization"])
    with tab1:
      st.header("Overal Hourly Average visualization")
      hourly_avrage_o = combined_dataFrame.groupby('hour')[weather_conditions].mean().reset_index()
      for item in weather_conditions:
        if item in selected_weather_conditions:
          st.subheader(f"{item} Overall Hourly Average visualization")
          plt.figure(figsize=(30, 6))
          plt.plot(hourly_avrage_o['hour'], hourly_avrage_o[item], marker='.', alpha=0.5, linestyle='-', label=item)
          plt.xlabel('Date')
          plt.ylabel(item)
          plt.legend()
          st.pyplot(plt.gcf())

    with tab2:
      st.header("Overall Daily Average visualization")
      daily_average_o = combined_dataFrame.groupby('day')[weather_conditions].mean().reset_index()
      for item in selected_weather_conditions:
        st.subheader(f"{item} Overal Daily Average Visualization")
        plt.figure(figsize=(30, 6))
        plt.plot(daily_average_o['day'], daily_average_o[item], marker='.', alpha=0.7, linestyle='-', label=item)
        plt.xlabel('Day')
        plt.ylabel(item)
        plt.title(f'{item} Daily Average Concentration Over Time')
        plt.legend()
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())

    with tab3:
      st.header("Overal Monthly Average visualization")
      months=['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
      monthly_avrage_o = combined_dataFrame.groupby('month')[weather_conditions].mean().reset_index()
      for item in selected_weather_conditions:
        st.subheader(f"{item} Overal Monthly Average Visualization")
        plt.figure(figsize=(30, 6))
        plt.plot(months, monthly_avrage_o[item], marker='o', linestyle='-', color='blue', alpha=0.7, label='Monthly Average')
        plt.xlabel('Months')
        plt.ylabel(item)
        plt.title(f'{item} Monthly Average Concentration Over Time')
        plt.legend()
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())

      with tab4:
        st.header("Overall Seasonal Average Visualization")
        seasonal_avrage_o = combined_dataFrame.groupby(['season'])[weather_conditions].mean().reset_index()
        for item in selected_weather_conditions:
          st.subheader(f"{item} Overall Seasonal Average Visualization")
          plt.figure(figsize=(14, 6))
          plt.plot(seasonal_avrage_o['season'], seasonal_avrage_o[item], marker='.', alpha=0.7, linestyle='-', label=item)
          plt.xlabel('Season')
          plt.ylabel(item)
          plt.title(f'{item} Overall Seasonal Average Concentration')
          plt.legend(title='Season')
          plt.xticks(rotation=45)
          st.pyplot(plt.gcf())











  elif (plot_mode == 'Plot pollutant levels and weather conditions at the same time')&(plot_yearwise_overall=='Overal Visualization'):
    selected_pollutant = st.selectbox('Please elect a pollutant',pollutants)
    selected_weather_conditions = st.multiselect('Please select weather conditions ?',weather_conditions,default=weather_conditions[:1])
    tab1, tab2, tab3 , tab4 = st.tabs(["Overall Hourly Average visualization","Overall Daily Average visualization", "Overall Monthly Average visualization", "Overall Seasonal Average visualization"])
    with tab1:
      hourly_avrage_overall = combined_dataFrame.groupby('hour')[pollutants].mean().reset_index()
      st.subheader(f"{selected_pollutant} Overall Hourly visualization")
      plt.figure(figsize=(30, 6))
      plt.plot(hourly_avrage_overall['hour'], hourly_avrage_overall[selected_pollutant], marker='.', alpha=0.5, linestyle='-', label=selected_pollutant)
      plt.xlabel('Date')
      plt.ylabel(selected_pollutant)
      plt.legend()
      st.pyplot(plt.gcf())
      hourly_avrage_o = combined_dataFrame.groupby('hour')[weather_conditions].mean().reset_index()
      for item in weather_conditions:
        if item in selected_weather_conditions:
          st.subheader(f"{item} Overall Hourly Average visualization")
          plt.figure(figsize=(30, 6))
          plt.plot(hourly_avrage_o['hour'], hourly_avrage_o[item], marker='.', alpha=0.5, linestyle='-', label=item)
          plt.xlabel('Date')
          plt.ylabel(item)
          plt.legend()
          st.pyplot(plt.gcf())





    with tab2:
      daily_average_overall = combined_dataFrame.groupby('day')[pollutants].mean().reset_index()
      st.subheader(f"{selected_pollutant} Overal Daily Average Visualization")
      plt.figure(figsize=(30, 6))
      plt.plot(daily_average_overall['day'], daily_average_overall[selected_pollutant], marker='.', alpha=0.7, linestyle='-', label=selected_pollutant)
      plt.xlabel('Day')
      plt.ylabel(selected_pollutant)
      plt.title(f'{selected_pollutant} Daily Average Concentration Over Time')
      plt.legend()
      plt.xticks(rotation=45)
      st.pyplot(plt.gcf())
      daily_average_o = combined_dataFrame.groupby('day')[weather_conditions].mean().reset_index()
      for item in selected_weather_conditions:
        st.subheader(f"{item} Overal Daily Average Visualization")
        plt.figure(figsize=(30, 6))
        plt.plot(daily_average_o['day'], daily_average_o[item], marker='.', alpha=0.7, linestyle='-', label=item)
        plt.xlabel('Day')
        plt.ylabel(item)
        plt.title(f'{item} Daily Average Concentration Over Time')
        plt.legend()
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())


    with tab3:
      months=['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
      monthly_avrage_overall = combined_dataFrame.groupby('month')[pollutants].mean().reset_index()
      st.subheader(f"{selected_pollutant} Overal Monthly Average Visualization")
      plt.figure(figsize=(30, 6))
      plt.plot(months, monthly_avrage_overall[selected_pollutant], marker='o', linestyle='-', color='blue', alpha=0.7, label='Monthly Average')
      plt.xlabel('Months')
      plt.ylabel(selected_pollutant)
      plt.title(f'{selected_pollutant} Monthly Average Concentration Over Time')
      plt.legend()
      plt.xticks(rotation=45)
      st.pyplot(plt.gcf())
      months=['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
      monthly_avrage_o = combined_dataFrame.groupby('month')[weather_conditions].mean().reset_index()
      for item in selected_weather_conditions:
        st.subheader(f"{item} Overal Monthly Average Visualization")
        plt.figure(figsize=(30, 6))
        plt.plot(months, monthly_avrage_o[item], marker='o', linestyle='-', color='blue', alpha=0.7, label='Monthly Average')
        plt.xlabel('Months')
        plt.ylabel(item)
        plt.title(f'{item} Monthly Average Concentration Over Time')
        plt.legend()
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())





    with tab4:
      seasonal_avrage_overall = combined_dataFrame.groupby(['season'])[pollutants].mean().reset_index()
      st.subheader(f"{selected_pollutant} Overall Seasonal Average Visualization")
      plt.figure(figsize=(14, 6))
      plt.plot(seasonal_avrage_overall['season'], seasonal_avrage_overall[selected_pollutant], marker='.', alpha=0.7, linestyle='-', label=selected_pollutant)
      plt.xlabel('Season')
      plt.ylabel(selected_pollutant)
      plt.title(f'{selected_pollutant} Overall Seasonal Average Concentration')
      plt.legend(title='Season')
      plt.xticks(rotation=45)
      st.pyplot(plt.gcf())
      seasonal_avrage_o = combined_dataFrame.groupby(['season'])[weather_conditions].mean().reset_index()
      for item in selected_weather_conditions:
        st.subheader(f"{item} Overall Seasonal Average Visualization")
        plt.figure(figsize=(14, 6))
        plt.plot(seasonal_avrage_o['season'], seasonal_avrage_o[item], marker='.', alpha=0.7, linestyle='-', label=item)
        plt.xlabel('Season')
        plt.ylabel(item)
        plt.title(f'{item} Overall Seasonal Average Concentration')
        plt.legend(title='Season')
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())








  elif (plot_mode == 'Plot pollutant levels and weather conditions at the same time')&(plot_yearwise_overall=='Year-wise Visualization'):
    selected_pollutant = st.selectbox('Please elect a pollutant',pollutants)
    selected_weather_conditions = st.multiselect('Please select weather conditions ?',weather_conditions,default=weather_conditions[:1])
    tab1, tab2, tab3 , tab4 = st.tabs(["Year-wise Hourly visualization","Year-wise Daily Average visualization", "Year-wise Monthly Average visualization", "Year-wise Seasonal Average visualization"])
    with tab1:
      st.subheader(f"{selected_pollutant} over time")
      plt.figure(figsize=(30, 6))
      plt.plot(combined_dataFrame.index, combined_dataFrame[selected_pollutant], marker='.', alpha=0.5, linestyle='-', label=selected_pollutant)
      plt.xlabel('Date')
      plt.ylabel(selected_pollutant)
      plt.legend()
      st.pyplot(plt.gcf())
      for item in weather_conditions:
        if item in selected_weather_conditions:
          st.subheader(f"{item} Year-wise Hourly visualization")
          plt.figure(figsize=(30, 6))
          plt.plot(combined_dataFrame.index, combined_dataFrame[item],marker='.', alpha=0.5, linestyle='None', label=item)
          plt.xlabel('Date')
          plt.ylabel(item)
          plt.legend()
          st.pyplot(plt.gcf())
      with tab2:
        daily_average = combined_dataFrame.groupby(['year', 'month', 'day'])[pollutants].mean().reset_index()
        daily_average['Date'] = pd.to_datetime(daily_average[['year', 'month', 'day']])
        st.subheader(f"{selected_pollutant} Year-wise Daily Average visualization")
        plt.figure(figsize=(30, 6))
        plt.plot(daily_average['Date'], daily_average[selected_pollutant], marker='.', alpha=0.7, linestyle='-', label=item)
        plt.xlabel('Date')
        plt.ylabel(selected_pollutant)
        plt.title(f'{selected_pollutant} Daily Average Concentration Over Time')
        plt.legend()
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())
        daily_average_w = combined_dataFrame.groupby(['year', 'month', 'day'])[weather_conditions].mean().reset_index()
        daily_average_w['Date'] = pd.to_datetime(daily_average_w[['year', 'month', 'day']])
        for item in selected_weather_conditions:
          st.subheader(f"{item} Year-wise Daily Average visualization")
          plt.figure(figsize=(30, 6))
          plt.plot(daily_average_w['Date'], daily_average_w[item], marker='.', alpha=0.7, linestyle='-', label=item)
          plt.xlabel('Date')
          plt.ylabel(item)
          plt.title(f'{item} Daily Average Concentration Over Time')
          plt.legend()
          plt.xticks(rotation=45)
          st.pyplot(plt.gcf())

      with tab3:
        monthly_avrage = combined_dataFrame.groupby(['year', 'month'])[pollutants].mean().reset_index()
        monthly_avrage['Date'] = pd.to_datetime(monthly_avrage[['year', 'month']].assign(DAY=1))
        st.subheader(f"{selected_pollutant} Year-wise Monthly Average visualization")
        plt.figure(figsize=(30, 6))
        plt.plot(monthly_avrage['Date'], monthly_avrage[selected_pollutant], marker='.', alpha=0.7, linestyle='-', label=item)
        plt.xlabel('Date')
        plt.ylabel(selected_pollutant)
        plt.title(f'{selected_pollutant} Monthly Average Concentration Over Time')
        plt.legend()
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())
        monthly_avrage_w = combined_dataFrame.groupby(['year', 'month'])[weather_conditions].mean().reset_index()
        monthly_avrage_w['Date'] = pd.to_datetime(monthly_avrage_w[['year', 'month']].assign(DAY=1))
        for item in selected_weather_conditions:
          st.subheader(f"{item} Year-wise Monthly Average visualization")
          plt.figure(figsize=(30, 6))
          plt.plot(monthly_avrage_w['Date'], monthly_avrage_w[item], marker='.', alpha=0.7, linestyle='-', label=item)
          plt.xlabel('Date')
          plt.ylabel(item)
          plt.title(f'{item} Monthly Average Concentration Over Time')
          plt.legend()
          plt.xticks(rotation=45)
          st.pyplot(plt.gcf())

      with tab4:
        seasonal_avrage = combined_dataFrame.groupby(['year', 'season'])[pollutants].mean().reset_index()
        st.subheader(f"{selected_pollutant} Year-wise Seasonal Average Visualization")
        plt.figure(figsize=(30, 6))
        seasonal= seasonal_avrage.pivot(index='year', columns='season', values=selected_pollutant)
        seasonal.plot(kind='bar', figsize=(14, 6), alpha=0.7)
        plt.xlabel('Year')
        plt.ylabel(selected_pollutant)
        plt.title(f'{selected_pollutant} Seasonal Average Concentration Over Time')
        plt.legend(title='Season')
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())
        seasonal_avrage_w = combined_dataFrame.groupby(['year', 'season'])[weather_conditions].mean().reset_index()
        for item in selected_weather_conditions:
          st.subheader(f"{item} Year-wise Seasonal Average Visualization")
          plt.figure(figsize=(30, 6))
          seasonal= seasonal_avrage_w.pivot(index='year', columns='season', values=item)
          seasonal.plot(kind='bar', figsize=(14, 6), alpha=0.7)
          plt.xlabel('Year')
          plt.ylabel(item)
          plt.title(f'{item} Seasonal Average Concentration Over Time')
          plt.legend(title='Season')
          plt.xticks(rotation=45)
          st.pyplot(plt.gcf())

