---
title: Make Inlay Type Hints in Python Appear/Disappear
date: 27 Jul 2022 14:35
tags: VS Code, Python
category: work
image: https://jmblogstorrage.blob.core.windows.net/media/type_literals.png
---

## A Type Hinting Tip for Those Not Completely Onboard


> TLDR: You can set `Inlay Hints: Enabled` to `On/OffUnless pressed` in the settings to show/hide inlay type hints in Python code. 

In July the VS Code Python Team released an [update for VS Code](https://devblogs.microsoft.com/python/python-in-visual-studio-code-july-2022-release/) that announced inlay Type Hint Support.

<iframe width="560" height="315" src="https://www.youtube.com/embed/hHBp0r4w86g" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Adding type hint inferences next to your code is very nice. The more I started playing with it, I noticed that sometimes the type hints didn't feel helpful and made my code look cluttered.

![type literals don't help that much when writing code](https://jmblogstorrage.blob.core.windows.net/media/type_literals.png)

Don't get me wrong, I like type hints. They are a massive help with troubleshooting and documentation. They are even used in [dataclasses](https://docs.python.org/3/library/dataclasses.html), one of my favorite standard library tools. Just as I tell my child, there is a time and place for everything. When it comes to type hints, _All the Time!_, is not the answer.

### Let's take the following example.

Let's say we have some dictionary objects that are brought into our code from multiple systems. Sometimes the `employee_id` will be a numerical id and other times it will be a unique string.

```python

jay = {
    "name": "Jay",
    "employee_id": "abcd1234" # some records could be integers depending on the schema
}
```

If we don't define types, PyLance will assume that the contact `jay` is the type `dict[str, str]` because all the values in the dictionary are `str`. What happens if we have a different record like:

```python
kevin = {
	"name": "Kevin",
	"employee_id": 12345678
}
```

The variable of `kevin` would be typed `dict[str, Any]` because the type of the `employee_id` differs from the `name`. 

If we build a function that gets the employee id of multiple entries and sorts by `employee_id`, We'll get a `TypeError`.

```python
def get_employee_id(contact):
 	"""retrieve employee id from contact"""
	return contact["employee_id"]

sorted_employees = sorted([jay, kevin], key=get_employee_id)
>>> Traceback (most recent call last):
  File "<stdin>", line 1, in <module>

TypeError: '<' not supported between instances of 'int' and 'str'
```

The solution is to return the contact variable as a str.  Type Hints would have told us that the contact would have been `Any` type (like `kevin`). And this would have been a hint we need to make types consistent. 

We could even create a custom named type as Łukasz Langa mentions in his [PyCon US 2022 Keynote](https://youtu.be/wbohVjhqg7c?t=753). This would provide helpful hints as we're writing the code.

![custom type hint](https://jmblogstorrage.blob.core.windows.net/media/custom_type_contact.png)

## The July 2022 Update
The aforementioned VS Code Python update made it so that types could be inlayed next to your code. This makes adding type hints much simpler because hints (which are not added to your code) are valid Python code and can be added by the author.

In this case the hints would have been helpful but I don't want them always be present. There is an existing feature that may be new to Python developers using VS Code that will make showing your type hints only when you want to see them.

## Turning On Inlay Hints

For this to work you must first turn on Inlay Hints for python. Make sure the [Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) is installed in VS Code and search "Python Inlay Hints" in settings.

![python inlay type hints](https://jmblogstorrage.blob.core.windows.net/media/set_python_inlay_hints.gif)

The first value to turn on is `Python › Analysis › Inlay Hints: Function Return Types`. This gives typing for what a function or method is returning.

The second is `Python › Analysis › Inlay Hints: Variable Types`. This inlays hints on variables that are written (like the ones above).

## Customizing How Inlay Hints Present in Your Editor

Next in settings just search for "Inlay".  You should find `Editor › Inlay Hints: Enabled`.  The value is set to `on` by default, but it has a few options, including `OnUnlessPressed` and `OffUnlessPressed`.

![Set Inlay Hints Enabled](https://jmblogstorrage.blob.core.windows.net/media/set_inlay_hints.gif)

**If you change the value to `OffUnlessPressed`, you will no longer see inlayed hints until you enter _Ctrl + Alt_ (_⌃ + ⌥_ on MacOS)**. When you need a hint, press the keys and the type hints will reappear. Release the keys and they disappear again.

![Toggle Inlay Hints](https://jmblogstorrage.blob.core.windows.net/media/toggle_inlay_hints.gif)

You can also set `OnUnlessPressed`. This does the opposite, only showing the code that exists in the file. This entry in settings is also next to other Inlay hint stylings that may help you differentiate your code from hints. 