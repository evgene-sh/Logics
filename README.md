# About
Фреймворк позволяет определять отношения вложенности на множестве многозначных логик

Для набора логик возможно получить результаты в виде 
* последовательности строк
* csv файла
* dot файла

# Usage
На вход – каталог с файлами mvlog 

На выходе – последовательность строк вида:

    <name of logic-1> and <name of logic-2> : relation

Входной каталог должен быть размещен в DATA_PATH

Выходные файлы будут сохраняться в RESULTS_PATH

### Interface 

    usage: main.py [-h] [-csv] [-dot] input
    
    positional arguments:
        input

    optional arguments:
        -h, --help  show this help message and exit
        -csv        if you need to generate csv file
        -dot        if you need to generate dot file
