#pip install Twint


import twint

c = twint.Config()

c.Search = ['Corona']       # topic
c.Lang = "de"
#c.Limit = 500      # number of Tweets to scrape
c.Store_csv = True       # store tweets in a csv file
c.Output = "corona tweets.csv"     # path to csv file

c1 = twint.Config()

c1.Search = ['Corona']       # topic
c1.Lang = "de"
c1.Until = "2021-12-01"
#c.Limit = 500      # number of Tweets to scrape
c1.Store_csv = True       # store tweets in a csv file
c1.Output = "corona tweets1.csv"     # path to csv file


c2 = twint.Config()

c2.Search = ['Corona']       # topic
c2.Lang = "de"
c2.Since = "2018-01-01"
#c.Limit = 500      # number of Tweets to scrape
c2.Store_csv = True       # store tweets in a csv file
c2.Output = "corona tweets2.csv"     # path to csv file


c3 = twint.Config()

c3.Username = 'ATTILA_HlLDMAN'       # topic
#c3.Lang = "de"
#c3.Since = "2018-01-01"
#c.Limit = 500      # number of Tweets to scrape
c3.Store_csv = True       # store tweets in a csv file
c3.Output = "hildebrand.csv"     # path to csv file


#twint.run.Search(c)
#twint.run.Search(c1)
#twint.run.Search(c2)
twint.run.Search(c3)

