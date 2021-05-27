# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change. 

Please note we have a code of conduct, please follow it in all your interactions with the project.

# Contributing

1. Fork the repository.
2. Add your section - make sure you follow the styling guide below.
3. Commit changes.
4. Push your commit.
5. Create a Pull Request.

## Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a 
   build.
2. Update the README.md with details of changes to the interface, this includes new environment 
   variables, exposed ports, useful file locations and container parameters.
3. Increase the version numbers in any examples files and the README.md to the new version that this
   Pull Request would represent.
4. You may merge the Pull Request in once you have the sign-off of two other developers, or if you 
   do not have permission to do that, you may request the second reviewer to merge it for you.

## Styling

### PEP-8
```python
def foo(bar: int = 0) -> int:
   """
   This is the foo bar function ..
   :parameter: bar describes the following
   :return: the abs val of bar
   """
   return abs(bar)
```

#### Example TODO / DON'T:
```diff
! TODO add type hints (if nothing is returned use None)

+ def foo(bar: int) -> int:
+    """
+    This is the foo bar function ..
+    :param: bar describes the following
+    :return: the abs val of bar
+    """
+    return abs(bar)

! If you want to misuse a lambda function that's ok  (but with documentation)

+ """
+ This is the foo bar function ..
+ ...
+ """
+ foo = lambda bar: abs(bar)

! DON'T

- def foo(bar):
-     return abs(bar)

! TODO wherever possible don't use while, do while or recursion etc. loops instead use for loops
! However, if other loops are more readable, you can use them too (recursion etc.).

+ for _ in range(10):
+    print('moin')

! DON'T

- while i <= 10:
-    print('moin')
-    i += 1   
```
