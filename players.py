import struct 

with open("Ken Griffey Jr's. Winning Run Baseball (U).smc",'rb') as f:
	data=f.read()



BASE_OFFSET=0x40200
CHUNK_LENGTH=36
NUM_PLAYERS=511


def decode_position(x):
	bats='Right'
	if x&0x80:
		bats='Both'
	if x&0x40:
		bats='Left'
	pos=x&0x3f
	positions={
		0:'Designated hitter',
		2:'1st Base',
		3:'2nd Base',
		4:'3rd Base',
		5:'Catcher',
		6:'Shortstop',
		7:'Center Field',
		8:'Left Field',
		9:'Right Field'
		}
	return '({} BATS={})'.format(bats,positions.get(pos,'{}?'.format(pos)))

def decode_nibbles(x):
	return (x>>4,x&0x0F)
def decode_bytes(x):
	return (x>>8,x&0xFF)
	
def decode_hit(x):
	return '(VS-L={} VS-R={})'.format(*decode_nibbles(x))

def decode_ps(x):
	return '(POWER={} SPEED={})'.format(*decode_nibbles(x))

def decode_af(x):
	return '(ARM={} FIELDING={})'.format(*(decode_nibbles(x)[::-1]))
TEAMS=[
	('Colorado Rockies',15),
	('Los Angeles Dodgers',15),
	('San Diego Padres',15),
	('San Francisco Giants',15),
	('Cincinnati Reds', 15),
	('Chicago Cubs',15),
	('Houston Astros',15),
	('Pittsburgh Pirates',15),
	('St. Louis Cardinals',15),
	('Atlanta Braves',15),
	('Florida Marlins',15),
	('Montreal Expos', 15),
	('New York Mets',15),
	('Philadelphia Phillies',15), #196
	('California Angels',15),#line211
	('Oakland Athletics',15),
	('Seattle Mariners',15),
	('Texas Rangers',15),
	('Chicago White Sox',15),
	('Cleveland Indians',15),
	('Kansas City Royals',15),
	('Milwaukee Brewers',15),
	('Minnesota Twins',15),
	('Baltimore Orioles',15),
	('Boston Red Sox',15),
	('Detroit Tigers',15),
	('New York Yankees',15),
	('Toronto Blue Jays',15),
	('NATIONAL',15),
	('AMERICAN',15),
	('Tampa Bay Devil Rays',15),
	('Arizona Diamondbacks',15),
	('Nintendo',15),
	('N64',15),
]
if 1:
	NAMES=('NAME POSITION G AB R H 2B 3B HR RBI BB SB HIT PS AF ? BA SA'+(' ?'*20)).split()
	BASE_OFFSET=0x40200

	CHUNK_LENGTH=0x24
	FORMATSTRING='<15sBBhBhBBBBBBBBBBhh'
	FORMATSTRING=FORMATSTRING+'{}B'.format((CHUNK_LENGTH-struct.calcsize(FORMATSTRING)))
	NUM_PLAYERS=511
	for i in range(NUM_PLAYERS):
		offset=BASE_OFFSET+CHUNK_LENGTH*i
		parts=list(struct.unpack(FORMATSTRING,data[offset:offset+CHUNK_LENGTH]))
		parts[0]=parts[0].split('\0')[0]
		outparts=[]
		for i,name in enumerate(NAMES):
			if i>=len(parts):
				break
			else:
				try:
					decoder = eval('decode_{}'.format(name.lower()))
				except (NameError,SyntaxError):
					decoder = lambda x:str(x)
				outparts.append('{}={}'.format(name,decoder(parts[i])))

		print ' '.join(outparts)

def decode_fraction(x):
	integer,decimal=decode_bytes(x)
	return '({}.{:02d})'.format(integer,decimal)

def decode_ip(x):
	return '({}.0)'.format(x)
decode_era=decode_br9=decode_so9=decode_fraction

def decode_convel(x):
	return '(Control={} Velocity={})'.format(*(decode_nibbles(x)[::-1]))

def decode_stamina(x):
	return '({})'.format(decode_nibbles(x)[0])

def decode_ft(x):
	return '(Fielding={} Throw={})'.format(*(decode_nibbles(x)))

def decode_special(x):
	specials={
			4:'Slider',
			5:'Super Curve',
			6:'Super Fast',
			7:'Change Up',
			8:'Ultra Curve',
			9: 'Knuckle Ball',
			10:'Screw Ball',
			15:'SL',
			16:'CV',
			17:'SF',
			18:'CU',
			19:'UC',
			20:'KN',
			21:'SC',
		}
	return '({})'.format(specials.get(x,'{}?'.format(x)))

def decode_w(x):
	wval=x&0x3f
	return '(W={} BATS={} THROWS={})'.format(wval,'Left' if x&0x80 else 'Right','Left' if x&0x40 else 'Right')

def decode_l(x):
	lval=x&0x7F
	return '(L={} POSITION={})'.format(lval,'Reliever' if x&0x80 else 'Starter')

def decode_h(x):
	hval=x&0x7F
	return '(H={} ?={})'.format(hval,'1' if x&0x80 else '0')

if 1:
	CHUNK_LENGTH=0x29
	NAMES=('NAME W L S ? IP ? H ER BB SO CONVEL STAMINA FT ? SPECIAL ERA BR9 SO9 LAST'+(' ?'*CHUNK_LENGTH)).split()
	BASE_OFFSET=0x449b8

	FORMATSTRING='<15sBBBBBBhhhhBBBBBHHHx'
	FORMATSTRING=FORMATSTRING+'{}B'.format((CHUNK_LENGTH-struct.calcsize(FORMATSTRING)))
	NUM_PLAYERS=340
	for i in range(NUM_PLAYERS):
		offset=BASE_OFFSET+CHUNK_LENGTH*i
		parts=list(struct.unpack(FORMATSTRING,data[offset:offset+CHUNK_LENGTH]))
		parts[0]=parts[0].split('\0')[0]
		outparts=[]
		for i,name in enumerate(NAMES):
			if i>=len(parts):
				break
			else:
				try:
					decoder = eval('decode_{}'.format(name.lower()))
				except (NameError,SyntaxError):
					decoder = lambda x:str(x)
				outparts.append('{}={}'.format(name,decoder(parts[i])))

		print ' '.join(outparts)

