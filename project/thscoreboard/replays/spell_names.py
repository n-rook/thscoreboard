from immutabledict import immutabledict
from django.utils.translation import get_language

spell_names_en = immutabledict({
    'th08': (
        'Firefly Sign "Earthly Meteor"',
        'Firefly Sign "Earthly Comet"',
        'Lamp Sign "Firefly Phenomenon"',
        'Lamp Sign "Firefly Phenomenon"',
        'Lamp Sign "Firefly Phenomenon"',
        'Lamp Sign "Firefly Phenomenon"',
        'Wriggle Sign "Little Bug"',
        'Wriggle Sign "Little Bug Storm"',
        'Wriggle Sign "Nightbug Storm"',
        'Wriggle Sign "Nightbug Tornado"',
        'Hidden Bug "Endless Night Seclusion"',
        'Hidden Bug "Endless Night Seclusion"',
        'Hidden Bug "Endless Night Seclusion"',
        'Vocal Sign "Hooting in the Night"',
        'Vocal Sign "Hooting in the Night"',
        'Vocal Sign "Howl of the Horned Owl"',
        'Vocal Sign "Howl of the Horned Owl"',
        'Moth Sign "Hawk Moth\'s Insect Curse"',
        'Moth Sign "Hawk Moth\'s Insect Curse"',
        'Toxin Sign "Poisonous Moth\'s Scales"',
        'Deadly Toxin "Poisonous Moth\'s Dance in the Dark"',
        'Hawk Sign "Ill-Starred Dive"',
        'Hawk Sign "Ill-Starred Dive"',
        'Hawk Sign "Ill-Starred Dive"',
        'Hawk Sign "Ill-Starred Dive"',
        'Night-Blindness "Song of the Night Sparrow"',
        'Night-Blindness "Song of the Night Sparrow"',
        'Night-Blindness "Song of the Night Sparrow"',
        'Night-Blindness "Song of the Night Sparrow"',
        'Night-Sparrow "Midnight Chorus-Master"',
        'Night-Sparrow "Midnight Chorus-Master"',
        'Night-Sparrow "Midnight Chorus-Master"',
        'Spiritual Birth "First Pyramid"',
        'Spiritual Birth "First Pyramid"',
        'Spiritual Birth "First Pyramid"',
        'Spiritual Birth "First Pyramid"',
        'Origin Sign "Ephemerality 137"',
        'Origin Sign "Ephemerality 137"',
        'Origin Sign "Ephemerality 137"',
        'Ambition Sign "Buretsu Crisis"',
        'Ambition Sign "Masakado Crisis"',
        'Ambition Sign "Yoshimitsu Crisis"',
        'Ambition Sign "General Headquarters Crisis"',
        'Land Sign "Three Sacred Treasures - Sword"',
        'Land Sign "Three Sacred Treasures - Orb"',
        'Land Sign "Three Sacred Treasures - Mirror"',
        'Land Scheme "Three Sacred Treasures - Country"',
        'Ending Sign "Phantasmal Emperor"',
        'Ending Sign "Phantasmal Emperor"',
        'Pseudo-History "The Legend of Gensokyo"',
        'Pseudo-History "The Legend of Gensokyo"',
        'Future "Gods\' Realm"',
        'Future "Gods\' Realm"',
        'Future "Gods\' Realm"',
        'Dream Sign "Duplex Barrier"',
        'Dream Sign "Duplex Barrier"',
        'Dream Land "Great Duplex Barrier"',
        'Dream Land "Great Duplex Barrier"',
        'Spirit Sign "Fantasy Seal -Spread-"',
        'Spirit Sign "Fantasy Seal -Spread-"',
        'Scattered Spirit "Fantasy Seal -Worn-"',
        'Scattered Spirit "Fantasy Seal -Worn-"',
        'Dream Sign "Evil-Sealing Circle"',
        'Dream Sign "Evil-Sealing Circle"',
        'Divine Arts "Omnidirectional Oni-Binding Circle"',
        'Divine Arts "Omnidirectional Dragon-Slaying Circle"',
        'Spirit Sign "Fantasy Seal -Concentrate-"',
        'Spirit Sign "Fantasy Seal -Concentrate-"',
        'Migrating Spirit "Fantasy Seal -Marred-"',
        'Migrating Spirit "Fantasy Seal -Marred-"',
        'Boundary "Duplex Danmaku Barrier"',
        'Boundary "Duplex Danmaku Barrier"',
        'Great Barrier "Hakurei Danmaku Barrier"',
        'Great Barrier "Hakurei Danmaku Barrier"',
        'Divine Spirit "Fantasy Seal -Blink-"',
        'Divine Spirit "Fantasy Seal -Blink-"',
        'Divine Spirit "Fantasy Seal -Blink-"',
        'Magic Sign "Milky Way"',
        'Magic Sign "Milky Way"',
        'Magic Space "Asteroid Belt"',
        'Magic Space "Asteroid Belt"',
        'Magic Sign "Stardust Reverie"',
        'Magic Sign "Stardust Reverie"',
        'Black Magic "Event Horizon"',
        'Black Magic "Event Horizon"',
        'Love Sign "Non-Directional Laser"',
        'Love Sign "Non-Directional Laser"',
        'Love Storm "Starlight Typhoon"',
        'Love Storm "Starlight Typhoon"',
        'Love Sign "Master Spark"',
        'Love Sign "Master Spark"',
        'Loving Heart "Double Spark"',
        'Loving Heart "Double Spark"',
        'Light Sign "Earthlight Ray"',
        'Light Sign "Earthlight Ray"',
        'Light Blast "Shoot the Moon"',
        'Light Blast "Shoot the Moon"',
        'Magicannon "Final Spark"',
        'Magicannon "Final Spark"',
        'Magicannon "Final Master Spark"',
        'Wave Sign "Red-Eyed Hypnosis (Mind Shaker)"',
        'Wave Sign "Red-Eyed Hypnosis (Mind Shaker)"',
        'Illusion Wave "Red-Eyed Hypnosis (Mind Blowing)"',
        'Illusion Wave "Red-Eyed Hypnosis (Mind Blowing)"',
        'Lunatic Sign "Hallucinogenic Tuning (Visionary Tuning)"',
        'Lunatic Sign "Hallucinogenic Tuning (Visionary Tuning)"',
        'Lunatic Gaze "Lunatic Stare Tuning (Illusion Seeker)"',
        'Lunatic Gaze "Lunatic Stare Tuning (Illusion Seeker)"',
        'Loafing Sign "Life & Spirit Stopping (Idling Wave)"',
        'Loafing Sign "Life & Spirit Stopping (Idling Wave)"',
        'Indolence "Life & Spirit Stopping (Mind Stopper)"',
        'Indolence "Life & Spirit Stopping (Mind Stopper)"',
        'Spread Sign "Moon of Truth (Invisible Full Moon)"',
        'Spread Sign "Moon of Truth (Invisible Full Moon)"',
        'Spread Sign "Moon of Truth (Invisible Full Moon)"',
        'Spread Sign "Moon of Truth (Invisible Full Moon)"',
        'Lunar Eyes "Lunar Rabbit\'s Remote Mesmerism (Tele-Mesmerism)"',
        'Lunar Eyes "Lunar Rabbit\'s Remote Mesmerism (Tele-Mesmerism)"',
        'Lunar Eyes "Lunar Rabbit\'s Remote Mesmerism (Tele-Mesmerism)"',
        'Spacesphere "Earth in a Pot"',
        'Spacesphere "Earth in a Pot"',
        'Spacesphere "Earth in a Pot"',
        'Spacesphere "Earth in a Pot"',
        'Awakened God "Memories of the Age of the Gods"',
        'Awakened God "Memories of the Age of the Gods"',
        'God Sign "Genealogy of the Celestials"',
        'God Sign "Genealogy of the Celestials"',
        'Revival "Seimei Yūgi -Life Game-"',
        'Revival "Seimei Yūgi -Life Game-"',
        'Resurrection "Rising Game"',
        'Resurrection "Rising Game"',
        'Leading God "Omoikane\'s Device"',
        'Leading God "Omoikane\'s Device"',
        'Mind of God "Omoikane\'s Brain"',
        'Mind of God "Omoikane\'s Brain"',
        'Curse of the Heavens "Apollo 13"',
        'Curse of the Heavens "Apollo 13"',
        'Curse of the Heavens "Apollo 13"',
        'Curse of the Heavens "Apollo 13"',
        'Esoterica "Astronomical Entombing"',
        'Esoterica "Astronomical Entombing"',
        'Esoterica "Astronomical Entombing"',
        'Esoterica "Astronomical Entombing"',
        'Forbidden Elixir "Hourai Elixir"',
        'Forbidden Elixir "Hourai Elixir"',
        'Forbidden Elixir "Hourai Elixir"',
        'Forbidden Elixir "Hourai Elixir"',
        'Medicine Sign "Galaxy in a Pot"',
        'Medicine Sign "Galaxy in a Pot"',
        'Medicine Sign "Galaxy in a Pot"',
        'Medicine Sign "Galaxy in a Pot"',
        'Impossible Request "Dragon\'s Neck\'s Jewel -Five-Colored Shots-"',
        'Impossible Request "Dragon\'s Neck\'s Jewel -Five-Colored Shots-"',
        'Divine Treasure "Brilliant Dragon Bullet"',
        'Divine Treasure "Brilliant Dragon Bullet"',
        'Impossible Request "Buddha\'s Stone Bowl -Indomitable Will-"',
        'Impossible Request "Buddha\'s Stone Bowl -Indomitable Will-"',
        'Divine Treasure "Buddhist Diamond"',
        'Divine Treasure "Buddhist Diamond"',
        'Impossible Request "Robe of Fire Rat -Patient Mind-"',
        'Impossible Request "Robe of Fire Rat -Patient Mind-"',
        'Divine Treasure "Salamander Shield"',
        'Divine Treasure "Salamander Shield"',
        'Impossible Request "Swallow\'s Cowrie Shell -Everlasting Life-"',
        'Impossible Request "Swallow\'s Cowrie Shell -Everlasting Life-"',
        'Divine Treasure "Life Spring Infinity"',
        'Divine Treasure "Life Spring Infinity"',
        'Impossible Request "Bullet Branch of Hourai -Rainbow Danmaku-"',
        'Impossible Request "Bullet Branch of Hourai -Rainbow Danmaku-"',
        'Divine Treasure "Jeweled Branch of Hourai -Dreamlike Paradise-"',
        'Divine Treasure "Jeweled Branch of Hourai -Dreamlike Paradise-"',
        '"End of Imperishable Night -New Moon-"',
        '"End of Imperishable Night -Crescent Moon-"',
        '"End of Imperishable Night -1st Quarter\'s Moon-"',
        '"End of Imperishable Night -Matsuyoi-"',
        '"End of Imperishable Night -11 o\'Clock-"',
        '"End of Imperishable Night -Half to Midnight-"',
        '"End of Imperishable Night -Midnight-"',
        '"End of Imperishable Night -Half Past Midnight-"',
        '"End of Imperishable Night -1 o\'Clock-"',
        '"End of Imperishable Night -Half Past 1-"',
        '"End of Imperishable Night -Dead of Night-"',
        '"End of Imperishable Night -Half Past 2-"',
        '"End of Imperishable Night -3 o\'Clock-"',
        '"End of Imperishable Night -Half Past 3-"',
        '"End of Imperishable Night -4 o\'Clock-"',
        '"End of Imperishable Night -Half Past 4-"',
        '"End of Imperishable Night -Morning Mist-"',
        '"End of Imperishable Night -Dawn-"',
        '"End of Imperishable Night -Morning Star-"',
        '"End of Imperishable Night -Rising World-"',
        'Past "Old History of an Untrodden Land -Old History-"',
        'Reincarnation "Ichijou Returning Bridge"',
        'Future "New History of Fantasy -Next History-"',
        'Limiting Edict "Curse of Tsuki-no-Iwakasa"',
        'Undying "Fire Bird -Feng Wing Ascension-"',
        'Fujiwara "Wounds of Metsuzai Temple"',
        'Undying "Xu Fu\'s Dimension"',
        'Expiation "Honest Man\'s Death"',
        'Hollow Being "Wu"',
        'Inextinguishable "Phoenix\'s Tail"',
        'Hourai "South Wind, Clear Sky -Fujiyama Volcano-"',
        '"Possessed by Phoenix"',
        '"Hourai Doll"',
        '"Imperishable Shooting"',
        '"Unseasonal Butterfly Storm"',
        '"Blind Nightbird"',
        '"Emperor of the Land of the Rising Sun"',
        '"Stare of the Hazy Phantom Moon (Lunatic Red Eyes)"',
        '"Heaven Spider\'s Butterfly-Capturing Web"',
        '"Tree-Ocean of Hourai"',
        '"Phoenix Rebirth"',
        '"Ancient Duper"',
        '"Total Purification"',
        '"Fantasy Nature"',
        '"Blazing Star"',
        '"Deflation World"',
        '"Matsuyoi-Reflecting Satellite Slash"',
        '"The Phantom of the Grand Guignol"',
        '"Scarlet Destiny"',
        '"Saigyouji Parinirvana"',
        '"Profound Danmaku Barrier -Phantasm, Foam, and Shadow-"',
    ),
    'th13': (
        'Symbol "Dance of the Dead Butterflies"',
        'Symbol "Dance of the Dead Butterflies"',
        'Symbol "Dance of the Dead Butterflies - Cherry Blossoms -"',
        'Symbol "Dance of the Dead Butterflies - Cherry Blossoms -"',
        'Ghostly Butterfly "Ghost Spot"',
        'Ghostly Butterfly "Ghost Spot"',
        'Ghostly Butterfly "Ghost Spot - Cherry Blossoms -"',
        'Ghostly Butterfly "Ghost Spot - Cherry Blossoms -"',
        'Nether Sign "Endless Evening Cherry Blossoms"',
        'Nether Sign "Endless Evening Cherry Blossoms"',
        'Nether Sign "Endless Evening Cherry Blossoms"',
        'Nether Sign "Endless Evening Cherry Blossoms"',
        'Cherry Blossom Sign "Saigyou Cherry Blossom Blizzard"',
        'Cherry Blossom Sign "Saigyou Cherry Blossom Blizzard"',
        'Echo Sign "Mountain Echo"',
        'Echo Sign "Mountain Echo"',
        'Echo Sign "Mountain Echo Scramble"',
        'Echo Sign "Mountain Echo Scramble"',
        'Echo Sign "Power Resonance"',
        'Echo Sign "Power Resonance"',
        'Echo Sign "Power Resonance"',
        'Echo Sign "Power Resonance"',
        'Mountain Echo "Long-Range Echo"',
        'Mountain Echo "Long-Range Echo"',
        'Mountain Echo "Amplify Echo"',
        'Mountain Echo "Amplify Echo"',
        'Great Voice "Charged Cry"',
        'Great Voice "Charged Cry"',
        'Great Voice "Charged Yahoo!"',
        'Great Voice "Charged Yahoo!"',
        'Rainbow Sign "Umbrella Cyclone"',
        'Rainbow Sign "Umbrella Cyclone"',
        'Recovery "Heal By Desire"',
        'Recovery "Heal By Desire"',
        'Recovery "Heal By Desire"',
        'Recovery "Heal By Desire"',
        'Poison Nail "Poison Raze"',
        'Poison Nail "Poison Raze"',
        'Poison Nail "Poison Murder"',
        'Poison Nail "Poison Murder"',
        'Desire Sign "Saved Up Desire Spirit Invitation"',
        'Desire Sign "Saved Up Desire Spirit Invitation"',
        'Desire Spirit "Score Desire Eater"',
        'Desire Spirit "Score Desire Eater"',
        'Evil Sign "Yǎng Xiǎoguǐ"',
        'Evil Sign "Gūhún Yěguǐ"',
        'Evil Sign "Gūhún Yěguǐ"',
        'Demonify "Zǒuhuǒ Rùmó"',
        'Demonify "Zǒuhuǒ Rùmó"',
        'Demonify "Zǒuhuǒ Rùmó"',
        'Demonify "Zǒuhuǒ Rùmó"',
        'Possession "Corpse Tóngjī"',
        'Possession "Corpse Tóngjī"',
        'Spirit Link "Tōnglíng Yoshika"',
        'Spirit Link "Tōnglíng Yoshika"',
        'Taoist Sign "Tao Fetal Movement"',
        'Taoist Sign "Tao Fetal Movement"',
        'Taoist Sign "Tao Fetal Movement"',
        'Taoist Sign "Tao Fetal Movement"',
        'Thunder Arrow "Gagouji\'s Cyclone"',
        'Thunder Arrow "Gagouji\'s Cyclone"',
        'Thunder Arrow "Gagouji\'s Tornado"',
        'Heaven Sign "Rainy Iwafune"',
        'Heaven Sign "Rainy Iwafune"',
        'Heaven Sign "Ame-no-Iwafune, Ascend to Heaven"',
        'Heaven Sign "Ame-no-Iwafune, Ascend to Heaven"',
        'Throwing Dishes "Mononobe\'s Eighty Saké Cups"',
        'Throwing Dishes "Mononobe\'s Eighty Saké Cups"',
        'Throwing Dishes "Mononobe\'s Eighty Saké Cups"',
        'Throwing Dishes "Mononobe\'s Eighty Saké Cups"',
        'Blaze Sign "Blazing Winds of Haibutsu"',
        'Blaze Sign "Blazing Winds of Haibutsu"',
        'Blaze Sign "Sakurai-ji in Flames"',
        'Blaze Sign "Sakurai-ji in Flames"',
        'Saint Girl "Oomonoimi\'s Dinner"',
        'Saint Girl "Oomonoimi\'s Dinner"',
        'Saint Girl "Oomonoimi\'s Dinner"',
        'Saint Girl "Oomonoimi\'s Dinner"',
        'Honor "Colors of Twelve Levels"',
        'Honor "Colors of Twelve Levels"',
        'Honor "Ranks of Twelve Levels"',
        'Honor "Ranks of Twelve Levels"',
        'Hermit Sign "Taoist of the Land of the Rising Sun"',
        'Hermit Sign "Taoist of the Land of the Rising Sun"',
        'Hermit Sign "Emperor of the Land of the Rising Sun"',
        'Hermit Sign "Emperor of the Land of the Rising Sun"',
        'Summon "Royal Clan\'s Chaotic Dance"',
        'Summon "Royal Clan\'s Chaotic Dance"',
        'Summon "Royal Clan\'s Chaotic Dance"',
        'Summon "Royal Clan\'s Chaotic Dance"',
        'Secret Treasure "Armillary Sphere of Ikaruga-dera"',
        'Secret Treasure "Armillary Sphere of Ikaruga-dera"',
        'Secret Treasure "Armillary Sphere of Ikaruga-dera"',
        'Secret Treasure "Prince Shotoku\'s Out-of-Place Artifact"',
        'Light Sign "Halo of the Guse Kannon"',
        'Light Sign "Halo of the Guse Kannon"',
        'Light Sign "Guse Flash"',
        'Light Sign "Guse Flash"',
        'Discernment "Lasers of Seventeen Articles"',
        'Discernment "Lasers of Seventeen Articles"',
        'Divine Light "Honor the Avoidance of Defiance"',
        'Divine Light "Honor the Avoidance of Defiance"',
        '"Falling Stars on Divine Spirit Mausoleum"',
        '"Falling Stars on Divine Spirit Mausoleum"',
        '"Newborn Divine Spirits"',
        '"Newborn Divine Spirits"',
        'Unknown "Will-o\'-wisps in Unknown Orbit"',
        'Unknown "Skyfish with Unknown Shape"',
        'Unknown "Youkai Orb of Unknown Mechanics"',
        'First Duel "Primate Danmaku Transformation"',
        'Second Duel "Carnivorous Danmaku Transformation"',
        'Third Duel "Avian Danmaku Transformation"',
        'Fourth Duel "Amphibian Danmaku Transformation"',
        'Fifth Duel "Scrolls of Frolicking Animals"',
        'Sixth Duel "Tanuki\'s Monstrous School"',
        'Seventh Duel "Wild Deserted Island"',
        'Transformation "Pseudo-Exorcism of the Stupid Shrine Maiden"',
        '"Mamizou Danmaku in Ten Transformations"',
        'Raccoon Sign "Full Moon Pompokolin"',
        'Cherry Blossom Sign "Cherry Blossom Blizzard Hell"',
        'Mountain Echo "Yamabiko\'s Specialty Echo Demonstration"',
        'Poison Nail "Undead Murderer"',
        'Taoist Sign "TAO Fetal Movement ~Dao~"',
        'Vengeful Spirit "Iruka\'s Thunder"',
        'Saint Girl "Sun Goddess\'s Sacrifice"',
        '"Divine Spirits\' Universe"',
        '"Wild Carpet"',
    ),
    'th14': (
        'Ice Sign "Ultimate Blizzard"',
        'Ice Sign "Ultimate Blizzard"',
        'Water Sign "Tail Fin Slap"',
        'Water Sign "Tail Fin Slap"',
        'Water Sign "Tail Fin Slap"',
        'Water Sign "Tail Fin Slap"',
        'Scale Sign "Scale Wave"',
        'Scale Sign "Scale Wave"',
        'Scale Sign "Raging Waves of the Reversed Scale"',
        'Scale Sign "Great Raging Waves of the Reversed Scale"',
        'Flight Sign "Flying Head"',
        'Flight Sign "Flying Head"',
        'Flight Sign "Flying Head"',
        'Flight Sign "Flying Head"',
        'Neck Sign "Close-Eye Shot"',
        'Neck Sign "Close-Eye Shot"',
        'Neck Sign "Rokurokubi Flight"',
        'Neck Sign "Rokurokubi Flight"',
        'Flying Head "Multiplicative Head"',
        'Flying Head "Multiplicative Head"',
        'Flying Head "Seventh Head"',
        'Flying Head "Ninth Head"',
        'Flying Head "Dullahan Night"',
        'Flying Head "Dullahan Night"',
        'Flying Head "Dullahan Night"',
        'Flying Head "Dullahan Night"',
        'Fang Sign "Moonlit Canine Teeth"',
        'Fang Sign "Moonlit Canine Teeth"',
        'Transformation "Triangle Fang"',
        'Transformation "Triangle Fang"',
        'Transformation "Star Fang"',
        'Transformation "Star Fang"',
        'Roar "Strange Roar"',
        'Roar "Strange Roar"',
        'Roar "Full Moon Howling"',
        'Roar "Full Moon Howling"',
        'Wolf Sign "Star Ring Pounce"',
        'Wolf Sign "Star Ring Pounce"',
        'Sirius "High-Speed Pounce"',
        'Sirius "High-Speed Pounce"',
        'Heikyoku "Sounds of Jetavana\'s Bell"',
        'Heikyoku "Sounds of Jetavana\'s Bell"',
        'Heikyoku "Sounds of Jetavana\'s Bell"',
        'Heikyoku "Sounds of Jetavana\'s Bell"',
        'Vengeful Spirit "Hoichi the Earless"',
        'Vengeful Spirit "Hoichi the Earless"',
        'Vengeful Spirit "Great Vengeful Spirit of Taira"',
        'Vengeful Spirit "Great Vengeful Spirit of Taira"',
        'Music Sign "Wicked Musical Score"',
        'Music Sign "Wicked Musical Score"',
        'Music Sign "Malicious Musical Score"',
        'Music Sign "Double Score"',
        'Koto Sign "Sounds of Anicca\'s Koto"',
        'Koto Sign "Sounds of Anicca\'s Koto"',
        'Koto Sign "Sounds of Anicca\'s Koto"',
        'Koto Sign "Sounds of Anicca\'s Koto"',
        'Echo Sign "Heian\'s Reverberation"',
        'Echo Sign "Heian\'s Reverberation"',
        'Echo Sign "Echo Chamber"',
        'Echo Sign "Echo Chamber"',
        'Koto Music "Social Upheaval Koto Music Complement"',
        'Koto Music "Social Upheaval Koto Music Complement"',
        'Koto Music "Social Upheaval Requiem"',
        'Koto Music "Social Upheaval Requiem"',
        'Deceit Sign "Reverse Needle Attack"',
        'Deceit Sign "Reverse Needle Attack"',
        'Deceit Sign "Reverse Needle Attack"',
        'Deceit Sign "Reverse Needle Attack"',
        'Reverse Sign "Danmaku Through the Looking-Glass"',
        'Reverse Sign "Danmaku Through the Looking-Glass"',
        'Reverse Sign "Evil in the Mirror"',
        'Reverse Sign "Evil in the Mirror"',
        'Reverse Sign "This Side Down"',
        'Reverse Sign "This Side Down"',
        'Reverse Sign "Overturning All Under Heaven"',
        'Reverse Sign "Overturning All Under Heaven"',
        'Reverse Bow "Dream Bow of Heaven & Earth"',
        'Reverse Bow "Dream Bow of Heaven & Earth"',
        'Reverse Bow "Decree of the Dream Bow of Heaven & Earth"',
        'Reverse Bow "Decree of the Dream Bow of Heaven & Earth"',
        'Turnabout "Reverse Hierarchy"',
        'Turnabout "Reverse Hierarchy"',
        'Turnabout "Change Air Brave"',
        'Turnabout "Change Air Brave"',
        'Small Barrage "Inchling\'s Path"',
        'Small Barrage "Inchling\'s Path"',
        'Small Barrage "Inchling\'s Thorny Path"',
        'Small Barrage "Inchling\'s Thorny Path"',
        'Mallet "Grow Bigger!"',
        'Mallet "Grow Bigger!"',
        'Mallet "Grow Even Bigger!"',
        'Mallet "Grow Even Bigger!"',
        'Bewitched Sword "Shining Needle Sword"',
        'Bewitched Sword "Shining Needle Sword"',
        'Bewitched Sword "Shining Needle Sword"',
        'Bewitched Sword "Shining Needle Sword"',
        'Mallet "You Grow Bigger!"',
        'Mallet "You Grow Bigger!"',
        'Mallet "You Grow Bigger!"',
        'Mallet "You Grow Bigger!"',
        '"Attack on Dwarf"',
        '"Attack on Dwarf"',
        '"Wall of Issun"',
        '"Wall of Issun"',
        '"Hop-o\'-My-Thumb Seven"',
        '"Hop-o\'-My-Thumb Seven"',
        '"The Seven Issun-Boshi"',
        '"The Seven Issun-Boshi"',
        'String Music "Storm Ensemble"',
        'String Music "Joururi World"',
        'First Drum "Raging Temple Taiko"',
        'Second Drum "Vengeful Spirit Aya-no-Tsuzumi"',
        'Third Drum "Three Strikes at Midnight"',
        'Death Drum "Land Percuss"',
        'Fifth Drum "Den-Den Daiko"',
        'Sixth Drum "Alternate Sticking"',
        'Seventh Drum "High Speed Taiko Rocket"',
        'Eighth Drum "Thunder God\'s Anger"',
        '"Blue Lady Show"',
        '"Pristine Beat"',
    ),
})

