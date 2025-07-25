# features/steps/web_steps.py
from behave import when, then

@when('I press the "{button_text}" button')
def step_click_button(context, button_text):
    button = context.browser.find_element_by_xpath(f'//button[text()="{button_text}"]')
    button.click()

@then('I should see "{text}" in the results')
def step_verify_text_present(context, text):
    assert text in context.browser.page_source

@then('I should not see "{text}" in the results')
def step_verify_text_absent(context, text):
    assert text not in context.browser.page_source

@then('I should see the message "{message_text}"')
def step_verify_message(context, message_text):
    assert message_text in context.browser.page_source
