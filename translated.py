from deep_translator import GoogleTranslator
import time
import re

# pip install deep-translator (напишите в терминал)
def translate_comment(comment):
    try:
        return GoogleTranslator(source='en', target='ru').translate(comment)
    except Exception as e:
        print(f"Ошибка при переводе: {e}")
        return comment

def translate_line(line):

    if line.strip().startswith('//'):  # JavaScript-style комментарии
        return f"// {translate_comment(line.strip()[2:].strip())}\n"
    elif line.strip().startswith('#'):  # Python-style комментарии
        return f"# {translate_comment(line.strip()[1:].strip())}\n"
    elif re.match(r'^\s*/\*', line):  # C-style block comments
        return f"{translate_comment(line.strip())}\n"
    elif re.match(r'.*\*/\s*', line):  # C-style end of block comments
        return f"{translate_comment(line.strip())}\n"
    else:
        return line

def translate_file(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f_in:
            lines = f_in.readlines()
    except FileNotFoundError:
        print(f"Файл {input_file} не найден.")
        return
    except Exception as e:
        print(f"Ошибка при открытии файла: {e}")
        return

    translated_lines = []
    total_lines = len(lines)
    for index, line in enumerate(lines):
        translated_line = translate_line(line)
        translated_lines.append(translated_line)

        if index % 50 == 0:
            print(f"Переведено {index}/{total_lines} строк...")

        time.sleep(0.1)

    try:
        with open(output_file, 'w', encoding='utf-8') as f_out:
            f_out.writelines(translated_lines)
        print(f"Перевод завершен! Переведенные комментарии сохранены в {output_file}.")
    except Exception as e:
        print(f"Ошибка при записи в файл: {e}")

input_filename = 'text.txt'
output_filename = 'text1.txt'

translate_file(input_filename, output_filename)
