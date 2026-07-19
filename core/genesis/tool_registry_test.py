from core.genesis.tool_registry import tool_registry


tools = [

(
"Flutter",
"mobile",
"Cross platform mobile application development",
["Digital Twin","Agent-X"]
),

(
"React Native",
"mobile",
"Mobile application framework",
["Digital Twin"]
),

(
"Termux API",
"device",
"Android device integration",
["Digital Twin","OpenClaw"]
),

(
"OpenRouter NVIDIA",
"ai",
"AI model provider",
["Genesis AI Hub"]
),

(
"Gemini",
"ai",
"Google AI communication",
["Digital Twin","Genesis AI Hub"]
),

(
"GitHub",
"development",
"Code repository and deployment",
["Agent-X"]
)

]


for tool in tools:

    tool_registry.register_tool(
        tool[0],
        tool[1],
        tool[2],
        tool[3]
    )



for tool in tool_registry.tools:

    tool_registry.verify_tool(tool)



print(
    tool_registry.report()
)
