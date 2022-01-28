import disnake

from configuratione import config

class Errata:
    def __init__(self, title: str, description: str, colour=config.ERROR_COLOR):
        self.title = title
        self.description = description
        self.colour = colour
    
    async def call(self, inter: disnake.CommandInteraction, error: Exception, *args):
        if args == ():
            embed = disnake.Embed(
                title=self.title,
                colour=self.colour
            )

        else:
            embed = disnake.Embed(
                title=self.title,
                description=self.description.format(*args),
                colour=self.colour
            )

        embed.set_author(name=inter.author.name, icon_url=inter.author.avatar)
        await inter.send(embed=embed, delete_after=config.ERROR_REMOTIONEM)
        raise error

Ignotis = Errata('Неизвестная ошибка', 'Отчёт записан')
Accessum = Errata('Не подходящий уровень доступа', 'Вы не имеете {0}', config.ACCESS_COLOR)
DBSyntax = Errata('Неверный синтаксис запроса', 'Запрос\n```{0}```')
DBUndefinedColumn = Errata('Неизвестная колонка', 'Колонка `{0}` не найдена')
DoctrinaCorpusLimit = Errata('Невозможное значение', 'Значение лимита для словарного корпуса не может быть > 100000')