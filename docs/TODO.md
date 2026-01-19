# TODO/PRIORITIES:

1. Be able to run the Ralph looper w/any model/system
	a. (retrofix to use OpenRouter)
		- Add OpenRouter API KEY entries to config file
		- Add a function which abstracts LLM/AIQuery calls
			- Simple LLM query
			- Proprietary LLM functions (mcp, images, files, special powers, etc)
			
		## LLM Model should be hot-swappable every query, in order to dynamically choose the *BEST* option(s)
		* Version(s) of LLM should be able to be upgraded ON THE FLY, even within a single run of Ralph (though maybe better for recording purposes if it's clearly marked and labelled and recorded as to which was used for which run(s).  Having this flexibility allows us to easily pivot between companies, models, and look to the future model (Claude/ChatGPT/Gemini/DeepSeek/etc) without having to rework/rethink the entire solution *
			- Find all mentions of claude & replace with generic AI.Query() 
				- Look at OpenRouter(s) tools and/or other tools which abstract out the LLM model
					(Cline and/or other tool) ?
		OR
	b. Stop being so cheap, pony up and buy Claude/ChatGPT subscription, 
		then use Ralph-loop(s) to build the system(s) above.


2. Fix for better running on Windows
	a. Fix file names (remove colons) - DONE
	b. rewrite .sh bash scripts in better, non jank cross-platform lang
		powershell (good), or C#/Java/python (Better?)
		
3. Add "Beads"/Trello/Jira support instead of flat files
	- Any other features that the other versions of Ralph included?

4. Add Prompt flow for VS Code
	- Watch videos and see how to use this tool, for visual/UI style stuff