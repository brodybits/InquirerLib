import unittest
from unittest.mock import patch

from prompt_toolkit.enums import EditingMode
from prompt_toolkit.key_binding.key_bindings import KeyBindings
from prompt_toolkit.styles.style import Style

from InquirerLib.InquirerPy.prompts.list import InquirerPyListControl, ListPrompt
from InquirerLib.InquirerPy.separator import Separator
from InquirerLib.InquirerPy.utils import InquirerPyStyle


class TestBaseList(unittest.TestCase):
    choices = [
        {"name": "apple", "value": "peach"},
        "pear",
        {"name": "melon", "value": "watermelon"},
    ]

    @patch("InquirerLib.InquirerPy.base.complex.shutil.get_terminal_size")
    def test_list_prompt(self, mocked_term):
        mocked_term.return_value = (24, 80)
        message = 15 * "i"
        qmark = "[?]"
        instruction = 2 * "i"
        prompt = ListPrompt(
            message=message,
            choices=self.choices,
            default="watermelon",
            style=InquirerPyStyle({"pointer": "#61afef"}),
            vi_mode=True,
            qmark=qmark,
            pointer=">",
            instruction=instruction,
            show_cursor=True,
            wrap_lines=True,
            border=True,
        )
        self.assertEqual(prompt._editing_mode, EditingMode.VI)
        self.assertIsInstance(prompt.content_control, InquirerPyListControl)
        self.assertIsInstance(prompt._kb, KeyBindings)
        self.assertIsInstance(prompt._style, Style)
        self.assertEqual(prompt._message, message)
        self.assertEqual(prompt._qmark, qmark)
        self.assertEqual(prompt.instruction, instruction)
        self.assertTrue(prompt._border, True)

    def test_prompt_message_with_cursor(self):
        prompt = ListPrompt(message="Select one:", choices=[1, 2, 3])
        self.assertEqual(
            prompt._get_prompt_message_with_cursor(),
            [
                ("class:questionmark", "?"),
                ("class:question", " Select one:"),
                ("class:instruction", " "),
                ("[SetCursorPosition]", ""),
                ("", " "),
            ],
        )

    def test_prompt_handle_toggle_choice_no_multiselect(self):
        prompt = ListPrompt(message="Select one:", choices=[1, 2, 3], multiselect=False)
        self.assertEqual(
            prompt.content_control.selection,
            {"enabled": False, "name": "1", "value": 1},
        )
        prompt._handle_toggle_choice(None)
        self.assertEqual(
            prompt.content_control.selection,
            {"enabled": False, "name": "1", "value": 1},
        )

    def test_prompt_handle_toggle_choice(self):
        prompt = ListPrompt(message="Select one:", choices=[1, 2, 3], multiselect=True)
        self.assertEqual(
            prompt.content_control.selection,
            {"enabled": False, "name": "1", "value": 1},
        )
        prompt._handle_toggle_choice(None)
        self.assertEqual(
            prompt.content_control.selection,
            {"enabled": True, "name": "1", "value": 1},
        )
        prompt._handle_toggle_choice(None)
        self.assertEqual(
            prompt.content_control.selection,
            {"enabled": False, "name": "1", "value": 1},
        )

    def test_prompt_handle_toggle_all_no_multiselect(self) -> None:
        prompt = ListPrompt(message="Select one:", choices=[1, 2, 3])
        self.assertEqual(
            prompt.content_control.choices,
            [
                {"enabled": False, "name": "1", "value": 1},
                {"enabled": False, "name": "2", "value": 2},
                {"enabled": False, "name": "3", "value": 3},
            ],
        )
        prompt._handle_toggle_all(None)
        self.assertEqual(
            prompt.content_control.choices,
            [
                {"enabled": False, "name": "1", "value": 1},
                {"enabled": False, "name": "2", "value": 2},
                {"enabled": False, "name": "3", "value": 3},
            ],
        )

    def test_prompt_handle_toggle_all(self):
        prompt = ListPrompt(message="Select one:", choices=[1, 2, 3], multiselect=True)
        self.assertEqual(
            prompt.content_control.choices,
            [
                {"enabled": False, "name": "1", "value": 1},
                {"enabled": False, "name": "2", "value": 2},
                {"enabled": False, "name": "3", "value": 3},
            ],
        )
        prompt._handle_toggle_all(None)
        self.assertEqual(
            prompt.content_control.choices,
            [
                {"enabled": True, "name": "1", "value": 1},
                {"enabled": True, "name": "2", "value": 2},
                {"enabled": True, "name": "3", "value": 3},
            ],
        )
        prompt._handle_toggle_all(None)
        self.assertEqual(
            prompt.content_control.choices,
            [
                {"enabled": False, "name": "1", "value": 1},
                {"enabled": False, "name": "2", "value": 2},
                {"enabled": False, "name": "3", "value": 3},
            ],
        )

    def test_handle_up(self):
        prompt = ListPrompt(message="Select one:", choices=[1, 2, Separator(), 3])
        self.assertEqual(prompt.content_control.selected_choice_index, 0)
        prompt._handle_up(None)
        self.assertEqual(prompt.content_control.selected_choice_index, 3)
        prompt._handle_up(None)
        self.assertEqual(prompt.content_control.selected_choice_index, 1)
        prompt._handle_up(None)
        self.assertEqual(prompt.content_control.selected_choice_index, 0)
        prompt._handle_up(None)
        self.assertEqual(prompt.content_control.selected_choice_index, 3)

        prompt = ListPrompt(message="Select one:", choices=[1, 2, 3, Separator()])
        self.assertEqual(prompt.content_control.selected_choice_index, 0)
        prompt._handle_up(None)
        self.assertEqual(prompt.content_control.selected_choice_index, 2)

    def test_handle_up_no_cycle(self):
        prompt = ListPrompt(
            message="Select one:",
            choices=[Separator(), 1, 2, 3, Separator()],
            cycle=False,
        )
        self.assertEqual(prompt.content_control.selected_choice_index, 1)
        prompt._handle_up(None)
        self.assertEqual(prompt.content_control.selected_choice_index, 1)

        prompt = ListPrompt(
            message="Select one:",
            choices=[1, 2, 3, Separator()],
            cycle=False,
        )
        self.assertEqual(prompt.content_control.selected_choice_index, 0)
        prompt._handle_up(None)
        self.assertEqual(prompt.content_control.selected_choice_index, 0)

    def test_handle_down(self) -> None:
        prompt = ListPrompt(
            message="Select one:",
            choices=[1, 2, 3, Separator()],
        )
        self.assertEqual(prompt.content_control.selected_choice_index, 0)
        prompt._handle_down(None)
        self.assertEqual(prompt.content_control.selected_choice_index, 1)
        prompt._handle_down(None)
        prompt._handle_down(None)
        self.assertEqual(prompt.content_control.selected_choice_index, 0)

    def test_handle_down_no_cycle(self):
        prompt = ListPrompt(
            message="Select one:",
            choices=[Separator(), 1, 2, 3, Separator()],
            cycle=False,
        )
        self.assertEqual(prompt.content_control.selected_choice_index, 1)
        prompt._handle_down(None)
        self.assertEqual(prompt.content_control.selected_choice_index, 2)
        prompt._handle_down(None)
        prompt._handle_down(None)
        self.assertEqual(prompt.content_control.selected_choice_index, 3)

        prompt = ListPrompt(
            message="Select one:",
            choices=[1, 2, 3, Separator()],
            cycle=False,
        )
        self.assertEqual(prompt.content_control.selected_choice_index, 0)
        prompt._handle_down(None)
        prompt._handle_down(None)
        prompt._handle_down(None)
        prompt._handle_down(None)
        self.assertEqual(prompt.content_control.selected_choice_index, 2)

    def test_handle_enter(self) -> None:
        prompt = ListPrompt(
            message="Select a fruit",
            choices=self.choices,
            default="watermelon",
            style=InquirerPyStyle({"pointer": "#61afef"}),
            vi_mode=True,
            qmark="[?]",
            pointer=">",
            instruction="(j/k)",
        )
        self.assertEqual(
            prompt.status, {"result": None, "answered": False, "skipped": False}
        )
        with patch("prompt_toolkit.utils.Event") as mock:
            event = mock.return_value
            prompt._handle_enter(event)
        self.assertEqual(
            prompt.status, {"result": "melon", "answered": True, "skipped": False}
        )

    def test_handle_enter_multi(self) -> None:
        prompt = ListPrompt(
            message="Select a fruit",
            choices=self.choices,
            default="watermelon",
            style=InquirerPyStyle({"pointer": "#61afef"}),
            vi_mode=True,
            qmark="[?]",
            pointer=">",
            instruction="(j/k)",
            multiselect=True,
        )
        self.assertEqual(
            prompt.status, {"result": None, "answered": False, "skipped": False}
        )
        with patch("prompt_toolkit.utils.Event") as mock:
            event = mock.return_value
            prompt._handle_enter(event)
        self.assertEqual(
            prompt.status, {"result": ["melon"], "answered": True, "skipped": False}
        )

    def test_handle_enter_validator(self):
        prompt = ListPrompt(
            message="Select a fruit",
            choices=self.choices,
            default="watermelon",
            style=InquirerPyStyle({"pointer": "#61afef"}),
            vi_mode=True,
            qmark="[?]",
            pointer=">",
            instruction="(j/k)",
            validate=lambda result: result != "watermelon",
        )
        self.assertFalse(prompt._invalid)
        self.assertEqual(
            prompt.status, {"result": None, "answered": False, "skipped": False}
        )
        with patch("prompt_toolkit.utils.Event") as mock:
            event = mock.return_value
            prompt._handle_enter(event)
        self.assertEqual(
            prompt.status, {"result": None, "answered": False, "skipped": False}
        )
        self.assertTrue(prompt._invalid)

        prompt.content_control.selected_choice_index = 0
        with patch("prompt_toolkit.utils.Event") as mock:
            event = mock.return_value
            prompt._handle_enter(event)
        self.assertEqual(
            prompt.status, {"result": "apple", "answered": True, "skipped": False}
        )

    @patch("InquirerLib.InquirerPy.base.complex.shutil.get_terminal_size")
    def test_wrap_lines_offset(self, mocked_term):
        mocked_term.return_value = (24, 80)
        message = 15 * "i"
        qmark = "[?]"
        instruction = 3 * "i"
        prompt = ListPrompt(
            message=message,
            choices=self.choices,
            default="watermelon",
            style=InquirerPyStyle({"pointer": "#61afef"}),
            vi_mode=True,
            qmark=qmark,
            pointer=">",
            instruction=instruction,
            show_cursor=True,
            wrap_lines=True,
        )
        self.assertEqual(
            prompt.extra_line_count,
            (len(qmark) + 1 + len(message) + 1 + len(instruction) + 1) // 24,
        )

        prompt = ListPrompt(
            message=message,
            choices=self.choices,
            default="watermelon",
            style=InquirerPyStyle({"pointer": "#61afef"}),
            vi_mode=True,
            qmark=qmark,
            pointer=">",
            instruction=instruction,
            show_cursor=False,
            wrap_lines=True,
        )
        self.assertEqual(
            prompt.extra_line_count,
            (len(qmark) + 1 + len(message) + 1 + len(instruction) + 1 - 1) // 24,
        )
        prompt._wrap_lines = False
        self.assertEqual(prompt.extra_line_count, 0)
