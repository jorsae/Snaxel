from datetime import datetime

# Formats a timedelta into readable text
def format_timedelta(tdelta):
    days = tdelta.days
    hours, remainder = divmod(tdelta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    hours = f'0{hours}' if hours < 10 else hours
    minutes = f'0{minutes}' if minutes < 10 else minutes
    seconds = f'0{seconds}' if seconds < 10 else seconds

    if days > 0:
        dayPlural = "days" if days > 1 else "day"
        return f'{days} {dayPlural}, {hours}:{minutes}:{seconds}'
    else:
        return f'{hours}:{minutes}:{seconds}'

# Get aliases for a command
def get_aliases(aliases):
    if aliases == []:
        return ''
    else:
        output = ' | ('
        for alias in aliases:
            output += f'{alias}, '
        output = output[:-2]
        return f'{output})'