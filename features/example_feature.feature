@first_test
Feature: Test Case for Portal

   Background: browser is launched and I navigated to Portal
     Given browser is launched
     When open Portal

   @a_test
   Scenario Outline: Login to Portal
     Given Login page with inputs for password and login
     When Enter <user> credentials
     Then Open main page
   Examples:
     |  user         |
     | admin         |
     | customer      |