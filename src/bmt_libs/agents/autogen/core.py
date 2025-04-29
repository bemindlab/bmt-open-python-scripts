"""
AutoGen Core Feature Library

This module is a core feature library for agent scripts using AutoGen from Microsoft
"""

import os
from typing import Any, Dict, List, Optional, Union

try:
    import autogen
    from dotenv import load_dotenv

    # Load environment variables from .env file
    load_dotenv()

    AUTOGEN_AVAILABLE = True
except ImportError:
    AUTOGEN_AVAILABLE = False

    # Create dummy classes/imports for type checking when autogen is not available
    class DummyClass:
        """Dummy class when autogen is not available"""

        pass

    autogen = type(
        "autogen",
        (),
        {
            "AssistantAgent": DummyClass,
            "UserProxyAgent": DummyClass,
            "Agent": DummyClass,
            "GroupChat": DummyClass,
            "GroupChatManager": DummyClass,
        },
    )


class AutoGenAgent:
    """Main class for AutoGen usage"""

    def __init__(
        self,
        name: str,
        system_message: str,
        llm_config: Optional[Dict[str, Any]] = None,
        api_key: Optional[str] = None,
    ):
        """
        Initialize AutoGen Agent

        Args:
            name: Agent name
            system_message: System message defining agent behavior
            llm_config: LLM configuration (default settings if not specified)
            api_key: API key for LLM (uses OPENAI_API_KEY environment variable if not specified)
        """
        if not AUTOGEN_AVAILABLE:
            raise ImportError(
                "AutoGen is not available. Install with: pip install 'bmt-scripts[agents]'"
            )

        self.name = name
        self.system_message = system_message
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError(
                "API key not specified. Please provide api_key or set OPENAI_API_KEY environment variable"
            )

        # Configure LLM config
        self.llm_config = llm_config or {
            "config_list": [
                {
                    "model": "gpt-3.5-turbo",
                    "api_key": self.api_key,
                }
            ],
            "temperature": 0.7,
            "timeout": 600,
        }

        # Create agent
        self.agent = autogen.AssistantAgent(
            name=self.name,
            system_message=self.system_message,
            llm_config=self.llm_config,
        )

        # Create user proxy agent
        self.user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            is_termination_msg=lambda x: x.get("content", "")
            .rstrip()
            .endswith("TERMINATE"),
            code_execution_config={"work_dir": "workspace"},
            llm_config=self.llm_config,
        )

    def chat(self, message: str) -> str:
        """
        Send message to agent and get response

        Args:
            message: Message to send to agent

        Returns:
            str: Response from agent
        """
        # Start conversation
        chat_result = self.user_proxy.initiate_chat(
            self.agent,
            message=message,
        )

        # Return response message
        return chat_result.summary

    def execute_code(self, code: str) -> Dict[str, Any]:
        """
        Run code through agent

        Args:
            code: Code to run

        Returns:
            Dict[str, Any]: Code execution results
        """
        # Create message with code
        message = f"```python\n{code}\n```"

        # Start conversation
        chat_result = self.user_proxy.initiate_chat(
            self.agent,
            message=message,
        )

        # Return results
        return {
            "summary": chat_result.summary,
            "messages": chat_result.messages,
        }

    def create_group_chat(
        self, agents: List["autogen.Agent"], group_name: str = "group_chat"
    ) -> "autogen.GroupChat":
        """
        Create group chat between multiple agents

        Args:
            agents: List of agents to include in group chat
            group_name: Name of group chat

        Returns:
            autogen.GroupChat: Created group chat
        """
        # Create group chat
        group_chat = autogen.GroupChat(
            agents=[self.user_proxy] + agents,
            messages=[],
            max_round=50,
        )

        return group_chat

    def run_group_chat(
        self, group_chat: "autogen.GroupChat", message: str
    ) -> Dict[str, Any]:
        """
        Run group chat

        Args:
            group_chat: Group chat to run
            message: Initial message for group chat

        Returns:
            Dict[str, Any]: Group chat results
        """
        # Start group chat
        chat_result = self.user_proxy.initiate_chat(
            group_chat,
            message=message,
        )

        # Return results
        return {
            "summary": chat_result.summary,
            "messages": chat_result.messages,
        }


