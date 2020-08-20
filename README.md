
<h2> Goal of this project </h2>
<p> Provide timely overview of twitter posts with COVID-19 related topics </p>
<p><i> suggested usage: pilot study, web-based study in social science fields  </i> </p>

<h3> What it provides</h3>
<p> 1. an overall distribution of sentiment polarity (positive/negative)</p>
<p> 2. histogram of emotions (enjoyment, neutral, anger, fear, sadness)</p>
<p> 3. frequent mentioned words under the topic</p>


<h3> Data source</h3>
<p> Twitter posts, 1000 recent tweets per search</p>
<p> Filtered to keep only Tweets tagged with US location (around 200 per search) </p>

<h3> Model used</h3>
<h4> Sentiment polariy analysis </h4>
<p>
Bags of words Approach using a SGDClassifier <br>
Training accuracy: .80 <br>
Testing accuracy: .79  <br>
</p>

<h4> Emotion Classification </h4>
<p>
Bags of words Approach using a SGDClassifier <br>
Base accuracy: .20 <br>
Testing accuracy: .60  <br>
</p>

<h3> Graph </h3>
<p> see chart.html and chart1.html for sample graph</p>



  

