import random
import asyncio

import disnake
from disnake.ext import commands as dis_commands

from constants import commands, config
import controller
from database import database
from external_libs.google_trans_new import google_trans_new


class Funcs(dis_commands.Cog):
    def __init__(self, bot: dis_commands.Bot):
        self.bot = bot

    @dis_commands.slash_command(**commands.funcs())
    @dis_commands.check(commands.funcs.acs)
    async def command_funcs(self, inter: disnake.CommandInteraction):
        pass

    @command_funcs.sub_command(**commands.funcs.sub['calc']())
    @dis_commands.check(commands.funcs.sub['calc'].acs)
    async def sub_calc(self, inter: disnake.CommandInteraction, primer: str):
        embed = disnake.Embed(
            title='Математический пример',
            description=f"{primer} = {eval(primer)}",
            colour=controller.RANKS_DICT['Колокольчик'].colour
        )
        await inter.edit_original_message(embed=embed)

    @command_funcs.sub_command(**commands.funcs.sub['learn-japanese']())
    @dis_commands.check(commands.funcs.sub['learn-japanese'].acs)
    async def sub_learn_japanese(self, inter: disnake.CommandInteraction, alphabet: str, only_complex: str = '0'):
        only_complex = int(only_complex)
        if alphabet == 'hiragana':
            alphabet = list(config.HIRAGANA.items())

        while True:
            if only_complex:
                complex_chars = database(f'SELECT complex_chars FROM users WHERE id = {inter.author.id}', 'one')[0]
                if complex_chars == '':
                    embed = disnake.Embed(
                        title='Список трудных мор пуст',
                        colour=controller.RANKS_DICT['Колокольчик'].colour
                    )
                    await inter.edit_original_message(embed=embed)
                    return

                else:
                    complex_chars = complex_chars.split(', ')
                    true_choice = random.choice(complex_chars)
                    for i in alphabet:
                        if i[1] == true_choice:
                            true_choice = i

            else:
                true_choice = random.choice(alphabet)
            available_choices = alphabet.copy()
            available_choices.remove(true_choice)
            false_choices = []
            for i in range(config.LJ_CHOICES_COUNT):
                false_choices.append(random.choice(available_choices))
                available_choices.remove(false_choices[-1])

            key_or_val = random.randint(0, 1)
            true_button = disnake.ui.Button(label=true_choice[key_or_val], style=disnake.ButtonStyle.green)
            false_buttons = [disnake.ui.Button(label=i[key_or_val], style=disnake.ButtonStyle.green) for i in
                             false_choices]
            buttons = [true_button, *false_buttons]
            random.shuffle(buttons)
            buttons.append(disnake.ui.Button(emoji='⚡', style=disnake.ButtonStyle.blurple, custom_id='hard'))
            true_answer = true_choice[not key_or_val]

            embed = disnake.Embed(
                title=true_answer,
                description='Выберете правильный иероглиф (мору). Если этот иероглиф вам трудно выучить, '
                            'тогда добавьте его в свой список трудных иероглифов кнопкой с молнией. '
                            'Второе нажатие удаляет иероглиф из списка',
                colour=controller.RANKS_DICT['Колокольчик'].colour
            )
            embed.set_author(name=inter.author.name, icon_url=inter.author.avatar.url)
            embed.set_footer(text=f'На ответ даётся {config.CHOICE_DELAY} с.')
            orig = await inter.edit_original_message(embed=embed, components=buttons)
            try:
                clicked = await self.bot.wait_for('button_click', check=lambda x: x.author.id == inter.author.id
                                                                                  and x.message.id == orig.id,
                                                  timeout=config.CHOICE_DELAY)
            except asyncio.TimeoutError:
                embed = disnake.Embed(
                    title='Время вышло',
                    colour=controller.RANKS_DICT['Колокольчик'].colour
                )
                embed.set_author(name=inter.author.name, icon_url=inter.author.avatar.url)
                await orig.edit(embed=embed, components=[])
                await orig.delete(delay=4)
                return

            if clicked.component.label == true_choice[key_or_val]:
                embed = disnake.Embed(
                    title='Ответ правильный',
                    description=f'{true_answer} = {true_choice[key_or_val]}',
                    colour=disnake.Colour.green()
                )
                embed.set_author(name=inter.author.name, icon_url=inter.author.avatar.url)

            elif clicked.component.custom_id == 'hard':
                complex_chars = database(f'SELECT complex_chars FROM users WHERE id = {inter.author.id}', 'one')[0]
                if complex_chars == '' and not only_complex:
                    complex_chars = [true_choice[1]]
                    complex_chars = ', '.join(complex_chars)
                    database(f'UPDATE users SET complex_chars = \'{complex_chars}\' WHERE id ='
                             f' {inter.author.id}')
                    embed = disnake.Embed(
                        title='Иероглиф отмечен как трудный',
                        description=f'Теперь {true_choice[0]} ({true_choice[1]}) в вашем списке трудных мор. '
                                    f'Список: {complex_chars}',
                        colour=disnake.Colour.green()
                    )

                elif complex_chars == '' and only_complex:
                    complex_chars = [true_choice[1]]
                    complex_chars = ', '.join(complex_chars)
                    database(f'UPDATE users SET complex_chars = \'{complex_chars}\' WHERE id ='
                             f' {inter.author.id}')
                    embed = disnake.Embed(
                        title='Список пуст',
                        description=f'Ваш список трудных мор пуст',
                        colour=disnake.Colour.green()
                    )

                else:
                    complex_chars = complex_chars.split(', ')
                    if true_choice[1] not in complex_chars:
                        complex_chars.append(true_choice[1])
                        complex_chars = ', '.join(complex_chars)
                        database(f'UPDATE users SET complex_chars = \'{complex_chars}\' WHERE id ='
                                 f' {inter.author.id}')
                        embed = disnake.Embed(
                            title='Изменение списка',
                            description=f'Теперь {true_choice[0]} ({true_choice[1]}) в вашем списке трудных мор. '
                                        f'Список: {complex_chars}',
                            colour=disnake.Colour.green()
                        )

                    else:
                        complex_chars.remove(true_choice[1])
                        complex_chars = ', '.join(complex_chars)
                        database(f'UPDATE users SET complex_chars = \'{complex_chars}\' WHERE id ='
                                 f' {inter.author.id}')
                        embed = disnake.Embed(
                            title='Изменение списка',
                            description=f'{true_choice[0]} ({true_choice[1]}) удалён из списка трудных мор. Список: '
                                        f'{complex_chars}',
                            colour=disnake.Colour.green()
                        )

            else:
                embed = disnake.Embed(
                    title='Ответ неверный',
                    description=f'{true_answer} = {true_choice[key_or_val]}',
                    colour=disnake.Colour.red()
                )
                embed.set_author(name=inter.author.name, icon_url=inter.author.avatar.url)

            await clicked.response.edit_message(embed=embed, components=[])
            await asyncio.sleep(2)

    @command_funcs.sub_command(**commands.funcs.sub['translate']())
    @dis_commands.check(commands.funcs.sub['translate'].acs)
    async def sub_translate(self, inter: disnake.CommandInteraction, text: str, from_lang: str = 'auto', to_lang: str
    = 'ru'):
        if (from_lang not in google_trans_new.LANGUAGES and from_lang != 'auto') or \
                (to_lang not in google_trans_new.LANGUAGES and to_lang != 'auto'):
            embed = disnake.Embed(
                title='Не соответствует IETF',
                description=f'Кода языка "{from_lang}" или "{to_lang}" не существует',
                colour=disnake.Colour.red()
            )

        else:
            translator = google_trans_new.google_translator()
            translated = translator.translate(text, to_lang, from_lang)
            embed = disnake.Embed(
                title='Перевод',
                colour=controller.RANKS_DICT['Колокольчик'].colour
            )
            embed.add_field(f'С {from_lang} на {to_lang}', translated)

        await inter.edit_original_message(embed=embed)


def setup(bot):
    bot.add_cog(Funcs(bot))
