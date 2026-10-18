import os

data = open('ChallangeLab2doc.enc', 'rb').read() 
pixels = data[54:] # skip the 54byte header
print('length:', len(data)) # total bytes in the file
os.makedirs('ChallangeLab2Images', exist_ok=True)
found = 0

for width in range(100, 2000): # modest file size can increase this range if needed 
    # each pixel is 3 bytes, and each row must be a multiple of 4 bytes
    row_size = width * 3
    if row_size % 4 != 0:
        row_size += 4 - (row_size % 4)

    height = len(pixels) // row_size
    if height * row_size != len(pixels): # only keep exact fits, no pixels left over. 
        continue

    # build the 54 byte bmp header
    header = bytearray(54)
    header[0:2] = b'BM'
    header[2:6] = (54 + len(pixels)).to_bytes(4,'little') # file size
    header[10:14] = (54).to_bytes(4,'little') # where pixels start
    header[14:18] = (40).to_bytes(4,'little') # info header size
    header[18:22] = width.to_bytes(4,'little')
    header[22:26] = height.to_bytes(4,'little')
    header[26:28] = (1).to_bytes(2,'little') # colour planes
    header[28:30] = (24).to_bytes(2,'little') # bits per pixel

    with open(f'ChallangeLab2Images/w{width}_h{height}.bmp', 'wb') as f:
        f.write(header + pixels)

    found += 1
    print(f'width {width}, height {height}')

print('done:', found, 'files created') # files created in the out2 folder 