# Timed Choices plugin for Ren'Py

This plugin allows you to offer timed choices in a Ren'Py project, where something happens if the player takes too long to select an option. It introduces a new command that integrates seamlessly in the Ren'Py scripting language.

## How to install

1. Create a `_plugins` folder inside your project's `game` folder. *NOTE: the naming of this folder is important becquse of the loading order of files in Ren'Py (sее [documentation](https://www.renpy.org/doc/html/lifecycle.html#early-phase)).*
2. Extract the files to your project's `game/_plugins/timedchoice` folder (or clone this repository inside `game/_plugins`).
3. You can test that the plugin works properly by including the following in your `game/script.rpy` file:

```rpy
label start:
    call plugin_timedchoice_demo
```

This will launch a demo script that explains the capabilities of the plugin next time you launch your game.

The `demo` folder from this plugin can be removed afterwards, as it only serves to showcase its capabilities, and is not essential for it to work peroperly.

## How to setup

### Adjust the appearance of the timer

You can adjust how the visual indicator looks by tweaking the following properties in `engine/timedchoice.rpy`:

```rpy
# The color of the bar background (when it's empty).
define gui.timedchoice_bar_bg_color = gui.muted_color

# The color of the bar fill (when it's full).
define gui.timedchoice_bar_fill_color = gui.accent_color

# The width of the timer bar in pixels.
define gui.timedchoice_bar_width = gui.choice_button_width / 2

# The height of the timer bar in pixels.
define gui.timedchoice_bar_height = 10
```

### Control the timer

You can adjust the default timer by tweaking the following property in `engine/timedchoice.rpy`:

```rpy
# The default time for timed choices in seconds.
define default_timer = 3.0
```

### Make timer speed adjustable in preferences

You can allow the user to adjust the speed of timed choices by adding the following code in the `preferences` screen in your `screens.rpy` file:

```rpy
screen preferences():
    # Add the following after the "Text Speed" slider

    label _("Timed Choice Speed")

    bar value VariableValue("persistent.timedchoice_speed", min=0.5, max=2.0, step=0.25, force_step=True, style="slider")
```

You can adjust the values in the [VariableValue](https://www.renpy.org/doc/html/screen_actions.html#VariableValue) constructor:

- `min` is the lowest possible speed;
- `max` is the highest possible speed;
- `step` is the speed difference between each step of the slider.

Using the settings provided in the example, you would end up with a slider that allows the user to select: 0.5, 0.75, 1.0, 1.25, 1.5, 1.75 and 2.0.

This speed parameter represents how much faster the timer elapses. For example, using a timer of 3s:

- A speed of 0.5 will make the choice last 6 seconds (twice slower);
- A speed of 1.0 will make the choice last 3 seconds;
- A speed of 2.0 will make the choice last 1.5 seconds (twice faster).

## How to use

The following examples are meant for technical reference. Please refer to the demo for more concrete examples that show how the plugin may be useful gamewise.

### Create a timed choice

The syntax of the new `timedchoice` command mimicks that of the built-in `menu` command.

**Rules:**

- The `timedchoice` command **must** be followed by `:` and a new block.
- Each option **must** be a `string` (arbitrary text marked by double quotes `"`), **must** be followed by `:` and a new block.
- The block of commands for each option can be any valid block in the Ren'Py syntax.

**Example:**

```rpy
timedchoice:
    "Option 1":
        # What to do when option 1 is selected
    "Option 2":
        # What to do when option 2 is selected
    "Option 3":
        # What to do when option 3 is selected
```

This will prompt the user to take a pick between all 3 options and execute only the block of commands associated with that option. If the choice times out (the user hasn't selected any options before the timer runs out), then nothing happens.

### Define a time-out option

It is possible to force an option to be picked when the choice times out. To do this, add a `timeout` keyword before the option's name.

**Rules:**

- The `timeout` keyword **may** be included, and **must** be written before the option's name.
- A single choice **must not** have more than 1 `timeout` option.

**Example:**

```rpy
timedchoice:
    "Option 1":
        # What to do when option 1 is selected
    "Option 2":
        # What to do when option 2 is selected
    timeout "Option 3":
        # What to do when option 3 is selected
```

This will behave like the previous example, except that if the choice times out (the user hasn't selected any options before the timer runs out), the block define after "Option 3" will be executed.

*NOTE: a transform will be applied to the default option that allows to visually identify it. This transform is labeled as `timedchoice_default_option` and can be overriden to suit your needs.*

***Example:***

```rpy
transform timedchoice_default_option:
    # This transform does not modify the base display,
    # thus rendering the default choice indistinguishable
    # from the others.
    matrixcolor IdentityMatrix()
```

## Hide the time-out option

It is possible to define a time-out option that cannot be picked manually, and thus is triggered only on time-out.

**Rules:**

- The `hidetimeout` parameter **may** be included in the `timedchoice` command block.
- If it is present, the `hidetimeout` paramter **must** be followed by an expression.
- The expression following the `hidetimeout` parameter **must** resolve to a **bool** (`True` or `False`).

**Example:**

```rpy
timedchoice:
    hidetimeout True
    "Option 1":
        # What to do when option 1 is selected
    "Option 2":
        # What to do when option 2 is selected
    timeout:
        # What to do when option 3 is selected
```

This will behave like the previous example, except that the third option will not be listed in the options that the user can pick.

*NOTE: though it is technically possible to give a caption to the hidden option, like for any other options, it doesn't really make any sense since the option will not be displayed anyway. However, you may want to give it a caption anyway, in the case the `hidetimeout` option is variable.*

**Example:**

```rpy
init python:
    def somelogic():
        # Write some logic that returns True or False

timedchoice:
    # Whether the time-out option is hidden will be decided according to the result of the somelogic() function
    hidetimeout somelogic()
    "Option 1":
        # What to do when option 1 is selected
    "Option 2":
        # What to do when option 2 is selected
    timeout "Option 3":
        # What to do when option 3 is selected
```

## Adjust the timer

It is possible to modify the time allocated to the user to make his decision.

**Rules:**

- The `timer` parameter **may** be included in the `timedchoice` command block.
- If it is present, the `timer` paramter **must** be followed by an expression.
- The expression following the `timer` parameter **must** resolve to a number.

**Example:**

```rpy
timedchoice:
    timer 10
    "Option 1":
        # What to do when option 1 is selected
    "Option 2":
        # What to do when option 2 is selected
    timeout "Option 3":
        # What to do when option 3 is selected
```

This will behave like the previous example, except that the user will have 10 seconds instead of the default 3 to think and make a choice.

*NOTE: just like the `hidetimeout` paramter, the `timer` parameter can be set using a variable or a function.*

**Example:**

```rpy
timedchoice:
    # This will cause the timer to be set to a random number between 2 and 5
    timer renpy.random.randint(2, 5)
    "Option 1":
        # What to do when option 1 is selected
    "Option 2":
        # What to do when option 2 is selected
    timeout "Option 3":
        # What to do when option 3 is selected
```
