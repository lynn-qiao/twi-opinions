

<h3> Business Objective</h3>
<p> Many studies have examined the effect of how COVID-19 impacts mental health and many of them were conducted using online forums. Since the situation is not yet stable, it's also important to keep the research topic up-to-date and make sure the collected data still reflects the present.</p>

<h4> Goal of this project </h4>
<p> Provide quick overview of twitter posts with COVID-19 related topics from a snippet of the US population </p>
<p><i> suggested usage: before large-scale data collection for web-based study in social science fields </i> </p>

<h4> What it provides</h4>
<p> 1. an overall distribution of sentiment polarity (positive/negative)</p>
<p> 2. histogram of emotions (enjoyment, neutral, anger, fear, sadness)</p>
<p> 3. frequent mentioned words under the topic</p>


<h4> To Use this Project</h4>
<p> Download this repository and run server.py</p>
<p> make sure your python has all modules with latest version listed in <a href='https://github.com/lynn-qiao/twi-opinions/blob/master/requirements.txt'> requirements.txt </a> </p>



<h3> Data Ingestion </h3>
<p> Twitter posts retrieved using Twitter API, 1000 recent tweets per search</p>
<p> Filtered to keep only Tweets tagged with US location (around 200 per search) </p>
<p> <i> depending on the length/complexity of search term, it will take about 1-2 minutes to retrieve the data, refresh the page if encounter timeout error/no response</i><br>
 <i> please avoid too specific search terms </i>
</p>


<h3> Machine Learning</h3>
<h4> Sentiment polariy analysis </h4>
<p>
Bags of words Approach using a SGDClassifier <br>
  <i> trained with <a href='https://www.kaggle.com/kazanova/sentiment140'> Sentiment140 dataset (avaliable on Kaggle)</a> </i> <br>
Training accuracy: .80 <br>
Testing accuracy: .79  <br>
</p>

<h4> Emotion Classification </h4>
<p>
Bags of words Approach using a SGDClassifier <br> 
<i> trained with tweets from various datasets and local datasets acquired by searching for emotional words on Twitter </i> <br>
Base accuracy: .20 <br>
Testing accuracy: .60  <br>
</p>

<h3> Visualization </h3>
<p> see <a href='https://github.com/lynn-qiao/twi-opinions/blob/master/chart.html'> chart.html</a> and  <a href='https://github.com/lynn-qiao/twi-opinions/blob/master/chart1.html'> chart1.html</a> for example</p>



  

