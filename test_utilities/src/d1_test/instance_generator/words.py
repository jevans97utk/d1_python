#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Random words

A selection of 1000 words pulled randomly from /usr/share/dict/words using the
randomWords method below.
"""

import codecs
import random

# Yapf gets into some kind of worst case performance when formatting this,
# so we disable it.
# yapf: disable
WORDS_1K = [
  u'untrimmed', u'Hydriote', u'burnish', u'tsia', u'petiolary', u'vocative',
  u'incensement', u'periodic', u'Klikitat', u'stipendiarian', u'witchwood',
  u'congressionally', u'caftaned', u'heartsease', u'mezcal', u'ostensibility',
  u'caudotibialis', u'adenopharyngeal', u'cyanophoric', u'unattempting',
  u'seawoman', u'interlaced', u'outquaff', u'topgallant', u'Mesohippus',
  u'geraniaceous', u'Gelechia', u'autothermy', u'dowie', u'Sorbus', u'fortlet',
  u'inferiorism', u'cystopyelitis', u'slart', u'bestench', u'Odontaspidae',
  u'cautioner', u'stowbordman', u'amphivasal', u'heroicity', u'unpatronizable',
  u'cockhorse', u'purtenance', u'indocible', u'untimedness', u'viscus',
  u'reinvolve', u'celiectomy', u'outcut', u'unsupped', u'nonamputation',
  u'syphilogenesis', u'seaplane', u'courtezanry', u'Coregonus', u'middlewards',
  u'submeningeal', u'unmethodicalness', u'duraplasty', u'aflagellar',
  u'semicriminal', u'caudally', u'mycetism', u'profiteering', u'nephridium',
  u'subobscure', u'unjointured', u'magnetostriction', u'membranocartilaginous',
  u'iteming', u'bestiality', u'illuminating', u'restoration', u'multisect',
  u'bellows', u'thalassinid', u'midweekly', u'typhloenteritis', u'Castilloa',
  u'betail', u'synoeciously', u'receiptor', u'syntypicism', u'gunyeh',
  u'sluggishly', u'landwhin', u'plaud', u'scrutinizingly', u'twanginess',
  u'diphyodont', u'sibship', u'sisham', u'stradine', u'geotechnic',
  u'recompetitor', u'tieback', u'coracoid', u'trapezohedron', u'beclog',
  u'diathermy', u'recrementitial', u'thaumaturgic', u'malengine', u'advanced',
  u'musicographer', u'algraphic', u'Rhinosporidium', u'absinthian', u'reman',
  u'dispositively', u'innocency', u'irresistance', u'lumbricoid',
  u'portulacaceous', u'fruitwise', u'kilostere', u'ascogonium', u'laughful',
  u'monoliteral', u'polytonic', u'ramfeezled', u'idiotry', u'subterrene',
  u'weakishness', u'lockbox', u'apronful', u'Dike', u'regrating',
  u'Hispaniolize', u'scazontic', u'Cyclosporeae', u'yez', u'Phylloceratidae',
  u'grangerite', u'brightsmith', u'amorphic', u'eudaemonical', u'butanolide',
  u'monetary', u'omental', u'macrostylospore', u'lam', u'Buddha', u'immerd',
  u'breediness', u'osmetic', u'ampyx', u'transaccidentation', u'fluoridation',
  u'domatophobia', u'sculpt', u'futural', u'auxanology', u'chalcographic',
  u'Anglophobiac', u'dealership', u'catelectrotonus', u'outfable',
  u'revealability', u'efflorescence', u'proczarist', u'forebody', u'unsteck',
  u'Darrell', u'blastid', u'piation', u'beetle', u'Batrachospermum',
  u'additionist', u'descriptionless', u'Alliaceae', u'carbanil', u'unboat',
  u'demifigure', u'amy', u'Anne', u'cereous', u'Platystomidae', u'antistrophic',
  u'daughterhood', u'probuilding', u'unrealizable', u'nonabstemious',
  u'tattlery', u'bicrescentic', u'arcking', u'tai', u'somepart',
  u'Potamochoerus', u'crookbacked', u'picturer', u'Smintheus', u'beauism',
  u'uprear', u'uncorseted', u'housebreaker', u'overconservatively',
  u'cerussite', u'Triangula', u'pesthouse', u'stoppableness', u'nebularization',
  u'escalloniaceous', u'helminthological', u'nondisinterested', u'popish',
  u'enlard', u'creosol', u'untransported', u'intermaxillar', u'incessable',
  u'enterolithiasis', u'semisacerdotal', u'unpointed', u'Deuterostomata',
  u'marbler', u'quaternate', u'willer', u'puddening', u'rapiner', u'bisexed',
  u'idolatrousness', u'undarkened', u'handicraftsmanship', u'oystered',
  u'stromateoid', u'thermostable', u'multiseated', u'panclastic', u'fifie',
  u'unnullified', u'sanguinivorous', u'hellborn', u'hypermetamorphic',
  u'telemetrical', u'V', u'continuando', u'phenoplast', u'invection',
  u'ostreiculturist', u'swaler', u'irritableness', u'impingence', u'Liparian',
  u'dosimetric', u'unplanned', u'Johannine', u'alkalinuria', u'semipenniform',
  u'goldbug', u'ameliorativ', u'ratwood', u'employless', u'unsusceptibility',
  u'multilaminar', u'burrito', u'psoriatic', u'kele', u'enterprising', u'begob',
  u'chaplain', u'hosting', u'nundine', u'spectroelectric', u'extracapsular',
  u'Alcicornium', u'westering', u'droop', u'deferrization', u'columbotitanate',
  u'hyperacid', u'enantiomorphism', u'flexured', u'sangreeroot', u'seizure',
  u'saumon', u'Ismaelitish', u'glyconin', u'brekkle', u'acotyledonous',
  u'crispness', u'upcrop', u'spermatangium', u'Melinae', u'cateran',
  u'momentariness', u'paintingness', u'radiometry', u'ballooner', u'arthropod',
  u'mincemeat', u'thyroidean', u'asterion', u'poetastry', u'penetrology',
  u'querimoniousness', u'hypha', u'strident', u'unclouded', u'obfuscous',
  u'regulatorship', u'scaffold', u'acclinal', u'isochroous', u'glossoid',
  u'infecter', u'venenation', u'antennal', u'funds', u'cantoon', u'chrysoprase',
  u'taleteller', u'effeteness', u'apathetic', u'postclavicular', u'radialia',
  u'guimpe', u'succeedingly', u'Lum', u'overhumanize', u'winnelstrae',
  u'unfloor', u'nonperishing', u'lovelessly', u'Rebeccaism', u'dobbing',
  u'epileptogenic', u'imperialization', u'sniffle', u'swanwort', u'necremia',
  u'subbranchial', u'octogynious', u'mystagogy', u'cavalry', u'sclerized',
  u'relower', u'latheron', u'trimetrical', u'crackmans', u'oxyrhine',
  u'beastling', u'trackman', u'unheler', u'necessitude', u'hypocarpium',
  u'intertriglyph', u'Quaitso', u'poker', u'innumerous', u'reassay',
  u'turbinated', u'collins', u'misderive', u'anticyclic', u'diplocardiac',
  u'pavonated', u'perithyroiditis', u'geisha', u'suppressor', u'gametogony',
  u'whyfor', u'Kuneste', u'emu', u'anoxemic', u'overrapture', u'dearworthiness',
  u'typical', u'isolability', u'cheesemonger', u'conduplicate', u'enervator',
  u'prideless', u'Soja', u'oreophasine', u'Bilin', u'acanthopod', u'iconoscope',
  u'dispensingly', u'coleopteran', u'thoracoscope', u'trump', u'azofication',
  u'gentisein', u'nigglingly', u'monotrematous', u'vota', u'mesopleuron',
  u'encephalomalacosis', u'demean', u'fesswise', u'coecal', u'overdosage',
  u'nourishingly', u'pluriflagellate', u'conformably', u'podothecal', u'hamingja',
  u'calomorphic', u'unejected', u'eristical', u'pseudofeverish', u'duckwing',
  u'revealed', u'cleaning', u'ricinelaidic', u'cononintelligent', u'Sidalcea',
  u'megalosplenia', u'noncrustaceous', u'inswept', u'pennyworth', u'pitcherlike',
  u'crystallography', u'phobic', u'Eldred', u'encolor', u'barkey', u'Timonize',
  u'undevoted', u'blepharoplasty', u'proselytize', u'impending', u'triacid',
  u'thallogenous', u'coreflexed', u'tubuliferan', u'onflowing', u'genioglossi',
  u'malcultivation', u'chlorometer', u'ransom', u'stereoplasm', u'quacksalver',
  u'asiento', u'Slavey', u'kuttab', u'centauromachia', u'distributee', u'forged',
  u'coberger', u'bravado', u'contortioned', u'producership', u'splanchnesthetic',
  u'strangletare', u'reversability', u'Casuarinaceae', u'disquietly', u'mobsman',
  u'mistful', u'bureaucracy', u'miscarriage', u'Huma', u'manufacture',
  u'twitteration', u'hyperpyrexial', u'gildable', u'twinkledum', u'dolmen',
  u'trachyphonous', u'unpreventable', u'Avicenniaceae', u'Viperoidea', u'bemirror',
  u'interbank', u'interdictive', u'betterly', u'tribunate', u'exteroceptor',
  u'belemnid', u'discontiguousness', u'skimmerton', u'aldermancy', u'estrepe',
  u'nondisclosure', u'irreformable', u'diatropism', u'scleromeninx', u'spithame',
  u'Astropecten', u'pommee', u'puerperalism', u'anaerobiont', u'disjointedness',
  u'comart', u'hyperanabolic', u'scholaptitude', u'houseboating', u'stadion',
  u'hyperexcitability', u'unbetoken', u'Amanitopsis', u'duction', u'minimize',
  u'visionmonger', u'infracortical', u'histamine', u'pluviometrical', u'wail',
  u'euhemerize', u'fingerprint', u'nematozooid', u'nonstudent', u'outport',
  u'athericerous', u'Arthuriana', u'Brahmanistic', u'victless', u'steelification',
  u'phraseologist', u'synonymous', u'vocular', u'moisture', u'albumean',
  u'sheldapple', u'mysel', u'Languedocian', u'ironical', u'unancient', u'rabitic',
  u'unexcrescent', u'tonguecraft', u'revulsion', u'learnedly', u'officerhood',
  u'flatulence', u'tubiporous', u'gignitive', u'archpatron', u'deliveryman',
  u'russety', u'pseudoencephalitic', u'electrostatics', u'Edith', u'septangular',
  u'noop', u'subrhomboidal', u'crowdedness', u'lecyth', u'hemigeusia',
  u'afterhold', u'verticillary', u'gimcrackery', u'Cetonia', u'Binitarian',
  u'ureal', u'sympathizing', u'bocardo', u'unrustling', u'dragsman', u'Hunyak',
  u'infusibility', u'snowcap', u'Pernettia', u'definitive', u'unconceited',
  u'unlid', u'underbury', u'creasy', u'amatrice', u'violable', u'hailse',
  u'expansionist', u'interluder', u'Snohomish', u'glaister', u'unsprouting',
  u'semantological', u'penumbral', u'filefish', u'plumagery', u'drail',
  u'immethodic', u'Acalypha', u'Hexagynia', u'hydrostat', u'sylphish',
  u'semuncia', u'sixhynde', u'unprosaic', u'lamblike', u'postrubeolar',
  u'tempestuousness', u'seemless', u'addiment', u'equilibrize', u'bandiness',
  u'unscotch', u'insphere', u'myeloblastic', u'unbrookable', u'eccentrate',
  u'multihearth', u'buckwasher', u'racketeer', u'hazel', u'frugivorous',
  u'jugation', u'Thebaic', u'wonting', u'aliturgic', u'vedika', u'enumerate',
  u'nonexistent', u'rudderstock', u'cognation', u'unpinched', u'verminproof',
  u'Kieffer', u'unyieldingness', u'unchiseled', u'Clupeodei', u'satyr',
  u'outquestion', u'oviparous', u'Leptotyphlops', u'thoracodorsal', u'Memphite',
  u'matronage', u'dentatocrenate', u'brimmingly', u'bingey', u'Wakore',
  u'Tagakaolo', u'enclaret', u'gliderport', u'hurr', u'unfrankly', u'Baianism',
  u'sandy', u'noncombining', u'carpingly', u'perverseness', u'rip', u'entitle',
  u'brakeless', u'Franklinian', u'sulfantimonide', u'biscacha', u'Isiacal',
  u'pilferingly', u'tucky', u'pilfering', u'vitrotype', u'isolative', u'Algieba',
  u'Hyolithes', u'xanthoprotein', u'impudent', u'pollinigerous', u'imaginer',
  u'underlinen', u'unadornable', u'scelotyrbe', u'scratchwork', u'unread',
  u'supersensualism', u'exfoliatory', u'docket', u'dysarthrosis', u'invaginable',
  u'nonrefrigerant', u'aumrie', u'pantle', u'Trisagion', u'antipatheticalness',
  u'snowbreak', u'uninfluentiality', u'unicornlike', u'methylsulfanol',
  u'melongena', u'megaphotography', u'untempested', u'slackage', u'retiform',
  u'counterexaggeration', u'breastweed', u'thermotaxis', u'shootboard',
  u'bituminization', u'wordily', u'rocambole', u'styptical', u'interpolation',
  u'abreast', u'resounding', u'officeless', u'deepening', u'slideproof', u'rookish',
  u'nontimbered', u'neurohypnology', u'meece', u'phytophysiology', u'plethory',
  u'postcoxal', u'anatomicophysiologic', u'unatoned', u'recollected', u'margent',
  u'autoallogamy', u'retractibility', u'monosulfone', u'unpsychic', u'swank',
  u'unprofessed', u'Tantalic', u'stickle', u'cocarboxylase', u'unwhistled',
  u'ovateconical', u'lancewood', u'supracentenarian', u'pretelephonic',
  u'mandriarch', u'chondroendothelioma', u'liftless', u'subclaim', u'catenate',
  u'thema', u'unangelical', u'leadiness', u'valuelessness', u'debituminization',
  u'numskulledness', u'caustically', u'zoodynamic', u'sexennially', u'uncrystaled',
  u'stocktaker', u'gainsayer', u'lilacthroat', u'phrenosinic', u'liveness',
  u'unweld', u'copolymer', u'utrubi', u'gerenuk', u'adfluxion', u'jingoist',
  u'gastrosplenic', u'introspectional', u'alphorn', u'daftly', u'Xiphosurus',
  u'Eudora', u'dogfall', u'hemiramph', u'craver', u'merogamy', u'hilltop',
  u'archmonarchist', u'palewise', u'spectacular', u'circumambience', u'breastwork',
  u'multiplane', u'unattributed', u'trinomialist', u'whereness', u'hawbuck',
  u'bronzewing', u'unfabulous', u'remigrant', u'loy', u'sulphantimonious',
  u'zygodactylic', u'pulleyless', u'nifling', u'metrorrhagic', u'condemnable',
  u'bejuggle', u'kylite', u'unfactored', u'subrogate', u'coruscant',
  u'showable', u'ophiasis', u'revictorious', u'carlin', u'expansional',
  u'journalizer', u'observatory', u'pursuitmeter', u'subchorionic', u'molary',
  u'blub', u'unchangedness', u'garran', u'suitability', u'septenary', u'woak',
  u'Zygnemaceae', u'noncompetent', u'periphysis', u'flam', u'chinawoman',
  u'dactylioglyphy', u'outlaw', u'preachification', u'trochilus', u'descale',
  u'neurohypnotic', u'sexualism', u'matranee', u'chromaticity', u'Herbartianism',
  u'scapethrift', u'nectarium', u'bromelin', u'institutionalism', u'Cinchona',
  u'slighted', u'muzzle', u'introducement', u'osteomyelitis', u'victordom',
  u'granitize', u'glossologist', u'decolorimeter', u'magniloquently',
  u'peptonaemia', u'cacomorphosis', u'orthography', u'phalera', u'montane',
  u'dyeleaves', u'subendocardial', u'Cistercian', u'bryological', u'rectangular',
  u'formaldehydesulphoxylate', u'infraocclusion', u'unoppressed', u'dairymaid',
  u'r', u'vasostimulant', u'pachyodont', u'luncheoner', u'garibaldi',
  u'hypertrophy', u'counternarrative', u'metascutellar', u'Keftiu', u'petrie',
  u'torchwood', u'gnostically', u'unroot', u'fig', u'Nemalionales',
  u'profiting', u'vagaristic', u'lormery', u'gurgoyle', u'intercurl', u'evoke',
  u'diabrosis', u'reactuate', u'gluma', u'prostheca', u'fernshaw', u'barras',
  u'Filaria', u'domnei', u'punctule', u'appropinquity', u'renavigate',
  u'unsafeguarded', u'tyrotoxicon', u'Vaseline', u'incalculable', u'outsound',
  u'logos', u'cicatrisive', u'hypertetrahedron', u'gopher', u'bathymetrically',
  u'allelomorph', u'intransigentism', u'petalite', u'removal', u'cleistothecium',
  u'sulphohydrate', u'cloverroot', u'fossilism', u'Manacus', u'Lophophorinae',
  u'predispositional', u'pachydermatocele', u'coroneted', u'fivefoldness',
  u'matronship', u'suggest', u'intraimperial', u'bigamic', u'introsuction',
  u'assailer', u'petrolific', u'beachcomber', u'nonconformer', u'antiattrition',
  u'fashiousness', u'scincoid', u'fjeld', u'subgeneric', u'uranoscope', u'purree',
  u'foggy', u'velvety', u'comprehensor', u'equilocation', u'impostorship',
  u'unskillful', u'cervicaprine', u'styceric', u'Corinna', u'paleotechnic',
  u'propolis', u'marquis', u'fulvid', u'monumental', u'noneastern', u'lapped',
  u'wyliecoat', u'moldwarp', u'pyloroscopy', u'congruously', u'mathematic',
  u'dorsiduct', u'uncriticisingly', u'pretemperate', u'epigene', u'battleward',
  u'hematocrit', u'trochitic', u'scythestone', u'pachydermatously',
  u'equiangle', u'overpour', u'underreckon', u'trionychoid', u'aortarctia',
  u'geophagia', u'hagiography', u'nub', u'simar', u'gourmet', u'dont',
  u'islandy', u'mothersome', u'unballasted', u'coloradoite', u'quadrifoliate',
  u'mugient', u'fipple', u'tapaculo', u'Hyphaene', u'wirble', u'ammodytoid',
  u'hydrotherapy', u'Marattiaceae', u'miscellaneousness', u'Esselenian',
  u'viatometer', u'demephitize', u'trophophorous', u'extort', u'namesake',
  u'cutaneal', u'therewhile', u'testing', u'Treculia', u'archworkmaster',
  u'nonattestation', u'chastely', u'Marathonian', u'earsore', u'amende',
  u'navette', u'unscanted', u'quashy', u'noncontradiction', u'berthing',
  u'reck', u'graze', u'foil', u'antipragmatist', u'uptree', u'recolonize',
  u'dianodal', u'gyromagnetic', u'subpanel', u'rumblegarie', u'hermitism',
  u'Anglify', u'Cycadofilicales', u'townland', u'chlorophenol', u'mouseproof'
]


def _count_lines(source):
  f = file(source, 'r')
  bufsize = 8192
  buf = f.read(bufsize)
  lc = buf.count('\n')
  while len(buf) == bufsize:
    buf = f.read(bufsize)
    lc += buf.count('\n')
  f.close()
  return lc


def random_words(count=100, source='/usr/share/dict/words'):
  """Returns a random selection of count words from WORDS_1K or by reading
  from source if the number of words requested is more than available in
  WORDS_1K.
  """
  if len(WORDS_1K) > count:
    return random.sample(WORDS_1K, count)
  nlines = _count_lines(source)
  linenos = random.sample(xrange(0, nlines - 1), count)
  linenos.sort()
  words = []
  fsrc = codecs.open(source, 'r', 'utf-8')
  cline = 0
  cpos = 0
  while cpos < count:
    while cline < linenos[cpos]:
      line = fsrc.readline()
      cline += 1
    words.append(line.strip())
    cpos += 1
  random.shuffle(words)
  return words