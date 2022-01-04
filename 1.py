#1:5000 축척지도에서 실제 거리 계산하기

print('1:5000 축척지도에서 실제 거리 계산하기')

map_length = int(input('지도 상에서의 거리를 입력하세요.: '))
length_in_reality = map_length * 5000

print('=' *15)
print('지도 상에서의 거리: ',map_length, 'cm')
print('실제 거리: ', length_in_reality, 'cm')
print('실제 거리: ', '%.2' 'f' %(length_in_reality/100), 'm')
print('실제 거리: ', '%.2f' %(length_in_reality/100000), 'km')
