# number

A prompt for entering numbers. All non number input will be disabled for this prompt.

## Example

![demo](https://assets.kazhala.me/InquirerPy/number.gif)

<details>
  <summary>Classic Syntax (PyInquirer)</summary>

```{eval-rst}
.. literalinclude :: ../../../examples/classic/number.py
   :language: python
```

</details>

<details open>
  <summary>Alternate Syntax</summary>

```{eval-rst}
.. literalinclude :: ../../../examples/alternate/number.py
   :language: python
```

</details>

## Keybindings

```{seealso}
{ref}`pages/kb:Keybindings`
```

```{include} ../kb.md
:start-after: <!-- start kb -->
:end-before: <!-- end kb -->
```

The following dictionary contains the additional keybindings created by this prompt.

```
{
  "down": [
    {"key": "down"},  # decrement the number
    {"key": "c-n"},
  ],
  "up": [
    {"key": "up"},  # increment the number
    {"key": "c-p"},
  ],
  "left": [
    {"key": "left"},  # move cursor to the left
    {"key": "c-b"},
  ],
  "right": [
    {"key": "right"},   # move cursor to the right
    {"key": "c-f"},
  ],
  "focus": [
    {"key": "c-i"},   # focus the alternate input buffer when float_allowed=True
    {"key": "s-tab"},
  ],
  "negative_toggle": [{"key": "-"}], # toggle result negativity
  "dot": [{"key": "."}],  # focus the integral buffer when float_allowed=True to enter decimal points
}
```

When `vi_mode` is True, the direction navigation key will be changed.

```{tip}
Additionally, the input buffer can also enter normal mode by pressing `esc` when `vi_mode` is True.
```

```
{
  "down": [
    {"key": "down"},
    {"key": "j"},
  ],
  "up": [
    {"key": "up"},
    {"key": "k"},
  ],
  "left": [
    {"key": "left"},
    {"key": "h"},
  ],
  "right": [
    {"key": "right"},
    {"key": "l"},
  ],
}
```

## Default Value

The default value of the input buffer is set to `0` to help differentiate with {ref}`InputPrompt <pages/prompts/input:text>`. You could disable
this value and have an empty input buffer by setting the parameter `default=None`.

<details>
  <summary>Classic Syntax (PyInquirer)</summary>

```{code-block} python
from InquirerLib import prompt

questions = [
  {
    "type": "number",
    "message": "Number:",
    "default": None,
  }
]

result = prompt(questions)
```

</details>

<details open>
  <summary>Alternate Syntax</summary>

```{code-block} python
from InquirerLib.InquirerPy import inquirer

result = inquirer.number(message="Number:", default=None).execute()
```

</details>

## Max and Min

You can set the maximum allowed value as well as the minimum allowed value for the prompt via `max_allowed` and `min_allowed`.

```{hint}
When the input value goes above/below the max/min value, the input value will automatically reset to the
configured max/min value.
```

<details>
  <summary>Classic Syntax (PyInquirer)</summary>

```{code-block} python
from InquirerLib import prompt

questions = [
  {
    "type": "number",
    "message": "Number:",
    "max_allowed": 10,
    "min_allowed": -100
  }
]

result = prompt(questions)
```

</details>

<details open>
  <summary>Alternate Syntax</summary>

```{code-block} python
from InquirerLib.InquirerPy import inquirer

result = inquirer.number(
  message="Number:", max_allowed=10, min_allowed=-100,
).execute()
```

</details>

## Decimal Input

```{tip}
Once you enable decimal input, the prompt will have a second input buffer. You can keep navigating `left`/`right`
to enter the other input buffer or you can use the `tab`/`shit-tab` to focus the other buffer.
```

You can enable decimal input by setting the argument `float_allowed` to True.

<details>
  <summary>Classic Syntax (PyInquirer)</summary>

```{code-block} python
from InquirerLib import prompt

questions = [
  {
    "type": "number",
    "message": "Number:",
    "float_allowed": True,
  }
]

result = prompt(questions)
```

</details>

<details open>
  <summary>Alternate Syntax</summary>

```{code-block} python
from InquirerLib.InquirerPy import inquirer

result = inquirer.number(
  message="Number:", float_allowed=True,
).execute()
```

</details>

## Replace Mode

By default, all input buffer has the exact same behavior as terminal input behavior. There is an optional replace mode
which you could enable for a better experience when working with decimal points input. You can enable it via
parameter `replace_mode=True`.

```{warning}
Replace mode introduce some slight inconsistency with the terminal input behavior that we are used to.
```

<details>
  <summary>Classic Syntax (PyInquirer)</summary>

```{code-block} python
from InquirerLib import prompt

questions = [
  {
    "type": "number",
    "message": "Number:",
    "replace_mode": True,
  }
]

result = prompt(questions)
```

</details>

<details open>
  <summary>Alternate Syntax</summary>

```{code-block} python
from InquirerLib.InquirerPy import inquirer

result = inquirer.number(
  message="Number:", replace_mode=True,
).execute()
```

</details>

The following gif demonstrate the different behavior when we are trying to input number "123.102". The first prompt is `replace_mode=False`
and the second prompt is `replace_mode=True`.

![demo](https://assets.kazhala.me/InquirerPy/number-replace.gif)

## Reference

```{eval-rst}
.. autoclass:: InquirerLib.InquirerLib.prompts.number.NumberPrompt
    :noindex:
```
