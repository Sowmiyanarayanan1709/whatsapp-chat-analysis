from shutil import which
from matplotlib import markers
from pandas import DataFrame
import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns



st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    if len(df) == 0:
        st.title("Please ensure that the uploaded text file has railway timing")
    else:    
        st.dataframe(df)     
        #fetch user_list
        
        user_list = df['name'].unique().tolist()
        user_list.remove("Group notfication")
        user_list.sort()
        user_list.insert(0,"Overall")

        selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

        if st.sidebar.button("show analysis"):
            num_messages, words, media_messages,links = helper.total_messages(selected_user,df)

            st.title("Top Statistics")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.header("Total Messages")
                st.title(num_messages)
            with col2:
                st.header("Total Words")
                st.title(words)
            with col3:
                st.header("Media Shared")
                st.title(media_messages)
            with col4:
                st.header("Links Shared")
                st.title(links)
            
            #monthly timeline
            st.title("Monthly Timeline")
            timeline_month = helper.monthly_timeline(selected_user,df)
            fig,ax = plt.subplots()
            ax.plot(timeline_month['time'],timeline_month['messages'],linestyle = 'solid',marker='o', markerfacecolor = 'red')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)  

            #daily timeline
            st.title("Daily Timeline")
            timeline_date = helper.daily_timeline(selected_user,df)
            fig,ax = plt.subplots()
            ax.plot(timeline_date['only_date'],timeline_date['messages'],color = 'black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            
            st.title("Activity Maps")
            col1, col2 = st.columns(2)
            timeline_day,busy_month = helper.day_month_timeline(selected_user,df)  # busy day and month

            with col1:
                st.header("Most busy Day")
                fig, ax = plt.subplots()
                ax.bar(timeline_day.index,timeline_day.values, color = '#FFDF00')   
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.header("Most busy Month")
                fig, ax = plt.subplots()
                ax.bar(busy_month.index,busy_month.values, color = '#800000')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            
            #Weekly activity map
            st.title("Weekly Activity Map")
            user_heatmap = helper.activity_heatmap(selected_user,df)
            fig, ax = plt.subplots()
            ax = sns.heatmap(user_heatmap)
            plt.yticks(rotation = 'horizontal')
            st.pyplot(fig)

            if selected_user == 'Overall':
                x,new_df = helper.most_busy_user(df)
                fig, ax = plt.subplots()
                
                col1, col2 = st.columns(2)

                with col1:   # Busy users in the group
                    st.title("Most Busy User")
                    ax.bar(x.index,x.values)
                    for i in range(len(x)):
                        plt.text(i,x.values[i],x.values[i],ha = 'center', va = 'bottom')
                    plt.xticks(rotation = 'vertical')
                    st.pyplot(fig)

                with col2:
                    st.title(" ")
                    st.dataframe(data=new_df, width=700, height=600)

            st.title("WordCloud")  #wordcloud        
            try:        
                df_wc = helper.create_wordcloud(selected_user,df)
                fig,ax = plt.subplots()
                ax.imshow(df_wc)
                st.pyplot(fig)
            except ValueError:
                st.write("Not enough words to form a word Cloud")
                
            # most used emoji
            emoji_df = helper.emoji_count(selected_user,df)
            st.title("Emoji Analysis")
            if len(emoji_df.columns) == 0:
                st.write("The user has not used any emoji")
            else:
                col1, col2 = st.columns(2)  
                with col1:
                    st.dataframe(data=emoji_df, width=700, height=400)
                with col2:
                    fig,ax = plt.subplots()
                    ax.pie(emoji_df['Count'].head(),labels = emoji_df['Emoji'].head(),autopct = "%0.2f")
                    st.pyplot(fig)
            
