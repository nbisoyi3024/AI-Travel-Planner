from graph.react_agent import react_agent_executor

response = react_agent_executor.invoke({
    "messages": [{"role": "user", "content": "Find restaurants near Eiffel Tower"}]
})

print(response["messages"][-1].content)