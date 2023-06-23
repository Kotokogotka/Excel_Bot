from datetime import date

date_day: int = date.today().day

LEXICON_RU: dict[str, str] = {
    '/statistic': f'Посещаемость на {date_day} число',
    '/help': f'Данный бот помогает отмечать детей в табеле и следить за посещаемостью\n\n'
             f'/start Команда выполняет запуск бота\n\n'
             f'/statistic Команда выводит посещаемость детей на сегодняшний день\n\n'
             f'/custom Команда  позволяет отметить ребенка в табеле выбранной тренировке по счету, где вы можете '
             f'поставить\n\n '
             f'+ если ребенок присутствовал на занятии\n\n'
             f'- если ребенка не было на занятии\n\n'
             f'O - если отсутствует по уважительной причине',
    'plus': '+',
    'minus': '-',
    'absent': 'o'
