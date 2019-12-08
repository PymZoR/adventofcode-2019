from collections import Counter

data = open('day8.data').read()
width = 25
height = 6
layer_size = width*height
layers_number = len(data) // layer_size

layers = [data[i*layer_size:(i+1)*layer_size] for i in range(layers_number)]
fewest_zero_layer = sorted(layers, key=lambda x: Counter(x).get('0'))[0]

layer_counter = Counter(fewest_zero_layer)
part1 = layer_counter.get('1') * layer_counter.get('2')
assert part1 == 1572

image = list(layers[0])
for layer in layers[1:]:
    for i, pixel in enumerate(layer):
        if pixel == '2' or image[i] != '2':
            continue
        image[i] = pixel

image = (''.join(image)).replace('0', ' ').replace('1', '█')
for row in range(height):
    print(image[row * width : (row+1) * width])
# KYHFE