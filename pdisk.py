import requests as re
import json 
def pdisk_url(api_key:str , link:str , title :str , thumb = None ):
		if thumb is None :
			data = { "api_key":api_key,
	                   "content_src":link,
	                    "link_type":"link",
	                     "title": title 
	                  } 	
			res = re.post("http://linkapi.net/open/create_item",data).content
			result = json.loads(res)
			try:
				id = result["data"]['item_id']
			except:
				id = result["msg"]
			return id 
		else:
			data = { "api_key":api_key,
	                   "content_src":link,
	                    "link_type":"link",
	                     "title": title ,
	                     "cover_url":thumb
	                  }
			res = re.post('http://linkapi.net/open/create_item',data).content
			result = json.loads(res)
			try:
				id = result["data"]['item_id']
			except:
				id = result["msg"]
			return id                                                                    
