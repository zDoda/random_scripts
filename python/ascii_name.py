import pyfiglet


def ascii_art(name):
    ascii_name = pyfiglet.figlet_format(name, font='small_slant')
    return ascii_name


# Replace 'YourName' with your actual name
print(ascii_art("Camdyn Zook"))
# print(pyfiglet.FigletFont.getFonts())
