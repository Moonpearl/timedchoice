label plugin_timedchoice_demo:
    # Basic example
    "This is an example of a timed choice where nothing happens on time-out."

    timedchoice:
        "Laugh":
            "You decided to laugh."
        "Cry":
            "You decided to cry."
    
    "This next line will happen, regardless of what you've chosen previously."
    "This allows you to offer opportunities that the player will pass on if they can't make up their mind."

    # Example with default option
    "Next…"
    "This is an example of a timed choice where an option is automatically selected on time-out."

    timedchoice:
        "Shout":
            "You decided to shout."
        timeout "Stay silent":
            "You decided to stay silent."

    "This allows you to enforce a choice if the player can't make up their mind."

    # Example with hidden default option
    "Next…"
    "This is an example of a timed choice where something happens on timeout, but you cannot select it."

    timedchoice:
        hidetimeout True
        "Run away":
            "You decided to run away."
        "Hide":
            "You decided to hide."
        timeout:
            "You just stand there and get crushed by a meteor."
    
    "This allows you to enforce consequences if the player can't make up their mind, without them knowing what's going to happen."

    # Example with specified timer
    "Next…"
    "This is an example of a timed choice with a timer set."

    timedchoice:
        timer 10
        "Ponder about the absurdity of life":
            "You now feel empty inside."
        "Reflect on your past choices":
            "You think that many things could have gone differently."
        timeout "Wait for something interesting to happen":
            "You wait for some time, but nothing happens."
    
    "This is useful when you want to allow the player more time to think, if there's a lot of text to read, or if the choice is especially difficult."
    "You can also shorten the timer to force players to react on the spot!"

    # Example using variables
    "Next…"
    "This is an example of how you can use variables to adjust the command's behavior."
    "You will get to choose how much time you want to give yourself to make up your mind, and whether the default option should be displayed."
    "Pick the default option to try again with different settings. Picking one of the other options will let you move on."

    call plugin_timedchoice_demo_variables

    # Wrap up
    "And that concludes our demo of the timed choice syntax."
    
    return


label plugin_timedchoice_demo_variables:
    menu:
        "Set the timer."
        "2 seconds":
            $ time = 2
        "5 seconds":
            $ time = 5
        "10 seconds":
            $ time = 10

    menu:
        "Do you want to the time-out option to be visible?"
        "Show the time-out option":
            $ hidden = False
        "Hide the time-out option":
            $ hidden = True

    timedchoice:
        timer time
        hidetimeout hidden
        "Pick the blue pill":
            "You get back to your sleep."
        "Pick the red pill":
            "You suddenly awaken."
        timeout "Don't pick anything":
            "You tremble as you hesitate."
            call plugin_timedchoice_demo_variables

    return
