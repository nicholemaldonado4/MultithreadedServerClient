# Nichole Maldonado
# Houses utility functions used by the
# programs.

# Gets port
# Input: None
# Output: Positive port num if successful,
#         negative number otherwise.
def str_to_pos_int(str_val, str_type):
    try:
        # Tries to cast argv[1] to an int.
        num = int(str_val)
        if num < 0:
            print("Error: <%s> cannot be negative" % str_type)
        return num
    except:
        # If unsuccessful, stop everything and tell user.
        print("Error: <%s> must be an integer" % str_type)
        return -1