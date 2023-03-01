from ..database.cosmo_db import users_container


def get_user_by_email_or_name(account_name: str, email: str) -> dict:
    """
    Returns the user data based on an email or account name.
    If you only have one of these values, set the other the same.

    :param account_name: The account name of the user
    :param email: The email of the user
    :return: A dictionary with the user's data
    """

    # When getting the user it will be possible to search with both name or email
    # So we can each by both at once, and works correctly

    query = """SELECT user.name, user.email, user.account_type, user.address , user.fiscal_code
                    FROM c user 
                    WHERE user.email = @email OR user.name = @name"""

    params = [dict(name="@email", value=email),
              dict(name="@name", value=account_name)]

    results = users_container.query_items(query=query,
                                          parameters=params,
                                          enable_cross_partition_query=True,
                                          max_item_count=1)

    items = list(results)

    if not items:
        return {}
    else:
        return items[0]
