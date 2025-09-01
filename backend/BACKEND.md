# AI ScriptWriter Backend

This directory contains the backend logic for the AI ScriptWriter application. It leverages a multi-agent system powered by Google's Gemini model to automate the creation of viral short-form video scripts.

## Overview

The backend is designed as an asynchronous pipeline of specialized AI agents. Given a user-defined niche, this system performs research, ideates topics, and generates a complete video script, including a catchy hook. The entire process is orchestrated to produce content that is timely, relevant, and optimized for virality.

## Core Functionality

The heart of the backend is a sequential, multi-agent workflow defined in `ScriptAgents.py`. Each agent has a specific role and passes its output to the next agent in the chain.

### The Agent Pipeline

1.  **Research Agent (`research-bot`)**:
    -   **Purpose**: To discover potentially viral content ideas within the user's specified niche.
    -   **Process**: It uses tools like `search_web`, `get_search_agent_tool`, and `youtube_transcript_summary_tool` to find and summarize trending content.
    -   **Output**: A list of 6 distinct topic ideas with a justification for their viral potential.

2.  **Topic Research Agent (`Topic-Research_Bot`)**:
    -   **Purpose**: To conduct in-depth research on a single, selected topic from the previous stage.
    -   **Process**: It performs a new, focused web search on the chosen topic, gathering detailed information from multiple sources.
    -   **Output**: A comprehensive research report in Markdown format, focusing on surprising, emotional, or counterintuitive facts to maximize engagement. It also includes a list of sources.

3.  **Hook Agent (`Hook_Bot`)**:
    -   **Purpose**: To create a compelling, attention-grabbing opening line (a "hook") for the script.
    -   **Process**: It analyzes the detailed research report and uses few-shot learning (from examples provided by `script_fetcher`) to generate a hook in a proven format and tone.
    -   **Output**: A single, powerful sentence to start the video script.

4.  **Script Agent (`Script_Bot`)**:
    -   **Purpose**: To write the final, complete video script.
    -   **Process**: It takes the generated hook and the detailed research report and weaves them into a coherent and engaging script of 170-200 words. It also references example scripts to maintain a consistent style.
    -   **Output**: The final video script, ready for production.

## Key Components

*   `ScriptAgents.py`: The main entry point for the backend. It defines the agents, orchestrates the pipeline, and manages the flow of data between them.
*   `prompts.py`: Contains detailed instructions (prompts) that define the personality, goals, and step-by-step processes for each AI agent.
*   `tools.py`: Provides the agents with their capabilities, such as `search_web`, `get_page_content`, and `youtube_transcript_summary_tool`. These are the external functions the agents can call.
*   `models.py`: Configures and initializes the connection to the Gemini LLM.
*   `scripts_fetch.py`: Contains the `script_fetcher` function, which loads example scripts to provide context and style guidance to the hook and scriptwriting agents.
*   `output_format.py`: Defines the Pydantic models for structured outputs, such as `ResearchOutputList`.
*   `utils.py`: Includes utility functions like `set_user_niche` to manage user preferences.

## Workflow

The end-to-end process is triggered by a single function call to `get_topic_ideas(user_niche)` in `ScriptAgents.py`.

1.  A user-provided `niche` (e.g., "AI in Healthcare") is passed to the function.
2.  The **Research Agent** is invoked to find 6 viral topic ideas related to the niche.
3.  A topic is selected from the list. (Note: Currently, the `choice_selector` function in `ScriptAgents.py` is hardcoded to select the 3rd topic. This is a placeholder for future user interaction).
4.  The **Topic Research Agent** receives the selected topic and generates a detailed report.
5.  The **Hook Agent** uses this report to craft a catchy hook.
6.  The **Script Agent** receives both the hook and the report to write the final script.
7.  The outputs from all agents (topic list, research report, hook, and final script) are collected and returned as a list.

## Setup

1.  **Environment Variables**: The application uses a `.env` file to manage secrets and API keys. Ensure you have a `.env` file in the root directory with the necessary credentials for the Gemini API and any web search tools.

    ```
    # .env
    GEMINI_API_KEY="your-api-key-here"
    # Other keys for search tools...
    ```

2.  **Dependencies**: Install the required Python packages. It is recommended to use a virtual environment.

    This project uses `uv` for package management. Dependencies are expected to be defined in a `pyproject.toml` file in the project root.

    ```bash
    # Create and activate a virtual environment
    python -m venv .venv
    source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

    # Install dependencies using uv
    uv pip install .
    ```

## Usage

To run the full script generation pipeline, execute the `main.py` script from the project root.

## Future Improvements

-   **Implement User Choice**: Replace the hardcoded `choice_selector` with a mechanism for the user to select their preferred topic.
-   **Robust Logging**: Replace `print()` statements with a structured logging library (e.g., `logging`) for better monitoring and debugging.
-   **Error Handling**: Enhance error handling within the agent pipeline to gracefully manage failures from API calls or tool usage.
-   **Configuration Management**: As noted in `ScriptAgents.py`, agent configurations could be moved to a separate file for better organization and easier modification.