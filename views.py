from typing import List

import disnake


# Defines a simple paginator of buttons for the embed.
class Paginator(disnake.ui.View):
    def __init__(self, embeds: List[disnake.Embed]):
        super().__init__()
        self.embeds = embeds
        self.embed_count = 0

        self.first_page.disabled = True
        self.prev_page.disabled = True

    @disnake.ui.button(emoji="⏪", style=disnake.ButtonStyle.blurple)
    async def first_page(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.embed_count = 0
        embed = self.embeds[self.embed_count]

        self.first_page.disabled = True
        self.prev_page.disabled = True
        self.next_page.disabled = False
        self.last_page.disabled = False
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(emoji="◀", style=disnake.ButtonStyle.blurple)
    async def prev_page(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.embed_count -= 1
        embed = self.embeds[self.embed_count]

        self.next_page.disabled = False
        self.last_page.disabled = False
        if self.embed_count == 0:
            self.first_page.disabled = True
            self.prev_page.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(emoji="❌", style=disnake.ButtonStyle.red)
    async def remove(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await interaction.response.edit_message(view=None)

    @disnake.ui.button(emoji="▶", style=disnake.ButtonStyle.blurple)
    async def next_page(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.embed_count += 1
        embed = self.embeds[self.embed_count]

        self.first_page.disabled = False
        self.prev_page.disabled = False
        if self.embed_count == len(self.embeds) - 1:
            self.next_page.disabled = True
            self.last_page.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(emoji="⏩", style=disnake.ButtonStyle.blurple)
    async def last_page(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.embed_count = len(self.embeds) - 1
        embed = self.embeds[self.embed_count]

        self.first_page.disabled = False
        self.prev_page.disabled = False
        self.next_page.disabled = True
        self.last_page.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)


class Dropdown(disnake.ui.Select):
    def __init__(self, placeholder: str, options: List[disnake.SelectOption], callback_func, min_options: int,
                 max_options: int):
        super().__init__(
            placeholder=placeholder,
            min_values=min_options,
            max_values=max_options,
            options=options,
        )
        self.callback_func = callback_func

    async def callback(self, inter: disnake.MessageInteraction):
        await self.callback_func(self, inter)


class DropdownView(disnake.ui.View):
    def __init__(self, placeholder: str, options: List[disnake.SelectOption], callback_func, min_options: int = 1,
                 max_options: int = 1):
        super().__init__()

        self.add_item(Dropdown(placeholder, options, callback_func, min_options, max_options))
