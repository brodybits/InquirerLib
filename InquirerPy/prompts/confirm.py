"""Module contains the class to create a confirm prompt."""
from typing import TYPE_CHECKING, Any, Callable, List, Tuple

from prompt_toolkit.keys import Keys
from prompt_toolkit.shortcuts import PromptSession

from InquirerPy.base import BaseSimplePrompt
from InquirerPy.exceptions import InvalidArgument
from InquirerPy.utils import (
    InquirerPyDefault,
    InquirerPyMessage,
    InquirerPySessionResult,
    InquirerPyStyle,
)

if TYPE_CHECKING:
    from prompt_toolkit.input.base import Input
    from prompt_toolkit.output.base import Output

__all__ = ["ConfirmPrompt"]


class ConfirmPrompt(BaseSimplePrompt):
    """Create a prompt that provides 2 options (confirm/deny) and controlled via single keypress.

    A wrapper class around :class:`~prompt_toolkit.shortcuts.PromptSession`.

    TODO:
        Refactor and use Application over PromptSession.

    Args:
        message: The question to ask the user.
            Refer to :ref:`pages/dynamic:message` documentation for more details.
        style: An :class:`InquirerPyStyle` instance.
            Refer to :ref:`Style <pages/style:Alternate Syntax>` documentation for more details.
        vi_mode: Used for compatibility .
        default: Set the default value of the prompt, should be either `True` or `False`.
            This affects the value returned when user directly hit `enter` key.
            Refer to :ref:`pages/dynamic:default` documentation for more details.
        qmark: Question mark symbol. Custom symbol that will be displayed infront of the question before its answered.
        amark: Answer mark symbol. Custom symbol that will be displayed infront of the question after its answered.
        instruction: Short instruction to display next to the question.
        long_instruction: Long instructions to display at the bottom of the prompt.
        transformer: A function which performs additional transformation on the value that gets printed to the terminal.
            Different than `filter` parameter, this is only visual effect and won’t affect the actual value returned by :meth:`~InquirerPy.base.simple.BaseSimplePrompt.execute`.
            Refer to :ref:`pages/dynamic:transformer` documentation for more details.
        filter: A function which performs additional transformation on the result.
            This affects the actual value returned by :meth:`~InquirerPy.base.simple.BaseSimplePrompt.execute`.
            Refer to :ref:`pages/dynamic:filter` documentation for more details.
        wrap_lines: Soft wrap question lines when question exceeds the terminal width.
        confirm_letter: Letter used to confirm the prompt. A keybinding will be created for this letter.
            Default is `y` and pressing `y` will answer the prompt with value `True`.
        reject_letter: Letter used to reject the prompt. A keybinding will be created for this letter.
            Default is `n` and pressing `n` will answer the prompt with value `False`.
        raise_keyboard_interrupt: Raise the :class:`KeyboardInterrupt` exception when `ctrl-c` is pressed. If false, the result
            will be `None` and the question is skiped.
        session_result: Used internally for :ref:`index:Classic Syntax (PyInquirer)`.
        input: Used internally and will be removed in future updates.
        output: Used internally and will be removed in future updates.

    Examples:
        >>> from InquirerPy import inquirer
        >>> result = inquirer.confirm(message="Confirm?").execute()
        >>> print(result)
        True
    """

    def __init__(
        self,
        message: InquirerPyMessage,
        style: InquirerPyStyle = None,
        default: InquirerPyDefault = False,
        vi_mode: bool = False,
        qmark: str = "?",
        amark: str = "?",
        instruction: str = "",
        long_instruction: str = "",
        transformer: Callable[[bool], Any] = None,
        filter: Callable[[bool], Any] = None,
        wrap_lines: bool = True,
        confirm_letter: str = "y",
        reject_letter: str = "n",
        raise_keyboard_interrupt: bool = True,
        session_result: InquirerPySessionResult = None,
        input: "Input" = None,
        output: "Output" = None,
    ) -> None:
        vi_mode = False
        super().__init__(
            message=message,
            style=style,
            vi_mode=vi_mode,
            qmark=qmark,
            amark=amark,
            instruction=instruction,
            transformer=transformer,
            filter=filter,
            default=default,
            wrap_lines=wrap_lines,
            raise_keyboard_interrupt=raise_keyboard_interrupt,
            session_result=session_result,
        )
        if not isinstance(self._default, bool):
            raise InvalidArgument(
                "confirm prompt argument default should be type of bool"
            )
        self._confirm_letter = confirm_letter
        self._reject_letter = reject_letter

        @self._kb.add(self._confirm_letter)
        @self._kb.add(self._confirm_letter.upper())
        def confirm(event) -> None:
            self._session.default_buffer.text = ""
            self.status["answered"] = True
            self.status["result"] = True
            event.app.exit(result=True)

        @self._kb.add(self._reject_letter)
        @self._kb.add(self._reject_letter.upper())
        def reject(event) -> None:
            self._session.default_buffer.text = ""
            self.status["answered"] = True
            self.status["result"] = False
            event.app.exit(result=False)

        @self._kb.add(Keys.Any)
        def _(event) -> None:
            """Disable all other key presses."""
            pass

        @self._kb.add(Keys.Enter)
        def enter(event) -> None:
            self.status["answered"] = True
            self.status["result"] = self._default
            event.app.exit(result=self._default)

        self._session = PromptSession(
            message=self._get_prompt_message,
            key_bindings=self._kb,
            style=self._style,
            wrap_lines=self._wrap_lines,
            bottom_toolbar=[("class:prompt_instruction", long_instruction)]
            if long_instruction
            else None,
            input=input,
            output=output,
        )

    def _get_prompt_message(self) -> List[Tuple[str, str]]:
        """Get message to display infront of the input buffer.

        Returns:
            Formatted text in list of tuple format.
        """
        if not self.instruction:
            pre_answer = (
                "class:instruction",
                " (%s/%s) " % (self._confirm_letter.upper(), self._reject_letter)
                if self._default
                else " (%s/%s) " % (self._confirm_letter, self._reject_letter.upper()),
            )
        else:
            pre_answer = ("class:instruction", " %s " % self.instruction)
        post_answer = ("class:answer", " Yes" if self.status["result"] else " No")
        return super()._get_prompt_message(pre_answer, post_answer)

    def _run(self) -> bool:
        return self._session.prompt()
