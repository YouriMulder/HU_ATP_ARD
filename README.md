# HU_ATP_ARD

## General
Programming language name:  **Youri**
Author:                     **Youri Mulder**

This programming language is called Youri. It is a programming language based on Spongebob case [spongebob meme](https://www.google.com/search?q=spongebob+mocking+meme&sxsrf=ALeKk01wwRb3FxAJ-eFPkkc8mbwIpe-exA:1588852253869&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjqx8Tx16HpAhVGnaQKHQIcCF0Q_AUoAXoECA0QAw&biw=1920&bih=948#imgrc=1CN5p3lhOrjvXM)

## Keywords
| Keyword | details          | Python equivalent |
|---------|------------------|-------------------|
| +       | Add              | +                 |
| -       | Reduce           | *                 |
| /       | Devide           | /                 |
| *       | Multiply         | *                 |
| iF      | Condition        | if                |
| WhIlE   | Loop             | while             |
| :==     | Equality         | ==                |
| :>=     | Greater or equal | >=                |
| :<=     | Less or equal    | <=                |
| :<      | Less             | <                 |
| :>      | Greater          | >                 |
| =       | Assignment       | =                 |
| ShOW    | Print to console | print             |
| !       | End of statement | enter / '\n'      |

## Syntax
The syntax of this programming language is based on the Spongebob meme. In addition to that is it required to place a whitespace after every keyword. In exception of the end of statement(!) Let's dive right into the code and show you some examples of how the programming language is structured.

### Identifier
Values can be stored in an identifier. The identifier must be cased in a special way. 
* The first character must always start with a capital character
* The following characters must be alternating in lower and upper case
* _ and 0-9 are also allowed after the first character
* After a _ or 0-9 should be a capital if there is a following character

:heavy_check_mark:  `CoUnTeR` <br>
:x:                 `coUnTeR` <br>
:x:                 `CounteR` <br>
:heavy_check_mark:  `ThIs_Is_11` <br>
:heavy_check_mark:  `I_11_I` <br>
:x:                 `1_1_2` <br>
:x:                 `13_ThIS_Is` <br>


### Assignments
To store data an assignment is necessary. An assignment is done using an identifier followed by `:=`. After the assignment operator the value which you want to store is placed. This could be an [expression](#expressions).

:heavy_check_mark:  `CoUnTeR     := 10!` <br>
:heavy_check_mark:  `ThIs_Is_11  := 11!` <br>
:x:                 `CoUnTeR        10!` <br>
:x:                 `ThIs_Is_11  := 11` <br>
:x:                 `ThIs_Is_11  :=11` <br>
:x:                 `ThIs_Is_11:= 11` <br>


### Expressions
Expressions are made terms and factors combined with mathematical operators. The mathematical order is applied when interpreting the expression.

:heavy_check_mark:  `DoUbLe     := CoUnTer + CoUnTer!` <br>
:heavy_check_mark:  `DoUbLe     := 1 * 2!` <br>
:heavy_check_mark:  `DoUbLe     := CoUnTer + CoUnTer!` <br>
:heavy_check_mark:  `SpOnGe  := 11 / 23 * 11 + 11 - 10101 + Id_1!` <br>
:x:                 `SpOnGe  := 11/23 * 11 + 11 - 10101 + Id_1!` <br>
:x:                 `SpOnGe  := 11 / 23 * 11 + 11 - + Id_1!` <br>
:x:                 `SpOnGe  := 11/23 * 11+11 - + Id_1!` <br>
:x:                 `CoUnTeR        10!` <br>
:x:                 `ThIs_Is_11  := ThIs_WaS_12 + 1` <br>

### Conditions
Conditions are if statements. The condition is written between parentheses (). The code block after the { is executed when the condition is valuated True. The code block must always end with a closing bracket.

:heavy_check_mark: 
``` 
iF ( FiB_TaRgEt :== 0 ) {
    ShOuLd_LoOp := 0!
}
```

:heavy_check_mark: 
``` 
iF ( BoOl :== Is_CoRrEct ) {
    Is_CoRrEct := 0!
}
```

:heavy_check_mark: 
``` 
iF ( BoOl :== Is_CoRrEct ) {
    Is_CoRrEct := 0!
    InCrEaSe_ThIs := InCrEaSe_ThIs + 1 / 2!
}
```

:heavy_check_mark: 
``` 
iF ( BoOl :== Is_CoRrEct ) { iF ( 10 := ThIS_iS_9 + 1 ) { ThIS_iS_9 := ThIS_iS_9 + 1 } }
```

:x: 
``` 
iF (BoOl:==Is_CoRrEct) {
    Is_CoRrEct := 0!
    InCrEaSe_ThIs := InCrEaSe_ThIs + 1 / 2!
}
```

:x: 
``` 
iF(BoOl :== Is_CoRrEct){
    Is_CoRrEct := 0!
    InCrEaSe_ThIs := InCrEaSe_ThIs + 1 / 2!
}
```

#### Loops
Loops are the same as conditions. Replace `iF` with `WhIlE` is the only thing required to create a loop instead of a condition. The loop is executed as long as the condition is True. The condition is evaluated before executing the body.
```diff
- Be careful for infinite loops!
```

### Console
Printing to the console is also supported. Printing to the console is done using `ShOw`. It is possible to print expression.


:heavy_check_mark:  
``` 
ShOw MyVaLuE!
```
:x: 
``` 
ShOwMyVaLuE
```

## How To Use
The [interpreter](https://github.com/YouriMulder/HU_ATP_ARD/tree/master/interpreter) is provided for the programming language. This contains the lexing, parsing and interpreting stages. Execute the main in the [interpreter folder](https://github.com/YouriMulder/HU_ATP_ARD/tree/master/interpreter) to execute the interpreter. In the [main](https://github.com/YouriMulder/HU_ATP_ARD/blob/master/interpreter/main.py) of the interpreter the location to the main file is provided to the interpreter `source_file_path = Path.source_main`. It is possible to either rename any file in the source folder to main.ym or change the `source_file_path` to the path of the `*.ym` file. <br>
For example `source_file_path = /home/youri/another_file.ym`<br>

The output of the interpreting stage is displayed in the console. The output should look as follows

```
Lexing
Parsing
Interpreting
interpreter: 0
interpreter: 0
interpreter: 0
interpreter: 0
{'In_0': 1, 'In_1': 0, 'In_2': 1, 'In_3': 0, 'CuRrEnT_In': 4, 'TaPe_EnD_ReAcHeD': 1, 'StAtE': 0, 'RaN_StAtE': 0, 'ReSeT': 1}
```

All the stages of interpreting are shown. The print statements are shown using `interpreter: x`.
After execution the final state of the program is printed to the console.


### Code samples
Code samples can be found [here](https://github.com/YouriMulder/HU_ATP_ARD/tree/master/source)
