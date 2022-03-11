intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )

def display_time(seconds: int, granularity: int = 2):
    """Преобразует время из секунд в время в максимальный формат (например: 600 сек. - 10 минут, 3600 сек. - 1 час и т.п.)

    Args:
        seconds (int): время в секундах, которое нужно преобразовать
        granularity (int, optional): детализация возвращаемой строки. По умолчанию - 2.

    Returns:
        str: _description_

    IN: display_time(3660)
    OUT: '1 hours, 1 minutes'

    IN: display_time(3661, 5)
    OUT: '1 hours, 1 minutes, 1 seconds'

    IN: display_time(99461, 5)
    OUT: '1 day, 3 hours, 37 minutes, 41 seconds'

    IN: display_time(99461, 3)
    OUT: '1 day, 3 hours, 37 minutes'
    """
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])
