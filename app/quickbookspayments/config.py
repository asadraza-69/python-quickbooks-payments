import importlib
import os

"""
/**
 * This is a file that required for using the files located in _Sample folders.
 * It is a SQL autoloader that performs the exact same function as composer "require "vendor/autoload.php";"
 * If you are using the _sample file. Remove the required include('../src/config.php'); line and add "require "vendor/autoload.php"" instead.

 *
 * @author Hao
 */
// PSR-4 Autoloader,QuickBooksOnline\Data;
"""


def autoload(class_name):
    prefix = 'QuickBooksOnline.Payments.'
    base_dir = os.path.dirname(__file__) + os.sep
    len_prefix = len(prefix)

    if not class_name.startswith(prefix):
        return

    relative_class = class_name[len_prefix:].replace('.', '/')
    file_without_extension = os.path.join(base_dir, relative_class)
    file = file_without_extension + '.py'

    # Below str.replace is for local testing. Remove it before putting on production.
    if os.path.exists(file):
        module_name = relative_class.replace('/', '.')
        importlib.import_module(module_name)

# Example usage:
# autoload('QuickBooksOnline.Payments.SomeModule')
