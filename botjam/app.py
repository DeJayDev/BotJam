import logging
from disco.bot import Plugin
from disco.types.permissions import Permissions


class JamPlugin(Plugin):

    log = logging.getLogger(__name__)

    @Plugin.listen('Ready')
    def on_ready(self, event):
        print('Connected to Discord API v{} as {}'.format(event.version, event.user))

    @Plugin.command('getmembers')
    def request_membesr(self, event):
        if not event.member.permissions.can(Permissions.MANAGE_GUILD):
            raise event.message.reply("You do not have permission to run this command.")
        
        self.client.gw.request_guild_members(event.guild.id, '', 0, False)

        return event.channel.send_message('{} users completely in this guild. Please verify before continuing?'.format(len(event.guild.members)))

    @Plugin.command('roleall', '<roleid:snowflake>')
    def on_og_command(self, event, roleid):
        if not event.member.permissions.can(Permissions.MANAGE_GUILD):
            raise event.message.reply("You do not have permission to run this command.")
        
        if roleid not in event.guild.roles:
            return event.channel.send_message('That role does not exist. Are you sure this is the right server?')

        if not event.guild.members[self.client.id].permissions.can(Permissions.MANAGE_ROLES):
            raise event.message.reply("You do not have permission to run this command.")

        amt = len(event.guild.members)
        ticker = 0
        
        for member in event.guild.members.values():
            member.add_role(roleid)
            ticker += 1
            self.log.info('Roled {}/{} users.'.format(ticker, amt))
            
        return event.channel.send_message('Task complete.')