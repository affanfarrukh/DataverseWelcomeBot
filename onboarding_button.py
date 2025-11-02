# onboarding_button.py

import discord
from introduction_flow import start_introduction  # reuse the DM Q&A function
from introduction_flow import get_dm_link

GENERAL_CHANNEL_ID = 1428272695593799703  # your #general channel ID
INTRODUCTIONS_CHANNEL_ID = 1428279420254425179  # your #introductions channel ID

class OnboardingView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(
        label="🚀 Start Onboarding",
        style=discord.ButtonStyle.success,
        custom_id="start_onboarding"
    )

    async def start_onboarding(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        intro_channel = self.bot.get_channel(INTRODUCTIONS_CHANNEL_ID)

        # Step 1: Create or get the DM channel
        dm_channel = await user.create_dm()

        dm_channel = await user.create_dm()
        print(f"✅ DM Channel ID for {user.name}: {dm_channel.id}")
        print(f"https://discord.com/channels/@me/{dm_channel.id}")

        # Send ephemeral confirmation with link to DMs
        dm_link = f"https://discord.com/channels/@me/{dm_channel.id}"
        print(dm_link)
        dm_view = discord.ui.View()
        dm_button = discord.ui.Button(label="📬 Open DMs", style=discord.ButtonStyle.link, url=dm_link)
        dm_view.add_item(dm_button)

        # Create a second button (link) to open DMs
        dm_view = discord.ui.View()
        dm_link_button = discord.ui.Button(
            label="📬 Open DMs",
            style=discord.ButtonStyle.link,
            url=dm_link
        )
        dm_view.add_item(dm_link_button)

        await interaction.response.send_message(
            "📩 Check your DMs — we’ll start your onboarding there. 💬",
            ephemeral=True,
            view = dm_view
        )


        #try:
        #    await start_introduction(self.bot, user, intro_channel)
        #except Exception as e:
        #    await interaction.followup.send(
        #        f"⚠️ Could not start onboarding: {str(e)}", ephemeral=True
        #    )


async def setup_onboarding_message(bot):
    """Posts the onboarding embed with a Start button in #general."""
    general_channel = bot.get_channel(GENERAL_CHANNEL_ID)
    if general_channel:
        embed = discord.Embed(
            title="🎉 Welcome to DataVerse!",
            description=(
                "This is where **data meets creativity!** 🚀\n\n"
                "To become a part of the community and unlock full access, "
                "please complete your onboarding journey.\n\n"
                "Click the button below to start your **onboarding process** 👇"
            ),
            color=0x1ABC9C
        )
        embed.set_footer(text="DataVerse — Explore. Learn. Collaborate.")
        await general_channel.send(embed=embed, view=OnboardingView(bot))
