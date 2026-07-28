previous_status = {}



# ==========================================================
# CHECK STATUS CHANGE
# ==========================================================

def check_status_change(
    user_id,
    status
):


    old_status = previous_status.get(
        user_id
    )



    previous_status[user_id] = status



    if old_status is None:

        return None



    if old_status != status:

        return status



    return None


