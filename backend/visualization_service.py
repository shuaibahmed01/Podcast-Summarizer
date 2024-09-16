from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import json
import re
def generate_visualizations(transcript, summary):
    print("in visualization function")
    model = ChatOpenAI(temperature=0.7)

    template = """
    You are an AI assistant that creates relevant and helpful visualizations for students based on lecture transcripts and summaries. Your task is to analyze the given transcript and summary, then propose and create Mermaid.js code for visualizations that would be most beneficial for a student's understanding.

    Transcript:
    {transcript}

    Summary:
    {summary}

    Please generate Mermaid.js code for 2-4 visualizations that you think would be most helpful for students. For each visualization, provide:
    1. A title
    2. A brief description of why this visualization is helpful
    3. The Mermaid.js code for the visualization

    Format your response as a JSON-like structure:
    [
        {{
            "title": "Visualization Title",
            "description": "Description of why this is helpful",
            "mermaidCode": "Mermaid.js code here"
        }},
        // ... more visualizations ...
    ]

    Be creative and consider various types of visualizations such as flowcharts, pie charts, timelines, or any other type that Mermaid.js supports and would be relevant to the content.
    """

    prompt = PromptTemplate(
        template=template,
        input_variables=["transcript", "summary"]
    )

    chain = LLMChain(llm=model, prompt=prompt)
    print("here")
    response = chain.run(transcript=transcript, summary=summary)
    print("response received")


    # Remove any leading/trailing whitespace and newlines
    response = response.strip()

    # Remove any markdown code block indicators if present
    response = re.sub(r'```json\s*|\s*```', '', response)

    # Parse the cleaned response as JSON
    visualizations = json.loads(response)
    print("at the end of visualization function")
    print("Visualizations:",visualizations)
    return visualizations
