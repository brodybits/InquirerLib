# Separator

You can use {class}`~InquirerLib.InquirerPy.separator.Separator` to effectively group {ref}`pages/dynamic:choices` visually in the
following types of prompts which involves list of choices:

- {ref}`pages/prompts/list:ListPrompt`
- {ref}`pages/prompts/rawlist:RawlistPrompt`
- {ref}`pages/prompts/expand:ExpandPrompt`
- {ref}`pages/prompts/checkbox:CheckboxPrompt`

```{eval-rst}
.. autoclass:: InquirerLib.InquirerPy.separator.Separator
    :noindex:
```

<details>
  <summary>Classic Syntax</summary>

```python
"""
? Select regions: █
  Sydney
❯ Singapore
  ---------------   <- Separator
  us-east-1
  us-east-2
"""
from InquirerLib import prompt
from InquirerLib.InquirerLib.base.control import Choice
from InquirerLib.InquirerPy.separator import Separator

result = prompt(
    questions=[
        {
            "type": "list",
            "message": "Select regions:",
            "choices": [
                Choice("ap-southeast-2", name="Sydney"),
                Choice("ap-southeast-1", name="Singapore"),
                Separator(),
                "us-east-1",
                "us-east-2",
            ],
            "multiselect": True,
            "transformer": lambda result: f"{len(result)} region{'s' if len(result) > 1 else ''} selected",
        },
    ],
)
```

</details>

<details open>
  <summary>Alternate Syntax</summary>

```python
"""
? Select regions: █
  Sydney
❯ Singapore
  ---------------   <- Separator
  us-east-1
  us-east-2
"""
from InquirerLib.InquirerPy import inquirer
from InquirerLib.InquirerLib.base.control import Choice
from InquirerLib.InquirerPy.separator import Separator

region = inquirer.select(
    message="Select regions:",
    choices=[
        Choice("ap-southeast-2", name="Sydney"),
        Choice("ap-southeast-1", name="Singapore"),
        Separator(),
        "us-east-1",
        "us-east-2",
    ],
    multiselect=True,
    transformer=lambda result: f"{len(result)} region{'s' if len(result) > 1 else ''} selected",
).execute()
```

</details>
