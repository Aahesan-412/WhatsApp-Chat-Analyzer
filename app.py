import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
# from sentiment_vader import get_sentiment_vader

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(page_title="WhatsApp Chat Analyzer", page_icon="💬", layout="wide")

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
h1, h2, h3 {
    color: white;
}
.stMetric {
    background-color: #1c1c1c;
    padding: 15px;
    border-radius: 10px;
}
.section-divider {
    border-top: 1px solid #333;
    margin-top: 25px;
    margin-bottom: 25px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #
st.sidebar.markdown("## 💬 WhatsApp Chat Analyzer")
st.sidebar.markdown("Upload your exported WhatsApp chat file")

uploaded_file = st.sidebar.file_uploader("Choose a File")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    
    # Fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    
    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)
    
    if st.sidebar.button("Show Analysis"):
        
        # ---------------- TOP STATISTICS ---------------- #
        st.markdown("## 📊 Top Statistics")
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        num_message, words , num_media_messages, links = helper.fetch_stats(selected_user,df)
        col1 , col2 , col3 , col4 = st.columns(4)
        
        col1.metric("📩 Total Messages", num_message)
        col2.metric("📝 Total Words", words)
        col3.metric("🖼️ Media Shared", num_media_messages)
        col4.metric("🔗 Links Shared", links)
        
        
        
        # ---------------- MONTHLY TIMELINE ---------------- #
        st.markdown("## 📅 Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)   
        fig,ax =  plt.subplots()
        ax.plot(timeline['time'],timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        # ---------------- DAILY TIMELINE ---------------- #
        st.markdown("## 📆 Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user,df)   
        fig,ax =  plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        # ---------------- ACTIVITY MAP ---------------- #
        st.markdown("## 🗺️ Activity Insights")
        col1,col2 = st.columns(2)
        
        with col1:
            st.subheader("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
        with col2:
            st.subheader("Most Busy Month")
            busy_month = helper.monthly_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
        # ---------------- HEATMAP ---------------- #
        st.markdown("## 🔥 Weekly Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        sns.heatmap(user_heatmap)
        st.pyplot(fig)
         
        # ---------------- MOST BUSY USER ---------------- #
        if selected_user  == 'Overall':
            st.markdown("## 👑 Most Busy User")
            x,new_df = helper.most_busy_user(df)
            
            col1 , col2 = st.columns(2)
            
            with col1:
                fig,ax = plt.subplots()
                ax.bar(x.index,x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
                
            with col2:
                st.dataframe(new_df)
                
        # ---------------- WORD CLOUD ---------------- #
        st.markdown("## ☁️ Word Cloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis("off")
        st.pyplot(fig)
        
        # ---------------- MOST COMMON WORDS ---------------- #
        st.markdown("## 🏆 Most Common Words")
        most_common_df = helper.most_common_words(selected_user,df)
        
        col1 , col2 = st.columns(2)
        
        with col1:
            fig,ax = plt.subplots()
            ax.barh(most_common_df['Word'], most_common_df['No of Times'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
        with col2:  
            st.dataframe(most_common_df)
            
        # ---------------- EMOJIS ---------------- #
        st.markdown("## 😂 Most Common Emojis")
        emoji_df = helper.emoji_helper(selected_user,df)
        
        col1 , col2 = st.columns(2)
        
        with col1:
            fig,ax = plt.subplots()
            ax.barh(emoji_df['Emojis'].head(), emoji_df['No of Times'].head())
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
        with col2:  
            
            st.dataframe(emoji_df)

        st.markdown("---")
        st.markdown("Made with ❤️ using Streamlit")