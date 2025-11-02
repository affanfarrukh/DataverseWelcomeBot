# introduction_flow.py
import discord
import asyncio
from assign_role import assign_role_to_member
from store_user_data import save_user_data

class RoleSelectionView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="🧑‍🎓 Student", style=discord.ButtonStyle.primary)
    async def student(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "Student"
        await interaction.response.send_message("✅ You selected **Student**.", ephemeral=True)
        self.stop()

    @discord.ui.button(label="💼 Professional", style=discord.ButtonStyle.success)
    async def professional(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "Professional"
        await interaction.response.send_message("✅ You selected **Professional**.", ephemeral=True)
        self.stop()

    @discord.ui.button(label="🚀 Enthusiast", style=discord.ButtonStyle.secondary)
    async def enthusiast(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "Enthusiast"
        await interaction.response.send_message("✅ You selected **Enthusiast**.", ephemeral=True)
        self.stop()

class GoalsSelectionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None
        self.add_item(GoalsSelect(self))


class GoalsSelect(discord.ui.Select):
    def __init__(self, view_ref):
        self.view_ref = view_ref
        options = [
            discord.SelectOption(label="📘 Learn Data Science", description="Start your journey in DS & AI"),
            discord.SelectOption(label="🧩 Build Projects", description="Work on practical data projects"),
            discord.SelectOption(label="🤝 Collaborate", description="Meet peers and share ideas"),
            discord.SelectOption(label="🚀 Launch a Startup", description="Turn ideas into products"),
            discord.SelectOption(label="💬 Improve Communication", description="Present and explain your ideas")
        ]
        super().__init__(
            placeholder="Select one or more goals...",
            min_values=1,
            max_values=3,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        selected = self.values  # <-- values are already strings
        self.view_ref.value = ", ".join(selected)
        await interaction.response.send_message(
            f"✅ You selected: {self.view_ref.value}", ephemeral=True
        )
        self.view_ref.stop()

async def get_dm_link(user: discord.User) -> str:
    """
    Creates or fetches the DM channel for the given user
    and returns the direct Discord link to open that DM.
    Example: https://discord.com/channels/@me/123456789012345678
    """
    dm_channel = await user.create_dm()
    print(f"🔗 DM link for {user.name}: {dm_channel}")

    return

class RestartOnboardingView(discord.ui.View):
    def __init__(self, bot, member, intro_channel):
        super().__init__(timeout=None)
        self.bot = bot
        self.member = member
        self.intro_channel = intro_channel

    @discord.ui.button(
        label="🚀 Restart Onboarding",
        style=discord.ButtonStyle.primary,
        emoji="🔁"
    )
    async def restart(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "✨ Restarting your onboarding process...",
            ephemeral=True
        )
        await start_introduction(self.bot, self.member, self.intro_channel)


async def start_introduction(bot, member, intro_channel):
    """
    Starts a private Q&A in DM and posts the final introduction as an embed in the introductions channel.
    """

    try:
        # Start DM session
        embed = discord.Embed(
            title="👋 Welcome to DataVerse!",
            description=(
                "We’re excited to have you here! 💫\n\n"
                "**This is your personal onboarding space.**\n"
                "Please answer a few quick questions so we can introduce you to the community.\n\n"
                "Take your time — your responses help us get to know you better 💬"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            ),
            color=0x1ABC9C
        )
        embed.set_footer(text="DataVerse — Explore. Learn. Collaborate.")
        await member.send(embed=embed)

        questions = [
            ("==================================\n👤 **Enter your full name** 👇\nIt will help you network with people of similar interests", "name"),
            ("📧 **Enter your email address!**\n You will receive the welcome kit on your email.\nPlease make sure your email Address is correct!", "email"),
            ("🧭 **Select which best describes you:**\nWe will be able to help you better when we know your role", "role"),
            ("💡 Select what you want to achieve on **DataVerse** (Pick Upto 3 choices):", "goal")
        ]

        answers = {}


        dm_channel = await member.create_dm()
        print(f"✅ DM Channel ID for {member.name}: {dm_channel.id}")

        def check(m):
            return m.author == member and isinstance(m.channel, discord.DMChannel)

        def check(m):
            return m.author == member and isinstance(m.channel, discord.DMChannel)

        for question, key in questions:
            if key == "role":
                # Special handling: show selection buttons
                await asyncio.sleep(.5)
                await member.send(question)
                view = RoleSelectionView()
                await member.send(view=view)

                # Wait until user clicks one button
                timeout = await view.wait()
                if view.value is None:
                    await timeout_logic(bot, member, intro_channel)
                answers[key] = view.value

            elif key == "goal":
                # Multiple selection for goals
                await asyncio.sleep(.5)
                view = GoalsSelectionView()
                await member.send(
                    question,
                    view=view
                )


                await view.wait()
                if view.value is None:
                    await timeout_logic(bot, member, intro_channel)
                    return
                answers[key] = view.value

            else:
                # Normal text-based question
                await asyncio.sleep(.5)
                await member.send(question)
                try:
                    msg = await bot.wait_for("message", timeout=180.0, check=check)
                    answers[key] = msg.content.strip()
                except asyncio.TimeoutError:
                    await asyncio.sleep(1)
                    await timeout_logic(bot, member, intro_channel)
                    return

        #Role Assigning
        await assign_role_to_member(bot, member, answers["role"])

        # Collect user info into a dictionary
        user_data = {
            "discord_id": str(member.id),
            "name": answers.get("name"),
            "email": answers.get("email"),
            "role": answers.get("role"),
            "goal": answers.get("goal")
        }

        # Save user details in JSON and Google Sheet
        save_user_data(user_data)

        # DM summary
        await member.send(f"✅ Thanks for sharing! Your introduction has been posted in **{intro_channel.mention}** 🎉")

        # Create embed for introductions channel
        summary_embed = discord.Embed(
            title=f"🌟 Meet {answers['name']}!",
            description=(
                f"🎓 **Role:** {answers['role']}\n"
                f"💡 **Goal:** {answers['goal']}\n"
                f"📧 **Email:** ||{answers['email']}|| (hidden for privacy)\n\n"
                f"Let's welcome {member.mention} to **DataVerse**! 🚀"
            ),
            color=0x1ABC9C
        )
        summary_embed.set_thumbnail(url=member.display_avatar.url)
        summary_embed.set_footer(text="DataVerse — Explore. Learn. Collaborate.")

        await intro_channel.send(embed=summary_embed)

    except discord.Forbidden:
        # If DMs are disabled
        await intro_channel.send(
            f"⚠️ {member.mention} has DMs disabled! Please answer your introduction questions here instead."
        )

async def timeout_logic(bot, member, intro_channel):
    await asyncio.sleep(1)

    timeout_embed = discord.Embed(
        title="⏰ Session Timed Out",
        description=(
            "It looks like you took a bit long to respond. No worries! 💫\n\n"
            "You can restart your onboarding anytime by clicking below 👇"
        ),
        color=0xED4245  # soft red
    )
    timeout_embed.set_footer(text="DataVerse — Onboarding Assistant")

    view = RestartOnboardingView(bot, member, intro_channel)
    await member.send(embed=timeout_embed, view=view)
