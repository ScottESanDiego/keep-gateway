#!/usr/bin/env python3
#
# Requires input of `listname` and `listitem`
# Assumes KEEPUSER and KEEPPASS environment variables are passed in

import web
import os
import gkeepapi

urls = (
	'/healthcheck', 'healthcheck',
    '/(.*)', 'default'
)

class default:
	def GET(self,name):
		# Force Content-Type
		web.header('Content-Type', 'text/plain')
		
		# Parse input, and set defaults to "INVALID" if not there
		user_data = web.input(listitem="INVALID", listname="INVALID")
		
		# Login to Keep and instantiate Keep object
		keep = gkeepapi.Keep()
		keep.login(os.environ['KEEPUSER'],os.environ['KEEPPASS'])
		
		KeepLists=keep.all()
	
		# Iterate through all the lists.  Works around odd query behavior with gkeepapi
		for List in KeepLists:
			# Find the list we want
			if List.title == user_data.listname:
				List.add(user_data.listitem, False)
				keep.sync()
				return "Adding " + user_data.listitem + " to list " + user_data.listname

		# We didn't find the list requested, to return a 404 error
		raise web.notfound("List " + user_data.listname + " does not exist")
		
class healthcheck:
	def GET(self):
		# Force Content-Type
		web.header('Content-Type', 'text/plain')
		return "Alive"
		
if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
