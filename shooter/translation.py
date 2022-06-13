"""Define objects for managing translations."""

import gettext
import os

path_to_locale = os.path.dirname(__file__) + "/locale/"
en = gettext.translation("shooter", path_to_locale, languages=["en"])
ru = gettext.translation("shooter", path_to_locale, languages=["ru"])
ru.install()
en.install()
tr = ru.gettext
