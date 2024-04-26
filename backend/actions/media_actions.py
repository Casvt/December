#-*- coding: utf-8 -*-

from dataclasses import dataclass
from json import dumps, loads
from os import remove
from os.path import getsize, isfile, splitext
from re import MULTILINE, compile, escape, search
from shutil import move
from subprocess import PIPE, Popen, run
from time import sleep
from typing import Any, Dict, List, Literal, Tuple, Union

from requests import RequestException, get

from backend.actions.general_actions import Action, ActionVars
from backend.config import Config

LANGS = {'aa': ['aar', 'aa', 'afar'], 'ab': ['abk', 'ab', 'abkhazian'], 'af': ['afr', 'af', 'afrikaans'], 'ak': ['aka', 'ak', 'akan'], 'am': ['amh', 'am', 'amharic'], 'an': ['arg', 'an', 'aragonese'], 'ar': ['ara', 'ar', 'arabic'], 'as': ['asm', 'as', 'assamese'], 'av': ['avar'], 'ay': ['aym', 'ay', 'aymara'], 'az': ['aze', 'az', 'azerbaijani'], 'ba': ['bak', 'ba', 'bashkir'], 'be': ['bel', 'be', 'belarusian'], 'bg': ['bul', 'bg', 'bulgarian'], 'bh': ['bihari'], 'bi': ['bis', 'bi', 'bislama'], 'bm': ['bam', 'bm', 'bambara'], 'bn': ['ben', 'bn', 'bengali'], 'bo': ['tib', 'bod', 'bo', 'tibetan'], 'br': ['bre', 'br', 'breton'], 'bs': ['bos', 'bs', 'bosnian'], 'ca': ['cat', 'ca', 'catalan'], 'ce': ['che', 'ce', 'chechen'], 'ch': ['cha', 'ch', 'chamorro'], 'co': ['cos', 'co', 'corsican'], 'cr': ['cre', 'cr', 'cree'], 'cs': ['cze', 'ces', 'cs', 'czech'], 'cu': ['old church slavonic / old bulgarian'], 'cv': ['chv', 'cv', 'chuvash'], 'cy': ['wel', 'cym', 'cy', 'welsh'], 'da': ['dan', 'da', 'danish'], 'de': ['ger', 'deu', 'de', 'german'], 'dv': ['divehi'], 'dz': ['dzo', 'dz', 'dzongkha'], 'ee': ['ewe', 'ee', 'ewe'], 'el': ['greek'], 'en': ['eng', 'en', 'english'], 'en-US': ['english united states'], 'en-GB': ['english great britain'], 'en-AU': ['english australian'], 'eo': ['epo', 'eo', 'esperanto'], 'es': ['spanish'], 'et': ['est', 'et', 'estonian'], 'eu': ['baq', 'eus', 'eu', 'basque'], 'fa': ['per', 'fas', 'fa', 'persian'], 'ff': ['peul'], 'fi': ['fin', 'fi', 'finnish'], 'fj': ['fij', 'fj', 'fijian'], 'fo': ['fao', 'fo', 'faroese'], 'fr': ['fre', 'fra', 'fr', 'french'], 'fy': ['west frisian'], 'ga': ['gle', 'ga', 'irish'], 'gd': ['scottish gaelic'], 'gl': ['glg', 'gl', 'galician'], 'gn': ['grn', 'gn', 'guarani'], 'gu': ['guj', 'gu', 'gujarati'], 'gv': ['glv', 'gv', 'manx'], 'ha': ['hau', 'ha', 'hausa'], 'he': ['heb', 'he', 'hebrew'], 'hi': ['hin', 'hi', 'hindi'], 'ho': ['hmo', 'ho', 'hiri motu'], 'hr': ['hrv', 'hr', 'croatian'], 'ht': ['hat', 'ht', 'haitian'], 'hu': ['hun', 'hu', 'hungarian'], 'hy': ['arm', 'hye', 'hy', 'armenian'], 'hz': ['her', 'hz', 'herero'], 'ia': ['interlingua'], 'id': ['ind', 'id', 'indonesian'], 'ie': ['ile', 'ie', 'interlingue'], 'ig': ['ibo', 'ig', 'igbo'], 'ii': ['sichuan yi'], 'ik': ['inupiak'], 'io': ['ido', 'io', 'ido'], 'is': ['ice', 'isl', 'is', 'icelandic'], 'it': ['ita', 'it', 'italian'], 'iu': ['iku', 'iu', 'inuktitut'], 'ja': ['jpn', 'ja', 'japanese'], 'jv': ['jav', 'jv', 'javanese'], 'ka': ['geo', 'kat', 'ka', 'georgian'], 'kg': ['kon', 'kg', 'kongo'], 'ki': ['kikuyu'], 'kj': ['kua', 'kj', 'kuanyama'], 'kk': ['kaz', 'kk', 'kazakh'], 'kl': ['kal', 'kl', 'greenlandic'], 'km': ['cambodian'], 'kn': ['kan', 'kn', 'kannada'], 'ko': ['kor', 'ko', 'korean'], 'kr': ['kau', 'kr', 'kanuri'], 'ks': ['kas', 'ks', 'kashmiri'], 'ku': ['kur', 'ku', 'kurdish'], 'kv': ['kom', 'kv', 'komi'], 'kw': ['cor', 'kw', 'cornish'], 'ky': ['kir', 'ky', 'kirghiz'], 'la': ['lat', 'la', 'latin'], 'lb': ['luxembourgish'], 'lg': ['lug', 'lg', 'ganda'], 'li': ['limburgian'], 'ln': ['lin', 'ln', 'lingala'], 'lo': ['laotian'], 'lt': ['lit', 'lt', 'lithuanian'], 'lu': ['lub', 'lu', 'luba-katanga'], 'lv': ['lav', 'lv', 'latvian'], 'mg': ['mlg', 'mg', 'malagasy'], 'mh': ['mah', 'mh', 'marshallese'], 'mi': ['mao', 'mri', 'mi', 'maori'], 'mk': ['mac', 'mkd', 'mk', 'macedonian'], 'ml': ['mal', 'ml', 'malayalam'], 'mn': ['mon', 'mn', 'mongolian'], 'mo': ['moldovan'], 'mr': ['mar', 'mr', 'marathi'], 'ms': ['may', 'msa', 'ms', 'malay'], 'mt': ['mlt', 'mt', 'maltese'], 'my': ['bur', 'mya', 'my', 'burmese'], 'na': ['nauruan'], 'nb': ['norwegian bokmål'], 'nd': ['north ndebele'], 'ne': ['nep', 'ne', 'nepali'], 'ng': ['ndo', 'ng', 'ndonga'], 'nl': ['dut', 'nld', 'nl', 'dutch'], 'nn': ['norwegian nynorsk'], 'no': ['nno', 'nn', 'nor', 'no', 'norwegian'], 'nr': ['south ndebele'], 'nv': ['navajo'], 'ny': ['chichewa'], 'oc': ['occitan'], 'oj': ['oji', 'oj', 'ojibwa'], 'om': ['orm', 'om', 'oromo'], 'or': ['ori', 'or', 'oriya'], 'os': ['ossetian / ossetic'], 'pa': ['panjabi / punjabi'], 'pi': ['pli', 'pi', 'pali'], 'pl': ['pol', 'pl', 'polish'], 'ps': ['pus', 'ps', 'pashto'], 'pt': ['por', 'pt', 'portuguese'], 'qu': ['que', 'qu', 'quechua'], 'rm': ['raeto romance'], 'rn': ['kirundi'], 'ro': ['romanian'], 'ru': ['rus', 'ru', 'russian'], 'rw': ['rwandi'], 'sa': ['san', 'sa', 'sanskrit'], 'sc': ['srd', 'sc', 'sardinian'], 'sd': ['snd', 'sd', 'sindhi'], 'se': ['sme', 'se', 'northern sami'], 'sg': ['sag', 'sg', 'sango'], 'sh': ['serbo-croatian'], 'si': ['sinhalese'], 'sk': ['slo', 'slk', 'sk', 'slovak'], 'sl': ['slv', 'sl', 'slovenian'], 'sm': ['smo', 'sm', 'samoan'], 'sn': ['sna', 'sn', 'shona'], 'so': ['somalia'], 'sq': ['alb', 'sqi', 'sq', 'albanian'], 'sr': ['srp', 'sr', 'serbian'], 'ss': ['ssw', 'ss', 'swati'], 'st': ['southern sotho'], 'su': ['sun', 'su', 'sundanese'], 'sv': ['swe', 'sv', 'swedish'], 'sw': ['swa', 'sw', 'swahili'], 'ta': ['tam', 'ta', 'tamil'], 'te': ['tel', 'te', 'telugu'], 'tg': ['tgk', 'tg', 'tajik'], 'th': ['tha', 'th', 'thai'], 'ti': ['tir', 'ti', 'tigrinya'], 'tk': ['tuk', 'tk', 'turkmen'], 'tl': ['tagalog / filipino'], 'tn': ['tsn', 'tn', 'tswana'], 'to': ['tonga'], 'tr': ['tur', 'tr', 'turkish'], 'ts': ['tso', 'ts', 'tsonga'], 'tt': ['tat', 'tt', 'tatar'], 'tw': ['twi', 'tw', 'twi'], 'ty': ['tah', 'ty', 'tahitian'], 'ug': ['uyghur'], 'uk': ['ukr', 'uk', 'ukrainian'], 'ur': ['urd', 'ur', 'urdu'], 'uz': ['uzb', 'uz', 'uzbek'], 've': ['ven', 've', 'venda'], 'vi': ['vie', 'vi', 'vietnamese'], 'vo': ['vol', 'vo', 'volapük'], 'wa': ['wln', 'wa', 'walloon'], 'wo': ['wol', 'wo', 'wolof'], 'xh': ['xho', 'xh', 'xhosa'], 'yi': ['yid', 'yi', 'yiddish'], 'yo': ['yor', 'yo', 'yoruba'], 'za': ['zhuang'], 'zh': ['chi', 'zho', 'zh', 'chinese'], 'zu': ['zul', 'zu', 'zulu'], 'ace': ['achinese'], 'ach': ['acoli'], 'ada': ['adangme'], 'ady': ['adygei'], 'afa': ['afro-asiatic languages'], 'afh': ['afrihili'], 'ain': ['ainu'], 'akk': ['akkadian'], 'ale': ['aleut'], 'alg': ['algonquian languages'], 'alt': ['southern altai'], 'ang': ['english old (ca.450-1100)'], 'anp': ['angika'], 'apa': ['apache languages'], 'arc': ['imperial aramaic (700-300 bce)'], 'arn': ['mapuche'], 'arp': ['arapaho'], 'art': ['artificial languages'], 'arw': ['arawak'], 'ast': ['asturian'], 'ath': ['athapascan languages'], 'aus': ['australian languages'], 'ava': ['av', 'avaric'], 'ave': ['ae', 'avestan'], 'awa': ['awadhi'], 'bad': ['banda languages'], 'bai': ['bamileke languages'], 'bal': ['baluchi'], 'ban': ['balinese'], 'bas': ['basa'], 'bat': ['baltic languages'], 'bej': ['bedawiyet'], 'bem': ['bemba'], 'ber': ['berber languages'], 'bho': ['bhojpuri'], 'bih': ['bh', 'bihari languages'], 'bik': ['bikol'], 'bin': ['bini'], 'bla': ['siksika'], 'bnt': ['bantu (other)'], 'bra': ['braj'], 'btk': ['batak languages'], 'bua': ['buriat'], 'bug': ['buginese'], 'byn': ['bilin'], 'cad': ['caddo'], 'cai': ['central american indian languages'], 'car': ['galibi carib'], 'cau': ['caucasian languages'], 'ceb': ['cebuano'], 'cel': ['celtic languages'], 'chb': ['chibcha'], 'chg': ['chagatai'], 'chk': ['chuukese'], 'chm': ['mari'], 'chn': ['chinook jargon'], 'cho': ['choctaw'], 'chp': ['chipewyan'], 'chr': ['cherokee'], 'chu': ['cu', 'church slavic'], 'chy': ['cheyenne'], 'cmc': ['chamic languages'], 'cop': ['coptic'], 'cpe': ['cpf', 'cpp', 'crp', 'creoles and pidgins'], 'crh': ['crimean tatar'], 'csb': ['kashubian'], 'cus': ['cushitic languages'], 'dak': ['dakota'], 'dar': ['dargwa'], 'day': ['land dayak languages'], 'del': ['delaware'], 'den': ['slave (athapascan)'], 'dgr': ['dogrib'], 'din': ['dinka'], 'div': ['dv', 'dhivehi'], 'doi': ['dogri'], 'dra': ['dravidian languages'], 'dsb': ['lower sorbian'], 'dua': ['duala'], 'dum': ['dutch middle (ca.1050-1350)'], 'dyu': ['dyula'], 'efi': ['efik'], 'egy': ['egyptian (ancient)'], 'eka': ['ekajuk'], 'elx': ['elamite'], 'enm': ['english middle (1100-1500)'], 'ewo': ['ewondo'], 'fan': ['fang'], 'fat': ['fanti'], 'fil': ['filipino'], 'fiu': ['finno-ugrian languages'], 'fon': ['fon'], 'frm': ['french middle (ca.1400-1600)'], 'fro': ['french old (842-ca.1400)'], 'frr': ['northern frisian'], 'frs': ['eastern frisian'], 'fry': ['fy', 'western frisian'], 'ful': ['ff', 'fulah'], 'fur': ['friulian'], 'gaa': ['ga'], 'gay': ['gayo'], 'gba': ['gbaya'], 'gem': ['germanic languages'], 'gez': ['geez'], 'gil': ['gilbertese'], 'gla': ['gd', 'gaelic'], 'gmh': ['german middle high (ca.1050-1500)'], 'goh': ['german old high (ca.750-1050)'], 'gon': ['gondi'], 'gor': ['gorontalo'], 'got': ['gothic'], 'grb': ['grebo'], 'grc': ['greek ancient (to 1453)'], 'gre': ['ell', 'el', 'greek modern (1453-)'], 'gsw': ['alemannic'], 'gwi': ["gwich'in"], 'hai': ['haida'], 'haw': ['hawaiian'], 'hil': ['hiligaynon'], 'him': ['himachali languages'], 'hit': ['hittite'], 'hmn': ['hmong'], 'hsb': ['upper sorbian'], 'hup': ['hupa'], 'iba': ['iban'], 'iii': ['ii', 'nuosu'], 'ijo': ['ijo languages'], 'ilo': ['iloko'], 'ina': ['ia', 'interlingua (international auxiliary language association)'], 'inc': ['indic languages'], 'ine': ['indo-european languages'], 'inh': ['ingush'], 'ipk': ['ik', 'inupiaq'], 'ira': ['iranian languages'], 'iro': ['iroquoian languages'], 'jbo': ['lojban'], 'jpr': ['judeo-persian'], 'jrb': ['judeo-arabic'], 'kaa': ['kara-kalpak'], 'kab': ['kabyle'], 'kac': ['jingpho'], 'kam': ['kamba'], 'kar': ['karen languages'], 'kaw': ['kawi'], 'kbd': ['kabardian'], 'kha': ['khasi'], 'khi': ['khoisan languages'], 'khm': ['km', 'central khmer'], 'kho': ['khotanese'], 'kik': ['ki', 'gikuyu'], 'kin': ['rw', 'kinyarwanda'], 'kmb': ['kimbundu'], 'kok': ['konkani'], 'kos': ['kosraean'], 'kpe': ['kpelle'], 'krc': ['karachay-balkar'], 'krl': ['karelian'], 'kro': ['kru languages'], 'kru': ['kurukh'], 'kum': ['kumyk'], 'kut': ['kutenai'], 'lad': ['ladino'], 'lah': ['lahnda'], 'lam': ['lamba'], 'lao': ['lo', 'lao'], 'lez': ['lezghian'], 'lim': ['li', 'limburgan'], 'lol': ['mongo'], 'loz': ['lozi'], 'ltz': ['lb', 'letzeburgesch'], 'lua': ['luba-lulua'], 'lui': ['luiseno'], 'lun': ['lunda'], 'luo': ['luo (kenya and tanzania)'], 'lus': ['lushai'], 'mad': ['madurese'], 'mag': ['magahi'], 'mai': ['maithili'], 'mak': ['makasar'], 'man': ['mandingo'], 'map': ['austronesian languages'], 'mas': ['masai'], 'mdf': ['moksha'], 'mdr': ['mandar'], 'men': ['mende'], 'mga': ['irish middle (900-1200)'], 'mic': ["mi'kmaq"], 'min': ['minangkabau'], 'mis': ['uncoded languages'], 'mkh': ['mon-khmer languages'], 'mnc': ['manchu'], 'mni': ['manipuri'], 'mno': ['manobo languages'], 'moh': ['mohawk'], 'mos': ['mossi'], 'mul': ['multiple languages'], 'mun': ['munda languages'], 'mus': ['creek'], 'mwl': ['mirandese'], 'mwr': ['marwari'], 'myn': ['mayan languages'], 'myv': ['erzya'], 'nah': ['nahuatl languages'], 'nai': ['north american indian languages'], 'nap': ['neapolitan'], 'nau': ['na', 'nauru'], 'nav': ['nv', 'navaho'], 'nbl': ['nr', 'nde', 'nd', 'ndebele'], 'nds': ['low'], 'new': ['nepal bhasa'], 'nia': ['nias'], 'nic': ['niger-kordofanian languages'], 'niu': ['niuean'], 'nob': ['nb', 'bokmål'], 'nog': ['nogai'], 'non': ['norse'], 'nqo': ["n'ko"], 'nso': ['northern sotho'], 'nub': ['nubian languages'], 'nwc': ['classical nepal bhasa'], 'nya': ['ny', 'chewa'], 'nym': ['nyamwezi'], 'nyn': ['nyankole'], 'nyo': ['nyoro'], 'nzi': ['nzima'], 'oci': ['oc', 'occitan (post 1500)'], 'osa': ['osage'], 'oss': ['os', 'ossetian'], 'ota': ['turkish ottoman (1500-1928)'], 'oto': ['otomian languages'], 'paa': ['papuan languages'], 'pag': ['pangasinan'], 'pal': ['pahlavi'], 'pam': ['kapampangan'], 'pan': ['pa', 'panjabi'], 'pap': ['papiamento'], 'pau': ['palauan'], 'peo': ['persian old (ca.600-400 b.c.)'], 'phi': ['philippine languages'], 'phn': ['phoenician'], 'pon': ['pohnpeian'], 'pra': ['prakrit languages'], 'pro': ['provençal old (to 1500)'], 'qaa-qtz': ['reserved for local use'], 'raj': ['rajasthani'], 'rap': ['rapanui'], 'rar': ['cook islands maori'], 'roa': ['romance languages'], 'roh': ['rm', 'romansh'], 'rom': ['romany'], 'rum': ['ron', 'ro', 'moldavian'], 'run': ['rn', 'rundi'], 'rup': ['aromanian'], 'sad': ['sandawe'], 'sah': ['yakut'], 'sai': ['south american indian (other)'], 'sal': ['salishan languages'], 'sam': ['samaritan aramaic'], 'sas': ['sasak'], 'sat': ['santali'], 'scn': ['sicilian'], 'sco': ['scots'], 'sel': ['selkup'], 'sem': ['semitic languages'], 'sga': ['irish old (to 900)'], 'sgn': ['sign languages'], 'shn': ['shan'], 'sid': ['sidamo'], 'sin': ['si', 'sinhala'], 'sio': ['siouan languages'], 'sit': ['sino-tibetan languages'], 'sla': ['slavic languages'], 'sma': ['southern sami'], 'smi': ['sami languages'], 'smj': ['lule sami'], 'smn': ['inari sami'], 'sms': ['skolt sami'], 'snk': ['soninke'], 'sog': ['sogdian'], 'som': ['so', 'somali'], 'son': ['songhai languages'], 'sot': ['st', 'sotho'], 'spa': ['es', 'castilian'], 'srn': ['sranan tongo'], 'srr': ['serer'], 'ssa': ['nilo-saharan languages'], 'suk': ['sukuma'], 'sus': ['susu'], 'sux': ['sumerian'], 'syc': ['classical syriac'], 'syr': ['syriac'], 'tai': ['tai languages'], 'tem': ['timne'], 'ter': ['tereno'], 'tet': ['tetum'], 'tgl': ['tl', 'tagalog'], 'tig': ['tigre'], 'tiv': ['tiv'], 'tkl': ['tokelau'], 'tlh': ['klingon'], 'tli': ['tlingit'], 'tmh': ['tamashek'], 'tog': ['tonga (nyasa)'], 'ton': ['to', 'tonga (tonga islands)'], 'tpi': ['tok pisin'], 'tsi': ['tsimshian'], 'tum': ['tumbuka'], 'tup': ['tupi languages'], 'tut': ['altaic languages'], 'tvl': ['tuvalu'], 'tyv': ['tuvinian'], 'udm': ['udmurt'], 'uga': ['ugaritic'], 'uig': ['ug', 'uighur'], 'umb': ['umbundu'], 'und': ['undetermined'], 'vai': ['vai'], 'vot': ['votic'], 'wak': ['wakashan languages'], 'wal': ['walamo'], 'war': ['waray'], 'was': ['washo'], 'wen': ['sorbian languages'], 'xal': ['kalmyk'], 'yao': ['yao'], 'yap': ['yapese'], 'ypk': ['yupik languages'], 'zap': ['zapotec'], 'zbl': ['bliss'], 'zen': ['zenaga'], 'zgh': ['standard moroccan tamazight'], 'zha': ['za', 'chuang'], 'znd': ['zande languages'], 'zun': ['zuni'], 'zxx': ['no linguistic content'], 'zza': ['dimili']}
extract_og_lang_tvdb = compile(r'<strong>Original Language</strong>\r\n\s+<span>(.*?)</span>')
extract_og_lang_tmdb = compile(r'Original Language</bdi></strong>\s(.*?)</p>')

