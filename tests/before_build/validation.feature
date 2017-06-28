Feature: Validating data
  Scenario: New event added _events
	Given an event added
	Then event files must exist
	Then all mandatory event fields must exist and be valid
