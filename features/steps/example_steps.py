from behave import *
from features.steps.utilities import *
from features.pages.example_page import ExamplePage


@given(u'browser is launched')
def step_impl(context):
    config = get_test_config()
    launch_browser(context, browser=config['browser'])
    init_web_pages(context, browser=config['browser'])


@step('open Portal')
def step_impl(context):
    context.pages.first_test = ExamplePage(context.driver.browser)
    data = get_data_for_first_test()
    context.pages.first_test.navigate_to_website(data['url'])


@step('Login page with inputs for password and login')
def step_impl(context):
    context.pages.audit_logs_channels = ExamplePage(context.driver.browser)
    context.pages.audit_logs_channels.click_audit_logs_icon()


@step('Enter {user} credentials')
def step_impl(context):
    context.pages.audit_logs_channels = ExamplePage(context.driver.browser)
    context.pages.audit_logs_channels.click_audit_logs_icon()


@step('Open main page')
def step_impl(context):
    context.pages.audit_logs_channels = ExamplePage(context.driver.browser)
    context.pages.audit_logs_channels.click_audit_logs_icon()