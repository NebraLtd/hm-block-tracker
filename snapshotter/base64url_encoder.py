import sys
import re
import base64

# Parse 1st argument
byte_array = sys.argv[1]

# Strip <> characters
byte_array = re.sub('[<>]', '', byte_array)

# Convert string to array
byte_array = byte_array.split(",")


# Convert char array to int array
def char_to_int(num):
    return int(num)


byte_array = map(char_to_int, byte_array)

# Convert int array to byte array
byte_array = bytearray(list(byte_array))

# Enecode bytearray as base64url
base64_encoded = base64.urlsafe_b64encode(byte_array)

#  Remove b'' syntax from output
base64_encoded = base64_encoded.decode('utf-8')

# Remove trailing =, which serve as padding
base64_encoded = re.sub('[=]*$', '', base64_encoded)
print(base64_encoded)
