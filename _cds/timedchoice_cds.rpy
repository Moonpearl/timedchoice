python early:
    class TimedChoice:
        def __init__(self):
            self.time = None
            self.default_option = None
            self.options = []

        def add_option(self, text, block, default = False, hidden=False):
            option = TimedChoiceOption(self, text, block)
            if not hidden:
                self.options.append(option)
            if (default):
                if (self.default_option != None):
                    raise Exception('More than one default options found in timed choice.')
                self.default_option = option

    class TimedChoiceOption:
        def __init__(self, timed_choice, text, block):
            self.timed_choice = timed_choice
            self.text = text
            self.block = block

        def is_default(self):
            return self.timed_choice.default_option == self

    class TimedChoiceCds:
        name = 'timedchoice'

        def parse(self, lexer):
            lexer.require(':')
            lexer.expect_eol()
            lexer.expect_block(self.name)

            choice = TimedChoice()

            sub_lexer = lexer.subblock_lexer()

            while sub_lexer.advance():
                with sub_lexer.catch_error():
                    sub_lexer.skip_whitespace()

                    if sub_lexer.eol():
                        continue

                    if sub_lexer.keyword('timer') != '':
                        time = sub_lexer.float()
                        if (time == None):
                            sub_lexer.error('No value provided for "timer" property.')
                        choice.time = time
                        sub_lexer.expect_eol()
                        continue

                    default = sub_lexer.keyword('default') != ''
                    hidden = sub_lexer.keyword('hidden') != ''
                    text = sub_lexer.string()
                    sub_lexer.require(':')
                    sub_lexer.expect_eol()
                    sub_lexer.expect_block(text)

                    contentblock_lexer = sub_lexer.subblock_lexer()
                    contentblock = contentblock_lexer.renpy_block(empty=True)
                    
                    choice.add_option(text=text, block=contentblock, default=default, hidden=hidden)

            return choice

        def lint(self, parsed_object):
            for option in parsed_object.options:
                check = renpy.check_text_tags(option.text)
                if check:
                    renpy.error(check)

        def execute(self, parsed_object):
            print(vars(parsed_object))
            renpy.call_screen('timedchoice', parsed_object)

        def register(self):
            renpy.register_statement(
                block=True,
                name=self.name,
                parse=self.parse,
                lint=self.lint,
                execute=self.execute,
            )
    
    TimedChoiceCds().register()
