def defaultconverter(o):
  if isinstance(o, datetime.datetime):
    return o.__str__() 
      
class Comments():
  
  #Собирает n-твиттов пользователя, включая сделанные им ретвитты
  def get_n_tweets(USER, n_tweets):
    gt =list(itertools.islice(sntwitter.TwitterSearchScraper(f'from:{USER} include:nativeretweets').get_items(), n_tweets))
    n_tweets = {'url' : [], 'date' : [], 'content' : [], 'id' : [], 'username' : [],'hashtags' : [],'outlinks' : [], 'outlinksss' : [], 'tcooutlinks' : [], 'tcooutlinksss' : []}

    for i in gt:
      n_tweets['url'].append(i.url)
      n_tweets['date'].append(defaultconverter(i.date))
      n_tweets['content'].append(i.content)
      n_tweets['id'].append(i.id)
      n_tweets['username'].append(i.username)
      n_tweets['hashtags'].append(re.findall(r'(#\w+)', i.content))
      n_tweets['outlinks'].append(i.outlinks)
      n_tweets['outlinksss'].append(i.outlinksss)
      n_tweets['tcooutlinks'].append(i.tcooutlinks)
      n_tweets['tcooutlinksss'].append(i.tcooutlinksss)
      
    with open(f'{USER}+{n_tweets}_tweets.json', 'w') as outfile:
      json.dump(n_tweets, outfile)
  
#собирает все комменты к твитту по id
  def comment_order(id):
    co = {'url' : [], 'date' : [], 'content' : [], 'id' : [], 'username' : [],'hashtags' : [],'outlinks' : [], 'outlinksss' : [], 'tcooutlinks' : [], 'tcooutlinksss' : []}
    comment_df = list(itertools.islice(sntwitter.TwitterSearchScraper(f'filter:replies conversation_id:{id}').get_items(), None))
    for i in comment_df:
      co['url'].append(i.url)
      co['date'].append(defaultconverter(i.date))
      co['content'].append(i.content)
      co['id'].append(i.id)
      co['username'].append(i.username)
      co['hashtags'].append(re.findall(r'(#\w+)', i.content))
      co['outlinks'].append(i.outlinks)
      co['outlinksss'].append(i.outlinksss)
      co['tcooutlinks'].append(i.tcooutlinks)
      co['tcooutlinksss'].append(i.tcooutlinksss)

    with open(f'{id}.json', 'w') as outfile:
      json.dump(co, outfile)