spell_names_jp = immutabledict({
    'th08': (
        '蛍符「地上の流星」',
        '蛍符「地上の彗星」',
        '灯符「ファイヤフライフェノメノン」',
        '灯符「ファイヤフライフェノメノン」',
        '灯符「ファイヤフライフェノメノン」',
        '灯符「ファイヤフライフェノメノン」',
        '蠢符「リトルバグ」',
        '蠢符「リトルバグストーム」',
        '蠢符「ナイトバグストーム」',
        '蠢符「ナイトバグトルネード」',
        '隠蟲「永夜蟄居」',
        '隠蟲「永夜蟄居」',
        '隠蟲「永夜蟄居」',
        '声符「梟の夜鳴声」',
        '声符「梟の夜鳴声」',
        '声符「木菟咆哮」',
        '声符「木菟咆哮」',
        '蛾符「天蛾の蠱道」',
        '蛾符「天蛾の蠱道」',
        '毒符「毒蛾の鱗粉」',
        '猛毒「毒蛾の暗闇演舞」',
        '鷹符「イルスタードダイブ」',
        '鷹符「イルスタードダイブ」',
        '鷹符「イルスタードダイブ」',
        '鷹符「イルスタードダイブ」',
        '夜盲「夜雀の歌」',
        '夜盲「夜雀の歌」',
        '夜盲「夜雀の歌」',
        '夜盲「夜雀の歌」',
        '夜雀「真夜中のコーラスマスター」',
        '夜雀「真夜中のコーラスマスター」',
        '夜雀「真夜中のコーラスマスター」',
        '産霊「ファーストピラミッド」',
        '産霊「ファーストピラミッド」',
        '産霊「ファーストピラミッド」',
        '産霊「ファーストピラミッド」',
        '始符「エフェメラリティ137」',
        '始符「エフェメラリティ137」',
        '始符「エフェメラリティ137」',
        '野符「武烈クライシス」',
        '野符「将門クライシス」',
        '野符「義満クライシス」',
        '野符「GHQクライシス」',
        '国符「三種の神器　剣」',
        '国符「三種の神器　玉」',
        '国符「三種の神器　鏡」',
        '国体「三種の神器　郷」',
        '終符「幻想天皇」',
        '終符「幻想天皇」',
        '虚史「幻想郷伝説」',
        '虚史「幻想郷伝説」',
        '未来「高天原」',
        '未来「高天原」',
        '未来「高天原」',
        '夢符「二重結界」',
        '夢符「二重結界」',
        '夢境「二重大結界」',
        '夢境「二重大結界」',
        '霊符「夢想封印　散」',
        '霊符「夢想封印　散」',
        '散霊「夢想封印　寂」',
        '散霊「夢想封印　寂」',
        '夢符「封魔陣」',
        '夢符「封魔陣」',
        '神技「八方鬼縛陣」',
        '神技「八方龍殺陣」',
        '霊符「夢想封印　集」',
        '霊符「夢想封印　集」',
        '回霊「夢想封印　侘」',
        '回霊「夢想封印　侘」',
        '境界「二重弾幕結界」',
        '境界「二重弾幕結界」',
        '大結界「博麗弾幕結界」',
        '大結界「博麗弾幕結界」',
        '神霊「夢想封印　瞬」',
        '神霊「夢想封印　瞬」',
        '神霊「夢想封印　瞬」',
        '魔符「ミルキーウェイ」',
        '魔符「ミルキーウェイ」',
        '魔空「アステロイドベルト」',
        '魔空「アステロイドベルト」',
        '魔符「スターダストレヴァリエ」',
        '魔符「スターダストレヴァリエ」',
        '黒魔「イベントホライズン」',
        '黒魔「イベントホライズン」',
        '恋符「ノンディレクショナルレーザー」',
        '恋符「ノンディレクショナルレーザー」',
        '恋風「スターライトタイフーン」',
        '恋風「スターライトタイフーン」',
        '恋符「マスタースパーク」',
        '恋符「マスタースパーク」',
        '恋心「ダブルスパーク」',
        '恋心「ダブルスパーク」',
        '光符「アースライトレイ」',
        '光符「アースライトレイ」',
        '光撃「シュート・ザ・ムーン」',
        '光撃「シュート・ザ・ムーン」',
        '魔砲「ファイナルスパーク」',
        '魔砲「ファイナルスパーク」',
        '魔砲「ファイナルマスタースパーク」',
        '波符「赤眼催眠(マインドシェイカー)」',
        '波符「赤眼催眠(マインドシェイカー)」',
        '幻波「赤眼催眠(マインドブローイング)」',
        '幻波「赤眼催眠(マインドブローイング)」',
        '狂符「幻視調律(ビジョナリチューニング)」',
        '狂符「幻視調律(ビジョナリチューニング)」',
        '狂視「狂視調律(イリュージョンシーカー)」',
        '狂視「狂視調律(イリュージョンシーカー)」',
        '懶符「生神停止(アイドリングウェーブ)」',
        '懶符「生神停止(アイドリングウェーブ)」',
        '懶惰「生神停止(マインドストッパー)」',
        '懶惰「生神停止(マインドストッパー)」',
        '散符「真実の月(インビジブルフルムーン)」',
        '散符「真実の月(インビジブルフルムーン)」',
        '散符「真実の月(インビジブルフルムーン)」',
        '散符「真実の月(インビジブルフルムーン)」',
        '月眼「月兎遠隔催眠術(テレメスメリズム)」',
        '月眼「月兎遠隔催眠術(テレメスメリズム)」',
        '月眼「月兎遠隔催眠術(テレメスメリズム)」',
        '天丸「壺中の天地」',
        '天丸「壺中の天地」',
        '天丸「壺中の天地」',
        '天丸「壺中の天地」',
        '覚神「神代の記憶」',
        '覚神「神代の記憶」',
        '神符「天人の系譜」',
        '神符「天人の系譜」',
        '蘇活「生命遊戯　-ライフゲーム-」',
        '蘇活「生命遊戯　-ライフゲーム-」',
        '蘇生「ライジングゲーム」',
        '蘇生「ライジングゲーム」',
        '操神「オモイカネディバイス」',
        '操神「オモイカネディバイス」',
        '神脳「オモイカネブレイン」',
        '神脳「オモイカネブレイン」',
        '天呪「アポロ１３」',
        '天呪「アポロ１３」',
        '天呪「アポロ１３」',
        '天呪「アポロ１３」',
        '秘術「天文密葬法」',
        '秘術「天文密葬法」',
        '秘術「天文密葬法」',
        '秘術「天文密葬法」',
        '禁薬「蓬莱の薬」',
        '禁薬「蓬莱の薬」',
        '禁薬「蓬莱の薬」',
        '禁薬「蓬莱の薬」',
        '薬符「壺中の大銀河」',
        '薬符「壺中の大銀河」',
        '薬符「壺中の大銀河」',
        '薬符「壺中の大銀河」',
        '難題「龍の頸の玉 -五色の弾丸-」',
        '難題「龍の頸の玉 -五色の弾丸-」',
        '神宝「ブリリアントドラゴンバレッタ」',
        '神宝「ブリリアントドラゴンバレッタ」',
        '難題「仏の御石の鉢 -砕けぬ意思-」',
        '難題「仏の御石の鉢 -砕けぬ意思-」',
        '神宝「ブディストダイアモンド」',
        '神宝「ブディストダイアモンド」',
        '難題「火鼠の皮衣 -焦れぬ心-」',
        '難題「火鼠の皮衣 -焦れぬ心-」',
        '神宝「サラマンダーシールド」',
        '神宝「サラマンダーシールド」',
        '難題「燕の子安貝 -永命線-」',
        '難題「燕の子安貝 -永命線-」',
        '神宝「ライフスプリングインフィニティ」',
        '神宝「ライフスプリングインフィニティ」',
        '難題「蓬莱の弾の枝 -虹色の弾幕-」',
        '難題「蓬莱の弾の枝 -虹色の弾幕-」',
        '神宝「蓬莱の玉の枝 -夢色の郷-」',
        '神宝「蓬莱の玉の枝 -夢色の郷-」',
        '「永夜返し -初月-」',
        '「永夜返し -三日月-」',
        '「永夜返し -上つ弓張-」',
        '「永夜返し -待宵-」',
        '「永夜返し -子の刻-」',
        '「永夜返し -子の二つ-」',
        '「永夜返し -子の三つ-」',
        '「永夜返し -子の四つ-」',
        '「永夜返し -丑の刻-」',
        '「永夜返し -丑の二つ-」',
        '「永夜返し -丑三つ時-」',
        '「永夜返し -丑の四つ-」',
        '「永夜返し -寅の刻-」',
        '「永夜返し -寅の二つ-」',
        '「永夜返し -寅の三つ-」',
        '「永夜返し -寅の四つ-」',
        '「永夜返し -朝靄-」',
        '「永夜返し -夜明け-」',
        '「永夜返し -明けの明星-」',
        '「永夜返し -世明け-」',
        '旧史「旧秘境史　-オールドヒストリー-」',
        '転世「一条戻り橋」',
        '新史「新幻想史　-ネクストヒストリー-」',
        '時効「月のいはかさの呪い」',
        '不死「火の鳥　-鳳翼天翔-」',
        '藤原「滅罪寺院傷」',
        '不死「徐福時空」',
        '滅罪「正直者の死」',
        '虚人「ウー」',
        '不滅「フェニックスの尾」',
        '蓬莱「凱風快晴　-フジヤマヴォルケイノ-」',
        '「パゼストバイフェニックス」',
        '「蓬莱人形」',
        '「インペリシャブルシューティング」',
        '「季節外れのバタフライストーム」',
        '「ブラインドナイトバード」',
        '「日出づる国の天子」',
        '「幻朧月睨(ルナティックレッドアイズ)」',
        '「天網蜘網捕蝶の法」',
        '「蓬莱の樹海」',
        '「フェニックス再誕」',
        '「エンシェントデューパー」',
        '「無何有浄化」',
        '「夢想天生」',
        '「ブレイジングスター」',
        '「デフレーションワールド」',
        '「待宵反射衛星斬」',
        '「グランギニョル座の怪人」',
        '「スカーレットディスティニー」',
        '「西行寺無余涅槃」',
        '「深弾幕結界　-夢幻泡影-」',
    ),
    'th13': (
        '符牒「死蝶の舞」',
        '符牒「死蝶の舞」',
        '符牒「死蝶の舞　- 桜花 -」',
        '符牒「死蝶の舞　- 桜花 -」',
        '幽蝶「ゴーストスポット」',
        '幽蝶「ゴーストスポット」',
        '幽蝶「ゴーストスポット　- 桜花 -」',
        '幽蝶「ゴーストスポット　- 桜花 -」',
        '冥符「常夜桜」',
        '冥符「常夜桜」',
        '冥符「常夜桜」',
        '冥符「常夜桜」',
        '桜符「西行桜吹雪」',
        '桜符「西行桜吹雪」',
        '響符「マウンテンエコー」',
        '響符「マウンテンエコー」',
        '響符「マウンテンエコースクランブル」',
        '響符「マウンテンエコースクランブル」',
        '響符「パワーレゾナンス」',
        '響符「パワーレゾナンス」',
        '響符「パワーレゾナンス」',
        '響符「パワーレゾナンス」',
        '山彦「ロングレンジエコー」',
        '山彦「ロングレンジエコー」',
        '山彦「アンプリファイエコー」',
        '山彦「アンプリファイエコー」',
        '大声「チャージドクライ」',
        '大声「チャージドクライ」',
        '大声「チャージドヤッホー」',
        '大声「チャージドヤッホー」',
        '虹符「アンブレラサイクロン」',
        '虹符「アンブレラサイクロン」',
        '回復「ヒールバイデザイア」',
        '回復「ヒールバイデザイア」',
        '回復「ヒールバイデザイア」',
        '回復「ヒールバイデザイア」',
        '毒爪「ポイズンレイズ」',
        '毒爪「ポイズンレイズ」',
        '毒爪「ポイズンマーダー」',
        '毒爪「ポイズンマーダー」',
        '欲符「稼欲霊招来」',
        '欲符「稼欲霊招来」',
        '欲霊「スコアデザイアイーター」',
        '欲霊「スコアデザイアイーター」',
        '邪符「ヤンシャオグイ」',
        '邪符「グーフンイエグイ」',
        '邪符「グーフンイエグイ」',
        '入魔「ゾウフォルゥモォ」',
        '入魔「ゾウフォルゥモォ」',
        '入魔「ゾウフォルゥモォ」',
        '入魔「ゾウフォルゥモォ」',
        '降霊「死人タンキー」',
        '降霊「死人タンキー」',
        '通霊「トンリン芳香」',
        '通霊「トンリン芳香」',
        '道符「タオ胎動」',
        '道符「タオ胎動」',
        '道符「タオ胎動」',
        '道符「タオ胎動」',
        '雷矢「ガゴウジサイクロン」',
        '雷矢「ガゴウジサイクロン」',
        '雷矢「ガゴウジトルネード」',
        '天符「雨の磐舟」',
        '天符「天の磐舟よ天へ昇れ」',
        '天符「天の磐舟よ天へ昇れ」',
        '投皿「物部の八十平瓮」',
        '投皿「物部の八十平瓮」',
        '投皿「物部の八十平瓮」',
        '投皿「物部の八十平瓮」',
        '炎符「廃仏の炎風」',
        '炎符「廃仏の炎風」',
        '炎符「桜井寺炎上」',
        '炎符「桜井寺炎上」',
        '聖童女「大物忌正餐」',
        '聖童女「大物忌正餐」',
        '聖童女「大物忌正餐」',
        '聖童女「大物忌正餐」',
        '名誉「十二階の色彩」',
        '名誉「十二階の色彩」',
        '名誉「十二階の冠位」',
        '名誉「十二階の冠位」',
        '仙符「日出ずる処の道士」',
        '仙符「日出ずる処の道士」',
        '仙符「日出ずる処の天子」',
        '仙符「日出ずる処の天子」',
        '召喚「豪族乱舞」',
        '召喚「豪族乱舞」',
        '召喚「豪族乱舞」',
        '召喚「豪族乱舞」',
        '秘宝「斑鳩寺の天球儀」',
        '秘宝「斑鳩寺の天球儀」',
        '秘宝「斑鳩寺の天球儀」',
        '秘宝「聖徳太子のオーパーツ」',
        '光符「救世観音の光後光」',
        '光符「救世観音の光後光」',
        '光符「グセフラッシュ」',
        '光符「グセフラッシュ」',
        '眼光「十七条のレーザー」',
        '眼光「十七条のレーザー」',
        '神光「逆らう事なきを宗とせよ」',
        '神光「逆らう事なきを宗とせよ」',
        '「星降る神霊廟」',
        '「星降る神霊廟」',
        '「生まれたての神霊」',
        '「生まれたての神霊」',
        'アンノウン「軌道不明の鬼火」',
        'アンノウン「姿態不明の空魚」',
        'アンノウン「原理不明の妖怪玉」',
        '壱番勝負「霊長化弾幕変化」',
        '弐番勝負「肉食化弾幕変化」',
        '参番勝負「延羽化弾幕変化」',
        '四番勝負「両生化弾幕変化」',
        '伍番勝負「鳥獣戯画」',
        '六番勝負「狸の化け学校」',
        '七番勝負「野生の離島」',
        '変化「まぬけ巫女の偽調伏」',
        '「マミゾウ化弾幕十変化」',
        '狢符「満月のポンポコリン」',
        '桜符「桜吹雪地獄」',
        '山彦「ヤマビコの本領発揮エコー」',
        '毒爪「死なない殺人鬼」',
        '道符「ＴＡＯ胎動　〜道〜」',
        '怨霊「入鹿の雷」',
        '聖童女「太陽神の贄」',
        '「神霊大宇宙」',
        '「ワイルドカーペット」',
    ),
    'th14': (
        '氷符「アルティメットブリザード」',
        '氷符「アルティメットブリザード」',
        '水符「テイルフィンスラップ」',
        '水符「テイルフィンスラップ」',
        '水符「テイルフィンスラップ」',
        '水符「テイルフィンスラップ」',
        '鱗符「スケールウェイブ」',
        '鱗符「スケールウェイブ」',
        '鱗符「逆鱗の荒波」',
        '鱗符「逆鱗の大荒波」',
        '飛符「フライングヘッド」',
        '飛符「フライングヘッド」',
        '飛符「フライングヘッド」',
        '飛符「フライングヘッド」',
        '首符「クローズアイショット」',
        '首符「クローズアイショット」',
        '首符「ろくろ首飛来」',
        '首符「ろくろ首飛来」',
        '飛頭「マルチプリケイティブヘッド」',
        '飛頭「マルチプリケイティブヘッド」',
        '飛頭「セブンズヘッド」',
        '飛頭「ナインズヘッド」',
        '飛頭「デュラハンナイト」',
        '飛頭「デュラハンナイト」',
        '飛頭「デュラハンナイト」',
        '飛頭「デュラハンナイト」',
        '牙符「月下の犬歯」',
        '牙符「月下の犬歯」',
        '変身「トライアングルファング」',
        '変身「トライアングルファング」',
        '変身「スターファング」',
        '変身「スターファング」',
        '咆哮「ストレンジロア」',
        '咆哮「ストレンジロア」',
        '咆哮「満月の遠吠え」',
        '咆哮「満月の遠吠え」',
        '狼符「スターリングパウンス」',
        '狼符「スターリングパウンス」',
        '天狼「ハイスピードパウンス」',
        '天狼「ハイスピードパウンス」',
        '平曲「祇園精舎の鐘の音」',
        '平曲「祇園精舎の鐘の音」',
        '平曲「祇園精舎の鐘の音」',
        '平曲「祇園精舎の鐘の音」',
        '怨霊「耳無し芳一」',
        '怨霊「耳無し芳一」',
        '怨霊「平家の大怨霊」',
        '怨霊「平家の大怨霊」',
        '楽符「邪悪な五線譜」',
        '楽符「邪悪な五線譜」',
        '楽符「凶悪な五線譜」',
        '楽符「ダブルスコア」',
        '琴符「諸行無常の琴の音」',
        '琴符「諸行無常の琴の音」',
        '琴符「諸行無常の琴の音」',
        '琴符「諸行無常の琴の音」',
        '響符「平安の残響」',
        '響符「平安の残響」',
        '響符「エコーチェンバー」',
        '響符「エコーチェンバー」',
        '箏曲「下克上送箏曲」',
        '箏曲「下克上送箏曲」',
        '箏曲「下克上レクイエム」',
        '箏曲「下克上レクイエム」',
        '欺符「逆針撃」',
        '欺符「逆針撃」',
        '欺符「逆針撃」',
        '欺符「逆針撃」',
        '逆符「鏡の国の弾幕」',
        '逆符「鏡の国の弾幕」',
        '逆符「イビルインザミラー」',
        '逆符「イビルインザミラー」',
        '逆符「天地有用」',
        '逆符「天地有用」',
        '逆符「天下転覆」',
        '逆符「天下転覆」',
        '逆弓「天壌夢弓」',
        '逆弓「天壌夢弓」',
        '逆弓「天壌夢弓の詔勅」',
        '逆弓「天壌夢弓の詔勅」',
        '逆転「リバースヒエラルキー」',
        '逆転「リバースヒエラルキー」',
        '逆転「チェンジエアブレイブ」',
        '逆転「チェンジエアブレイブ」',
        '小弾「小人の道」',
        '小弾「小人の道」',
        '小弾「小人の茨道」',
        '小弾「小人の茨道」',
        '小槌「大きくなあれ」',
        '小槌「大きくなあれ」',
        '小槌「もっと大きくなあれ」',
        '小槌「もっと大きくなあれ」',
        '妖剣「輝針剣」',
        '妖剣「輝針剣」',
        '妖剣「輝針剣」',
        '妖剣「輝針剣」',
        '小槌「お前が大きくなあれ」',
        '小槌「お前が大きくなあれ」',
        '小槌「お前が大きくなあれ」',
        '小槌「お前が大きくなあれ」',
        '「進撃の小人」',
        '「進撃の小人」',
        '「ウォールオブイッスン」',
        '「ウォールオブイッスン」',
        '「ホップオマイサムセブン」',
        '「ホップオマイサムセブン」',
        '「七人の一寸法師」',
        '「七人の一寸法師」',
        '弦楽「嵐のアンサンブル」',
        '弦楽「浄瑠璃世界」',
        '一鼓「暴れ宮太鼓」',
        '二鼓「怨霊アヤノツヅミ」',
        '三鼓「午前零時のスリーストライク」',
        '死鼓「ランドパーカス」',
        '五鼓「デンデン太鼓」',
        '六鼓「オルタネイトスティッキング」',
        '七鼓「高速和太鼓ロケット」',
        '八鼓「雷神の怒り」',
        '「ブルーレディショー」',
        '「プリスティンビート」',
    ),
})


def _CheckDictIntegrity() -> bool:
    for i in spell_names_en:
        try:
            if len(spell_names_en[i]) != len(spell_names_jp[i]):
                return False
        except KeyError:
            return False
    return True


assert len(spell_names_en) == len(spell_names_jp)
assert _CheckDictIntegrity()


def get(game_id: str, spell_id: int):
    """
    Obtains a spell card name given a game ID and a spell ID
    
    Uses the language set in gettext to automatically retrieve the spell name in English or in Japanese
    """
    try:
        if get_language() == 'ja':
            return spell_names_jp[game_id][spell_id]
        else:
            return spell_names_en[game_id][spell_id]
    except (IndexError, KeyError, TypeError):
        return None
