"""Module contains the main question function to create a confirm prompt."""
from typing import Dict, List, Tuple

from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit.styles import Style

from InquirerPy.exceptions import InvalidArgumentType


class Confirm:
    """A wrapper class around PromptSession.

    This class is used for confirm prompt.

    :param message: the question message to display
    :type message: str
    :param style: the style dictionary to apply
    :type style: Dict[str, str]
    :param default: set default answer to true
    :type default: bool
    :param symbol: the custom symbol to display infront of the question
    :type symbol: str
    """

    def __init__(
        self,
        message: str,
        style: Dict[str, str],
        default: bool = False,
        symbol: str = "?",
        **kwargs
    ) -> None:
        """Construct a PromptSession object and apply keybindings."""
        self.message = message
        self.question_style = Style.from_dict(style)
        self.default = default
        if not isinstance(self.default, bool):
            raise InvalidArgumentType(
                "default for confirm type question should be type of bool."
            )
        self.symbol = symbol
        self.status = {"answered": False, "result": None}
        self.kb = KeyBindings()

        @self.kb.add("c-c")
        def _(event) -> None:
            """Raise KeyboardInterrupt when ctrl-c is pressed.

            Remove the extra empty line raised by prompt_toolkit by default.
            """
            raise KeyboardInterrupt

        @self.kb.add("y")
        @self.kb.add("Y")
        def _(event) -> None:
            """Bind y and Y to accept confirmation."""
            self.session.default_buffer.text = ""
            self.status["answered"] = True
            self.status["result"] = True
            event.app.exit(result=True)

        @self.kb.add("n")
        @self.kb.add("N")
        def _(event) -> None:
            """Bind n and N to reject confirmation."""
            self.session.default_buffer.text = ""
            self.status["answered"] = True
            self.status["result"] = False
            event.app.exit(result=False)

        @self.kb.add(Keys.Any)
        def _(event) -> None:
            """Disable all other key presses."""
            pass

        @self.kb.add(Keys.Enter)
        def _(event) -> None:
            """Bind enter to use the default answer."""
            self.status["answered"] = True
            self.status["result"] = self.default
            event.app.exit(result=self.default)

        self.session = PromptSession(
            message=self._get_prompt_message,
            key_bindings=self.kb,
            style=self.question_style,
            input=kwargs.pop("input", None),
            output=kwargs.pop("output", None),
        )

    def _get_prompt_message(self) -> List[Tuple[str, str]]:
        """Dynamically update the prompt message.

        After user select an answer, remove (Y/n) or (y/N) and inject
        the pretty answer.

        :return: a list of formatted message to use for PromptSession
        :rtype: List[Tuple[str, str]]
        """
        display_message = []
        display_message.append(("class:symbol", self.symbol))
        display_message.append(("class:question", " %s " % self.message))
        if self.status["answered"]:
            display_message.append(
                ("class:answer", " Yes" if self.status["result"] else " No")
            )
        else:
            display_message.append(
                (
                    "class:instruction",
                    "%s" % " (Y/n)" if self.default else " (y/N)",
                )
            )
        return display_message

    def execute(self) -> bool:
        """Display a confirm prompt and get user input for confirmation.

        :return: user selected answer, either True or False
        :rtype: bool
        """
        return self.session.prompt()
