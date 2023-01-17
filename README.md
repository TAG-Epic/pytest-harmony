# Pytest harmony
A library to make test trees.  

## What is test chains?
- Test 1 starts  
- Test 1 finishes, output goes to all depending tests  
  - Test 2 starts with output from test 1  
  - Test 2 finishes, output goes to all depending tests  
    - Test 3 starts  
    - Test 3 fails, depending tests gets skipped  
    - Test 3 cleanup gets called  
  - Test 2 cleanup gets called  
- Test 1 cleanup gets called  
