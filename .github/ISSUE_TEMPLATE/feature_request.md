---
name: Feature request
about: Suggest an idea for this project
title: ''
labels: ''
assignees: ''

---

**Is your feature request related to a problem? Please describe.**  
A clear and concise description of what the problem is.

**Describe the solution you'd like**  
A clear and concise description of what you want to happen. Ideally, use Gherkin syntax.
Example:

```Gherkin
Feature: Run validation as an operator
  Let users run the validation by calling an operator.

  Rule: Calling the operator runs the validation
    Background:
      Given I have installed the validator

    Example: Operator call
      When I choose the the validator operator
      Then validation is executed
      And I get a report of the validation results

    Example: Change asset config in Redo panel
      Given I have called the validator operator
      When I change the config in the Redo panel
      Then validation is executed again with the new config
      And I get a report of the validation results
  ...
```

**Describe the impact**  
Gauge how much **impact** this feature would have for its users [e.g. how much time it will save].
What is its value?

**Describe alternatives you've considered**  
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**  
Add any other context or screenshots about the feature request here.
