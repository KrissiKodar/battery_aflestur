word = 21396;
# make word 16 bits long
word = word & 0xFFFF
#date = 20299;
# convert word to binary string
binary = bin(word)[2:].zfill(16)
# get year
year = int(binary[:7], 2) + 1980
# get month
month = int(binary[7:11], 2)
# get day
day = int(binary[11:], 2)

date_string = f'{day}.{month}.{year}'
print(f'date_string: {date_string}')