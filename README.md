# NewsClusters

## Goal
Using New York Times article headlines and leads, I will attempt to group reporters together based on topic and sentiment.  This will allow users to find reporters that report on similar topics with similar viewpoints.

## History
I have found a number of papers on using K-Means clustering and other models to cluster news based on topics, however I haven't found anything that specifically tries to cluster together the authors of the articles.

## Approach, Who Cares?
Clustering reporters together, as opposed to just clustering the topics, will allow press people and others the ability to fid reporters that report on topics of interest to them, allowing them to use content to find new leads.

## Presentation
I would like to present this using a combination of a slideshow and a website with functionality allowing the user to search for reporters by entering key words.

## Data
I collected the data using the NY Times Archive API going back 5 years using an AWS instance.  The data was added to csv files and will then be stored in a SQL database.  The total data size is upwards of 700MB.

## Potential Problems
I may not be able to do accuracte sentiment analysis using only the headline and the lead.  In my research, I found that typically the first 10 sentences of an article are used to determine sentiment, but I only have two.

## Next Steps
Nex tstep is to organize the data in to a SQL database that makes sense.  I am considering having a table for reporters, and a table for articles.

