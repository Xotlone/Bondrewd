DEFAULT_COLOR = 0x2f3136

HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
}

ERROR_REMOVE = 60

SEGMENTED_HIRAGANA = [
	{
		'あ': 'а',
		'い': 'и',
		'う': 'у',
		'え': 'э',
		'お': 'о'
	},
	{
		'か': 'ка',
		'き': 'ки',
		'く': 'ку',
		'け': 'кэ',
		'こ': 'ко'
	},
	{
		'さ': 'са',
		'し': 'си',
		'す': 'су',
		'せ': 'сэ',
		'そ': 'со'
	},
	{
		'た': 'та',
		'ち': 'чи',
		'つ': 'цу',
		'て': 'тэ',
		'と': 'то'
	},
	{
		'な': 'на',
		'に': 'ни',
		'ぬ': 'ну',
		'ね': 'нэ',
		'の': 'но'
	},
	{
		'は': 'ха',
		'ひ': 'хи',
		'ふ': 'фу',
		'へ': 'хэ',
		'ほ': 'хо'
	},
	{
		'ま': 'ма',
		'み': 'ми',
		'む': 'му',
		'め': 'мэ',
		'も': 'мо'
	},
	{
		'や': 'я',
		'ゆ': 'ю',
		'よ': 'ё'
	},
	{
		'ら': 'ра',
		'り': 'ри',
		'る': 'ру',
		'れ': 'рэ',
		'ろ': 'ро',
	},
	{
		'わ': 'ва',
		'を': 'во',
	},
	{
		'ん': 'н'
	}
]

HIRAGANA = {}
for seg in SEGMENTED_HIRAGANA:
	for sym in seg.items():
		HIRAGANA[sym[0]] = sym[1]

LJ_CHOICES_COUNT = 8
CHOICE_DELAY = 60

ANIMEITEMSCOUNT = 4175858
ANIMELINK = 'https://safebooru.donmai.us/'
HENTAILINK = 'https://anitokyo.tv/hentai/'

owner_id = 0

connect_time = 0
command_time = 0
shutdown_time = 0