#-*- coding: utf-8 -*-

import os


class action:
	def __init__(self, vars):
		self.vars = vars
		self.logging = vars['logger']
		self.media_filter = vars['media_filter']
		self.subtitle_filter = vars['subtitle_filter']

		self.langs = {'aa': ['aar', 'aa', 'afar'], 'ab': ['abk', 'ab', 'abkhazian'], 'af': ['afr', 'af', 'afrikaans'], 'ak': ['aka', 'ak', 'akan'], 'am': ['amh', 'am', 'amharic'], 'an': ['arg', 'an', 'aragonese'], 'ar': ['ara', 'ar', 'arabic'], 'as': ['asm', 'as', 'assamese'], 'av': ['avar'], 'ay': ['aym', 'ay', 'aymara'], 'az': ['aze', 'az', 'azerbaijani'], 'ba': ['bak', 'ba', 'bashkir'], 'be': ['bel', 'be', 'belarusian'], 'bg': ['bul', 'bg', 'bulgarian'], 'bh': ['bihari'], 'bi': ['bis', 'bi', 'bislama'], 'bm': ['bam', 'bm', 'bambara'], 'bn': ['ben', 'bn', 'bengali'], 'bo': ['tib', 'bod', 'bo', 'tibetan'], 'br': ['bre', 'br', 'breton'], 'bs': ['bos', 'bs', 'bosnian'], 'ca': ['cat', 'ca', 'catalan'], 'ce': ['che', 'ce', 'chechen'], 'ch': ['cha', 'ch', 'chamorro'], 'co': ['cos', 'co', 'corsican'], 'cr': ['cre', 'cr', 'cree'], 'cs': ['cze', 'ces', 'cs', 'czech'], 'cu': ['old church slavonic / old bulgarian'], 'cv': ['chv', 'cv', 'chuvash'], 'cy': ['wel', 'cym', 'cy', 'welsh'], 'da': ['dan', 'da', 'danish'], 'de': ['ger', 'deu', 'de', 'german'], 'dv': ['divehi'], 'dz': ['dzo', 'dz', 'dzongkha'], 'ee': ['ewe', 'ee', 'ewe'], 'el': ['greek'], 'en': ['eng', 'en', 'english'], 'en-US': ['english united states'], 'en-GB': ['english great britain'], 'en-AU': ['english australian'], 'eo': ['epo', 'eo', 'esperanto'], 'es': ['spanish'], 'et': ['est', 'et', 'estonian'], 'eu': ['baq', 'eus', 'eu', 'basque'], 'fa': ['per', 'fas', 'fa', 'persian'], 'ff': ['peul'], 'fi': ['fin', 'fi', 'finnish'], 'fj': ['fij', 'fj', 'fijian'], 'fo': ['fao', 'fo', 'faroese'], 'fr': ['fre', 'fra', 'fr', 'french'], 'fy': ['west frisian'], 'ga': ['gle', 'ga', 'irish'], 'gd': ['scottish gaelic'], 'gl': ['glg', 'gl', 'galician'], 'gn': ['grn', 'gn', 'guarani'], 'gu': ['guj', 'gu', 'gujarati'], 'gv': ['glv', 'gv', 'manx'], 'ha': ['hau', 'ha', 'hausa'], 'he': ['heb', 'he', 'hebrew'], 'hi': ['hin', 'hi', 'hindi'], 'ho': ['hmo', 'ho', 'hiri motu'], 'hr': ['hrv', 'hr', 'croatian'], 'ht': ['hat', 'ht', 'haitian'], 'hu': ['hun', 'hu', 'hungarian'], 'hy': ['arm', 'hye', 'hy', 'armenian'], 'hz': ['her', 'hz', 'herero'], 'ia': ['interlingua'], 'id': ['ind', 'id', 'indonesian'], 'ie': ['ile', 'ie', 'interlingue'], 'ig': ['ibo', 'ig', 'igbo'], 'ii': ['sichuan yi'], 'ik': ['inupiak'], 'io': ['ido', 'io', 'ido'], 'is': ['ice', 'isl', 'is', 'icelandic'], 'it': ['ita', 'it', 'italian'], 'iu': ['iku', 'iu', 'inuktitut'], 'ja': ['jpn', 'ja', 'japanese'], 'jv': ['jav', 'jv', 'javanese'], 'ka': ['geo', 'kat', 'ka', 'georgian'], 'kg': ['kon', 'kg', 'kongo'], 'ki': ['kikuyu'], 'kj': ['kua', 'kj', 'kuanyama'], 'kk': ['kaz', 'kk', 'kazakh'], 'kl': ['kal', 'kl', 'greenlandic'], 'km': ['cambodian'], 'kn': ['kan', 'kn', 'kannada'], 'ko': ['kor', 'ko', 'korean'], 'kr': ['kau', 'kr', 'kanuri'], 'ks': ['kas', 'ks', 'kashmiri'], 'ku': ['kur', 'ku', 'kurdish'], 'kv': ['kom', 'kv', 'komi'], 'kw': ['cor', 'kw', 'cornish'], 'ky': ['kir', 'ky', 'kirghiz'], 'la': ['lat', 'la', 'latin'], 'lb': ['luxembourgish'], 'lg': ['lug', 'lg', 'ganda'], 'li': ['limburgian'], 'ln': ['lin', 'ln', 'lingala'], 'lo': ['laotian'], 'lt': ['lit', 'lt', 'lithuanian'], 'lu': ['lub', 'lu', 'luba-katanga'], 'lv': ['lav', 'lv', 'latvian'], 'mg': ['mlg', 'mg', 'malagasy'], 'mh': ['mah', 'mh', 'marshallese'], 'mi': ['mao', 'mri', 'mi', 'maori'], 'mk': ['mac', 'mkd', 'mk', 'macedonian'], 'ml': ['mal', 'ml', 'malayalam'], 'mn': ['mon', 'mn', 'mongolian'], 'mo': ['moldovan'], 'mr': ['mar', 'mr', 'marathi'], 'ms': ['may', 'msa', 'ms', 'malay'], 'mt': ['mlt', 'mt', 'maltese'], 'my': ['bur', 'mya', 'my', 'burmese'], 'na': ['nauruan'], 'nb': ['norwegian bokmål'], 'nd': ['north ndebele'], 'ne': ['nep', 'ne', 'nepali'], 'ng': ['ndo', 'ng', 'ndonga'], 'nl': ['dut', 'nld', 'nl', 'dutch'], 'nn': ['norwegian nynorsk'], 'no': ['nno', 'nn', 'nor', 'no', 'norwegian'], 'nr': ['south ndebele'], 'nv': ['navajo'], 'ny': ['chichewa'], 'oc': ['occitan'], 'oj': ['oji', 'oj', 'ojibwa'], 'om': ['orm', 'om', 'oromo'], 'or': ['ori', 'or', 'oriya'], 'os': ['ossetian / ossetic'], 'pa': ['panjabi / punjabi'], 'pi': ['pli', 'pi', 'pali'], 'pl': ['pol', 'pl', 'polish'], 'ps': ['pus', 'ps', 'pashto'], 'pt': ['por', 'pt', 'portuguese'], 'qu': ['que', 'qu', 'quechua'], 'rm': ['raeto romance'], 'rn': ['kirundi'], 'ro': ['romanian'], 'ru': ['rus', 'ru', 'russian'], 'rw': ['rwandi'], 'sa': ['san', 'sa', 'sanskrit'], 'sc': ['srd', 'sc', 'sardinian'], 'sd': ['snd', 'sd', 'sindhi'], 'se': ['sme', 'se', 'northern sami'], 'sg': ['sag', 'sg', 'sango'], 'sh': ['serbo-croatian'], 'si': ['sinhalese'], 'sk': ['slo', 'slk', 'sk', 'slovak'], 'sl': ['slv', 'sl', 'slovenian'], 'sm': ['smo', 'sm', 'samoan'], 'sn': ['sna', 'sn', 'shona'], 'so': ['somalia'], 'sq': ['alb', 'sqi', 'sq', 'albanian'], 'sr': ['srp', 'sr', 'serbian'], 'ss': ['ssw', 'ss', 'swati'], 'st': ['southern sotho'], 'su': ['sun', 'su', 'sundanese'], 'sv': ['swe', 'sv', 'swedish'], 'sw': ['swa', 'sw', 'swahili'], 'ta': ['tam', 'ta', 'tamil'], 'te': ['tel', 'te', 'telugu'], 'tg': ['tgk', 'tg', 'tajik'], 'th': ['tha', 'th', 'thai'], 'ti': ['tir', 'ti', 'tigrinya'], 'tk': ['tuk', 'tk', 'turkmen'], 'tl': ['tagalog / filipino'], 'tn': ['tsn', 'tn', 'tswana'], 'to': ['tonga'], 'tr': ['tur', 'tr', 'turkish'], 'ts': ['tso', 'ts', 'tsonga'], 'tt': ['tat', 'tt', 'tatar'], 'tw': ['twi', 'tw', 'twi'], 'ty': ['tah', 'ty', 'tahitian'], 'ug': ['uyghur'], 'uk': ['ukr', 'uk', 'ukrainian'], 'ur': ['urd', 'ur', 'urdu'], 'uz': ['uzb', 'uz', 'uzbek'], 've': ['ven', 've', 'venda'], 'vi': ['vie', 'vi', 'vietnamese'], 'vo': ['vol', 'vo', 'volapük'], 'wa': ['wln', 'wa', 'walloon'], 'wo': ['wol', 'wo', 'wolof'], 'xh': ['xho', 'xh', 'xhosa'], 'yi': ['yid', 'yi', 'yiddish'], 'yo': ['yor', 'yo', 'yoruba'], 'za': ['zhuang'], 'zh': ['chi', 'zho', 'zh', 'chinese'], 'zu': ['zul', 'zu', 'zulu'], 'ace': ['achinese'], 'ach': ['acoli'], 'ada': ['adangme'], 'ady': ['adygei'], 'afa': ['afro-asiatic languages'], 'afh': ['afrihili'], 'ain': ['ainu'], 'akk': ['akkadian'], 'ale': ['aleut'], 'alg': ['algonquian languages'], 'alt': ['southern altai'], 'ang': ['english old (ca.450-1100)'], 'anp': ['angika'], 'apa': ['apache languages'], 'arc': ['imperial aramaic (700-300 bce)'], 'arn': ['mapuche'], 'arp': ['arapaho'], 'art': ['artificial languages'], 'arw': ['arawak'], 'ast': ['asturian'], 'ath': ['athapascan languages'], 'aus': ['australian languages'], 'ava': ['av', 'avaric'], 'ave': ['ae', 'avestan'], 'awa': ['awadhi'], 'bad': ['banda languages'], 'bai': ['bamileke languages'], 'bal': ['baluchi'], 'ban': ['balinese'], 'bas': ['basa'], 'bat': ['baltic languages'], 'bej': ['bedawiyet'], 'bem': ['bemba'], 'ber': ['berber languages'], 'bho': ['bhojpuri'], 'bih': ['bh', 'bihari languages'], 'bik': ['bikol'], 'bin': ['bini'], 'bla': ['siksika'], 'bnt': ['bantu (other)'], 'bra': ['braj'], 'btk': ['batak languages'], 'bua': ['buriat'], 'bug': ['buginese'], 'byn': ['bilin'], 'cad': ['caddo'], 'cai': ['central american indian languages'], 'car': ['galibi carib'], 'cau': ['caucasian languages'], 'ceb': ['cebuano'], 'cel': ['celtic languages'], 'chb': ['chibcha'], 'chg': ['chagatai'], 'chk': ['chuukese'], 'chm': ['mari'], 'chn': ['chinook jargon'], 'cho': ['choctaw'], 'chp': ['chipewyan'], 'chr': ['cherokee'], 'chu': ['cu', 'church slavic'], 'chy': ['cheyenne'], 'cmc': ['chamic languages'], 'cop': ['coptic'], 'cpe': ['cpf', 'cpp', 'crp', 'creoles and pidgins'], 'crh': ['crimean tatar'], 'csb': ['kashubian'], 'cus': ['cushitic languages'], 'dak': ['dakota'], 'dar': ['dargwa'], 'day': ['land dayak languages'], 'del': ['delaware'], 'den': ['slave (athapascan)'], 'dgr': ['dogrib'], 'din': ['dinka'], 'div': ['dv', 'dhivehi'], 'doi': ['dogri'], 'dra': ['dravidian languages'], 'dsb': ['lower sorbian'], 'dua': ['duala'], 'dum': ['dutch middle (ca.1050-1350)'], 'dyu': ['dyula'], 'efi': ['efik'], 'egy': ['egyptian (ancient)'], 'eka': ['ekajuk'], 'elx': ['elamite'], 'enm': ['english middle (1100-1500)'], 'ewo': ['ewondo'], 'fan': ['fang'], 'fat': ['fanti'], 'fil': ['filipino'], 'fiu': ['finno-ugrian languages'], 'fon': ['fon'], 'frm': ['french middle (ca.1400-1600)'], 'fro': ['french old (842-ca.1400)'], 'frr': ['northern frisian'], 'frs': ['eastern frisian'], 'fry': ['fy', 'western frisian'], 'ful': ['ff', 'fulah'], 'fur': ['friulian'], 'gaa': ['ga'], 'gay': ['gayo'], 'gba': ['gbaya'], 'gem': ['germanic languages'], 'gez': ['geez'], 'gil': ['gilbertese'], 'gla': ['gd', 'gaelic'], 'gmh': ['german middle high (ca.1050-1500)'], 'goh': ['german old high (ca.750-1050)'], 'gon': ['gondi'], 'gor': ['gorontalo'], 'got': ['gothic'], 'grb': ['grebo'], 'grc': ['greek ancient (to 1453)'], 'gre': ['ell', 'el', 'greek modern (1453-)'], 'gsw': ['alemannic'], 'gwi': ["gwich'in"], 'hai': ['haida'], 'haw': ['hawaiian'], 'hil': ['hiligaynon'], 'him': ['himachali languages'], 'hit': ['hittite'], 'hmn': ['hmong'], 'hsb': ['upper sorbian'], 'hup': ['hupa'], 'iba': ['iban'], 'iii': ['ii', 'nuosu'], 'ijo': ['ijo languages'], 'ilo': ['iloko'], 'ina': ['ia', 'interlingua (international auxiliary language association)'], 'inc': ['indic languages'], 'ine': ['indo-european languages'], 'inh': ['ingush'], 'ipk': ['ik', 'inupiaq'], 'ira': ['iranian languages'], 'iro': ['iroquoian languages'], 'jbo': ['lojban'], 'jpr': ['judeo-persian'], 'jrb': ['judeo-arabic'], 'kaa': ['kara-kalpak'], 'kab': ['kabyle'], 'kac': ['jingpho'], 'kam': ['kamba'], 'kar': ['karen languages'], 'kaw': ['kawi'], 'kbd': ['kabardian'], 'kha': ['khasi'], 'khi': ['khoisan languages'], 'khm': ['km', 'central khmer'], 'kho': ['khotanese'], 'kik': ['ki', 'gikuyu'], 'kin': ['rw', 'kinyarwanda'], 'kmb': ['kimbundu'], 'kok': ['konkani'], 'kos': ['kosraean'], 'kpe': ['kpelle'], 'krc': ['karachay-balkar'], 'krl': ['karelian'], 'kro': ['kru languages'], 'kru': ['kurukh'], 'kum': ['kumyk'], 'kut': ['kutenai'], 'lad': ['ladino'], 'lah': ['lahnda'], 'lam': ['lamba'], 'lao': ['lo', 'lao'], 'lez': ['lezghian'], 'lim': ['li', 'limburgan'], 'lol': ['mongo'], 'loz': ['lozi'], 'ltz': ['lb', 'letzeburgesch'], 'lua': ['luba-lulua'], 'lui': ['luiseno'], 'lun': ['lunda'], 'luo': ['luo (kenya and tanzania)'], 'lus': ['lushai'], 'mad': ['madurese'], 'mag': ['magahi'], 'mai': ['maithili'], 'mak': ['makasar'], 'man': ['mandingo'], 'map': ['austronesian languages'], 'mas': ['masai'], 'mdf': ['moksha'], 'mdr': ['mandar'], 'men': ['mende'], 'mga': ['irish middle (900-1200)'], 'mic': ["mi'kmaq"], 'min': ['minangkabau'], 'mis': ['uncoded languages'], 'mkh': ['mon-khmer languages'], 'mnc': ['manchu'], 'mni': ['manipuri'], 'mno': ['manobo languages'], 'moh': ['mohawk'], 'mos': ['mossi'], 'mul': ['multiple languages'], 'mun': ['munda languages'], 'mus': ['creek'], 'mwl': ['mirandese'], 'mwr': ['marwari'], 'myn': ['mayan languages'], 'myv': ['erzya'], 'nah': ['nahuatl languages'], 'nai': ['north american indian languages'], 'nap': ['neapolitan'], 'nau': ['na', 'nauru'], 'nav': ['nv', 'navaho'], 'nbl': ['nr', 'nde', 'nd', 'ndebele'], 'nds': ['low'], 'new': ['nepal bhasa'], 'nia': ['nias'], 'nic': ['niger-kordofanian languages'], 'niu': ['niuean'], 'nob': ['nb', 'bokmål'], 'nog': ['nogai'], 'non': ['norse'], 'nqo': ["n'ko"], 'nso': ['northern sotho'], 'nub': ['nubian languages'], 'nwc': ['classical nepal bhasa'], 'nya': ['ny', 'chewa'], 'nym': ['nyamwezi'], 'nyn': ['nyankole'], 'nyo': ['nyoro'], 'nzi': ['nzima'], 'oci': ['oc', 'occitan (post 1500)'], 'osa': ['osage'], 'oss': ['os', 'ossetian'], 'ota': ['turkish ottoman (1500-1928)'], 'oto': ['otomian languages'], 'paa': ['papuan languages'], 'pag': ['pangasinan'], 'pal': ['pahlavi'], 'pam': ['kapampangan'], 'pan': ['pa', 'panjabi'], 'pap': ['papiamento'], 'pau': ['palauan'], 'peo': ['persian old (ca.600-400 b.c.)'], 'phi': ['philippine languages'], 'phn': ['phoenician'], 'pon': ['pohnpeian'], 'pra': ['prakrit languages'], 'pro': ['provençal old (to 1500)'], 'qaa-qtz': ['reserved for local use'], 'raj': ['rajasthani'], 'rap': ['rapanui'], 'rar': ['cook islands maori'], 'roa': ['romance languages'], 'roh': ['rm', 'romansh'], 'rom': ['romany'], 'rum': ['ron', 'ro', 'moldavian'], 'run': ['rn', 'rundi'], 'rup': ['aromanian'], 'sad': ['sandawe'], 'sah': ['yakut'], 'sai': ['south american indian (other)'], 'sal': ['salishan languages'], 'sam': ['samaritan aramaic'], 'sas': ['sasak'], 'sat': ['santali'], 'scn': ['sicilian'], 'sco': ['scots'], 'sel': ['selkup'], 'sem': ['semitic languages'], 'sga': ['irish old (to 900)'], 'sgn': ['sign languages'], 'shn': ['shan'], 'sid': ['sidamo'], 'sin': ['si', 'sinhala'], 'sio': ['siouan languages'], 'sit': ['sino-tibetan languages'], 'sla': ['slavic languages'], 'sma': ['southern sami'], 'smi': ['sami languages'], 'smj': ['lule sami'], 'smn': ['inari sami'], 'sms': ['skolt sami'], 'snk': ['soninke'], 'sog': ['sogdian'], 'som': ['so', 'somali'], 'son': ['songhai languages'], 'sot': ['st', 'sotho'], 'spa': ['es', 'castilian'], 'srn': ['sranan tongo'], 'srr': ['serer'], 'ssa': ['nilo-saharan languages'], 'suk': ['sukuma'], 'sus': ['susu'], 'sux': ['sumerian'], 'syc': ['classical syriac'], 'syr': ['syriac'], 'tai': ['tai languages'], 'tem': ['timne'], 'ter': ['tereno'], 'tet': ['tetum'], 'tgl': ['tl', 'tagalog'], 'tig': ['tigre'], 'tiv': ['tiv'], 'tkl': ['tokelau'], 'tlh': ['klingon'], 'tli': ['tlingit'], 'tmh': ['tamashek'], 'tog': ['tonga (nyasa)'], 'ton': ['to', 'tonga (tonga islands)'], 'tpi': ['tok pisin'], 'tsi': ['tsimshian'], 'tum': ['tumbuka'], 'tup': ['tupi languages'], 'tut': ['altaic languages'], 'tvl': ['tuvalu'], 'tyv': ['tuvinian'], 'udm': ['udmurt'], 'uga': ['ugaritic'], 'uig': ['ug', 'uighur'], 'umb': ['umbundu'], 'und': ['undetermined'], 'vai': ['vai'], 'vot': ['votic'], 'wak': ['wakashan languages'], 'wal': ['walamo'], 'war': ['waray'], 'was': ['washo'], 'wen': ['sorbian languages'], 'xal': ['kalmyk'], 'yao': ['yao'], 'yap': ['yapese'], 'ypk': ['yupik languages'], 'zap': ['zapotec'], 'zbl': ['bliss'], 'zen': ['zenaga'], 'zgh': ['standard moroccan tamazight'], 'zha': ['za', 'chuang'], 'znd': ['zande languages'], 'zun': ['zuni'], 'zxx': ['no linguistic content'], 'zza': ['dimili']}

	#General actions
	def plex_scan(self, func_name, files):
		"""
		title: 'plex_scan'
		trigger: acion.plex_scan
		requirements: requests
		action:
			Trigger a scan of the plex library/libraries the file(s) is/are in.
			This is a partial scan, so plex only scans the sub-folder with the media file in it,
				not the complete library.
			The plex library get's correctly updated but doesn't apply the load of a complete library scan,
				because of the partial scan that is triggered.
			That means that you can use this action without needing to worry about load on the plex server,
				and it takes a really short time to do because it only needs to scan the media sub-folder.
			This action is usefull to trigger at the end of the process,
				where file properties have probably changed (subtitles extracted, audio streams added, video transcoded, etc.)
		arguments:
			No arguments needed
		example:
			arguments: {}

			plex library updated
		action-specific variables:
			-	key:	plex_baseurl
				value:	str ('')
				use:	specify the base url of the plex server to connect to
				example: 'plex_baseurl': 'http://192.168.2.15:32400'
						this example will lead to all plex requests being send to this base url

			-	key:	plex_api_token
				value:	str ('')
				use:	specify the api token used for authenticating the requests to the plex server
				example: 'plex_api_token': 'abcdefghijklmnop'
						this example will lead to all plex requests being authenticated with this api token
		"""
		#check if action-specific vars are set
		if self.vars.get('plex_baseurl', '') == '':
			self.logging.error(f'{func_name} The action-specific variable "plex_baseurl" is not set')
			return 'ERROR'
		elif self.vars.get('plex_api_token', '') == '':
			self.logging.error(f'{func_name} The action-specific variable "plex_api_token" is not set')
			return 'ERROR'

		import requests
		result_scanned = False

		#get all plex libs (most importantly their folders and matching id's)
		try:
			plex_libs = requests.get(f'{self.vars["plex_baseurl"].rstrip("/")}/library/sections', params={'X-Plex-Token': self.vars["plex_api_token"]}, headers={'Accept': 'application/json'}).json()['MediaContainer']['Directory']
		except ConnectionError as e:
			self.logging.exception(f'{func_name} Failed to connect to plex server')
			return 'ERROR'

		paths = []
		for file in files:
			filepath = os.path.dirname(file)
			if not filepath in paths:
				#folder in which file lives has not been scanned yet
				#loop through the plex libraries
				for lib in plex_libs:
					#loop through the folders that are connected to the library
					for lib_folder in lib['Location']:
						lib_folder = lib_folder['path']
						#check if file is in this library
						if filepath.startswith(lib_folder):
							#library found in which file lives; refresh folder in it
							requests.get(f'{self.vars["plex_baseurl"].rstrip("/")}/library/sections/{lib["key"]}/refresh', params={'X-Plex-Token': self.vars["plex_api_token"], 'path': filepath})
							result_scanned = True
				paths.append(filepath)

		if result_scanned == True:
			self.logging.info(f'{func_name} Updated plex library')
		else:
			self.logging.info(f'{func_name} File not present in plex')

		return files
