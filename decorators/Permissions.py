import tanjun


class Permissions(object):
    def __init__(self, rolesList):
        self.rolesList = rolesList
    def __call__(self, function):
        async def wrapper(*args, **kwds):
            ctx = args[0]
            if isinstance(ctx,tanjun.abc.SlashContext):
                hasPermission = False
                roles = ctx.member.get_roles()
                for role in roles:
                    if role.id in self.rolesList or ctx.member.id in self.rolesList:
                        hasPermission = True
                if hasPermission:
                    value = function(*args, **kwds)
                    return await value
                else:
                    await ctx.respond("You don't have permission to do this")
            else:
                print("Improper use of permissions decorator")
        return wrapper