# https://trac.ffmpeg.org/wiki/AudioChannelManipulation
# https://superuser.com/questions/852400/properly-downmix-5-1-to-stereo-using-ffmpeg
CHANNEL_FILTERS = {
	'3.0': {
		'2.0': 'pan=stereo|FL = 0.414214*FC + 0.585786*FL | FR = 0.414214*FC + 0.585786*FR'
	},
	'4.0': {
		'2.0': 'pan=stereo|FL = 0.422650*FL + 0.366025*BL + 0.211325*BR | FR = 0.422650*FR + 0.366025*BR + 0.211325*BL'
	},
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

TERM_TO_LAYOUT = {
	"mono": "1.0",
	"stereo": "2.0",
	"quad": "4.0",
	"hexagonal": "6.0",
	"octagonal": "8.0"
}

@dataclass
class MediaExtractSubsVars(ActionVars):
	codec: str
	"The codec of the subtitles when it's extracted (e.g. `srt`)"

	language_tag: bool
	"Add the language code to the filename (e.g. `.en.srt` or `.nl.ass`)"

	extract_unknown_language: bool
	"Extract the subtitles that don't have a language tagged"

	remove_from_media: bool
	"After extracting the subtitles from the media file, should the extracted subs be removed from the media file?"

	extract_languages: Union[List[str], None] = None
	"When given, only extract the subtitles that are tagged with one of the given 2 letter language codes"

	extract_codecs: Union[List[str], None] = None
	"When given, only extract the subtitles that are one of the given codecs (e.g. `[\"subrip\", \"hdmv_pgs_subtitle\"]`)"

	exclude_versions: Union[List[str], None] = None
	"When given, don't extract subtitles if they are at least one of the given versions (e.g. `sdh` or `forced`)"

	file_filter: Union[List[str], None] = None
	"Only process files that contain at least one of the strings in the list"

	def __post_init__(self) -> None:
		if not isinstance(self.remove_from_media, bool):
			raise TypeError

		if not isinstance(self.codec, str):
			raise TypeError
		if not (2 <= len(self.codec) <= 4):
			raise ValueError(f"Unknown codec: {self.codec}")

		if not isinstance(self.language_tag, bool):
			raise TypeError

		if not isinstance(self.extract_unknown_language, bool):
			raise TypeError

		if self.extract_languages is not None:
			if not isinstance(self.extract_languages, list):
				raise TypeError
			if not all(isinstance(f, str) for f in self.extract_languages):
				raise TypeError
			if not all(f in LANGS for f in self.extract_languages):
				raise ValueError(f"Unknown language code in list: {self.extract_languages}")

		if self.extract_codecs is not None:
			if not isinstance(self.extract_codecs, list):
				raise TypeError
			if not all(isinstance(f, str) for f in self.extract_codecs):
				raise TypeError

		if self.exclude_versions is not None:
			if not isinstance(self.exclude_versions, list):
				raise TypeError
			if not all(isinstance(f, str) for f in self.exclude_versions):
				raise TypeError
			if not all(f in ('sdh', 'forced') for f in self.exclude_versions):
				raise ValueError(f"Unknown version in list: {self.exclude_versions}")

		if self.file_filter is not None:
			if not isinstance(self.file_filter, list):
				raise TypeError
			if not all(isinstance(f, str) for f in self.file_filter):
				raise TypeError
		return


class MediaExtractSubs(Action):
	"""
	Extract subtitles from a media file into their own seperate files. The files
	are placed into the same folder as the media file. The files will have the
	same filename as the media file, but with subtitle extensions.

	Example:

	Arguments:
	```json
	{
		"codec": "srt",
		"language_tag": true,
		"extract_unknown_language": true,
		"remove_from_media": true,
		"extract_languages": ["en", "nl", "it"],
		"extract_codecs": ["subrip"],
		"exclude_versions": ["sdh", "forced"]
	}
	```

	Result:

		1. media.mkv
		2. sub.en.srt
		3. sub.nl.srt
		4. sub.srt

	The file contained an English, Dutch and Unknown sub, which were extracted
	and tagged in their filename. There was no Italian subtitle in the file.
	There also was an English, SDH, HDMV PGS, subtitle, but it wasn't extracted. The media file
	doesn't contain the extracted Dutch, English and unknown subtitles.
	"""

	var_class = MediaExtractSubsVars

	def __init__(self, vars: MediaExtractSubsVars) -> None:
		self.vars = vars
		return

	def __is_sdh(self, stream: Dict[str, Any], stream_title: str) -> bool:
		return (
			stream['disposition']['hearing_impaired']
			or
			any(term in stream_title for term in ('sdh', 'hearing impaired', 'cc'))
		)

	def __is_forced(self, stream: Dict[str, Any], stream_title: str) -> bool:
		return (
			stream['disposition']['forced']
			or
			'forced' in stream_title
		)

	def run(self, files: List[str]) -> List[str]:
		self.config = Config().config
		extra_files: List[str] = []

		if self.vars.file_filter is not None:
			med_files = [
				file for file in files
				if file.endswith(self.config.media_filter)
					and any(f in file for f in self.vars.file_filter)
			]
		else:
			med_files = [
				file for file in files
				if file.endswith(self.config.media_filter)
			]

		for file in med_files:
			comm = [
				self.config.ffprobe,
				'-print_format', 'json',
				'-show_streams',
				'-v', 'quiet',
				file
			]
			file_info: Dict[str, List[Dict[str, Any]]] = loads(
				run(comm, capture_output=True, text=True).stdout
			)
			self.config.logger.debug(f"File info: {dumps(file_info, indent=4)}")
			st = splitext(file)
			base_filename = st[0]
			extracted_streams: List[int] = []
			stream_settings: List[str] = []

			for stream in file_info['streams']:
				if not stream['codec_type'] == 'subtitle':
					continue

				if (
					self.vars.extract_codecs
					and not stream["codec_name"] in self.vars.extract_codecs
				):
					continue

				tags = []
				stream_title: str = stream.get('tags', {}).get('title', '').lower()
				lang_tag: str = stream.get('tags', {}).get('language', '').lower()

				if self.__is_sdh(stream, stream_title):
					if 'sdh' in (self.vars.exclude_versions or []):
						continue
					tags.append('sdh')

				if self.__is_forced(stream, stream_title):
					if 'forced' in (self.vars.exclude_versions or []):
						continue
					tags.append('forced')

				# Find language of stream
				stream_lang = 'und'
				for lang_key, lang_opts in LANGS.items():
					lang_versions = [lang_key] + lang_opts
					if any(
						v == lang_tag
						or v in stream_title
						for v in lang_versions
					):
						stream_lang = lang_key
						break

				if stream_lang == 'und' and not self.vars.extract_unknown_language:
					continue

				if (
					self.vars.extract_languages
					and
					not stream_lang in self.vars.extract_languages
				):
					continue

				if stream_lang != 'und' and self.vars.language_tag:
					tags.append(stream_lang)

				tags.append(self.vars.codec)
				resulting_filename = ".".join([base_filename, *tags])
				extracted_streams.append(stream["index"])
				stream_settings += [
					"-map", f"0:{stream['index']}",
					resulting_filename
				]
				self.config.logger.info(f"Extracted subtitle: {resulting_filename}")
				extra_files.append(resulting_filename)

			if not extracted_streams:
				continue

			if self.vars.remove_from_media:
				stream_settings += [
					"-map", "0"
				]
				for s in extracted_streams:
					stream_settings += ["-map", f"-0:{s}"]
				stream_settings += [
					"-c", "copy",
					st[0] + ".transcoded" + st[1]
				]

			comm = [
				self.config.ffmpeg, "-y",
				"-v", "quiet",
				"-i", file
			] + stream_settings
			self.config.logger.debug(f"Command used: {comm}")
			run(comm)

			if self.vars.remove_from_media:
				# Delete original file, replace with new transcoded file
				remove(file)
				while isfile(file):
					sleep(0.1)
				source_file = st[0] + ".transcoded" + st[1]
				move(source_file, file)

		if not extra_files:
			self.config.logger.info("Extracted no subtitles")
		else:
			files += extra_files
		return files


@dataclass
class VideoTranscodeVars:
	keep_video: bool
	"Set to false to remove all video streams from the media file"

	codec: str
	"""
	The target codec of the video streams (e.g. 'libx264' or 'hevc_nvenc').
	Give 'copy' to keep current codec.
	"""

	force_transcode: bool
	"""
	Even if the video stream is already in the desired codec, still transcode it.
	Can be useful for reducing file size with a more aggressive configuration of
	the codec.
	"""

	preset: Union[str, None] = None
	"""
	The ffmpeg preset to use for the encoding (e.g. `slow` or `p7`).
	Don't supply to let ffmpeg figure it out itself.
	"""

	bitrate_ratio: Union[float, None] = None
	"""
	The bitrate ratio between the source stream and the transcoded stream.
	Must be bigger than `0.0`.
	"""

	def __post_init__(self) -> None:
		if not isinstance(self.keep_video, bool):
			raise TypeError

		if not isinstance(self.force_transcode, bool):
			raise TypeError

		if self.preset is not None:
			if not isinstance(self.preset, str):
				raise TypeError

		if self.bitrate_ratio is not None:
			if not isinstance(self.bitrate_ratio, float):
				raise TypeError
			if not 0 < self.bitrate_ratio:
				raise TypeError

		return


@dataclass
class AudioTranscodeVars:
	keep_audio: bool
	"Set to false to remove all audio streams from the media file"

	codec: str
	"""
	The target codec of the audio streams (e.g. 'libfdk_aac' or 'ac3').
	Give 'copy' to keep current codec.
	"""

	force_transcode: bool
	"""
	Even if the audio stream is already in the desired codec, still transcode it.
	Can be useful for reducing file size with a more aggressive configuration of
	the codec.
	"""

	keep_unknowns: bool
	"Keep the audio tracks that don't have a language tagged"

	keep_commentary: bool = False
	"Keep the audio tracks that are marked as 'commentary' tracks"

	keep_languages: Union[List[str], None] = None
	"When given, only keep the audio tracks that are tagged with one of the given 2 letter language codes"

	keep_original_language: bool = False
	"""
	Keep the audio track with the language that the media originally was spoken in,
	according to the TVDB or TMDB. Requires Sonarr and/or Radarr information to be filled in.
	"""

	keep_duplicates: bool = False
	"""
	If multiple audio tracks are duplicates of each other, keep them all instead
	of removing all but one. Tracks are considered duplicates of each other when
	the channel layout (e.g. 5.1), codec (e.g. aac) and language (e.g. English)
	all match.
	"""

	on_no_matches: Union[
		Literal['empty'],
		Literal['no_commentary'],
		Literal['avoid_commentary'],
		Literal['all']
	] = 'avoid_commentary'
	"""
	What to do when no audio tracks match the filters. E.g. `keep_languages = ["it"]`
	but there are only English audio tracks.

	1. `empty` = Leave it. Keep none.
	2. `no_commentary` = Keep all except commentary. If there are only commentary, keep none.
	3. `avoid_commentary` = Keep all except commantary. If there are only commentary, keep all.
	4. `all` = Keep all.
	"""

	create_channels: Union[List[str], None] = None
	"""
	Create new audio tracks with the given channel configurations if an audio
	track exists with a higher channel count. E.g. if the media file has a `5.1`
	audio track, then supplying `["2.0", "1.0"]` will make the resulting media file
	have a `5.1`, `2.0` and `1.0` audio track. Support depends on source and target
	channel configuration.
	"""

	def __post_init__(self) -> None:
		for key in (self.keep_audio, self.force_transcode, self.keep_unknowns,
			  		self.keep_commentary, self.keep_original_language,
					self.keep_duplicates
		):
			if not isinstance(key, bool):
				raise TypeError

		if self.keep_languages is not None:
			if not isinstance(self.keep_languages, list):
				raise TypeError
			if not all(isinstance(f, str) for f in self.keep_languages):
				raise TypeError
			if not all(f in LANGS for f in self.keep_languages):
				raise ValueError(f"Unknown language code in list: {self.keep_languages}")

		if not self.on_no_matches in ('empty', 'no_commentary', 'avoid_commentary', 'all'):
			raise TypeError

		if self.create_channels is not None:
			if not isinstance(self.create_channels, list):
				raise TypeError
			if not all(isinstance(f, str) for f in self.create_channels):
				raise TypeError

			allow_configs = []
			for v in CHANNEL_FILTERS.values():
				allow_configs += list(v.keys())
			if not all(f in allow_configs for f in self.create_channels):
				raise ValueError(f"Unknown/unsupported channel configuration in list: {self.create_channels}")

		return


@dataclass
class SubtitleTranscodeVars:
	keep_subtitle: bool
	"Set to false to remove all subtitle streams from the media file"

	keep_unknowns: bool
	"Keep the subtitles that don't have a language tagged"

	keep_languages: Union[List[str], None] = None
	"When given, only keep the subtitles that are tagged with one of the given 2 letter language codes"

	keep_codecs: Union[List[str], None] = None
	"When given, only keep the subtitles that are one of the given codecs (e.g. `[\"subrip\", \"hdmv_pgs_subtitle\"]`)"

	exclude_versions: Union[List[str], None] = None
	"When given, remove subtitles if they are at least one of the given versions (e.g. `sdh` or `forced`)"

	def __post_init__(self) -> None:
		if not isinstance(self.keep_subtitle, bool):
			raise TypeError

		if not isinstance(self.keep_unknowns, bool):
			raise TypeError

		if self.keep_languages is not None:
			if not isinstance(self.keep_languages, list):
				raise TypeError
			if not all(isinstance(f, str) for f in self.keep_languages):
				raise TypeError
			if not all(f in LANGS for f in self.keep_languages):
				raise ValueError(f"Unknown language code in list: {self.keep_languages}")

		if self.keep_codecs is not None:
			if not isinstance(self.keep_codecs, list):
				raise TypeError
			if not all(isinstance(f, str) for f in self.keep_codecs):
				raise TypeError

		if self.exclude_versions is not None:
			if not isinstance(self.exclude_versions, list):
				raise TypeError
			if not all(isinstance(f, str) for f in self.exclude_versions):
				raise TypeError
			if not all(f in ('sdh', 'forced') for f in self.exclude_versions):
				raise ValueError(f"Unknown version in list: {self.exclude_versions}")

		return


@dataclass
class GeneralTranscodeVars:
	keep_metadata: bool
	"""
	Set to false to remove all unnecessary metadata from the media file.
	Language metadata for streams are kept.
	"""

	keep_poster: bool = False
	"Set to false to remove any integrated media posters"

	file_filter: Union[List[str], None] = None
	"Only process files that contain at least one of the strings in the list"

	def __post_init__(self) -> None:
		if not isinstance(self.keep_metadata, bool):
			raise TypeError

		if not isinstance(self.keep_poster, bool):
			raise TypeError

		if self.file_filter is not None:
			if not isinstance(self.file_filter, list):
				raise TypeError
			if not all(isinstance(f, str) for f in self.file_filter):
				raise TypeError

		return


@dataclass
class MediaTranscodeVars(ActionVars):
	video: Dict[str, Any]
	"The video settings defined in `media_actions.VideoTranscodeVars`."

	audio: Dict[str, Any]
	"The audio settings defined in `media_actions.AudioTranscodeVars`."

	subtitle: Dict[str, Any]
	"The subtitle settings defined in `media_actions.SubtitleTranscodeVars`."

	general: Dict[str, Any]
	"The general settings defined in `media_actions.GeneralTranscodeVars`."

	def __post_init__(self) -> None:
		for value in (self.video, self.audio, self.subtitle, self.general):
			if not isinstance(value, dict):
				raise TypeError

		self._video = VideoTranscodeVars(**self.video)
		self._audio = AudioTranscodeVars(**self.audio)
		self._subtitle = SubtitleTranscodeVars(**self.subtitle)
		self._general = GeneralTranscodeVars(**self.general)
		return


class MediaTranscode(Action):
	"""
	Transcode a media file and change the stream setups while doing so.
	"""

	var_class = MediaTranscodeVars

	def __init__(self, vars: MediaTranscodeVars) -> None:
		self.vars = vars
		return

	def __check_codecs(self) -> Tuple[str, str]:
		all_codecs = run([self.config.ffmpeg, "-codecs"], capture_output=True, text=True).stdout

		if self.vars._video.codec == "copy":
			v_result = ''
		else:
			video_match = search(
				r'^\s.EV...\s(?:(' + escape(self.vars._video.codec) + r')(?!.*?encoders)|(' + escape(self.vars._video.codec) + r').*?encoders:|(\w+)\s.*?encoders:.*\s' + escape(self.vars._video.codec) + r'\s.*\))',
				all_codecs,
				MULTILINE
			)
			if video_match is None:
				raise ValueError(f"Codec not supported by ffmpeg: {self.vars._video.codec}")
			v_result = (video_match.group(1) or video_match.group(2) or video_match.group(3)).strip()

		if self.vars._audio.codec == "copy":
			a_result = ''
		else:
			audio_match = search(
				r'^\s.EA...\s(?:(' + escape(self.vars._audio.codec) + r')(?!.*?encoders)|(' + escape(self.vars._audio.codec) + r').*?encoders:|(\w+)\s.*?encoders:.*\s' + escape(self.vars._audio.codec) + r'\s.*\))',
				all_codecs,
				MULTILINE
			)
			if audio_match is None:
				raise ValueError(f"Codec not supported by ffmpeg: {self.vars._audio.codec}")
			a_result = (audio_match.group(1) or audio_match.group(2) or audio_match.group(3)).strip()

		return (
			v_result,
			a_result
		)

	def __find_original_lang(self, file: str) -> Union[str, None]:
		if not self.vars._audio.keep_original_language:
			return None

		lang = None
		if self.config.sonarr_setup:
			try:
				result = get(
					f'{self.config.sonarr_base_url}/api/v3/parse',
					params={'path': file, 'apikey': self.config.sonarr_api_token}
				).json().get('series')
				if result and file.startswith(result['path']):
					# Found in Sonarr
					text = get(
						f"https://thetvdb.com/dereferrer/series/{result['tvdbId']}",
						headers={'User-Agent': 'December', 'Accept-Language': 'en'}
					).text
					re_result = extract_og_lang_tvdb.search(text)
					if re_result:
						lang = re_result.group(1)

			except RequestException:
				self.config.logger.warning(f'Sonarr not reachable')

		if not lang and self.config.radarr_setup:
			try:
				result = get(
					f'{self.config.radarr_base_url}/api/v3/movie',
					params={'apikey': self.config.radarr_api_token}
				).json()
				result = [m for m in result if m['path'] in file]
				if result:
					# Found in Radarr
					text = get(
						f"https://www.themoviedb.org/movie/{result[0]['tmdbId']}",
						headers={'User-Agent': 'December', 'Accept-Language': 'en'}
					).text
					re_result = extract_og_lang_tmdb.search(text)
					if re_result:
						lang = re_result.group(1)

			except RequestException:
				self.config.logger.warning(f'Radarr not reachable')

		if lang is not None:
			for lang_key, lang_vars in LANGS.items():
				if lang.lower() == lang_key or lang.lower() in lang_vars:
					return lang_key

		return None

	def __get_stream_lang(self, stream: Dict[str, Any]) -> str:
		stream_title: str = stream.get('tags', {}).get('title', '').lower()
		lang_tag: str = stream.get('tags', {}).get('language', '').lower()
		for lang_key, lang_opts in LANGS.items():
			lang_versions = [lang_key] + lang_opts
			if any(
				v == lang_tag
				or v in stream_title
				for v in lang_versions
			):
				return lang_key
		return "und"

	def __is_version(self, stream: Dict[str, Any]) -> Union[None, str]:
		stream_title: str = stream.get('tags', {}).get('title', '').lower()

		if (
			stream['disposition']['hearing_impaired']
			or
			any(term in stream_title for term in ('sdh', 'hearing impaired', 'cc'))
		):
			return 'sdh'

		if (
			stream['disposition']['forced']
			or
			'forced' in stream_title
		):
			return 'forced'

		return None

	def run(self, files: List[str]) -> List[str]:
		self.config = Config().config
		video_codec, audio_codec = self.__check_codecs()

		if self.vars._general.file_filter is not None:
			med_files = [
				file for file in files
				if file.endswith(self.config.media_filter)
					and any(f in file for f in self.vars._general.file_filter)
			]
		else:
			med_files = [
				file for file in files
				if file.endswith(self.config.media_filter)
			]

		for file in med_files:
			if getsize(file) < 1000:
				self.config.logger.error(f"File is empty: {file}")
				continue

			original_lang = self.__find_original_lang(file)
			if self.vars._audio.keep_original_language and not original_lang:
				self.config.logger.warning(f'Original language not found')

			allowed_langs: List[str] = []
			if original_lang is not None:
				allowed_langs.append(original_lang)
			if self.vars._audio.keep_languages:
				allowed_langs += self.vars._audio.keep_languages

			# Get media info
			comm = [
				self.config.ffprobe,
				'-print_format', 'json',
				'-show_format', '-show_streams',
				'-v', 'quiet',
				file
			]
			file_info: dict = loads(
				run(comm, capture_output=True, text=True).stdout
			)
			self.config.logger.debug(f"File info: {dumps(file_info, indent=4)}")
			self.config.logger.info(f"Current media file size: {int(file_info['format']['size']) // 1_048_576} MiB")

			# First filter the streams to decide what to keep and what to ditch
			poster_streams: List[Dict[str, Any]] = []
			video_streams: List[Dict[str, Any]] = []
			all_audio_streams: List[Dict[str, Any]] = []
			audio_streams: List[Dict[str, Any]] = []
			comment_streams: List[Dict[str, Any]] = []
			subs_streams: List[Dict[str, Any]] = []
			for stream in file_info["streams"]:
				stream: Dict[str, Any]
				if (
					stream["codec_type"] == "video"
					and (
						stream["disposition"]["attached_pic"]
						or stream["display_aspect_ratio"] == "2:3"
					)
				):
					# Stream is poster
					if not self.vars._general.keep_poster:
						continue
					poster_streams.append(stream)

				elif stream["codec_type"] == "video":
					# Stream is video
					if not self.vars._video.keep_video:
						continue

					video_streams.append(stream)

				elif stream["codec_type"] == "audio":
					# Stream is audio
					if not self.vars._audio.keep_audio:
						continue

					stream["__language"] = self.__get_stream_lang(stream)

					if (
						stream["disposition"]["comment"] == 1
						or "comment" in stream.get("tags", {}).get("title", "").lower()
					):
						comment_streams.append(stream)
						continue

					if (
							not self.vars._audio.keep_languages
							and stream["__language"] != "und"
						or
							self.vars._audio.keep_unknowns
							and stream["__language"] == "und"
						or
							self.vars._audio.keep_languages
							and stream["__language"] in allowed_langs
					):
						audio_streams.append(stream)

					all_audio_streams.append(stream)

				elif stream["codec_type"] == "subtitle":
					# Stream is subtitle
					if not self.vars._subtitle.keep_subtitle:
						continue

					stream["__language"] = self.__get_stream_lang(stream)
					stream["__version"] = self.__is_version(stream)

					if stream["__version"] in (self.vars._subtitle.exclude_versions or []):
						continue

					if (
						self.vars._subtitle.keep_codecs
						and not stream["codec_name"] in self.vars._subtitle.keep_codecs
					):
						continue

					if (
							not self.vars._subtitle.keep_languages
							and stream["__language"] != "und"
						or
							self.vars._subtitle.keep_unknowns
							and stream["__language"] == "und"
						or
							self.vars._subtitle.keep_languages
							and stream["__language"] in self.vars._subtitle.keep_languages
					):
						subs_streams.append(stream)

			keep_audio = [*audio_streams]
			if self.vars._audio.keep_commentary:
				keep_audio += comment_streams

			onm = self.vars._audio.on_no_matches
			if not keep_audio and onm != 'empty':
				keep_audio += all_audio_streams
				if (
					not keep_audio and onm == 'avoid_commentary'
					or
					onm == 'all'
				):
					keep_audio += comment_streams

			target_bitrate = None
			if (self.vars._video.bitrate_ratio is not None
			and file_info["format"]["bit_rate"] is not None):
				target_bitrate = float(file_info["format"]["bit_rate"]) // (1 / self.vars._video.bitrate_ratio)

			stream_settings: List[str] = []
			audio_log: List[str] = []
			index = 0

			# File metadata
			if not self.vars._general.keep_metadata:
				for tag in file_info["format"].get("tags", {}):
					stream_settings += ["-metadata", f"{tag}="]

			for stream in video_streams:
				stream_settings += ["-map", f"0:{stream['index']}"]

				# Determine if video is already in desired codec
				if (
					self.vars._video.codec == 'copy'
					or (
						not self.vars._video.force_transcode
						and stream["codec_name"] == video_codec
					)
				):
					stream_settings += [f"-codec:{index}", "copy"]

				else:
					# Change codec of video
					stream_settings += [f"-codec:{index}", self.vars._video.codec]
					if target_bitrate is not None:
						stream_settings += [f"-b:{index}", str(target_bitrate)]

				if not self.vars._general.keep_metadata:
					for tag in stream.get("tags", {}):
						stream_settings += [f"-metadata:s:{index}", f"{tag}="]

				index += 1

			for stream in poster_streams:
				stream_settings += [
					"-map", f"0:{stream['index']}",
					f"-codec:{index}", "copy",
					f"-disposition:{index}", "attached_pic"
				]

				if not self.vars._general.keep_metadata:
					for tag in stream.get("tags", {}):
						stream_settings += [f"-metadata:s:{index}", f"{tag}="]

				index += 1

			for stream in keep_audio:
				# Determine if audio is already in desired codec
				keep_codec = (
					self.vars._audio.codec == 'copy'
					or (
						not self.vars._audio.force_transcode
						and stream["codec_name"] == audio_codec
					)
				)
				codec_setting = "copy" if keep_codec else self.vars._audio.codec

				if not self.vars._audio.keep_duplicates:
					codec_name = stream["codec_name"] if keep_codec else self.vars._audio.codec
					audio_rep = f"{codec_name}|{stream['channels']}|{stream['__language']}"
					if audio_rep in audio_log:
						continue
					audio_log.append(audio_rep)

				stream_settings += [
					"-map", f"0:{stream['index']}",
					f"-codec:{index}", codec_setting
				]

				if not self.vars._general.keep_metadata:
					for tag in stream.get("tags", {}):
						if tag == "language":
							continue
						stream_settings += [f"-metadata:s:{index}", f"{tag}="]

				stream_settings += [
					f"-metadata:s:{index}", f"language={stream['__language']}",
					f"-disposition:{index}", "0"
				]

				index += 1

				if not self.vars._audio.create_channels:
					continue

				cl = stream["channel_layout"].replace("(side)", "").strip()
				channel_layout = TERM_TO_LAYOUT.get(cl, cl)

				if [channel_layout] == self.vars._audio.create_channels:
					continue

				if not channel_layout in CHANNEL_FILTERS:
					self.config.logger.warning(f"Can't create clones from channel with layout '{channel_layout}'")
					continue

				for target_clone in self.vars._audio.create_channels:
					if not target_clone in CHANNEL_FILTERS[channel_layout]:
						self.config.logger.warning(f"Converting a channel from '{channel_layout}' to '{target_clone}' is not supported")
						continue

					channel_codec = stream["codec_name"] if keep_codec else self.vars._audio.codec
					if not self.vars._audio.keep_duplicates:
						channel_count = sum((int(c) for c in target_clone.split('.')))
						audio_rep = f"{channel_codec}|{channel_count}|{stream['__language']}"
						if audio_rep in audio_log:
							continue
						audio_log.append(audio_rep)

					stream_settings += [
						"-map", f"0:{stream['index']}",
						f"-filter:{index}", CHANNEL_FILTERS[channel_layout][target_clone],
						f"-codec:{index}", channel_codec
					]

					if not self.vars._general.keep_metadata:
						for tag in stream.get("tags", {}):
							if tag == "language":
								continue
							stream_settings += [f"-metadata:s:{index}", f"{tag}="]

					stream_settings += [
						f"-metadata:s:{index}", f"language={stream['__language']}",
						f"-disposition:{index}", "0"
					]

					index += 1

			for stream in subs_streams:
				stream_settings += [
					"-map", f"0:{stream['index']}",
					f"-codec:{index}", "copy"
				]

				if stream["__version"] == "sdh":
					stream_settings += [
						f"-disposition:{index}", "hearing_impaired"
					]

				elif stream["__version"] == "forced":
					stream_settings += [
						f"-disposition:{index}", "forced"
					]

				else:
					stream_settings += [
						f"-disposition:{index}", "0"
					]

				if not self.vars._general.keep_metadata:
					for tag in stream.get("tags", {}):
						if tag == 'language':
							continue
						stream_settings += [f"-metadata:s:{index}", f"{tag}="]

				stream_settings += [
					f"-metadata:s:{index}", f"language={stream['__language']}"
				]

				index += 1

			if self.vars._video.preset:
				preset_settings = ["-preset", self.vars._video.preset]
			else:
				preset_settings = []

			output_file = splitext(file)[0] + '.transcoded.mkv'
			comm = [
				self.config.ffmpeg, "-y",
				"-v", "quiet",
				"-progress", "-",
				"-stats_period", "7",
				"-strict", "2",
				"-i", file,
			] + preset_settings + stream_settings + [output_file]
			self.config.logger.debug(f'Settings used for transcode: {" ".join(comm)}')

			proc = Popen(comm, stdout=PIPE, text=True)
			if proc.stdout is None:
				proc.wait()
			else:
				duration = float(file_info["format"]["duration"]) * 1_000_000
				stats = {
					"out_time_ms": 0.0,
					"speed": 0.0,
					"fps": 0.0
				}
				for line in proc.stdout:
					key, value = line.split("=")
					key = key.strip()
					value = value.strip()
					if key == "out_time_ms" and value != "N/A":
						stats[key] = float(value)

					elif key == "speed" and value != "N/A":
						stats[key] = float(value.strip(" x"))

					elif key == "fps" and value != "N/A":
						stats[key] = float(value)

					elif (
						key == "progress"
						and stats["speed"]
						and stats["out_time_ms"]
					):
						progress = stats["out_time_ms"] / duration * 100
						etr = abs(duration - stats["out_time_ms"]) / stats["speed"] / 1_000_000 / 60
						self.config.logger.info(f"{progress:.0f}%	| {stats['fps']:.0f} FPS	| {etr:.1f} minutes remaining")

			self.config.logger.info(f"New media file size: {getsize(output_file) // 1_048_576} MiB")
			if proc.returncode:
				# Failed
				remove(output_file)
				self.config.logger.error("Something went wrong")
				with open(self.config.error_file, 'a') as f:
					f.write(file + '\n')

			else:
				# Success
				remove(file)
				while isfile(file):
					sleep(0.1)
				move(output_file, file)

		return files
