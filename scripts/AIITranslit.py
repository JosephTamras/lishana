import re
import unicodedata

def AIITranslit(aiiText):
    # -----------------------------------------
    # 1. Define constants (mirroring JS)
    # -----------------------------------------
    HBASA = '\u073C'
    RWAHA = '\u073F'
    ZLAMA_ANGULAR = '\u0739'
    ZLAMA_HORIZONTAL = '\u0738'
    PTHAHA = '\u0732'
    ZQAPHA = '\u0735'

    diacriticVowels = f"{HBASA}{RWAHA}{ZLAMA_ANGULAR}{ZLAMA_HORIZONTAL}{PTHAHA}{ZQAPHA}"
    diacriticVowelsCapture = f"([{diacriticVowels}])"

    TALQANA_ABOVE = '\u0747'
    COMBINING_DIAERESIS = '\u0308'

    ALAPH = 'ܐ'
    SUPERSCRIPT_ALAPH = '\u0711'
    WAW = 'ܘ'
    YUDH = 'ܝ'

    COMBINING_TILDE_BELOW = '\u0330'
    COMBINING_TILDE_ABOVE = '\u0303'
    COMBINING_MACRON_BELOW = '\u0331'
    COMBINING_MACRON = '\u0304'
    QUSHSHAYA = '\u0741'
    RUKKAKHA = '\u0742'
    COMBINING_BREVE_BELOW = '\u032E'
    NON_VOWEL_DIACRITICS = (
        f"{COMBINING_TILDE_BELOW}"
        f"{COMBINING_TILDE_ABOVE}"
        f"{QUSHSHAYA}"
        f"{RUKKAKHA}"
        f"{COMBINING_BREVE_BELOW}"
        f"{TALQANA_ABOVE}"
    )

    COMBINING_DOT_BELOW = '\u0323'
    COMBINING_DOT_ABOVE = '\u0307'

    GLOTTAL_STOP = 'ʾ'
    PHARYNGEAL = 'ʿ'

    TR_THIRD_PERSON_FEM_SUFFIX = 'oh'
    TR_WAW_PLUS_RVASA = 'u'

    # -----------------------------------------
    # 2. Character mapping tables
    # -----------------------------------------
    tt = {
        'ܦ': 'p',
        'ܒ': 'b',
        'ܬ': 't',
        'ܛ': 'ṭ',
        'ܕ': 'd',
        'ܟ': 'k',
        'ܓ': 'g',
        'ܩ': 'q',
        'ܣ': 's',
        'ܨ': 'ṣ',
        'ܙ': 'z',
        'ܫ': 'š',
        'ܚ': 'ḥ',
        'ܥ': PHARYNGEAL,
        'ܗ': 'h',
        'ܡ': 'm',
        'ܢ': 'n',
        'ܪ': 'r',
        'ܠ': 'l',
    }

    consonants = ''.join(tt.keys())
    consonantsCapture = f"([{consonants}])"
    ttValues = ''.join(tt.values())

    mhagjana = ''.join(tt[ch] for ch in 'ܗܠܡܢܥܪ') + ALAPH + YUDH + WAW
    mhagjanaCapture = f"([{mhagjana}])"

    marhetana = ''.join(tt[ch] for ch in 'ܦܒܬܛܕܟܓܩܣܨܙܫܚ')
    marhetanaCapture = f"([{marhetana}])"

    bdul = 'ܒܕܘܠ'
    bdulCapture = f"([{bdul}])"
    bdulCapture2 = f"([{bdul}])([{bdul}])"

    ttTransposePunc = {
        '“': '”',
        '”': '“',
        '‘': '’',
        '’': '‘',
        '؟': '?',
        '«': '“',
        '»': '”',
        '،': ',',
        '؛': ';',
    }
    ttTransposePuncKeys = ''.join(ttTransposePunc.keys())
    ttTransposePuncKeysCapture = f"([{ttTransposePuncKeys}])"

    ttNext = {
        WAW: 'w',
        YUDH: 'y',
        ZLAMA_ANGULAR: 'ē',
        ZLAMA_HORIZONTAL: 'i',
        PTHAHA: 'a',
        ZQAPHA: 'ā',
    }
    ttNextKeysCapture = f"([{''.join(ttNext.keys())}])"

    phoneticReplacements = {
        # 'ṭ': 't',
        'ṣ': 's',
        'š': 'sh',
        'ḥ': 'kh',
        'ž': 'zh',
        'ḇ': 'v',
        'ṯ': 'th',
        'ḏ': 'd',
        'ḵ': 'kh',
        'ḡ': 'gh',
        'ē': 'e',  # 'eh' sound
        'ī': 'ee',
        'ā': 'a',
        PHARYNGEAL: '`',
        GLOTTAL_STOP: "'",
        'č': 'ch',
    }
    phoneticReplacementsKeysCapture = f"([{''.join(phoneticReplacements.keys())}])"

    glides = f"{ALAPH}{YUDH}{WAW}"
    consonantsMinusGlides = f"{ttValues}čjžfḇṯḏḵḡ"
    lettersCapture = f"([{glides}{consonantsMinusGlides}])"
    lettersNonCapture = f"(?:[{glides}{consonantsMinusGlides}])"
    consonantsWawYudhCapture = f"([{WAW}{YUDH}{consonantsMinusGlides}])"
    vowelsW = f"{TR_WAW_PLUS_RVASA}o"
    vowelsY = 'eiēī'
    vowels = f"{vowelsW}{vowelsY}aā"
    consonantsAndVowelsCapture = f"([{glides}{consonantsMinusGlides}{vowels}])"

    fixes = [
        # Each entry: (pattern, replacement)
        (f"{diacriticVowelsCapture}{QUSHSHAYA}", f"{QUSHSHAYA}\\1"),
        (f"([{ttTransposePuncKeys}()!.:\"'])", r"#\1#"),
    ]

    specialCases = [
        # [ matching_text, replacement ]
        ['ܝܼܗܘܼܕ', 'īhud'],
        ['ܝܼܚܝܼܕܘܼܬܵܐ', 'īḥīdutā'],
        ['ܝܼܣܲܪ', 'īsar'],
        ['ܝܼܠܝܼܕܘܼܬܵܐ', 'īlidutā'],
        ['ܝܼܕܵܥ', 'īdāʿ'],

        [f"#ܒܗ{COMBINING_DOT_ABOVE}ܝ#", '#b-ay#'],
        [f"ܗ{COMBINING_DOT_ABOVE}ܝ#", 'aya#'],
        [f"ܗ{COMBINING_DOT_ABOVE}ܘ#", 'awa#'],
        [f"ܡ{COMBINING_DOT_ABOVE}ܢ#", 'man#'],
        [f"ܡ{COMBINING_DOT_BELOW}ܢ#", 'min#'],
        ['ܒܵܬܹܐ#', 'bāttē#'],
        ['ܟ̰ܵܐܝ', 'čāy'],
        ['ܒܵܐܝ', 'bāy'],
        ['ܐܲܦ̮ܘܿܟܵܕ', 'avokād'],
        ['ܝܼܫܘܿܥ#', 'īšoʿ#'],
        ['ܢܲܦ̮ܫ', 'noš'],
        ['ܘܼܦ̮', 'ܘܼ'],
        ['#ܝܘܸܢ#', '#ìwen#'],
        ['#ܝܘܵܢ#', '#ìwān#'],
        ['#ܝܘܲܚ#', '#ìwaḥ#'],
        ['#ܝܘܸܬ#', '#ìwet#'],
        ['#ܝܘܵܬܝ#', '#ìwāt#'],
        ['#ܝܬܘܿܢ#', '#ìton#'],
        ['#ܝܠܹܗ#', '#ìlēh#'],
        ['#ܝܠܵܗ̇#', '#ìlāh#'],
        ['#ܝܢܵܐ#', '#ìnā#'],
        ['#ܝܗ݇ܘܵܐ#', '#ìwā#'],
        ['#ܝܗ݇ܘܵܬ݇#', '#ìwā#'],
        ['#ܝܗ݇ܘܵܘ#', '#ìwā#'],
        ['ܝܼܘܸܢ#', 'īwen#'],
        ['ܝܼܘܵܢ', 'īwān'],
        ['ܝܼܘܸܬ#', 'īwet#'],
        ['ܝܼܘܵܬܝ#', 'īwāt#'],
        ['ܝܼܠܹܗ#', 'īlēh#'],
        ['ܝܼܠܵܗ̇#', 'īlāh#'],
        ['ܝܼܘܲܚ#', 'īwaḥ#'],
        ['ܝܼܬܘܿܢ#', 'īton#'],
        ['ܝܼܢܵܐ#', 'īnā#'],
        ['ܝܼܗ݇ܘܵܐ#', 'īwā#'],
        ['ܝܼܗ݇ܘܵܘ#', 'īwā#'],
        ['#ܗ݇ܘܝܼ', '#wī'],
        ['#ܗ݇ܘܹܝܡܘܼܢ#', '#wēmun#'],
        ['#ܗ݇ܘܵܐ#', '#wā#'],
        ['#ܗ݇ܘܵܘ#', '#wā#'],
        ['#ܗ݇ܘܹܐ#', '#wē#'],
        ['ܟܠ#', 'kul#'],
        ['ܟܠܵܢ#', 'kullān#'],
        ['ܟܠܘܼܟ݂#', 'kulloḵ#'],
        ['ܟܠܵܟ݂ܝ#', 'kullāḵ#'],
        ['ܟܠܹܗ#', 'kullēh#'],
        ['ܟܠܵܗ̇#', 'kullāh#'],
        ['ܟܠܘܼܗܝ#', 'kulluh#'],
        ['ܟܠܘܿܗ̇#', 'kulloh#'],
        ['ܟܠܲܢ#', 'kullan#'],
        ['ܟܠܵܘܟ݂ܘܿܢ#', 'kullāwḵon#'],
        ['ܟܠܵܝܗܝ#', 'kullāyh#'],
        ['ܟܠܗܘܿܢ#', 'kullhon#'],
        ['ܟܠܵܢܵܐܝܼܬ#', 'kullānāʾīt#'],
        ['ܟܠܵܢܵܐܝܼܬ݂#', 'kullānāʾīṯ#'],
        ['ܟܠܵܢܵܝ', 'kullānāy'],
        ['ܟܘܿܠܵܝ', 'kollāy'],
        ['ܟܠܚܲܕ݇#', 'kulḥa#'],
        ['ܟܠܚܕ݂ܵܐ#', 'kulḥḏā#'],
        ['ܟܠܫܲܢ݇ܬ#', 'kulšat#'],
        ['ܝܲܐܠܵܗ#', 'yallāh#'],
        ['ܘܲܐܠܵܗ#', 'wallāh#'],
        ['ܙܹܠ݇ܝ#', 'zē#'],
        ['ܬܵܐܝ#', 'tā#'],
    ]

    # -----------------------------------------
    # 3. Start applying transformations
    # -----------------------------------------
    # Normalize
    text = unicodedata.normalize('NFC', aiiText)

    # JS: text.replaceAll(' | ', '# | #')
    text = text.replace(' | ', '# | #')

    # JS: `##${text.replaceAll(' ', '# #')}##`
    text = f"##{text.replace(' ', '# #')}##"

    # JS: text.replaceAll('ـ', '')
    text = text.replace('ـ', '')

    # JS: text.replaceAll(COMBINING_DIAERESIS, '')
    text = text.replace(COMBINING_DIAERESIS, '')

    # JS: text.replaceAll(SUPERSCRIPT_ALAPH, '')
    text = text.replace(SUPERSCRIPT_ALAPH, '')

    # Apply fixes (array of [pattern, replacement])
    for pattern, repl in fixes:
        text = re.sub(pattern, repl, text)

    # Apply special cases
    for pattern, repl in specialCases:
        text = text.replace(pattern, repl)

    # urmian pronunciation for g-stem imperatives
    eConj = [
        'ܥ',
        'ܥܝ',
        f"ܥܡܘ{HBASA}ܢ",
    ]
    # re = new RegExp(`([${consonants}${YUDH}][${NON_VOWEL_DIACRITICS}]?[${consonants}][${NON_VOWEL_DIACRITICS}]?)${ZLAMA_ANGULAR}(${eConj.join('|')})#`, 'g');
    pattern = (
        f"([{consonants}{YUDH}][{NON_VOWEL_DIACRITICS}]?"
        f"[{consonants}][{NON_VOWEL_DIACRITICS}]?)"
        f"{ZLAMA_ANGULAR}("
        + "|".join(eConj) +
        ")#"
    )
    repl = fr"\1{YUDH}{HBASA}\2#"
    text = re.sub(pattern, repl, text)

    # in urmian, verbs ending in ܪ follow a past tense contraction
    rConj = [
        f"{ZQAPHA}ܟ{RUKKAKHA}{YUDH}",
        f"{ZLAMA_ANGULAR}ܗ",
        f"{ZQAPHA}ܗ{COMBINING_DOT_ABOVE}",
        f"{PTHAHA}ܢ",
        f"{ZQAPHA}{WAW}ܟ{RUKKAKHA}{WAW}{RWAHA}ܢ",
    ]
    pattern = f"{YUDH}{HBASA}ܪ(" + "|".join(rConj) + ")#"
    repl = f"{ZLAMA_HORIZONTAL}ܪ\\1#"
    text = re.sub(pattern, repl, text)

    # text.replaceAll(`ܟ${COMBINING_TILDE_BELOW}`, 'č')
    text = text.replace(f"ܟ{COMBINING_TILDE_BELOW}", 'č')
    text = text.replace(f"ܓ{COMBINING_TILDE_BELOW}", 'j')
    text = text.replace(f"ܫ{COMBINING_TILDE_BELOW}", 'ž')

    text = text.replace(f"ܙ{COMBINING_TILDE_ABOVE}", 'ž')
    text = text.replace(f"ܟ{COMBINING_TILDE_ABOVE}", 'č')
    text = text.replace(f"ܫ{COMBINING_TILDE_ABOVE}", 'ž')

    text = text.replace(f"ܦ{COMBINING_BREVE_BELOW}", 'f')

    text = text.replace(f"ܦ{QUSHSHAYA}", 'p')
    text = text.replace(f"ܒ{QUSHSHAYA}", 'b')
    text = text.replace(f"ܬ{QUSHSHAYA}", 't')
    text = text.replace(f"ܕ{QUSHSHAYA}", 'd')
    text = text.replace(f"ܟ{QUSHSHAYA}", 'k')
    text = text.replace(f"ܓ{QUSHSHAYA}", 'g')

    text = text.replace(f"ܒ{RUKKAKHA}", 'ḇ')
    text = text.replace(f"ܬ{RUKKAKHA}", 'ṯ')
    text = text.replace(f"ܕ{RUKKAKHA}", 'ḏ')
    text = text.replace(f"ܟ{RUKKAKHA}", 'ḵ')
    text = text.replace(f"ܓ{RUKKAKHA}", 'ḡ')

    # b-, d-, w-, l- prefixing for words starting with ALAPH or substituted vowels
    initialTranslitChar = 'aī'
    initialCharCapture = f"([{ALAPH}{initialTranslitChar}])"
    # #$1-$2-$3
    pattern = f"#{bdulCapture2}{initialCharCapture}"
    repl = "#\\1-\\2-\\3"
    text = re.sub(pattern, repl, text)
    pattern = f"#{bdulCapture}{initialCharCapture}"
    repl = "#\\1-\\2"
    text = re.sub(pattern, repl, text)

    # text.replaceAll(`${WAW}${HBASA}ܗ${COMBINING_DOT_ABOVE}#`, `${TR_THIRD_PERSON_FEM_SUFFIX}#`);
    text = text.replace(f"{WAW}{HBASA}ܗ{COMBINING_DOT_ABOVE}#", f"{TR_THIRD_PERSON_FEM_SUFFIX}#")

    # text.replaceAll(`${YUDH}${HBASA}ܥ`, 'īܥ');
    text = text.replace(f"{YUDH}{HBASA}ܥ", f"īܥ")
    # text.replaceAll(`${YUDH}${HBASA}`, '⚹'); placeholder
    text = text.replace(f"{YUDH}{HBASA}", '⚹')

    # text.replaceAll(`${WAW}${RWAHA}`, 'o');
    text = text.replace(f"{WAW}{RWAHA}", 'o')

    # text.replaceAll(`${WAW}${HBASA}`, TR_WAW_PLUS_RVASA);
    text = text.replace(f"{WAW}{HBASA}", TR_WAW_PLUS_RVASA)

    # Transform punctuation
    # re = new RegExp(ttTransposePuncKeysCapture, 'g');
    def _transpose_punc(m):
        return ttTransposePunc[m.group(1)]

    text = re.sub(ttTransposePuncKeysCapture, _transpose_punc, text)

    # Transform base consonants
    def _tt_replace(m):
        return tt[m.group(1)]

    text = re.sub(consonantsCapture, _tt_replace, text)

    # text.replaceAll(`#${ALAPH}#`, `#${GLOTTAL_STOP}#`)
    text = text.replace(f"#{ALAPH}#", f"#{GLOTTAL_STOP}#")

    # ([letters])([mhagjana])COMBINING_MACRON_BELOW([letters]) => $1e$2$3
    pattern = f"{lettersCapture}{mhagjanaCapture}{COMBINING_MACRON_BELOW}{lettersCapture}"
    repl = r"\1e\2\3"
    text = re.sub(pattern, repl, text)

    # ([letters])([marhetana])COMBINING_MACRON([letters]) => $1$2e$3
    pattern = f"{lettersCapture}{marhetanaCapture}{COMBINING_MACRON}{lettersCapture}"
    repl = r"\1\2e\3"
    text = re.sub(pattern, repl, text)

    # remove TALQANA_ABOVE if it appears after a letter
    pattern = f"{lettersNonCapture}{TALQANA_ABOVE}"
    text = re.sub(pattern, '', text)

    # doubling consonants
    pattern = f"([{ZLAMA_HORIZONTAL}{PTHAHA}]){lettersCapture}{diacriticVowelsCapture}"
    repl = r"\1\2\2\3"
    text = re.sub(pattern, repl, text)

    pattern = (
        f"([{ZLAMA_HORIZONTAL}{PTHAHA}]){lettersCapture}"
        f"{TR_WAW_PLUS_RVASA}{lettersCapture}{diacriticVowelsCapture}"
    )
    repl = fr"\1\2\2{TR_WAW_PLUS_RVASA}\3\4"
    text = re.sub(pattern, repl, text)

    pattern = f"([{ZLAMA_HORIZONTAL}{PTHAHA}]){lettersCapture}{TR_THIRD_PERSON_FEM_SUFFIX}"
    repl = fr"\1\2\2{TR_THIRD_PERSON_FEM_SUFFIX}"
    text = re.sub(pattern, repl, text)

    # remove combining dot above
    text = text.replace(COMBINING_DOT_ABOVE, '')

    # yudh+khwasa sandwiched between voweless atwateh => <i>
    pattern = f"{consonantsWawYudhCapture}⚹{lettersCapture}([^{diacriticVowels}])"
    repl = r"\1i\2\3"
    text = re.sub(pattern, repl, text)
    text = text.replace('⚹', 'ī')

    # ([letters])ZLAMA_ANGULARYUDH([letters]) => $1ē$2
    pattern = f"{lettersCapture}{ZLAMA_ANGULAR}{YUDH}{lettersCapture}"
    repl = r"\1ē\2"
    text = re.sub(pattern, repl, text)

    # bdwl for g-stems starting w/ yudh
    pattern = f"#{bdulCapture}{YUDH}{lettersCapture}"
    repl = "#\\1-\\2"
    text = re.sub(pattern, repl, text)

    # ([letters])YUDH([letters]) => $1i$2
    pattern = f"{lettersCapture}{YUDH}{lettersCapture}"
    repl = r"\1i\2"
    text = re.sub(pattern, repl, text)

    # ([consonantsMinusGlides])YUDH# => $1#
    pattern = f"([{consonantsMinusGlides}]){YUDH}#"
    repl = r"\1#"
    text = re.sub(pattern, repl, text)

    text = text.replace(f"{ALAPH}{PTHAHA}{WAW}#", "aw#")
    text = text.replace(f"{ALAPH}{PTHAHA}{YUDH}#", "ay#")

    text = text.replace(f"#{ALAPH}{ZLAMA_ANGULAR}{YUDH}", "#ē")
    text = text.replace(f"#{ALAPH}{YUDH}", "#ī")

    pattern = f"#{YUDH}{lettersCapture}"
    repl = "#\\1"
    text = re.sub(pattern, repl, text)

    text = text.replace(f"{PTHAHA}{ALAPH}#", "a#")
    text = text.replace(f"{ZLAMA_ANGULAR}{ALAPH}#", "ē#")

    pattern = f"{ZLAMA_HORIZONTAL}{ALAPH}(?:{YUDH})?#"
    repl = f"i{GLOTTAL_STOP}#"
    text = re.sub(pattern, repl, text)

    text = text.replace(f"{ZQAPHA}{ALAPH}#", "ā#")
    text = text.replace(f"{ALAPH}#", "ā#")
    text = text.replace(f"#{ALAPH}", "#")
    text = text.replace(ALAPH, GLOTTAL_STOP)

    pattern = f"#{WAW}{consonantsAndVowelsCapture}"
    repl = "#w-\\1"
    text = re.sub(pattern, repl, text)

    def _ttNext_replace(m):
        return ttNext[m.group(1)]

    text = re.sub(ttNextKeysCapture, _ttNext_replace, text)

    # ([ēīā])GLOTTAL_STOP([lettersCapture]) => $1$2
    pattern = f"([ēīā]){GLOTTAL_STOP}{lettersCapture}"
    repl = r"\1\2"
    text = re.sub(pattern, repl, text)

    # ([vowelsW])([vowels]) => $1w$2
    pattern = f"([{vowelsW}])([{vowels}])"
    repl = r"\1w\2"
    text = re.sub(pattern, repl, text)

    # ([vowelsY])([vowels]) => $1y$2
    pattern = f"([{vowelsY}])([{vowels}])"
    repl = r"\1y\2"
    text = re.sub(pattern, repl, text)

    # ( [aā] ) ḇ ( [consonantsMinusGlides not ḇ] ) => $1w$2
    pattern = f"([aā])ḇ([{consonantsMinusGlides.replace('ḇ','')}])"
    repl = r"\1w\2"
    text = re.sub(pattern, repl, text)

    # (u)ḇ([consonantsMinusGlides]) => remove ḇ => $1$2
    pattern = f"uḇ([{consonantsMinusGlides}])"
    repl = r"u\1"
    text = re.sub(pattern, repl, text)

    # remove consecutive duplicate characters for certain set
    # ([ʿʾāšyḥhčžj])\1+ => \1
    pattern = r"([ʿʾāšyḥhčžj])\1+"
    repl = r"\1"
    text = re.sub(pattern, repl, text)

    # text.replaceAll(/([ḥčḡš])h/g, '$1');
    text = re.sub(r'([ḥčḡš])h', r'\1', text)

    # text.replaceAll(`-${GLOTTAL_STOP}`, '-')
    text = text.replace(f"-{GLOTTAL_STOP}", "-")

    # We keep a separate copy for phonetic transformations
    phoneticText = text

    # remove all # from the final "latin" form
    text = text.replace('#', '')

    # -----------------------------------------
    # 4. Additional phonetic transformations
    # -----------------------------------------
    # e.g.  text.replaceAll(/ē([ʿʾ])/g, 'eh$1')
    pattern = f"ē([{PHARYNGEAL}{GLOTTAL_STOP}])"
    repl = r"eh\1"
    phoneticText = re.sub(pattern, repl, phoneticText)

    # /([ʿʾ])ā#/ => $1ah#
    pattern = f"([{PHARYNGEAL}{GLOTTAL_STOP}])ā#"
    repl = r"\1ah#"
    phoneticText = re.sub(pattern, repl, phoneticText)

    # phoneticText = phoneticText.replaceAll(/ē#/g, 'eh#');
    phoneticText = re.sub(r"ē#", "eh#", phoneticText)

    # phoneticText = phoneticText.replaceAll(/uh#/g, 'oo#');
    phoneticText = re.sub(r"uh#", "oo#", phoneticText)

    # remove # from phoneticText
    phoneticText = phoneticText.replace('#', '')

    # handle special delimiters sDelimiter / eDelimiter from JS
    sDelimiter = ' ❋ '
    eDelimiter = ' ❊ '
    # we replicate the same logic
    # re = new RegExp(`([${consonantsMinusGlides}${vowels}wy])${nonCG}ì`, 'g')
    # but for brevity, these steps are rarely used unless you replicate the exact JS environment
    # here we do them as placeholders in case needed:

    # Build the nonCapture pattern used in JS
    nonCG1 = rf"(?:[ ]+){sDelimiter}(?:[ ]*)"
    nonCG2 = rf"(?:[ ]*){sDelimiter}(?:[ ]+)"
    nonCG = rf"(?:{nonCG1}|{nonCG2})"

    pattern = rf"([{consonantsMinusGlides}{vowels}wy]){nonCG}ì"
    repl = rf"\1-{sDelimiter}"
    phoneticText = re.sub(pattern, repl, phoneticText)

    pattern = rf"([{consonantsMinusGlides}{vowels}wy])(?:[ ]+)ì"
    repl = r"\1-"
    phoneticText = re.sub(pattern, repl, phoneticText)

    # handle standalone "to be" haweh => phoneticText = phoneticText.replaceAll('ì', '-')
    phoneticText = phoneticText.replace('ì', '-')

    # We replicate the final replacements in JS:
    # w- => oo-
    phoneticText = phoneticText.replace('w-', 'oo-')
    phoneticText = phoneticText.replace('āyh', 'āy')
    phoneticText = phoneticText.replace('ayh', 'ay')

    # Apply the final re-based phonetic replacements
    def _phonetic_replace(m):
        return phoneticReplacements[m.group(1)]

    phoneticText = re.sub(phoneticReplacementsKeysCapture, _phonetic_replace, phoneticText)

    # Return dict with both forms
    return {
        'latin': text,
        'phonetic': phoneticText,
    }

if __name__ == "__main__":
    example_text = "ܟܝܼ"
    result = AIITranslit(example_text)
    print("Latin transliteration:", result['latin'])
    print("Phonetic transliteration:", result['phonetic'])