class CodeAgent(AutoGenAgent):
    """Agent for writing and editing code"""

    def __init__(
        self,
        name: str = "code_agent",
        api_key: Optional[str] = None,
        llm_config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize Code Agent

        Args:
            name: Agent name
            api_key: API key for LLM
            llm_config: LLM configuration
        """
        system_message = """You are an expert in writing and editing Python code.
        You can help write code, edit code, and fix bugs.
        Please write clean, efficient code that follows PEP 8 standards.
        """

        super().__init__(
            name=name,
            system_message=system_message,
            llm_config=llm_config,
            api_key=api_key,
        )

    def write_code(self, description: str) -> str:
        """
        Write code based on description

        Args:
            description: Description of code to write

        Returns:
            str: Written code
        """
        message = f"Please write Python code based on the following description:\n\n{description}"

        return self.chat(message)

    def fix_bug(self, code: str, error_message: str) -> str:
        """
        Fix bug in code

        Args:
            code: Code with bug
            error_message: Error message

        Returns:
            str: Fixed code
        """
        message = f"""The following code has a bug:

```python
{code}
```

Error message:
{error_message}

Please fix the bug in this code"""

        return self.chat(message)

    def refactor_code(self, code: str) -> str:
        """
        Improve code efficiency and readability

        Args:
            code: Code to improve

        Returns:
            str: Improved code
        """
        message = f"""Please improve the following code for better efficiency and readability:

```python
{code}
```"""

        return self.chat(message)


class ResearchAgent(AutoGenAgent):
    """Agent for research and data analysis"""

    def __init__(
        self,
        name: str = "research_agent",
        api_key: Optional[str] = None,
        llm_config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize Research Agent

        Args:
            name: Agent name
            api_key: API key for LLM
            llm_config: LLM configuration
        """
        system_message = """You are an expert in research and data analysis.
        You can help research topics, analyze data, and summarize information.
        Please provide accurate information with references and useful insights.
        """

        super().__init__(
            name=name,
            system_message=system_message,
            llm_config=llm_config,
            api_key=api_key,
        )

    def research(self, topic: str) -> str:
        """
        Research information about given topic

        Args:
            topic: Topic to research

        Returns:
            str: Research results
        """
        message = f"Please research information about the following topic:\n\n{topic}"

        return self.chat(message)

    def analyze_data(self, data: str) -> str:
        """
        Analyze data

        Args:
            data: Data to analyze

        Returns:
            str: Data analysis results
        """
        message = f"Please analyze the following data:\n\n{data}"

        return self.chat(message)

    def summarize(self, text: str) -> str:
        """
        Summarize text

        Args:
            text: Text to summarize

        Returns:
            str: Summarized text
        """
        message = f"Please summarize the following text:\n\n{text}"

        return self.chat(message)


class CreativeAgent(AutoGenAgent):
    """Agent for content creation"""

    def __init__(
        self,
        name: str = "creative_agent",
        api_key: Optional[str] = None,
        llm_config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize Creative Agent

        Args:
            name: Agent name
            api_key: API key for LLM
            llm_config: LLM configuration
        """
        system_message = """You are an expert in content creation.
        You can help write articles, scripts, and other content.
        Please create interesting, creative, and helpful content.
        """

        super().__init__(
            name=name,
            system_message=system_message,
            llm_config=llm_config,
            api_key=api_key,
        )

    def write_article(self, topic: str, length: str = "medium") -> str:
        """
        Write article

        Args:
            topic: Article topic
            length: Article length (short, medium, long)

        Returns:
            str: Written article
        """
        message = f"Please write an article about the following topic, length {length}:\n\n{topic}"

        return self.chat(message)

    def write_script(self, description: str) -> str:
        """
        Write script

        Args:
            description: Script description

        Returns:
            str: Written script
        """
        message = f"Please write a script based on the following description:\n\n{description}"

        return self.chat(message)

    def generate_ideas(self, topic: str, count: int = 5) -> str:
        """
        Generate ideas

        Args:
            topic: Topic for idea generation
            count: Number of ideas to generate

        Returns:
            str: Generated ideas
        """
        message = f"Please generate {count} ideas about the following topic:\n\n{topic}"

        return self.chat(message)
