
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def m(combined_dataFrame):
  combined_dataFrame['PM2.5'] = combined_dataFrame['PM2.5'].ffill()
  combined_dataFrame['PM10'] = combined_dataFrame['PM10'].ffill()
  combined_dataFrame['SO2'] = combined_dataFrame['SO2'].ffill()
  combined_dataFrame['NO2'] = combined_dataFrame['NO2'].ffill()
  combined_dataFrame['CO'] = combined_dataFrame['CO'].ffill()
  combined_dataFrame['O3'] = combined_dataFrame['O3'].ffill()
  combined_dataFrame['TEMP'] = combined_dataFrame['TEMP'].ffill()
  combined_dataFrame['PRES'] = combined_dataFrame['PRES'].ffill()
  combined_dataFrame['DEWP'] = combined_dataFrame['DEWP'].ffill()
  combined_dataFrame['RAIN'] = combined_dataFrame['RAIN'].ffill()
  combined_dataFrame['WSPM'] = combined_dataFrame['WSPM'].ffill()
  combined_dataFrame['wd'] = combined_dataFrame['wd'].ffill()
  combined_dataFrame['WSPM'] = combined_dataFrame['WSPM'].ffill()




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



  Morning_index=[6, 7, 8,9,10,11]
  Afternoon_index=[12,13,14,15,16,17]
  Evening_index=[18, 19, 20,21]
  Night_index=[22,23,0,1,2,3,4,5]

  def time_detection(hour):
    if hour in Morning_index:
      time ='Morning'
    elif hour in Afternoon_index:
      time = 'Afternoon'
    elif hour in Evening_index:
      time ='Evening'
    elif hour in Night_index:
      time = 'Night'
    return time

  combined_dataFrame['time'] = combined_dataFrame['hour'].apply(time_detection)

  combined_dataFrame['date'] = pd.to_datetime(combined_dataFrame[['year', 'month', 'day', 'hour']])
  combined_dataFrame.set_index('date', inplace=True)
  combined_dataFrame['wd'] = combined_dataFrame['wd'].astype(str)
  combined_dataFrame['year'] = combined_dataFrame.index.year
  combined_dataFrame['month'] = combined_dataFrame.index.month
  combined_dataFrame['day'] = combined_dataFrame.index.day
  combined_dataFrame['hour'] = combined_dataFrame.index.hour

  pollutants=['PM2.5','PM10','SO2','NO2','CO','O3']

  plot_yearwise_overall=st.radio('Select the type of visualization you would like to view:',('Year-wise Visualization','Overal Visualization'))
  if (plot_yearwise_overall=='Year-wise Visualization'):
    selected_pollutants = st.multiselect('Which pollutant would you like to track on a Year-wise basis?',pollutants,default=pollutants[:])
    tab1, tab2, tab3 , tab4,tab5 = st.tabs(["Hourly","Daily", "Monthly", "Seasonal","Time of the day"])
    with tab1:
      st.subheader("Pollutants Year-wise Hourly Concentration")
      for item in pollutants:
        if item in selected_pollutants:
          plt.figure(figsize=(30, 6))
          plt.plot(combined_dataFrame.index, combined_dataFrame[item],marker='.', alpha=0.5, linestyle='None', label=item)
          plt.xlabel('Years')
          plt.ylabel(item+' (ug/m3)')
          plt.title(item+' Year-wise Hourly Concentration')
          plt.legend()
          plt.show()
          st.pyplot(plt.gcf())
    with tab2:
      st.subheader("Pollutants Year-wise Daily Average Concentration")
      daily_average_y = combined_dataFrame.groupby(['year', 'month', 'day'])[pollutants].mean().reset_index()
      daily_average_y['Date'] = pd.to_datetime(daily_average_y[['year', 'month', 'day']])
      for item in selected_pollutants:
        plt.figure(figsize=(30, 6))
        plt.plot(daily_average_y['Date'], daily_average_y[item], marker='.', alpha=0.7, linestyle='-', label=item)
        plt.xlabel('Years')
        plt.ylabel(item+' (ug/m3)')
        plt.title(f'{item} Year-wise Daily Average Concentration')
        plt.legend()
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())

    with tab3:
      st.subheader("Pollutants Year-wise Monthly Average Concentration")
      monthly_avrage_y = combined_dataFrame.groupby(['year', 'month'])[pollutants].mean().reset_index()
      monthly_avrage_y['Date'] = pd.to_datetime(monthly_avrage_y[['year', 'month']].assign(DAY=1))
      for item in selected_pollutants:
        plt.figure(figsize=(30, 6))
        plt.plot(monthly_avrage_y['Date'], monthly_avrage_y[item], marker='.', alpha=0.7, linestyle='-', label=item)
        plt.xlabel('Years')
        plt.ylabel(item+' (ug/m3)')
        plt.title(f'{item} Yearwise Monthly Average Concentration')
        plt.legend()
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())


      with tab4:
        st.subheader("Pollutants Year-wise Seasonal Average Concentration")
        seasonal_avrage_y = combined_dataFrame.groupby(['year', 'season'])[pollutants].mean().reset_index()
        for item in selected_pollutants:
          plt.figure(figsize=(30, 6))
          seasonal_y= seasonal_avrage_y.pivot(index='year', columns='season', values=item)
          seasonal_y.plot(kind='bar', figsize=(14, 6), alpha=0.7)
          plt.xlabel('Years')
          plt.ylabel(item+' (ug/m3)')
          plt.title(f'{item} Year-wise Seasonal Average Concentration')
          plt.legend(title='Season')
          plt.xticks(rotation=45)
          st.pyplot(plt.gcf())

      with tab5:
        st.subheader("Pollutants Year-wise Time of the day Average Concentration")
        time_average_y = combined_dataFrame.groupby(['year', 'time'])[pollutants].mean().reset_index()
        for item in selected_pollutants:
          plt.figure(figsize=(30, 6))
          time_y= time_average_y.pivot(index='year', columns='time', values=item)
          time_y.plot(kind='bar', figsize=(14, 6), alpha=0.7)
          plt.xlabel('Years')
          plt.ylabel(item+' (ug/m3)')
          plt.title(f'{item} Year-wise Time of the day Average Concentration')
          plt.legend(title='Time')
          plt.xticks(rotation=45)
          st.pyplot(plt.gcf())

  elif (plot_yearwise_overall=='Overal Visualization'):
    selected_pollutants = st.multiselect('Which pollutant would you like to track on an overall basis (not by year)?',pollutants,default=pollutants[:])
    tab1, tab2, tab3 , tab4,tab5 = st.tabs(["Hourly","Daily", "Monthly", "Seasonal","Time of the day"])
    with tab1:
      st.header("Pollutants Overal Hourly Avarege Concentration")
      hourly_average_overall = combined_dataFrame.groupby('hour')[pollutants].mean().reset_index()
      for item in selected_pollutants:
        plt.figure(figsize=(30, 6))
        plt.plot(hourly_average_overall['hour'], hourly_average_overall[item], marker='.', alpha=0.5, linestyle='-', label=item)
        plt.xlabel('Hours')
        plt.ylabel(item+' (ug/m3)')
        plt.title(f'{item} Overall Hourly Average Concentration')
        plt.legend()
        st.pyplot(plt.gcf())

    with tab2:
      st.header("Pollutants Overal Daily Avarege Concentration")
      daily_average_overall = combined_dataFrame.groupby('day')[pollutants].mean().reset_index()
      for item in selected_pollutants:
        plt.figure(figsize=(30, 6))
        plt.plot(daily_average_overall['day'], daily_average_overall[item], marker='.', alpha=0.7, linestyle='-', label=item)
        plt.xlabel('Days')
        plt.ylabel(item+' (ug/m3)')
        plt.title(f'{item} Overall Daily Average Concentration')
        plt.legend()
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())

    with tab3:
      st.header("Pollutants Overal Monthly Avarege Concentration")
      months=['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
      monthly_average_overall = combined_dataFrame.groupby('month')[pollutants].mean().reset_index()
      for item in selected_pollutants:
        plt.figure(figsize=(30, 6))
        plt.plot(months, monthly_average_overall[item], marker='o', linestyle='-', color='blue', alpha=0.7, label='Monthly Average')
        plt.xlabel('Months')
        plt.ylabel(item+'(ug/m3)')
        plt.title(f'{item} Overal Monthly Average Concentration Over Time')
        plt.legend()
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())

    with tab4:
      st.header("Pollutants Overal Seasonal Avarege Concentration")
      seasonal_avrage_overall = combined_dataFrame.groupby(['season'])[pollutants].mean().reset_index()
      for item in selected_pollutants:
        plt.figure(figsize=(14, 6))
        plt.plot(seasonal_avrage_overall['season'], seasonal_avrage_overall[item], marker='.', alpha=0.7, linestyle='-', label=item)
        plt.xlabel('Season')
        plt.ylabel(item+' (ug/m3)')
        plt.title(f'{item} Overall Seasonal Average Concentration')
        plt.legend()
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())


    with tab5:
      st.header("Pollutants Overal Time of the day Avarege Concentration")
      time_average_overall = combined_dataFrame.groupby(['time'])[pollutants].mean().reset_index()
      for item in selected_pollutants:
        plt.figure(figsize=(14, 6))
        plt.plot(time_average_overall['time'], time_average_overall[item], marker='.', alpha=0.7, linestyle='-', label=item)
        plt.xlabel('Time of the day')
        plt.ylabel(item+' (ug/m3)')
        plt.title(f'{item} Overall Time of the day Average Concentration')
        plt.legend()
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())



