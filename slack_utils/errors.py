class SlackError(Exception):
    pass


class SlackLimitRateError(SlackError):
    pass


class SlackMixinError(SlackError):
    pass


class SlackTokenError(SlackError):
    pass
