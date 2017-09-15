# -*- coding: utf-8 -*-

import random
import string


def generate_sid():

    valid_characters = string.ascii_letters + string.digits
    sid = ''.join(random.SystemRandom().choice(valid_characters)
                  for _
                  in range(32))
    return sid
