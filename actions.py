import os

class action:
	def __init__(self, vars):
		self.vars = vars
		self.logging = vars['logger']
		self.media_filter = vars['media_filter']
		self.subtitle_filter = vars['subtitle_filter']

		self.langs = {'aa': ['aar', 'aa', 'afar'], 'ab': ['abk', 'ab', 'abkhazian'], 'af': ['afr', 'af', 'afrikaans'], 'ak': ['aka', 'ak', 'akan'], 'am': ['amh', 'am', 'amharic'], 'an': ['arg', 'an', 'aragonese'], 'ar': ['ara', 'ar', 'arabic'], 'as': ['asm', 'as', 'assamese'], 'av': ['avar'], 'ay': ['aym', 'ay', 'aymara'], 'az': ['aze', 'az', 'azerbaijani'], 'ba': ['bak', 'ba', 'bashkir'], 'be': ['bel', 'be', 'belarusian'], 'bg': ['bul', 'bg', 'bulgarian'], 'bh': ['bihari'], 'bi': ['bis', 'bi', 'bislama'], 'bm': ['bam', 'bm', 'bambara'], 'bn': ['ben', 'bn', 'bengali'], 'bo': ['tib', 'bod', 'bo', 'tibetan'], 'br': ['bre', 'br', 'breton'], 'bs': ['bos', 'bs', 'bosnian'], 'ca': ['cat', 'ca', 'catalan'], 'ce': ['che', 'ce', 'chechen'], 'ch': ['cha', 'ch', 'chamorro'], 'co': ['cos', 'co', 'corsican'], 'cr': ['cre', 'cr', 'cree'], 'cs': ['cze', 'ces', 'cs', 'czech'], 'cu': ['old church slavonic / old bulgarian'], 'cv': ['chv', 'cv', 'chuvash'], 'cy': ['wel', 'cym', 'cy', 'welsh'], 'da': ['dan', 'da', 'danish'], 'de': ['ger', 'deu', 'de', 'german'], 'dv': ['divehi'], 'dz': ['dzo', 'dz', 'dzongkha'], 'ee': ['ewe', 'ee', 'ewe'], 'el': ['greek'], 'en': ['eng', 'en', 'english'], 'en-US': ['english united states'], 'en-GB': ['english great britain'], 'en-AU': ['english australian'], 'eo': ['epo', 'eo', 'esperanto'], 'es': ['spanish'], 'et': ['est', 'et', 'estonian'], 'eu': ['baq', 'eus', 'eu', 'basque'], 'fa': ['per', 'fas', 'fa', 'persian'], 'ff': ['peul'], 'fi': ['fin', 'fi', 'finnish'], 'fj': ['fij', 'fj', 'fijian'], 'fo': ['fao', 'fo', 'faroese'], 'fr': ['fre', 'fra', 'fr', 'french'], 'fy': ['west frisian'], 'ga': ['gle', 'ga', 'irish'], 'gd': ['scottish gaelic'], 'gl': ['glg', 'gl', 'galician'], 'gn': ['grn', 'gn', 'guarani'], 'gu': ['guj', 'gu', 'gujarati'], 'gv': ['glv', 'gv', 'manx'], 'ha': ['hau', 'ha', 'hausa'], 'he': ['heb', 'he', 'hebrew'], 'hi': ['hin', 'hi', 'hindi'], 'ho': ['hmo', 'ho', 'hiri motu'], 'hr': ['hrv', 'hr', 'croatian'], 'ht': ['hat', 'ht', 'haitian'], 'hu': ['hun', 'hu', 'hungarian'], 'hy': ['arm', 'hye', 'hy', 'armenian'], 'hz': ['her', 'hz', 'herero'], 'ia': ['interlingua'], 'id': ['ind', 'id', 'indonesian'], 'ie': ['ile', 'ie', 'interlingue'], 'ig': ['ibo', 'ig', 'igbo'], 'ii': ['sichuan yi'], 'ik': ['inupiak'], 'io': ['ido', 'io', 'ido'], 'is': ['ice', 'isl', 'is', 'icelandic'], 'it': ['ita', 'it', 'italian'], 'iu': ['iku', 'iu', 'inuktitut'], 'ja': ['jpn', 'ja', 'japanese'], 'jv': ['jav', 'jv', 'javanese'], 'ka': ['geo', 'kat', 'ka', 'georgian'], 'kg': ['kon', 'kg', 'kongo'], 'ki': ['kikuyu'], 'kj': ['kua', 'kj', 'kuanyama'], 'kk': ['kaz', 'kk', 'kazakh'], 'kl': ['kal', 'kl', 'greenlandic'], 'km': ['cambodian'], 'kn': ['kan', 'kn', 'kannada'], 'ko': ['kor', 'ko', 'korean'], 'kr': ['kau', 'kr', 'kanuri'], 'ks': ['kas', 'ks', 'kashmiri'], 'ku': ['kur', 'ku', 'kurdish'], 'kv': ['kom', 'kv', 'komi'], 'kw': ['cor', 'kw', 'cornish'], 'ky': ['kir', 'ky', 'kirghiz'], 'la': ['lat', 'la', 'latin'], 'lb': ['luxembourgish'], 'lg': ['lug', 'lg', 'ganda'], 'li': ['limburgian'], 'ln': ['lin', 'ln', 'lingala'], 'lo': ['laotian'], 'lt': ['lit', 'lt', 'lithuanian'], 'lu': ['lub', 'lu', 'luba-katanga'], 'lv': ['lav', 'lv', 'latvian'], 'mg': ['mlg', 'mg', 'malagasy'], 'mh': ['mah', 'mh', 'marshallese'], 'mi': ['mao', 'mri', 'mi', 'maori'], 'mk': ['mac', 'mkd', 'mk', 'macedonian'], 'ml': ['mal', 'ml', 'malayalam'], 'mn': ['mon', 'mn', 'mongolian'], 'mo': ['moldovan'], 'mr': ['mar', 'mr', 'marathi'], 'ms': ['may', 'msa', 'ms', 'malay'], 'mt': ['mlt', 'mt', 'maltese'], 'my': ['bur', 'mya', 'my', 'burmese'], 'na': ['nauruan'], 'nb': ['norwegian bokmål'], 'nd': ['north ndebele'], 'ne': ['nep', 'ne', 'nepali'], 'ng': ['ndo', 'ng', 'ndonga'], 'nl': ['dut', 'nld', 'nl', 'dutch'], 'nn': ['norwegian nynorsk'], 'no': ['nno', 'nn', 'nor', 'no', 'norwegian'], 'nr': ['south ndebele'], 'nv': ['navajo'], 'ny': ['chichewa'], 'oc': ['occitan'], 'oj': ['oji', 'oj', 'ojibwa'], 'om': ['orm', 'om', 'oromo'], 'or': ['ori', 'or', 'oriya'], 'os': ['ossetian / ossetic'], 'pa': ['panjabi / punjabi'], 'pi': ['pli', 'pi', 'pali'], 'pl': ['pol', 'pl', 'polish'], 'ps': ['pus', 'ps', 'pashto'], 'pt': ['por', 'pt', 'portuguese'], 'qu': ['que', 'qu', 'quechua'], 'rm': ['raeto romance'], 'rn': ['kirundi'], 'ro': ['romanian'], 'ru': ['rus', 'ru', 'russian'], 'rw': ['rwandi'], 'sa': ['san', 'sa', 'sanskrit'], 'sc': ['srd', 'sc', 'sardinian'], 'sd': ['snd', 'sd', 'sindhi'], 'se': ['sme', 'se', 'northern sami'], 'sg': ['sag', 'sg', 'sango'], 'sh': ['serbo-croatian'], 'si': ['sinhalese'], 'sk': ['slo', 'slk', 'sk', 'slovak'], 'sl': ['slv', 'sl', 'slovenian'], 'sm': ['smo', 'sm', 'samoan'], 'sn': ['sna', 'sn', 'shona'], 'so': ['somalia'], 'sq': ['alb', 'sqi', 'sq', 'albanian'], 'sr': ['srp', 'sr', 'serbian'], 'ss': ['ssw', 'ss', 'swati'], 'st': ['southern sotho'], 'su': ['sun', 'su', 'sundanese'], 'sv': ['swe', 'sv', 'swedish'], 'sw': ['swa', 'sw', 'swahili'], 'ta': ['tam', 'ta', 'tamil'], 'te': ['tel', 'te', 'telugu'], 'tg': ['tgk', 'tg', 'tajik'], 'th': ['tha', 'th', 'thai'], 'ti': ['tir', 'ti', 'tigrinya'], 'tk': ['tuk', 'tk', 'turkmen'], 'tl': ['tagalog / filipino'], 'tn': ['tsn', 'tn', 'tswana'], 'to': ['tonga'], 'tr': ['tur', 'tr', 'turkish'], 'ts': ['tso', 'ts', 'tsonga'], 'tt': ['tat', 'tt', 'tatar'], 'tw': ['twi', 'tw', 'twi'], 'ty': ['tah', 'ty', 'tahitian'], 'ug': ['uyghur'], 'uk': ['ukr', 'uk', 'ukrainian'], 'ur': ['urd', 'ur', 'urdu'], 'uz': ['uzb', 'uz', 'uzbek'], 've': ['ven', 've', 'venda'], 'vi': ['vie', 'vi', 'vietnamese'], 'vo': ['vol', 'vo', 'volapük'], 'wa': ['wln', 'wa', 'walloon'], 'wo': ['wol', 'wo', 'wolof'], 'xh': ['xho', 'xh', 'xhosa'], 'yi': ['yid', 'yi', 'yiddish'], 'yo': ['yor', 'yo', 'yoruba'], 'za': ['zhuang'], 'zh': ['chi', 'zho', 'zh', 'chinese'], 'zu': ['zul', 'zu', 'zulu'], 'ace': ['achinese'], 'ach': ['acoli'], 'ada': ['adangme'], 'ady': ['adygei'], 'afa': ['afro-asiatic languages'], 'afh': ['afrihili'], 'ain': ['ainu'], 'akk': ['akkadian'], 'ale': ['aleut'], 'alg': ['algonquian languages'], 'alt': ['southern altai'], 'ang': ['english old (ca.450-1100)'], 'anp': ['angika'], 'apa': ['apache languages'], 'arc': ['imperial aramaic (700-300 bce)'], 'arn': ['mapuche'], 'arp': ['arapaho'], 'art': ['artificial languages'], 'arw': ['arawak'], 'ast': ['asturian'], 'ath': ['athapascan languages'], 'aus': ['australian languages'], 'ava': ['av', 'avaric'], 'ave': ['ae', 'avestan'], 'awa': ['awadhi'], 'bad': ['banda languages'], 'bai': ['bamileke languages'], 'bal': ['baluchi'], 'ban': ['balinese'], 'bas': ['basa'], 'bat': ['baltic languages'], 'bej': ['bedawiyet'], 'bem': ['bemba'], 'ber': ['berber languages'], 'bho': ['bhojpuri'], 'bih': ['bh', 'bihari languages'], 'bik': ['bikol'], 'bin': ['bini'], 'bla': ['siksika'], 'bnt': ['bantu (other)'], 'bra': ['braj'], 'btk': ['batak languages'], 'bua': ['buriat'], 'bug': ['buginese'], 'byn': ['bilin'], 'cad': ['caddo'], 'cai': ['central american indian languages'], 'car': ['galibi carib'], 'cau': ['caucasian languages'], 'ceb': ['cebuano'], 'cel': ['celtic languages'], 'chb': ['chibcha'], 'chg': ['chagatai'], 'chk': ['chuukese'], 'chm': ['mari'], 'chn': ['chinook jargon'], 'cho': ['choctaw'], 'chp': ['chipewyan'], 'chr': ['cherokee'], 'chu': ['cu', 'church slavic'], 'chy': ['cheyenne'], 'cmc': ['chamic languages'], 'cop': ['coptic'], 'cpe': ['cpf', 'cpp', 'crp', 'creoles and pidgins'], 'crh': ['crimean tatar'], 'csb': ['kashubian'], 'cus': ['cushitic languages'], 'dak': ['dakota'], 'dar': ['dargwa'], 'day': ['land dayak languages'], 'del': ['delaware'], 'den': ['slave (athapascan)'], 'dgr': ['dogrib'], 'din': ['dinka'], 'div': ['dv', 'dhivehi'], 'doi': ['dogri'], 'dra': ['dravidian languages'], 'dsb': ['lower sorbian'], 'dua': ['duala'], 'dum': ['dutch middle (ca.1050-1350)'], 'dyu': ['dyula'], 'efi': ['efik'], 'egy': ['egyptian (ancient)'], 'eka': ['ekajuk'], 'elx': ['elamite'], 'enm': ['english middle (1100-1500)'], 'ewo': ['ewondo'], 'fan': ['fang'], 'fat': ['fanti'], 'fil': ['filipino'], 'fiu': ['finno-ugrian languages'], 'fon': ['fon'], 'frm': ['french middle (ca.1400-1600)'], 'fro': ['french old (842-ca.1400)'], 'frr': ['northern frisian'], 'frs': ['eastern frisian'], 'fry': ['fy', 'western frisian'], 'ful': ['ff', 'fulah'], 'fur': ['friulian'], 'gaa': ['ga'], 'gay': ['gayo'], 'gba': ['gbaya'], 'gem': ['germanic languages'], 'gez': ['geez'], 'gil': ['gilbertese'], 'gla': ['gd', 'gaelic'], 'gmh': ['german middle high (ca.1050-1500)'], 'goh': ['german old high (ca.750-1050)'], 'gon': ['gondi'], 'gor': ['gorontalo'], 'got': ['gothic'], 'grb': ['grebo'], 'grc': ['greek ancient (to 1453)'], 'gre': ['ell', 'el', 'greek modern (1453-)'], 'gsw': ['alemannic'], 'gwi': ["gwich'in"], 'hai': ['haida'], 'haw': ['hawaiian'], 'hil': ['hiligaynon'], 'him': ['himachali languages'], 'hit': ['hittite'], 'hmn': ['hmong'], 'hsb': ['upper sorbian'], 'hup': ['hupa'], 'iba': ['iban'], 'iii': ['ii', 'nuosu'], 'ijo': ['ijo languages'], 'ilo': ['iloko'], 'ina': ['ia', 'interlingua (international auxiliary language association)'], 'inc': ['indic languages'], 'ine': ['indo-european languages'], 'inh': ['ingush'], 'ipk': ['ik', 'inupiaq'], 'ira': ['iranian languages'], 'iro': ['iroquoian languages'], 'jbo': ['lojban'], 'jpr': ['judeo-persian'], 'jrb': ['judeo-arabic'], 'kaa': ['kara-kalpak'], 'kab': ['kabyle'], 'kac': ['jingpho'], 'kam': ['kamba'], 'kar': ['karen languages'], 'kaw': ['kawi'], 'kbd': ['kabardian'], 'kha': ['khasi'], 'khi': ['khoisan languages'], 'khm': ['km', 'central khmer'], 'kho': ['khotanese'], 'kik': ['ki', 'gikuyu'], 'kin': ['rw', 'kinyarwanda'], 'kmb': ['kimbundu'], 'kok': ['konkani'], 'kos': ['kosraean'], 'kpe': ['kpelle'], 'krc': ['karachay-balkar'], 'krl': ['karelian'], 'kro': ['kru languages'], 'kru': ['kurukh'], 'kum': ['kumyk'], 'kut': ['kutenai'], 'lad': ['ladino'], 'lah': ['lahnda'], 'lam': ['lamba'], 'lao': ['lo', 'lao'], 'lez': ['lezghian'], 'lim': ['li', 'limburgan'], 'lol': ['mongo'], 'loz': ['lozi'], 'ltz': ['lb', 'letzeburgesch'], 'lua': ['luba-lulua'], 'lui': ['luiseno'], 'lun': ['lunda'], 'luo': ['luo (kenya and tanzania)'], 'lus': ['lushai'], 'mad': ['madurese'], 'mag': ['magahi'], 'mai': ['maithili'], 'mak': ['makasar'], 'man': ['mandingo'], 'map': ['austronesian languages'], 'mas': ['masai'], 'mdf': ['moksha'], 'mdr': ['mandar'], 'men': ['mende'], 'mga': ['irish middle (900-1200)'], 'mic': ["mi'kmaq"], 'min': ['minangkabau'], 'mis': ['uncoded languages'], 'mkh': ['mon-khmer languages'], 'mnc': ['manchu'], 'mni': ['manipuri'], 'mno': ['manobo languages'], 'moh': ['mohawk'], 'mos': ['mossi'], 'mul': ['multiple languages'], 'mun': ['munda languages'], 'mus': ['creek'], 'mwl': ['mirandese'], 'mwr': ['marwari'], 'myn': ['mayan languages'], 'myv': ['erzya'], 'nah': ['nahuatl languages'], 'nai': ['north american indian languages'], 'nap': ['neapolitan'], 'nau': ['na', 'nauru'], 'nav': ['nv', 'navaho'], 'nbl': ['nr', 'nde', 'nd', 'ndebele'], 'nds': ['low'], 'new': ['nepal bhasa'], 'nia': ['nias'], 'nic': ['niger-kordofanian languages'], 'niu': ['niuean'], 'nob': ['nb', 'bokmål'], 'nog': ['nogai'], 'non': ['norse'], 'nqo': ["n'ko"], 'nso': ['northern sotho'], 'nub': ['nubian languages'], 'nwc': ['classical nepal bhasa'], 'nya': ['ny', 'chewa'], 'nym': ['nyamwezi'], 'nyn': ['nyankole'], 'nyo': ['nyoro'], 'nzi': ['nzima'], 'oci': ['oc', 'occitan (post 1500)'], 'osa': ['osage'], 'oss': ['os', 'ossetian'], 'ota': ['turkish ottoman (1500-1928)'], 'oto': ['otomian languages'], 'paa': ['papuan languages'], 'pag': ['pangasinan'], 'pal': ['pahlavi'], 'pam': ['kapampangan'], 'pan': ['pa', 'panjabi'], 'pap': ['papiamento'], 'pau': ['palauan'], 'peo': ['persian old (ca.600-400 b.c.)'], 'phi': ['philippine languages'], 'phn': ['phoenician'], 'pon': ['pohnpeian'], 'pra': ['prakrit languages'], 'pro': ['provençal old (to 1500)'], 'qaa-qtz': ['reserved for local use'], 'raj': ['rajasthani'], 'rap': ['rapanui'], 'rar': ['cook islands maori'], 'roa': ['romance languages'], 'roh': ['rm', 'romansh'], 'rom': ['romany'], 'rum': ['ron', 'ro', 'moldavian'], 'run': ['rn', 'rundi'], 'rup': ['aromanian'], 'sad': ['sandawe'], 'sah': ['yakut'], 'sai': ['south american indian (other)'], 'sal': ['salishan languages'], 'sam': ['samaritan aramaic'], 'sas': ['sasak'], 'sat': ['santali'], 'scn': ['sicilian'], 'sco': ['scots'], 'sel': ['selkup'], 'sem': ['semitic languages'], 'sga': ['irish old (to 900)'], 'sgn': ['sign languages'], 'shn': ['shan'], 'sid': ['sidamo'], 'sin': ['si', 'sinhala'], 'sio': ['siouan languages'], 'sit': ['sino-tibetan languages'], 'sla': ['slavic languages'], 'sma': ['southern sami'], 'smi': ['sami languages'], 'smj': ['lule sami'], 'smn': ['inari sami'], 'sms': ['skolt sami'], 'snk': ['soninke'], 'sog': ['sogdian'], 'som': ['so', 'somali'], 'son': ['songhai languages'], 'sot': ['st', 'sotho'], 'spa': ['es', 'castilian'], 'srn': ['sranan tongo'], 'srr': ['serer'], 'ssa': ['nilo-saharan languages'], 'suk': ['sukuma'], 'sus': ['susu'], 'sux': ['sumerian'], 'syc': ['classical syriac'], 'syr': ['syriac'], 'tai': ['tai languages'], 'tem': ['timne'], 'ter': ['tereno'], 'tet': ['tetum'], 'tgl': ['tl', 'tagalog'], 'tig': ['tigre'], 'tiv': ['tiv'], 'tkl': ['tokelau'], 'tlh': ['klingon'], 'tli': ['tlingit'], 'tmh': ['tamashek'], 'tog': ['tonga (nyasa)'], 'ton': ['to', 'tonga (tonga islands)'], 'tpi': ['tok pisin'], 'tsi': ['tsimshian'], 'tum': ['tumbuka'], 'tup': ['tupi languages'], 'tut': ['altaic languages'], 'tvl': ['tuvalu'], 'tyv': ['tuvinian'], 'udm': ['udmurt'], 'uga': ['ugaritic'], 'uig': ['ug', 'uighur'], 'umb': ['umbundu'], 'und': ['undetermined'], 'vai': ['vai'], 'vot': ['votic'], 'wak': ['wakashan languages'], 'wal': ['walamo'], 'war': ['waray'], 'was': ['washo'], 'wen': ['sorbian languages'], 'xal': ['kalmyk'], 'yao': ['yao'], 'yap': ['yapese'], 'ypk': ['yupik languages'], 'zap': ['zapotec'], 'zbl': ['bliss'], 'zen': ['zenaga'], 'zgh': ['standard moroccan tamazight'], 'zha': ['za', 'chuang'], 'znd': ['zande languages'], 'zun': ['zuni'], 'zxx': ['no linguistic content'], 'zza': ['dimili']}

	#Subtitle actions
	def sub_clone(self, func_name, files, target_versions: list, replace: bool=False):
		"""
		title: 'sub_clone'
		trigger: action.sub_clone
		requirements: none
		action:
			Make multiple versions of a subtitle with different extensions.
			It is okay if one of the target extensions is the extension of the given file.
			Newly created files will be added to the list of files.
			When a version already exists, it is NOT added to the list of files unless replace is set to True (as the file is then replaced = new file).
		arguments:
			-	key:	target_versions
				value:	list ([])
				use:	give list of file extensions to create a clone for
				example: ['.srt','ass']
						this example will create a .srt and .ass version of the given subtitle

			-	key:	replace
				value:	bool (True | False)
				use:	if a target_version already exists, replace it instead of skipping it (aka "force" a clone)
				example: True
						this example will replace any existing versions of the subtitle with the new clone
				note:	settings this to True is handy after something like sub_remove_ads,
							to ensure that the ad-removal is applied on already existing versions
		example:
			arguments: {
				'target_versions': ['srt','.ass'],
				'replace': True
			}

			sub.srt -> sub.srt + sub.ass
		"""
		import subprocess
		result_files = []

		for file in files:
			if file.endswith(self.subtitle_filter):
				new_files = []
				#get file without extension
				filename = os.path.splitext(file)[0]
				#loop through the target versions of the subtitle
				for extension in target_versions:
					#check if the subtitle with the target extension exists (or make it anyway if replace = True)
					if (not os.path.isfile(filename + '.' + extension.lstrip('.'))) or (replace == True and filename + '.' + extension.lstrip('.') != file):
						#subtitle with target extension doesn't exist so add it to list of versions to create
						new_files.append(filename + '.' + extension.lstrip('.'))
				if len(new_files) > 0:
					#create new subtitle versions
					with open(os.devnull, 'w') as log:
						comm = [
							self.vars['ffmpeg'], '-y',
							'-v','quiet',
							'-i', file
						] + new_files
						subprocess.run(comm, stdout=log, stderr=log)
					#add new files to list of processing files
					result_files += new_files
					#log new files
					for new_file in new_files:
						self.logging.info(f'{func_name} Created {new_file}')
		#log if not a single clone has been made
		if len(result_files) == 0:
			self.logging.info(f'{func_name} No clones made')

		files += result_files
		return files

	def sub_remove_ads(self, func_name, files):
		"""
		title: 'sub_remove_ads'
		trigger: action.sub_remove_ads
		requirements: chardet, pysrt
		action:
			Remove advertisements from a subtitle.
		arguments:
			No arguments needed
		example:
			arguments: {}

			sub.ass -> sub.ass (without ads)
		"""
		import subprocess, chardet, pysrt
		ad_list = ['nordvpn', 'a Card Shark AMERICASCARDROOM', 'OpenSubtitles', 'Advertise your product or brand here', 'Apóyanos y conviértete en miembro VIP Para', 'Addic7ed', 'argenteam', 'AllSubs', 'Created and Encoded by', 'correctedby', 'Entre a AmericasCardroom. com Hoy', 'Everyone is intimidated by a shark. Become', 'Juegue Poker en Línea por Dinero Real', 'OpenSubtitles', 'Open Subtitles', 'MKV Player', 'MKV player', 'Resyncfor', 'Resyncimproved', 'Ripped?By', 'Sigue "Community" en', 'Subtitlesby', 'Subt?tulospor', 'Support us and become VIP member', 'SubsTeam', 'subscene', 'Subtitulado por', 'subtitulamos', 'Synchronizedby', 'Sincronizado y corregido por', 'subdivx', 'SyncCorrected', 'Synccorrectionsby', 'sync and corrections by', 'Syncby', 'Unatraducci?nde', 'tvsubtitles', 'Unatraducci?nde', 'Tacho8']
		result_modified = False

		def ads_in_line(line):
			for ad in ad_list:
				if ad in line:
					return True
			return False

		for file in files:
			if file.endswith(self.subtitle_filter):
				#if file is not .srt: convert it to .srt. Later on: remove ads, convert back to original version
				if not file.endswith('.srt'):
					process_file = os.path.splitext(file)[0] + '.ad_removal.srt'
					with open(os.devnull, 'w') as log:
						comm = [
							self.vars['ffmpeg'], '-y',
							'-v','quiet',
							'-i', file,
							process_file
						]
						subprocess.run(comm, stdout=log, stderr=log)
				else:
					process_file = file

				#remove ads
				with open(process_file, 'rb') as f:
					encoding = chardet.detect(f.read())['encoding']
				if not encoding:
					encoding = 'utf-8'

				try:
					subs = pysrt.open(process_file, encoding=encoding)
					for i, line in enumerate(subs):
						if ads_in_line(line.text) == True:
							del subs[i]
							result_modified = True
					subs.save(process_file)
				except UnicodeDecodeError:
					self.logging.error(f'{func_name} Failed to decode subtitle: {process_file}')
					os.remove(process_file)
				except Exception as e:
					self.logging.exception(f'{func_name} Failed to process subtitle: {process_file}')
					os.remove(process_file)

				#convert converted subs back
				if process_file.endswith('.ad_removal.srt'):
					with open(os.devnull, 'w') as log:
						comm = [
							self.vars['ffmpeg'], '-y',
							'-v','quiet',
							'-i', process_file,
							file
						]
						subprocess.run(comm, stdout=log, stderr=log)
					os.remove(process_file)

		if result_modified == True:
			self.logging.info(f'{func_name} Ads removed')
		else:
			self.logging.info(f'{func_name} No ads found')

		return files

	#Media actions
	def media_extract_sub(self, func_name, files, extension: str='srt', language_tagging: bool=True, language_tags: list=[], exclude_versions: list=[], extract_unknown_language: bool=True):
		"""
		title: 'media_extract_sub'
		trigger: action.media_extract_sub
		requirements: none
		action:
			Extract subtitles from a media file into their own seperate files.
			The files are placed into the same folder as the media file.
			The files will have the same filename as the media file, but with subtitle-extensions.
		arguments:
			-	key: 	extension
				value:	str ('')
				use:	give the extension of the extracted subtitles
				example: '.ass'
						this example will lead to the extracted subtitles being .ass subtitles

			-	key:	language_tagging
				value:	bool (True | False)
				use:	allow the action to add the language code to the filename
				example: True
						this example will make subtitles follow the format of [name].[lang_code].[extension]
							instead of [name].[extension]
				note:	the language code is the two letter code of a language (e.g. English -> 'en')

			-	key:	language_tags
				value:	list ([])
				use:	only extract subtitles that have one of these languages
				example: ['en','nl']
						this example will lead to only english and dutch subtitles being extracted
				note:	there is a seperate argument for if no language is defined

			-	key:	exclude_versions
				value:	list with options: ['sdh','forced']
				use:	don't extract subtitles if they fall in one of these categories
				example: ['forced']
						this example will lead to no forced subtitle being extracted (regardless of language)

			-	key:	extract_unknown_language
				value:	bool (True | False)
				use:	extract the subtitles that don't have a language tagged
				example: True
						this example will lead to subtitles being extracted who don't have a language tagged to them
		example:
			arguments: {
				'extension': '.srt',
				'language_tagging': True,
				'language_tags': ['en','nl','it'],
				'exclude_versions': ['sdh','forced'],
				'extract_unknown_language': True
			}

			media.mkv -> media.mkv
					+ sub.en.srt	#english subtitle
					+ sub.nl.srt	#dutch subtitle
					+ sub.srt	#unknown language subtitle
							#there was no italian subtitle in the media file
							#the english sdh subtitle wasn't extracted
		"""
		extension = '.' + extension.lstrip('.')
		exclude_versions = [v.lstrip('.') for v in exclude_versions]
		for v in exclude_versions:
			if not v in ('sdh','forced'):
				self.logging.error(f'{func_name} The version "{v}" is not a valid value in the list')
				return 'ERROR'

		import subprocess, json
		result_files = []

		for file in files:
			if file.endswith(self.media_filter):
				#get info about the streams of the file
				comm = [
					self.vars['ffprobe'],
					'-print_format','json',
					'-show_format',
					'-show_streams',
					'-v','quiet',
					file
				]
				file_info = json.loads(subprocess.run(comm, capture_output=True, text=True).stdout)
				self.logging.debug(f'{func_name} File info')
				self.logging.debug(json.dumps(file_info, indent=4))
				filename = os.path.splitext(file)[0]

				#select the subtitle streams to extract
				stream_settings = []
				for stream in file_info['streams']:
					#only process subtitle streams
					if stream['codec_type'] == 'subtitle':
						#note down if subtitle is special version
						version = ''
						if stream['disposition']['hearing_impaired'] == 1 or ('tags' in stream.keys() and 'title' in stream['tags'].keys() and stream['tags']['title'].lower() in ('hearing impared','sdh')):
							#subtitle is hearing impaired version
							if 'sdh' in exclude_versions: continue
							version += '.sdh'
						if stream['disposition']['forced'] == 1 or ('tags' in stream.keys() and 'title' in stream['tags'].keys() and stream['tags']['title'].lower() == 'forced'):
							#subtitle is forced
							if 'forced' in exclude_versions: continue
							version += '.forced'

						index = str(stream['index'])
						if 'tags' in stream.keys() and 'language' in stream['tags'].keys() and language_tagging == True:
							#subtitle has a language tagged to it (and language tagging is allowed)
							if language_tags and stream['tags']['language'] != 'und':
								#check if language is allowed
								for lang in language_tags:
									if not lang in self.langs.keys(): continue
									if stream['tags']['language'].lower() in [lang] + self.langs[lang]:
										stream_settings += [
											'-map', f'0:{index}',
											filename + '.' + lang + version + extension
										]
										result_files.append(filename + '.' + lang + version + extension)
										break
								else:
									for code, langs in self.langs.items():
										if stream['tags']['language'].lower() in [code] + langs:
											#language is found but just not allowed
											break
									else:
										#language is not found
										if extract_unknown_language == True:
											stream_settings += [
												'-map', f'0:{index}',
												filename + version + extension
											]
											result_files.append(filename + version + extension)
							else:
								#settings allow every language
								stream_settings += [
									'-map', f'0:{index}',
									filename + version + extension
								]
								result_files.append(filename + version + extension)

						elif ('tags' in stream.keys() and 'language' in stream['tags'].keys() and language_tagging == False) \
						or ((not 'tags' in stream.keys() or not 'language' in stream['tags'].keys()) and extract_unknown_language == True):
							#subtitle has unknown language but extracting unknown language is allowed, or language tagging is disabled
							stream_settings += [
								'-map', f'0:{index}',
								filename + version + extension
							]
							result_files.append(filename + version + extension)
				#setup and run command
				comm = [
					self.vars['ffmpeg'], '-y',
					'-v','quiet',
					'-progress', '-',
					'-i', file
				] + stream_settings
				self.logging.debug(f'{func_name} Settings used for subtitle extraction')
				self.logging.debug(json.dumps(comm, indent=4))

				with open(os.devnull, 'w') as log:
					subprocess.run(comm, stdout=log, stderr=log)

		if len(result_files) > 0:
			for result_file in result_files:
				self.logging.info(f'{func_name} Created {result_file}')
			files += result_files
		else:
			self.logging.info(f'{func_name} No subtitles extracted')

		return files

	def media_transcode(self, func_name, files, container: str='mkv', video: dict={}, audio: dict={}, subtitle: dict={}, various: dict={}):
		"""
		title: 'media_transcode'
		trigger: action.media_transcode
		requirements: requests (only when 'keep_audio_originally_spoken_language' is set to True)
		action:
			Transcode a media file.
			The capabilities of the action are explained in the arguments section.
		arguments:
			-	key:	video
				value:	dict ({})
				use:	define video-stream specific arguments in this dictionary (see example)
				example: see example below
				note:	1. every sub-argument of this argument is documented below with one indent more
						2. every sub-argument is required to be given

				-	key:	keep_video
					value:	bool (True | False)
					use:	set to False to remove all video streams from the media file
					example: True
							this example will lead to certain (or all) video streams being kept in the transcoded file
				
				-	key:	video_codec
					value:	string with options: 
								'libx265'	#h265
								'libx264'	#h264
								'copy'		#copy current codec (aka don't change the codec)
					use:	define the target codec of the video streams inside the media file
					example: 'libx265'
							this example will lead to all video streams being transcoded into the h265 codec (when needed)
					note:	1. when the source video stream is already in the target codec, the codec is set to 'copy' (duh...)
							2. more codecs are supported out of the box, but these are 'verified' right now

			-	key:	audio
				value:	dict ({})
				use:	define audio-stream specific arguments in this dictionary (see example)
				example: see example below
				note:	1. every sub-argument of this argument is documented below with one indent more
						2. every sub-argument is required to be given

				-	key:	keep_audio
					value:	bool (True | False)
					use:	set to False to remove all audio streams from the media file
					example: True
							this example will lead to certain (or all) audio streams being kept in the transcoded file

				-	key:	keep_audio_commentary
					value:	bool (True | False)
					use:	set to False to remove all commentary audio tracks from the media file
					example: False
							this example will lead to all commentary audio tracks being removed from the media file
					note:	when this sub-argument is set to True, the commentary audio tracks are treated just like normal tracks are
				
				-	key:	keep_audio_unknown_language
					value:	bool (True | False)
					use:	set to False to remove any audio track that doesn't have a language tagged to it
					example: True
							this example will lead to all audio tracks with an unknown language to be kept in the transcoded file
					note:	when this sub-argument is set to True, the audio tracks with unknown language are treated just like normal tracks are
				
				-	key:	keep_audio_duplicates
					value:	bool (True | False)
					use:	set to False to remove any duplicate audio tracks (if there are two duplicate audio streams, only keep one)
					example: False
							this example will lead to all duplicate audio tracks being removed from the media file
					note:	if an audio stream is a duplicate is based on if the following matches: 
								channel layout (e.g. 5.1), codec (e.g. aac) and language (e.g. English)

				-	key:	keep_audio_language_tags
					value:	list ([])
					use:	only keep audio tracks that have one of these languages
					example: ['en','it']
							this example will lead to only english and italian audio tracks being kept
					note:	1. if you have 'keep_audio_unknown_language' set to True, audio tracks with unknown languages will also be kept
							2. if you have 'keep_audio_originally_spoken_language' set to True, audio tracks with the originally spoken language will also be kept

				-	key:	keep_audio_all_on_no_match_ex_com
					value:	bool (True | False)
					use:	set to True to keep all audio tracks (except commentary) when not a single audio track is saved
								e.g. keep_audio_language_tags: ['it'] but the file only has english audio tracks
					example: True
							this example will lead to all audio tracks, except commentary, being saved when no audio track is originally kept
				
				-	key:	keep_audio_all_on_no_match_in_com
					value:	bool (True | False)
					use:	this expands on 'keep_audio_all_on_no_match_ex_com', but here commentary tracks are also kept
					example: True
							this example will lead to all normal and commentary tracks being added when no audio track is originally kept
				
				-	key:	keep_audio_originally_spoken_language
					value:	bool (True | False)
					use:	find the originally spoken language of the media and safe audio tracks in that language too
					example: True
							this example will lead to Italian audio tracks being kept when the movie was originally spoken in Italian
					note:	this requires sonarr and radarr data to be set in the variables (see 'action-specific variables' section below)

				-	key:	keep_audio_originally_spoken_language_on_error
					value:	string with options:
								'exit'	#cancel the process when the originally spoken language of the media can't be found
								'ignore' #continue the process without keeping the originally spoken language (as it couldn't be found)
					use:	what should happen when the originally spoken language of the media can't be found (e.g. the media is not added in sonarr/radarr)
					example: 'ignore'
							this example will lead to the process continuing even though the originally spoken language couldn't be found 
								and won't be kept (unless it was already kept by 'keep_audio_language_tags')

				-	key:	audio_codec
					value:	dict ({})
					use:	define for every channel layout (e.g. 5.1) what the audio codec should be
							the key inside the dict is the channel layout and the value is the codec
							the options for the codec are:
								'libfdk_aac' 	#aac
								'copy'			#copy current codec (aka don't change the codec)
					example:
							'audio_codec': {
								'2.0': 'libfdk_aac',
								'5.0': 'copy',
								'5.1': 'copy',
								'6.1': 'copy',
								'7.1': 'copy'
							}
							this example will lead to all the stereo audio tracks being transcoded into aac
								but all the surround sound tracks being copied over (copying the codec instead of transcoding)
					note:	1. when the source audio stream is already in the target codec, the codec is set to 'copy' (duh...)
							2. more codecs are supported out of the box, but these are 'verified' right now

				-	key:	clone_audio
					value:	dict ({})
					use:	define for every channel layout (e.g. 5.1) if a clone of it should be made with a different channel layout
							the key inside the dict is the original channel layout and the value is a list of layouts that
								there should be a clone made for
							the clones will have the audio codec defined for their channel layout in 'audio_codec'
					example:
							'clone_audio': {
								'5.0': ['2.0'],
								'5.1': ['2.0'],
								'6.1': ['2.0'],
								'7.1': ['2.0']
							}
							this example will lead to all surround sound audio tracks having a stereo version also being made
					note:	when a clone isn't supported (the conversion from one layout to another), a warning will be logged and the clone will be skipped

			-	key:	subtitle
				value:	dict ({})
				use:	define subtitle-stream specific arguments in this dictionary (see example)
				example: see example below
				note:	1. every sub-argument of this argument is documented below with one indent more
						2. every sub-argument is required to be given
				
				-	key:	keep_subtitle
					value:	bool (True | False)
					use:	set to False to remove all subtitle streams from the media file
					example: True
							this example will lead to certain (or all) subtitle streams being kept in the transcoded file
				
				-	key:	keep_subtitle_language_tags
					value:	list ([])
					use:	only keep subtitle tracks that have one of these languages
					example: ['en','it']
							this example will lead to only english and italian subtitle tracks being kept

				-	key:	keep_subtitle_unknown_language
					value:	bool (True | False)
					use:	set to False to remove any subtitle track that doesn't have a language tagged to it
					example: True
							this example will lead to all subtitle tracks with an unknown language to be kept in the transcoded file
					note:	when this sub-argument is set to True, the subtitle tracks with unknown language are treated just like normal tracks are

				-	key:	exclude_versions
					value:	list with options: ['sdh','forced']
					use:	don't extract subtitles if they fall in one of these categories
					example: ['forced']
							this example will lead to no forced subtitle being extracted (regardless of language)

			-	key:	various
				value:	dict ({})
				use:	define various arguments in this dictionary (see example)
				example: see example below
				note:	1. every sub-argument of this argument is documented below with one indent more
						2. every sub-argument is required to be given

				-	key:	keep_metadata
					value:	bool (True | False)
					use:	set to False to remove all unnecessary metadata inside a file
					example: False
							this example will lead to all unnecessary metadata being removed from the file
					note:	language metadata is kept (so what language a stream is)

				-	key:	keep_poster
					value:	bool (True | False)
					use:	set to False to remove any integrated media posters
					example: False
							this example will lead to all integrated posters being removed from the file
		example:
			'arguments': {
				'video': {
					'keep_video': True,
					'video_codec': 'libx265'
				},
				'audio': {
					'keep_audio': True,
					'keep_audio_commentary': False,
					'keep_audio_unknown_language': True,
					'keep_audio_duplicates': False,
					'keep_audio_language_tags': ['en'],

					'keep_audio_all_on_no_match_ex_com': True,
					'keep_audio_all_on_no_match_in_com': True,

					'keep_audio_originally_spoken_language': True,
					'keep_audio_originally_spoken_language_on_error': 'ignore',

					'audio_codec': {
						'2.0': 'libfdk_aac',
						'5.0': 'libfdk_aac',
						'5.1': 'libfdk_aac',
						'6.1': 'libfdk_aac',
						'7.1': 'libfdk_aac'
					},
					'clone_audio': {
						'5.0': ['2.0'],
						'5.1': ['2.0'],
						'6.1': ['2.0'],
						'7.1': ['2.0']
					}
				},
				'subtitle': {
					'keep_subtitle': True,
					'keep_subtitle_language_tags': ['en','nl'],
					'keep_subtitle_unknown_language': True,
					'exclude_versions': ['sdh','forced']
				},
				'various': {
					'keep_metadata': False,
					'keep_poster': False
				}
			}

			Inside the media file:
				keep the video tracks and transcode them to x265 if they aren't already
				keep audio tracks,
					but not commentary
					or duplicates
					do keep audio tracks with unknown language
					also keep audio tracks that are english or the originally spoken language
					when the originally spoken language can't be found, just continue with only english tracks
					when no audio tracks match, add all except commentary
					when all tracks are commentary, add all tracks
					convert all audio tracks to AAC
					make a stereo version of every surround sound audio track
				keep subtitles,
					but only english, dutch or unknown language ones
					don't keep any sdh or forced subtitles (regardless of language)
				ditch metadata and posters
		action-specific variables:
			-	key:	transcode_bitrate_ratio_[video_codec]
				value:	float (n.n)
				use:	specificy the bitrate ratio between the source stream and the transcoded stream
				example: 'transcode_bitrate_ratio_libx265': 0.5
						this example will lead to stream transcoded to x265 having half the bitrate of the original stream
				note:	when no bitrate ratio is defined for a codec, a target bitrate will not be passed to ffmpeg
							and it will just become what it will become

			#only needed when 'keep_audio_originally_spoken_language' is set to True
			-	key:	sonarr_baseurl
				value:	str ('')
				use:	specify the base url of the sonarr server to connect to
				example: 'sonarr_baseurl': 'http://192.168.2.15:8989'
						this example will lead to all sonarr requests being send to this base url

			-	key:	sonarr_api_token
				value:	str ('')
				use:	specify the api token used for authenticating the requests to the sonarr server
				example: 'sonarr_api_token': 'abcdefghijklmnop'
						this example will lead to all sonarr requests being authenticated with this api token

			-	key:	radarr_baseurl
				value:	str ('')
				use:	specify the base url of the radarr server to connect to
				example: 'radarr_baseurl': 'http://192.168.2.15:7878'
						this example will lead to all radarr requests being send to this base url

			-	key:	radarr_api_token
				value:	str ('')
				use:	specify the api token used for authenticating the requests to the radarr server
				example: 'radarr_api_token': 'abcdefghijklmnop'
						this example will lead to all radarr requests being authenticated with this api token
		"""
		container = '.' + container.lstrip('.')

		from re import compile as re_compile
		from re import DOTALL as re_DOTALL
		from random import random
		import json, subprocess, threading, time
		#https://trac.ffmpeg.org/wiki/AudioChannelManipulation
		filters = {
			'5.0': {
				'2.0': 'pan=stereo|FL = 0.460186*FC + 0.650802*FL + 0.563611*BL + 0.325401*BR | FR = 0.460186*FC + 0.650802*FR + 0.563611*BR + 0.325401*BL'
			},
			'5.1': {
				'2.0': 'pan=stereo|FL<FL+0.707*FC+0.707*BL+0.5*LFE|FR<FR+0.707*FC+0.707*BR+0.5*LFE'
			},
			'6.1': {
				'2.0': 'pan=stereo|FL = 0.321953*FC + 0.455310*FL + 0.394310*SL + 0.227655*SR + 278819*BC + 0.321953*LFE | FR = 0.321953*FC + 0.455310*FR + 0.394310*SR + 0.227655*SL + 278819*BC + 0.321953*LFE'
			},
			'7.1': {
				'2.0': 'pan=stereo|FL = 0.274804*FC + 0.388631*FL + 0.336565*SL + 0.194316*SR + 0.336565*BL + 0.194316*BR + 0.274804*LFE | FR = 0.274804*FC + 0.388631*FR + 0.336565*SR + 0.194316*SL + 0.336565*BR + 0.194316*BL + 0.274804*LFE',
				'5.0': 'pan=5.1|FL=0.8*FL+0.2*LFE|FR=0.8*FR+0.2*LFE|FC=FC|BL=0.5*BL+0.5*SL|BR=0.5*BR+0.5*SR',
				'5.1': 'pan=5.1|FL=FL|FR=FR|FC=FC|LFE=LFE|BL=0.5*BL+0.5*SL|BR=0.5*BR+0.5*SR',
				'6.0': 'pan=6.0|FL=0.8*FL+0.2*LFE|FR=0.8*FR+0.2*LFE|FC=FC|SL=SL|SR=SR|BC=0.5*BL+0.5*BR',
				'6.1': 'pan=6.1|FL=FL|FR=FR|FC=FC|LFE=LFE|SL=SL|SR=SR|BC=0.5*BL+0.5*BR'
			}
		}

		def key_check(key: str, source: dict, type):
			if not key in source.keys():
				self.logging.error(f'{func_name} The option "{key}" is not defined')
				return False
			if not isinstance(source[key], type):
				self.logging.error(f'{func_name} The option "{key}" has an invalid value (should be a {type.__name__})')
				return False
			return True

		def og_audio_error():
			if audio['keep_audio_originally_spoken_language_on_error'] == 'exit':
				self.logging.error(f'{func_name} The originally spoken language of the media could not be found')
				return 'exit'
			else:
				self.logging.warning(f'{func_name} The originally spoken language of the media could not be found; ignoring')
				return None

		def transcode_thread(comm, log_file):
			with open(log_file, 'w') as log:
				with open(os.devnull, 'w') as err:
					subprocess.run(comm, stdout=log, stderr=err)

		for file in files:
			if file.endswith(self.media_filter):
				#check if file is actually media file
				if os.path.getsize(file) < 1000:
					self.logging.error(f'{func_name} The media file is empty')
					return 'ERROR', file

				#first create lists of what is allowed to be copied over to new file

				#audio
				audio_keep = []
				if key_check('keep_audio', audio, bool) == False: return 'ERROR', file
				if audio['keep_audio'] == False:
					#don't keep audio
					pass
				else:
					#certain audio tracks need to be kept
					if key_check('keep_audio_commentary', audio, bool) == False: return 'ERROR', file
					if key_check('keep_audio_unknown_language', audio, bool) == False: return 'ERROR', file
					if key_check('keep_audio_all_on_no_match_ex_com', audio, bool) == False: return 'ERROR', file
					if key_check('keep_audio_all_on_no_match_in_com', audio, bool) == False: return 'ERROR', file

					if key_check('keep_audio_language_tags', audio, list) == False: return 'ERROR', file
					for tag in audio['keep_audio_language_tags']:
						if not tag in self.langs.keys():
							self.logging.error(f'{func_name} Unknown language given in "keep_audio_language_tags": {tag}')
							return 'ERROR', file
						else:
							audio_keep += self.langs[tag] + [tag]

					if key_check('keep_audio_originally_spoken_language', audio, bool) == False: return 'ERROR', file
					if audio['keep_audio_originally_spoken_language'] == True:
						#find originally spoken language of media using sonarr/radarr
						import requests

						if self.vars.get('sonarr_baseurl','') == '':
							self.logging.error(f'{func_name} The action-specific variable "sonarr_baseurl" is not set (for "keep_audio_originally_spoken_language" option)')
							return 'ERROR', file
						elif self.vars.get('sonarr_api_token','') == '':
							self.logging.error(f'{func_name} The action-specific variable "sonarr_api_token" is not set (for "keep_audio_originally_spoken_language" option)')
							return 'ERROR', file
						elif self.vars.get('radarr_baseurl','') == '':
							self.logging.error(f'{func_name} The action-specific variable "radarr_baseurl" is not set (for "keep_audio_originally_spoken_language" option)')
							return 'ERROR', file
						elif self.vars.get('radarr_api_token','') == '':
							self.logging.error(f'{func_name} The action-specific variable "radarr_api_token" is not set (for "keep_audio_originally_spoken_language" option)')
							return 'ERROR', file
						elif key_check('keep_audio_originally_spoken_language_on_error', audio, str) == False: return 'ERROR', file
						elif not audio['keep_audio_originally_spoken_language_on_error'] in ('exit','ignore'):
							self.logging.error(f'{func_name} The argument "keep_audio_originally_spoken_language_on_error" does not have a valid value ("exit" or "ignore")')
							return 'ERROR', file

						#first try to find the file in sonarr
						try:
							og_found = False
							sonarr_search = requests.get(f'{self.vars["sonarr_baseurl"]}/api/v3/parse', params={'path': file, 'apikey': self.vars['sonarr_api_token']}).json()
							if 'series' in sonarr_search.keys() and sonarr_search['series']['path'] in file:
								#file found in sonarr
								og_found = True
								r = re_compile(r'(?<=<strong>Original Language</strong>\r\n                    <span>).*?(?=</span>)')
								t = requests.get(f'https://thetvdb.com/dereferrer/series/{sonarr_search["series"]["tvdbId"]}').text

							else:
								#not found in sonarr; try to find file in radarr
								radarr_search = requests.get(f'{self.vars["radarr_baseurl"]}/api/v3/movie', params={'apikey': self.vars["radarr_api_token"]}).json()
								radarr_search = [m for m in radarr_search if m['path'] in file]
								if radarr_search:
									#file found in radarr
									og_found = True
									r = re_compile(r'(?<=Original Language</bdi></strong> ).*?(?=(?:</p>|;))')
									t = requests.get(f'https://www.themoviedb.org/movie/{radarr_search[0]["tmdbId"]}', headers={'User-Agent':'Transcodarr'}).text
								else:
									#file not found in any *arr
									if og_audio_error() == 'exit': return 'ERROR', file

							if og_found == True:
								#search for spoken language and convert to lang code
								og_lang = r.search(t)
								if og_lang == None:
									#spoken language could not be found
									if og_audio_error() == 'exit': return 'ERROR', file
								else:
									og_lang = og_lang.group(0)
									for lang_code, lang in self.langs.items():
										if og_lang.lower() in lang:
											#spoken language found, recognized, converted and added; successful
											audio_keep += [lang_code] + lang
											break
									else:
										#spoken language was found but could not be converted (e.g. failed to do "English" -> "en")
										self.logging.error(f'{func_name} The language "{og_lang}" was not recognized')
										if og_audio_error() == 'exit': return 'ERROR', file

						except ConnectionError as e:
							self.logging.exception(f'{func_name} Failed to connect to sonarr')

				#subtitle
				subtitle_keep = []
				if key_check('keep_subtitle', subtitle, bool) == False: return 'ERROR', file
				if subtitle['keep_subtitle'] == False:
					#don't keep any subtitles (might be because user did 'media_extract_sub' before this action)
					pass
				else:
					#certain subtitle tracks need to be kept
					if key_check('keep_subtitle_unknown_language', subtitle, bool) == False: return 'ERROR', file

					if key_check('keep_subtitle_language_tags', subtitle, list) == False: return 'ERROR', file
					for tag in subtitle['keep_subtitle_language_tags']:
						if not tag in self.langs.keys():
							self.logging.error(f'{func_name} Unknown language given in "keep_subtitle_language_tags": {tag}')
							return 'ERROR', file
						else:
							subtitle_keep += self.langs[tag] + [tag]

					if key_check('exclude_versions', subtitle, list) == False: return 'ERROR', file
					for version in subtitle['exclude_versions']:
						if not version in ('sdh','forced'):
							self.logging.error(f'{func_name} Unknown subtitle version given in "exclude_versions": {version}')
							return 'ERROR', file

				#check if other options are present and if they have valid values

				if key_check('keep_video', video, bool) == False: return 'ERROR', file
				if video['keep_video'] == True:
					if key_check('video_codec', video, str) == False: return 'ERROR', file
					if not video['video_codec'] in ('libx265','libx264','copy'):
						self.logging.error(f'{func_name} The argument "video_codec" does not have a valid value ("libx265","libx264" or "copy")')
						return 'ERROR', file

				if audio['keep_audio'] == True:
					if key_check('audio_codec', audio, dict) == False: return 'ERROR', file
					for channels, codec in audio['audio_codec'].items():
						if not codec in ('libfdk_aac', 'copy'):
							self.logging.error(f'{func_name} The argument "audio_codec" -> "{channels}" does not have a valid value ("libfdk_aac","copy")')
							return 'ERROR', file
					if key_check('clone_audio', audio, dict) == False: return 'ERROR', file
					r = re_compile(r'^(?:[0-9]{1,2}(?:\.|,)){1,2}[0-9]{1,2}$')
					for channels, clones in audio['clone_audio'].items():
						if key_check(channels, audio['clone_audio'], list) == False: return 'ERROR', file
						for clone in clones:
							if not isinstance(clone, str):
								self.logging.error(f'{func_name} The argument "clone_audio" -> "{channels}" contains an invalid value (should be a str)')
							if r.search(clone) == None:
								self.logging.error(f'{func_name} The argument "clone_audio" -> "{channels}" contains an invalid channel layout: {clone}')
								return 'ERROR', file

				if key_check('keep_metadata', various, bool) == False: return 'ERROR', file
				if key_check('keep_poster', various, bool) == False: return 'ERROR', file

				#get media file info and calc target values

				comm = [
					self.vars['ffprobe'],
					'-print_format', 'json',
					'-show_format',
					'-show_streams',
					'-v','quiet',
					file
				]
				file_info = json.loads(subprocess.run(comm, capture_output=True, text=True).stdout)
				self.logging.debug(f'{func_name} File info extracted')
				self.logging.debug(file_info)
				codec_bitrate_ratio = self.vars.get(f'transcode_bitrate_ratio_{video["video_codec"]}', '')
				if codec_bitrate_ratio != '' and not isinstance(codec_bitrate_ratio, float):
					self.logging.error(f'{func_name} The action-specific variable "transcode_bitrate_ratio_{video["video_codec"]}" has an invalid value (type should be float)')
				if codec_bitrate_ratio != '':
					#bitrate ratio is defined for this video codec
					bitrate = int(int(file_info['format']['bit_rate']) * codec_bitrate_ratio)
					self.logging.debug(f'{func_name} Target bitrate: {bitrate}')
				else:
					bitrate = ''
				self.logging.info(f'{func_name} Current media file size: {int(file_info["format"]["size"]) // (1024 * 1024)} MiB')

				#setup the ffmpeg settings (aka selecting streams and setting values based on the settings)

				self.logging.info(f'{func_name} Setting up transcode')
				stream_settings = []
				video_index = 0
				video_added = False
				audio_index = 0
				audio_added = False
				audio_log = [] #used for finding duplicate audio streams
				#file metadata
				if various['keep_metadata'] == False:
					if 'tags' in file_info['format'].keys():
						for tag in file_info['format']['tags'].keys():
							stream_settings += ['-metadata', f'{tag}=']
				#loop through every stream in the file and decide if it should be kept based on settings
				for stream in file_info['streams']:
					index = str(stream['index'])
					self.logging.debug(f'{func_name} The current stream settings')
					self.logging.debug(json.dumps(stream_settings, indent=4))
					self.logging.debug(f'{func_name} The stream that will be processed')
					self.logging.debug(json.dumps(stream, indent=4))

					if stream['codec_type'] == 'video' and \
					(stream['disposition']['attached_pic'] == 1 or stream['display_aspect_ratio'] == '2:3'):
						#stream is a attached poster
						if various['keep_poster'] == True:
							#settings say to keep poster
							stream_settings += [
								'-map', f'0:{index}',
								f'-codec:v:{video_index}', 'copy'
							]
							if various['keep_metadata'] == False:
								#remove metadata from poster
								if 'tags' in stream.keys():
									for tag in stream['tags'].keys():
										stream_settings += [f'-metadata:v:{video_index}', f'{tag}=']
							video_index += 1

					elif stream['codec_type'] == 'video':
						#stream is a video
						if video['keep_video'] == True:
							#settings say to keep video
							stream_settings += ['-map', f'0:{index}']
							video_added = True
							#set codec of video
							if video['video_codec'] == 'copy' \
							or (video['video_codec'] == 'libx265' and stream['codec_name'] == 'hevc') \
							or (video['video_codec'] == 'libx264' and stream['codec_name'] == 'h264'):
								#copy codec because settings say so or because video codec is already target codec
								stream_settings += [f'-codec:v:{video_index}', 'copy']
							else:
								#change codec of video
								stream_settings += [f'-codec:v:{video_index}', video['video_codec']]
								if bitrate != '':
									#target bitrate is set
									stream_settings += [f'-b:v:{video_index}', str(bitrate)]
							if various['keep_metadata'] == False:
								#remove metadata from video
								if 'tags' in stream.keys():
									for tag in stream['tags'].keys():
										stream_settings += [f'-metadata:s:{index}', f'{tag}=']

							#note down frame count of video (used for calculations of status)
							comm = [
								self.vars['ffprobe'],
								file,
								'-select_streams', index,
								'-count_packets',
								'-show_entries', 'stream=nb_read_packets', '-of', 'csv=p=0',
								'-v','quiet'
							]
							frame_count = (subprocess.run(comm, capture_output=True, text=True).stdout).strip()
							if frame_count.isdigit():
								frame_count = int(frame_count)
							else:
								#failed to get frame count of video
								self.logging.error(f'{func_name} Failed to get frame count of video stream')
								return 'ERROR', file

							video_index += 1

					elif stream['codec_type'] == 'audio':
						#stream is an audio
						if audio['keep_audio'] == True:
							#settings say to keep audio
							if (stream['disposition']['comment'] == 1) or ('tags' in stream.keys() and 'title' in stream['tags'].keys() and 'comment' in stream['tags']['title'].lower()):
								#audio is commentary
								if audio['keep_audio_commentary'] == False:
									#settings say to ditch commentary audio
									continue

							#audio is normal or it's commentary but the settings allow it; audio type is allowed
							if 'tags' in stream.keys() and 'language' in stream['tags'].keys():
								#stream has a language tagged
								if audio_keep and not stream['tags']['language'] in audio_keep:
									#settings say to ditch audio with this language
									continue
							else:
								#stream has unknown language
								if audio['keep_audio_unknown_language'] == False:
									#settings say to ditch audio with unknown language
									continue

							#audio type is allowed and language (or lack of) too
							audio_duplicate = False
							if audio['keep_audio_duplicates'] == False:
								#settings say to check if a duplicate version isn't already added
								for audio_stream in audio_log:
									if audio_stream['index'] != stream['index'] \
									and audio_stream['codec_type'] == 'audio' \
									and (
										(
											'tags' in audio_stream.keys() and 'language' in audio_stream['tags'].keys() \
											and 'tags' in stream.keys() and 'language' in stream['tags'].keys() \
											and audio_stream['tags']['language'] == stream['tags']['language']
										) \
										or \
										(
											'tags' in audio_stream.keys() and not 'language' in audio_stream['tags'].keys() \
											and 'tags' in stream.keys() and not 'language' in stream['tags'].keys()
										) \
										or \
										(
											not 'tags' in audio_stream.keys() \
											and not 'tags' in stream.keys()
										) #this if-statement checks if language or lack there of matches
									) \
									and audio_stream['channel_layout'] == stream['channel_layout'] \
									and audio_stream['codec_name'] == stream['codec_name']:
										#audio already has a duplicate version added so skip this one
										audio_duplicate = True
										break
							if audio_duplicate == True:
								continue

							#audio passes all restrictions so add it

							#add audio
							stream_settings += ['-map', f'0:{index}']
							audio_added = True
							#set codec of audio
							channel_layout = stream['channel_layout'].replace('(side)','').strip()
							if audio['audio_codec'][channel_layout] == 'copy' \
							or (audio['audio_codec'][channel_layout] == 'libfdk_aac' and stream['codec_name'] == 'aac'):
								#copy codec because settings say so or because audio codec is already target codec
								stream_settings += [f'-codec:a:{audio_index}', 'copy']
							else:
								#change codec of audio
								stream_settings += [f'-codec:a:{audio_index}', audio['audio_codec'][channel_layout]]

							if various['keep_metadata'] == False:
								#remove metadata from audio
								if 'tags' in stream.keys():
									for tag in stream['tags'].keys():
										if tag in ('language'): continue
										stream_settings += [f'-metadata:s:a:{audio_index}', f'{tag}=']

							audio_index += 1

							if channel_layout in audio['clone_audio'].keys() and audio['clone_audio'][channel_layout]:
								#settings say to make clone(s) of this audio
								if not channel_layout in filters.keys():
									self.logging.warning(f'{func_name} There are no filters for a {channel_layout} layout; skipping clone')
								else:
									for target_clone in audio['clone_audio'][channel_layout]:
										if not target_clone in filters[channel_layout].keys():
											self.logging.warning(f'{func_name} There is no filter for a {channel_layout} to {target_clone} clone; skipping clone')
											continue
										if not target_clone in audio['audio_codec'].keys():
											self.logging.warning(f'{func_name} One of the requested clones, {target_clone} (for {channel_layout} streams), does not have a codec defined in "audio_codec"; skipping clone')
											continue

										#{channel_layout} -> {target_clone} can be done (option found inside {filters})
										if audio['keep_audio_duplicates'] == False:
											#settings say to check if a duplicate version isn't already added
											audio_duplicate = False
											for audio_stream in audio_log:
												if audio_stream['index'] != stream['index'] \
												and audio_stream['codec_type'] == 'audio' \
												and (
													(
														'tags' in audio_stream.keys() and 'language' in audio_stream['tags'].keys() \
														and 'tags' in stream.keys() and 'language' in stream['tags'].keys() \
														and audio_stream['tags']['language'] == stream['tags']['language']
													) \
													or \
													(
														'tags' in audio_stream.keys() and not 'language' in audio_stream['tags'].keys() \
														and 'tags' in stream.keys() and not 'language' in stream['tags'].keys()
													) \
													or \
													(
														not 'tags' in audio_stream.keys() \
														and not 'tags' in stream.keys()
													) #this if-statement checks if language or lack there of matches
												) \
												and (
													(
														target_clone in ('2.0', '2.1', '2.2', '1.0', '1.1') \
														and audio_stream['channel_layout'] in ('stereo','mono')
													) \
													or (audio_stream['channel_layout'] == target_clone)
												) \
												and audio_stream['codec_name'] == stream['codec_name']:
													#audio already has a {target_clone} version added so skip this one
													audio_duplicate = True
													break
											if audio_duplicate == True:
												continue

										#add clone
										stream_settings += [
											'-map', f'0:{index}',
											f'-filter:a:{audio_index}', filters[channel_layout][target_clone],
											f'-codec:a:{audio_index}', audio['audio_codec'][target_clone]
										]
										if various['keep_metadata'] == False:
											#remove metadata from audio clone
											if 'tags' in stream.keys():
												for tag in stream['tags'].keys():
													if tag in ('language'): continue
													stream_settings += [f'-metadata:s:a:{audio_index}', f'{tag}=']
										audio_index += 1

							audio_log.append(stream)

					elif stream['codec_type'] == 'subtitle':
						#stream is a subtitle
						if subtitle['keep_subtitle'] == True:
							#settings say to keep subtitle

							if subtitle['exclude_versions']:
								if 'sdh' in subtitle['exclude_versions'] \
								and ( \
									stream['disposition']['hearing_impaired'] == 1 \
									or ( \
										'tags' in stream.keys() and 'title' in stream['tags'].keys() \
										and (
											'sdh' in stream['tags']['title'].lower() \
											or 'cc' in stream['tags']['title'].lower()
										)
									) #this if-statement checks if sdh or cc is present in the title tagged to the stream
								):
									#settings say to not add sdh versions
									continue
								if 'forced' in subtitle['exclude_versions'] \
								and ( \
									stream['disposition']['forced'] == 1 \
									or ( \
										'tags' in stream.keys() \
										and 'title' in stream['tags'].keys() \
										and 'forced' in stream['tags']['title'].lower()
									) #this if-statement checks if forced is present in the title tagged to the stream
								):
									#settings say to not add forced versions
									continue

							if 'tags' in stream.keys() and 'language' in stream['tags'].keys():
								#stream has a language tagged
								if subtitle_keep and not stream['tags']['language'] in subtitle_keep:
									#settings say to ditch subtitles with this language
									continue
							else:
								#stream has unknown language
								if subtitle['keep_subtitle_unknown_language'] == False:
									#settings say to ditch subtitles with unknown language
									continue

							#add subtitle
							stream_settings += ['-map', f'0:{index}']

							if various['keep_metadata'] == False:
								#remove metadata from subtitle
								if 'tags' in stream.keys():
									for tag in stream['tags'].keys():
										if tag in ('language'): continue
										stream_settings += [f'-metadata:s:0:{index}', f'{tag}=']

				#act on streams of certain types not being added
				if video['keep_video'] == True and video_added == False:
					self.logging.error(f'{func_name} No video stream found in file')
					return 'ERROR', file
				if audio['keep_audio'] == True and audio_added == False:
					if audio['keep_audio_all_on_no_match_ex_com'] == True:
						#settings say to keep all audio streams except commentary
						#this is a "rescue" of the audio streams so no duplicates removed, clones made, codec changed or metadata removed
						self.logging.warning(f'{func_name} Current media file has no matching audio tracks; adding all except commentary')
						for stream in file_info['streams']:
							if stream['codec_type'] == 'audio':
								if not ((stream['disposition']['comment'] == 1) or ('tags' in stream.keys() and 'title' in stream['tags'].keys() and 'comment' in stream['tags']['title'].lower())):
									#non-commentary audio track found
									index = str(stream['index'])
									#add audio
									stream_settings += [
										'-map', f'0:{index}',
										f'-codec:0:{index}', 'copy'
									]
									audio_added = True
				if audio['keep_audio'] == True and audio_added == False:
					if audio['keep_audio_all_on_no_match_in_com'] == True:
						#settings say to keep all audio stream including commentary (all audio streams are commentary)
						#this is a "rescue" of the audio streams so no duplicates removed, clones made, codec changed or metadata removed
						self.logging.warning(f'{func_name} Current media file only has commentary audio tracks; adding all')
						stream_settings += [
							'-map', '0:a',
							'-codec:a', 'copy'
						]

				#setup the transcode thread

				output_file = os.path.splitext(file)[0] + '.transcoded' + container
				while True:
					log_file = f'.ffmpeg-transcode-{"".join([str(int(random() * 10)) for x in range(4)])}'
					if not os.path.isfile(log_file):
						break
				comm = [
					self.vars['ffmpeg'], '-y',
					'-v', 'quiet',
					'-progress', '-',
					'-strict', '2',
					'-i', file
				] + stream_settings + [
					output_file
				]
				self.logging.debug(f'{func_name} Settings used for transcode')
				self.logging.debug(json.dumps(comm, indent=4))
				thread = threading.Thread(target=transcode_thread, args=(comm, log_file,))

				r_data = re_compile(r'frame.*?progress=\w+', re_DOTALL)
				r_frame = re_compile(r'(?<=frame=)\d+')
				r_size = re_compile(r'(?<=total_size=)\d+')

				#start the transcode!

				self.logging.info(f'{func_name} Starting transcode')
				start_time = time.perf_counter()
				thread.start()
				time.sleep(5)
				#log the status of the thread
				with open(log_file, 'r') as f:
					while True:
						if not thread.is_alive():
							break
						f.seek(0)
						data = f.read()
						data = r_data.findall(data)
						if data:
							data = data[-1]
							current_frame = int(r_frame.search(data).group(0))
							if current_frame == 0: continue
							current_size = int(r_size.search(data).group(0))
							current_time = time.perf_counter() - start_time

							progress = round(current_frame / frame_count * 100, 1)
							est_size = int(current_size / current_frame * frame_count) // (1024 * 1024)
							fps = current_frame // current_time
							est_time_rem = (current_time / progress * 100 - current_time) // 60

							self.logging.info(f'{func_name} {progress}% | {est_size} MiB estimated | {fps}fps | {est_time_rem} minutes remaining estimated')
						time.sleep(7)
				#transcoding is done
				self.logging.info(f'{func_name} Time: {(time.perf_counter() - start_time) // 60} minutes')
				if os.path.getsize(output_file) < 1000:
					os.remove(output_file)
					self.logging.error(f'{func_name} Something went wrong')
					with open(self.vars['error_file'],'a') as f:
						f.write(file + '\n')
				else:
					#transcode successful; clean up files
					#remove old file
					os.remove(file)
					#rename transcoded file to old file (result is replacing the old file)
					target_file = os.path.splitext(os.path.splitext(output_file)[0])[0] + container
					os.rename(output_file, target_file)
					#remove the temp transcode logging file
					os.remove(log_file)
					self.logging.info(f'{func_name} New file size: {os.path.getsize(target_file) // (1024 * 1024)} MiB')

		return files

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

	def select_files(self, func_name, files, target_files: list=[''], exclude_self: bool=False):
		"""
		title: 'select_files'
		trigger: action.select_files
		requirements: none
		action:
			Select specific files before going to the next action.
			In general, this action is not needed or can be avoided.
			This can be usefull if you need to include a new file in the process in the middle of... the process
			Or when you want the next action to apply to only a certain file instead of all targeted files
		arguments:
			-	key:	target_files
				value:	list ([])
				use:	give list of files to grab from the media file folder (file match going backwards from the filename)
				example: ['.en.ass', '.en.srt']
						this example will add all files inside the media folder, ending with '.en.ass' or '.en.srt',
							to the process to be manipulated from now by actions

			-	key:	exclude_self
				value:	bool (True | False)
				use:	ONLY select the targeted files instead of adding them to the currently selected files
				example: True
						this example will make the targeted files the ONLY files from then on to be in the process,
							until a new select_files action is triggered or the process ends
		example:
			arguments: {
				'target_files': ['.nl.srt','.nl.ass'],
				'exclude_self': True
			}

			From now on, only apply the actions to the matching files, until a new select_files is triggered
		note:
			you can do '' as a value inside the list for 'target_files' if you want to select every file inside the media folder,
				e.g. 'target_files': ['']
		"""
		target_files = tuple(set(target_files))

		#get the directories of all current files
		dirs = []
		for file in files:
			dirs.append(os.path.dirname(file))
		dirs = list(set(dirs))

		#get all files of all directories that end with one of the things in target_files
		dir_files = []
		for dir in dirs:
			dir_files += [os.path.join(dir, f) for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and f.endswith(target_files)]

		if exclude_self == False:
			files += dir_files
		else:
			files = dir_files
		files = list(set(files))

		self.logging.info(f'{func_name} Selected {len(files)} files')

		return files
