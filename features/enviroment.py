from platform import python_version
from pprint import pprint
from features.utilities import *
from datetime import datetime as dt
from zipfile import ZipFile
import os
from os.path import basename


list_of_environments = ['dev', 'qa']


def before_all(context):
    """
    Prepare the test environment at a global level.
    """

    active_tags = [item for sub_list in context.config.tags.ands for item in sub_list]
    env = [tag for tag in active_tags if tag in list_of_environments]
    env = 'dev' if env.__len__() == 0 else env[0]
    env_file = 'environments/{}.yaml'.format(env)
    config_file = load_config_file_yaml(file_name=env_file)
    set_test_config(config_file)

    if config_file is not None:

        pprint(dict(config_file))

    setup_python_path()
    start_testing(context)


# def before_feature(context, feature):
#     context.feature_result = dict()
#
#
# def before_scenario(context):
#     pass
#
#
# def before_step(context):
#     pass


def after_step(context, step):
    import traceback

    if step.status == "failed":

        step_line = u"%s %s" % (step.keyword, step.name)
        message = "\n%s\n SUB-STEP: %s" % \
                  (step.status.name.upper(), step_line)
        message += u"\nTraceback (of failed substep):\n"
        message += u"".join(traceback.format_tb(step.exc_traceback))

    else:
        message = ""
    step.traceback = message
    context.traceback = message


def after_scenario(context, scenario):
    global non_connection_failure

    for step_for_scenario in scenario.all_steps:
        if step_for_scenario.status == 'failed':
            save_screenshot(context)
            non_connection_failure = True
            scenario.traceback = context.traceback

    scenario_dict = dict()
    scenario_dict["sc_sno"] = context.report_for_scenarios.__len__() + 1
    scenario_dict["scenario_name"] = scenario.feature.name + ' -> \n' + scenario.name
    scenario_dict["scenario_description"] = scenario.description
    scenario_dict["duration"] = scenario.duration
    scenario_dict["status"] = scenario.status.name.upper()
    scenario_dict["filename"] = scenario.filename
    scenario_dict["line"] = scenario.line
    temp_step = list()
    for st in scenario.steps:
        temp_str = st.status.name.upper() + ": " + st.step_type.upper() + " " + \
                   st.name
        if st.status.name == 'failed':
            temp_str = temp_str + "ERROR_LOG: " + st.traceback
        temp_step.append(temp_str)
    scenario_dict["scenario_step_and_status"] = temp_step
    # print("Scenario: <{}>".format(scenario_dict))
    context.report_for_scenarios.append(scenario_dict)
    context.driver.browser.quit()


def after_feature(context, feature):
    """
    "feature_name" : (dict)
        {
        name        :
        description :
        duration    :
        status      :
        filename    :
        }
    :param context:
    :param feature:
    :return:
    """

    feature_dict = dict()
    feature_dict["sc_sno"] = context.report_for_features.__len__() + 1
    feature_dict["feature_name"] = feature.name
    feature_dict["feature_description"] = feature.description
    feature_dict["duration"] = feature.duration
    feature_dict["status"] = feature.status.name.upper()
    feature_dict["feature_filename"] = feature.filename
    feature_dict["number_of_scenarios"] = len([sc for sc in feature.scenarios
                                               if sc.status.name in ['passed', 'failed']])
    # print("feature: <{}>".format(feature_dict))
    context.report_for_features.append(feature_dict)


# def after_all(context):
#     pass
