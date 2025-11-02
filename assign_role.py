# assign_role.py
sys.modules["audioop"] = types.ModuleType("audioop")
import discord

async def assign_role_to_member(bot, member: discord.Member, role_name: str):
    """
    Assigns a role (Student, Professional, or Enthusiast) to the given member.
    If the role does not exist, logs a warning.
    """

    try:
        # Fetch the guild (server) object
        guild = member.guild

        # Try to find the role by name (case-insensitive)
        role = discord.utils.find(lambda r: r.name.lower() == role_name.lower(), guild.roles)

        if role is None:
            # Role not found — log and optionally create it
            print(f"⚠️ Role '{role_name}' not found in {guild.name}. Please create it manually.")
            await member.send(f"⚠️ The role **'{role_name}'** does not exist in the server. Please notify an admin.")
            return

        # Assign role
        await member.add_roles(role)
        print(f"✅ Assigned '{role.name}' role to {member.name} in {guild.name}.")
        await member.send(f"🎓 You’ve been assigned the **{role.name}** role in **{guild.name}**! 🚀")

    except discord.Forbidden:
        print(f"🚫 Missing permission to assign roles in {guild.name}.")
        await member.send("⚠️ I don’t have permission to assign roles. Please notify an admin.")
    except discord.HTTPException as e:
        print(f"❌ Failed to assign role '{role_name}' to {member.name}: {e}")
