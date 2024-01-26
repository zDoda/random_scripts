import pyfiglet


def ascii_art(name):
    ascii_name = pyfiglet.figlet_format(name, font='ogre')
    return ascii_name


# Replace 'YourName' with your actual name
print(ascii_art("Julia Hornung"))
# print(pyfiglet.FigletFont.getFonts())
