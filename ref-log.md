What did you learn from implementing a multi-agent workflow?

I learnt how useful multi-agent workflows can be especially in checking the output of LLMs. This can be a strong tool to use against AI hallucinations and other errors of the initial LLM output. I also learnt a lot about how important prompt engineering can be to help get better answers. Specifically, I witnessed how my prompt added structure to the result that would be more palatable to the end user

Challenges faced and how you addressed them


One of the challenges I faced was trying to figure out which parts of the prompt would be a part of the planner and which parts of the prompt would be part of the reviewer. I had to look up some examples of reviewer agents to get a better understanding of this


Any creative ideas, variations, or design choices (e.g., persona roles, prompt design).


I created a structured output pattern that I believe would be the most helpful for someone planning a trip. I asked for a time-dependent schedule and I made sure to ask both the planner agent and the reviewer agent to include the time it takes to get from one location to another. I also made sure to have built in time for breakfast, lunch and dinner because I believe food and keeping your energy up during travelling is vital. I also made sure to include prices for everything in my prompt so the user can make their own calculations as well. I also added that the planner should suggest a hotel within the user’s budget and the reviewer should use the internet search tool to ensure that the hotel price is indeed within the user’s budget. I also included that reviewer should try to use fewer more precise google searches so as to not drive up the costs

I used chatgpt to help refine my prompts
