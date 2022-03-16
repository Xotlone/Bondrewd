import disnake

from constants import config

class OtherError:
    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description
    
    async def __call__(self, inter: disnake.CommandInteraction, error: Exception, *args):
        if args == ():
            embed = disnake.Embed(
                title=self.title,
                colour=config.DEFAULT_COLOR
            )

        else:
            embed = disnake.Embed(
                title=self.title,
                description=self.description.format(*args),
                colour=config.DEFAULT_COLOR
            )

        embed.set_author(name=inter.author.name, icon_url=inter.author.avatar)
        await inter.edit_original_message(embed=embed, delete_after=config.ERROR_REMOVE)
        raise error

UndefinedError = OtherError('Неизвестная ошибка', 'Отчёт записан')
Access = OtherError('Не подходящий уровень доступа', 'Вы не имеете **{0}**')
Bot = OtherError('Пользователь является ботом', 'Пользователь не должен быть ботом')
DBSyntax = OtherError('Неверный синтаксис запроса', 'Запрос\n```{0}```')
DBUndefinedColumn = OtherError('Неизвестная колонка', 'Колонка `{0}` не найдена')
MLCorpusLimit = OtherError('Невозможное значение лимита', 'Значение лимита для словарного корпуса должно быть в пределах [1000, 100000]')