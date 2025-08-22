# The speed of the timer.
# 1.0 = 1s on the timer actually lasts 1s.
# 2.0 = 1s on the timer actually lasts 0.5s.
# 0.5 = 1s on the timer actually lasts 2.0s.
default persistent.timedchoice_speed = 1.0

# The color of the bar background (when it's empty).
define gui.timedchoice_bar_bg_color = gui.muted_color

# The color of the bar fill (when it's full).
define gui.timedchoice_bar_fill_color = gui.accent_color

# The width of the timer bar in pixels.
define gui.timedchoice_bar_width = gui.choice_button_width / 2

# The height of the timer bar in pixels.
define gui.timedchoice_bar_height = 10

# The default time for timed choices in seconds.
define default_timer = 3.0


# Translations.
translate None strings:
    old "Timed Choice Speed"
    new "Timed Choice Speed"


# The sceeen that handles the display of timed choices.
screen timedchoice(choice):
    style_prefix "choice"

    # Adjust the total time by the speed setting.
    if (choice.time == None):
        default time = float(default_timer) / persistent.timedchoice_speed
    else:
        default time = float(choice.time) / persistent.timedchoice_speed

    # Manage timer.
    default timer_finished = False

    if not timer_finished:  
        # If the timer has not finished, then wait.
        timer time action SetScreenVariable("timer_finished", True)
    else:
        # Otherwise, execute the time-out action.
        if choice.default_option == None:
            timer 0.01 action Return()
        else:
            timer 0.01 action Jump(choice.default_option.block)

    # Show the list of choices.
    vbox:
        # The choices.
        for option in choice.options:
            textbutton option.text:
                action Jump(option.block)
                if option.is_default():
                    at timedchoice_default_option

        # The timer visual.
        use timedchoice_bar(time)


# Visual indicator of the time remaining.
screen timedchoice_bar(time):

    fixed:
        xsize int(gui.timedchoice_bar_width) 
        ysize int(gui.timedchoice_bar_height)
        xalign 0.5
        
        # Bar background (when it's empty).
        add Solid(gui.timedchoice_bar_bg_color) 

        # Bar fill (when it's full).
        add Solid(gui.timedchoice_bar_fill_color):
            at transform:
                xalign 0.5
                xzoom 1.0
                linear time xzoom 0.0


# Visual transform applied to the default option.
transform timedchoice_default_option:
    matrixcolor SepiaMatrix()
