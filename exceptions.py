import disnake

from constants import config


class OtherError:
    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description

    async def __call__(self, inter: disnake.CommandInteraction, *args):
        if args == ():
            embed = disnake.Embed(
                title=self.title,
                description=self.description,
                colour=config.DEFAULT_COLOR
            )

        else:
            embed = disnake.Embed(
                title=self.title,
                description=self.description.format(*args),
                colour=config.DEFAULT_COLOR
            )

        embed.set_author(name=inter.author.name, icon_url=inter.author.avatar)
        await inter.send(embed=embed)
        await inter.delete_original_message(delay=config.ERROR_REMOVE)


UndefinedError = OtherError('Неизвестная ошибка', 'Отчёт записан')
Access = OtherError('Не подходящий уровень доступа', 'Вы не имеете **{0}**')
Bot = OtherError('Пользователь является ботом', 'Пользователь не должен быть ботом')
DBSyntax = OtherError('Неверный синтаксис запроса', 'Запрос\n```{0}```')
DBUndefinedColumn = OtherError('Неизвестная колонка', 'Колонка `{0}` не найдена')
MLCorpusLimit = OtherError('Невозможное значение лимита', 'Значение лимита для словарного корпуса должно быть в '
                                                          'пределах [1000, 100000]')
NSFW = OtherError('Не NSFW', 'Эту команду вызывать только в канале с меткой NSFW')
