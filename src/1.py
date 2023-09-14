a = [{'1':'2','2':'3'},{'32':'4', '33':'9'},{'42':'5', '43':'5'}]

text = '\n'
for i in a:
    for key, value in i.items(): 
        text += value
print(text)