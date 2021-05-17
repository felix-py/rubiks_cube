# Rubik’s Cube Solver (Old Pochmann)

## Setup:
> ```bash
> pip3 install -r requirements.txt 
> ```

### EXAMPLE OF USE:
>#### Class Obj:
>```python
>my_cube = CubeObj(3, True)
>
>print(f'before:\n\n { str(my_cube) } \n\n')
>
># do some moves ...
>my_cube.translate("U F F' B D R2")
>
>print(f'afterwards:\n\n { str(my_cube) } \n\n')
>```

>#### Old Pochmann:
>```python
>scramble = input('Enter your scramble: ').upper().replace("'", "’").replace('(', '').replace('(', '')
>for char in scramble:
>    if char not in POSSIBLE_MOVES:
>        raise ValueError('Неизвестная манипуляция.')
>my_cool_cube = create_scrambled_cube(scramble)
>
>print(f'Scrambled Cube:\n\n { str(my_cool_cube) } \n')
>print(f'Solution:\n { solve_old_pochmann(my_cool_cube) } \n')
>print(f'Solved Cube:\n\n { str(my_cool_cube) } \n')
>```




