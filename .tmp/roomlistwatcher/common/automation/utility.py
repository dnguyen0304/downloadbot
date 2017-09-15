# -*- coding: utf-8 -*-

import selenium.common
from selenium.webdriver.support import expected_conditions


def find_button(wait_context, locator):

    """
    Look for the button specified by the locator.

    Parameters
    ----------
    wait_context : selenium.webdriver.support.ui.WebDriverWait
    locator : tuple
        Two-element tuple. The first element is the select strategy.
        The second element is the value.

    Returns
    -------
    selenium.webdriver.remote.webelement.WebElement
        If the button could be found. Otherwise None.
    """

    condition = expected_conditions.element_to_be_clickable(locator=locator)
    try:
        button = wait_context.until(condition)
    except selenium.common.exceptions.TimeoutException:
        button = None
    return button
