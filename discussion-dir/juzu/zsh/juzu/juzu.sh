#!/usr/bin/zsh

juzu() {
    ESC=$(printf '\033')
    BOLD="${ESC}[1m"
    GREEN="${ESC}[32m"
    NORMAL="${ESC}[m"
    TAB="\t"

    systemDir=$1
    inputDir=$2

    # ==========  UZUME SETTINGS  ========== #

    minAudibleFreq=$3
    maxAudibleFreq=$4

    minFreqDif=$5
    minContDif=$6
    outFormantNum=$7
    minContDifStr=$8

    # ==========  UZUME SETTINGS  ========== #

    # ==========  KAZUNE SETTINGS  ========== #

    kazuneFormantNum=$9
    kazuneThreshold=$10
    kazuneErrorRange=$11
    kazuneAccuracy=$12

    # ==========  KAZUNE SETTINGS  ========== #

    # ==========  SWITCHES  ========== #

    typeset -g -A procs=(
        "init" true
        "fuzuki" false # unnecessary for 2nd or later executions
        "nuzume" false
        "kazune" false
        "kurabe" false
        "finale" false
        "term" false
    )

    # ==========  SWITCHES  ========== #

    outDirs=(
        "seg-files"
        "log-files"
        "cut-sound-files"
        "formants-fig"
        "formants-json"
        "fund-approx-fig"
        "overtones-json"
        "syll-pairs"
        "result1-json"
        "result1-fig"
        "result2-json"
        "result2-fig"
        "final-output-fig"
        "final-output-json"
    )
    speechTypes=(
        "normal"
        "whisper"
    )
    subjectNums=(
        "0019"
        "0132"
        "0208"
        "0303"
        "0420"
        "0518"
        "0623"
        "0821"
        "0927"
        "1112"
        "1231"
        "1314"
        "1417"
        "1602"
        "1705"
        "1809"
        "1933"
        "2000"
        "2104"
        "2213"
        "2329"
        "2410"
        "2511"
        "2616"
        "2715"
        "2834"
        "2925"
        "3024"
        "3122"
        "3230"
        "3306"
        "5000"
    )
    sentenceNums=(
        "01"
        "02"
        "03"
        "04"
        "05"
        "06"
        "07"
        "08"
        "09"
        "10"
        "11"
        "12"
        "13"
        "14"
    )

    echo -e "${BOLD}started  ${TAB}JUZU${NORMAL}"
    echo

    if [ $procs[init] = true ]; then
        init $inputDir \
            $minContDifStr
    fi
    if [ $procs[fuzuki] = true ]; then
        fuzuki \
            $inputDir \
            $systemDir
    fi
    if [ $procs[nuzume] = true ]; then
        nuzume \
            $inputDir \
            $systemDir \
            \
            $minAudibleFreq \
            $maxAudibleFreq \
            \
            $minFreqDif \
            $minContDif \
            $outFormantNum
    fi
    if [ $procs[kazune] = true ]; then
        kazune \
            $inputDir \
            $systemDir \
            \
            $kazuneFormantNum \
            $kazuneThreshold \
            $kazuneErrorRange \
            $kazuneAccuracy
    fi
    if [ $procs[kurabe] = true ]; then
        kurabe \
            $inputDir \
            $systemDir
    fi
    if [ $procs[finale] = true ]; then
        finale
    fi
    if [ $procs[term] = true ]; then
        term
    fi

    echo
    echo -e "${BOLD}completed${TAB}JUZU${NORMAL}"
    echo
}

# ==========  INIT  ========== #

function init() {
    local inputDir=$1
    local minContDifStr=$2

    echo -e "${GREEN}init:${TAB}started${NORMAL}"
    constants_info="data-dir/constants.txt"
    rm $constants_info
    touch $constants_info

    echo "    ===== CONSTANTS INFO =====" >>$constants_info
    echo >>$constants_info
    echo "system dir:   $systemDir" >>$constants_info
    echo "input dir:    $inputDir" >>$constants_info
    echo >>$constants_info
    echo "uzume settings:" >>$constants_info
    echo "    minimum audible frequency:        $minAudibleFreq" >>$constants_info
    echo "    maximum audible frequency:        $maxAudibleFreq" >>$constants_info
    echo >>$constants_info
    echo "    minimum frequency difference:     $minFreqDif" >>$constants_info
    echo "    minimum contribution difference:  $minContDifStr" >>$constants_info
    echo "    out formant number:               $outFormantNum" >>$constants_info
    echo >>$constants_info
    echo >>$constants_info
    echo "kazune settings:" >>$constants_info
    echo "    kazune formant number:            $kazuneFormantNum" >>$constants_info
    echo "    kazune threshold:                 $kazuneThreshold" >>$constants_info
    echo "    kazune error range:               $kazuneErrorRange" >>$constants_info
    echo "    kazune accuracy:                  $kazuneAccuracy" >>$constants_info

    cd $inputDir
    for outDir in ${outDirs[@]}; do
        rm -r $outDir
        for speechType in ${speechTypes[@]}; do
            if [ $outDir = "result2-json" ] || [ $outDir = "result2-fig" ] || [ $outDir = "final-output-fig" ] || [ $outDir = "final-output-json" ]; then
                mkdir -p "$outDir/$speechType"
            else # elif [ $outDir != "seg-files" ] && [ $outDir != "log-files" ] && [ $outDir != "cut-sound-files" ]; then # excluded due to not running `fuzuki` for 2nd or later executions
                for subjectNum in ${subjectNums[@]}; do
                    mkdir -p "$outDir/$speechType/$subjectNum"
                done
            fi
        done
    done

    echo -e "${GREEN}init:${TAB}done${NORMAL}"
}

function fuzuki() {
    local inputDir=$1
    local systemDir=$2

    echo -e "${GREEN}fuzuki:${TAB}started${NORMAL}"

    echo -e "${GREEN}fuzuki:${TAB}wav2seg:${TAB}started${NORMAL}"
    wav2seg $inputDir
    echo -e "${GREEN}fuzuki:${TAB}wav2seg:${TAB}done${NORMAL}"

    echo -e "${GREEN}fuzuki:${TAB}seg2cut:${TAB}started${NORMAL}"
    seg2cut $inputDir $systemDir
    echo -e "${GREEN}fuzuki:${TAB}seg2cut:${TAB}done${NORMAL}"

    echo -e "${GREEN}fuzuki:${TAB}done${NORMAL}"
}

# ==========  WAV2SEG  ========== #

function wav2seg() {
    local inputDir=$1

    for speechType in ${speechTypes}; do
        echo -e "fuzuki:${TAB}wav2seg:${TAB}type=${TAB}$speechType"

        for subjectNum in ${subjectNums[@]}; do
            echo -e "fuzuki:${TAB}wav2seg:${TAB}subject num=${TAB}$subjectNum"

            soundFilesDir="$inputDir/sound-files/$speechType/$subjectNum"
            tempoDir="$soundFilesDir/tempo-dir"

            for sentenceNum in ${sentenceNums[@]}; do
                echo -e "fuzuki:${TAB}wav2seg:${TAB}file name=${TAB}$sentenceNum"

                wav2segTempoDir \
                    $inputDir \
                    $sentenceNum \
                    $subjectNum

                juliusSegmentation $tempoDir

                cpSegLog \
                    $inputDir \
                    $sentenceNum \
                    $subjectNum

                rm -r $tempoDir
            done
        done
    done
}

function wav2segTempoDir() {
    local dir=$1
    local sentenceNum=$2
    local subjectNum=$3

    local transFilesDir="$dir/transcription-files"
    local soundFilesDir="$dir/sound-files/$speechType/$subjectNum"
    local tempoDir="$soundFilesDir/tempo-dir"

    mkdir $tempoDir
    cp "$soundFilesDir/$sentenceNum.wav" $tempoDir
    cp "$transFilesDir/$sentenceNum.txt" $tempoDir
}

function juliusSegmentation() {
    local dir=$1

    cd "$systemDir/perl/julius"
    perl julius.pl $1

    cd $dir
}

function cpSegLog() {
    local dir=$1
    local sentenceNum=$2
    local subjectNum=$3

    local soundFilesDir="$dir/sound-files/$speechType/$subjectNum"
    local segFilesDir="$dir/seg-files/$speechType/$subjectNum"
    local logFilesDir="$dir/log-files/$speechType/$subjectNum"
    local tempoDir="$soundFilesDir/tempo-dir"

    cp "$tempoDir/$sentenceNum.lab" "$segFilesDir/$sentenceNum.txt"
    cp "$tempoDir/$sentenceNum.log" $logFilesDir
}

# ==========  SEG2CUT  ========== #

function seg2cut() {
    for speechType in ${speechTypes}; do
        echo -e "fuzuki:${TAB}seg2cut:${TAB}type=${TAB}$speechType"

        for subjectNum in ${subjectNums[@]}; do
            echo -e "fuzuki:${TAB}seg2cut:${TAB}subject num=${TAB}$subjectNum"

            for sentenceNum in ${sentenceNums[@]}; do
                echo -e "fuzuki:${TAB}seg2cut:${TAB}file name=${TAB}$sentenceNum"

                seg2cutTempoDir \
                    $inputDir \
                    $speechType \
                    $sentenceNum \
                    $subjectNum

                soundFilesDir="$inputDir/sound-files/$speechType/$subjectNum"
                tempoDir="$soundFilesDir/tempo-dir"

                cd $tempoDir
                python3 "$systemDir/py/fuzuki/run-fuzuki.py" "$sentenceNum"

                rm "$sentenceNum.wav"
                rm "$sentenceNum.txt"

                cutSoundFilesDir="$inputDir/cut-sound-files/$speechType/$subjectNum"

                cp -r $tempoDir $cutSoundFilesDir

                cd $inputDir
                rm -r $tempoDir

                cd $cutSoundFilesDir
                mv "tempo-dir" $sentenceNum

                cd $systemDir
            done
        done
    done
}

function seg2cutTempoDir() {
    local dir=$1
    local speechType=$2
    local sentenceNum=$3
    local subjectNum=$4

    local segFilesDir="$dir/seg-files/$speechType/$subjectNum"
    local soundFilesDir="$dir/sound-files/$speechType/$subjectNum"
    local tempoDir="$soundFilesDir/tempo-dir"

    mkdir $tempoDir
    cp "$soundFilesDir/$sentenceNum.wav" $tempoDir
    cp "$segFilesDir/$sentenceNum.txt" $tempoDir
}

# ==========  NUZUME  ========== #

function nuzume() {
    echo -e "${GREEN}nuzume:${TAB}started${NORMAL}"

    local inputDir=$1
    local systemDir=$2
    local minAudibleFreq=$3
    local maxAudibleFreq=$4
    local minFreqDif=$5
    local minContDif=$6
    local outFormantNum=$7

    cd $inputDir
    for speechType in ${speechTypes[@]}; do
        for subjectNum in ${subjectNums[@]}; do
            for sentenceNum in ${sentenceNums[@]}; do
                local dirPath="cut-sound-files/$speechType/$subjectNum/$sentenceNum/"
                mkdir "formants-fig/$speechType/$subjectNum/$sentenceNum"
                mkdir "formants-json/$speechType/$subjectNum/$sentenceNum"
                python3 \
                    "$systemDir/py/nuzume/run-nuzume.py" \
                    "$dirPath" \
                    "$speechType" \
                    "$subjectNum" \
                    "$sentenceNum" \
                    "$minAudibleFreq" \
                    "$maxAudibleFreq" \
                    "$minFreqDif" \
                    "$minContDif" \
                    "$outFormantNum" &
            done
            wait
        done
    done

    echo -e "${GREEN}nuzume:${TAB}done${NORMAL}"
}

# ==========  KAZUNE  ========== #

function kazune() {
    echo -e "${GREEN}kazune:${TAB}started${NORMAL}"

    local inputDir=$1
    local systemDir=$2
    local kazuneFormantNum=$3
    local kazuneThreshold=$4
    local kazuneErrorRange=$5
    local kazuneAccuracy=$6

    cd $inputDir
    for speechType in ${speechTypes[@]}; do
        for subjectNum in ${subjectNums[@]}; do
            for sentenceNum in ${sentenceNums[@]}; do
                mkdir "fund-approx-fig/$speechType/$subjectNum/$sentenceNum"
                mkdir "overtones-json/$speechType/$subjectNum/$sentenceNum"

                local jsonDir="formants-json/$speechType/$subjectNum/$sentenceNum"
                local jsonFiles=($(find $jsonDir -type f))
                local jsonFilesSorted=($(printf "%s\n" "${jsonFiles[@]}" | sort))
                local figFileName="fund-approx-fig/$speechType/$subjectNum/$sentenceNum/$(basename $jsonFile .json).jpg"

                for jsonFile in ${jsonFilesSorted}; do
                    python3 \
                        "$systemDir/py/kazune/run-kazune.py" \
                        "$jsonFile" \
                        "$speechType" \
                        "$subjectNum" \
                        "$sentenceNum" \
                        "$figFileName" \
                        "$kazuneFormantNum" \
                        "$kazuneThreshold" \
                        "$kazuneErrorRange" \
                        "$kazuneAccuracy" &
                done
            done
            wait
        done
    done

    echo -e "${GREEN}kazune:${TAB}done${NORMAL}"
}

function kurabe() {
    local inputDir=$1
    local systemDir=$2

    typeset -g -A syllables=(
        "p0" "01/09po"
        "b0" "03/05ba"
        "p1" "02/04po"
        "b1" "04/05be"
        "pj0" "05/04pi"
        "bj0" "06/04bi"
        "pj1" "06/02pi"
        "bj1" "07/07bi"
        "t0" "06/08ta"
        "d0" "01/10da"
        "t1" "02/01ta"
        "d1" "11/07da"
        "k0" "03/01ka"
        "g0" "08/01ga"
        "k1" "03/08ka"
        "g1" "10/03ga"
        "kj0" "07/06kyuu"
        "gj0" "10/01gyoo"
        "kj1" "07/02ki"
        "gj1" "13/01gi"
        "tsh0" "07/05chi"
        "dzh0" "14/01ji"
        "tsh1" "01/07chii"
        "dzh1" "09/01ji"
        "s0" "11/02sa"
        "z0" "09/03za"
        "s1" "11/01sa"
        "z1" "10/02za"
        "sh0" "06/07shi"
        "zh0" "12/02ji"
        "sh1" "06/01shi"
        "zh1" "01/12ji"
    )

    pairs=(
        "p-b0"
        "p-b1"
        "pj-bj0"
        "pj-bj1"
        "t-d0"
        "t-d1"
        "k-g0"
        "k-g1"
        "kj-gj0"
        "kj-gj1"
        "tsh-dzh0"
        "tsh-dzh1"
        "s-z0"
        "s-z1"
        "sh-zh0"
        "sh-zh1"
    )

    typeset -g -A kurabePairs=(
        "p0" "p-b0"
        "b0" "p-b0"
        "p1" "p-b1"
        "b1" "p-b1"
        "pj0" "pj-bj0"
        "bj0" "pj-bj0"
        "pj1" "pj-bj1"
        "bj1" "pj-bj1"
        "t0" "t-d0"
        "d0" "t-d0"
        "t1" "t-d1"
        "d1" "t-d1"
        "k0" "k-g0"
        "g0" "k-g0"
        "k1" "k-g1"
        "g1" "k-g1"
        "kj0" "kj-gj0"
        "gj0" "kj-gj0"
        "kj1" "kj-gj1"
        "gj1" "kj-gj1"
        "tsh0" "tsh-dzh0"
        "dzh0" "tsh-dzh0"
        "tsh1" "tsh-dzh1"
        "dzh1" "tsh-dzh1"
        "s0" "s-z0"
        "z0" "s-z0"
        "s1" "s-z1"
        "z1" "s-z1"
        "sh0" "sh-zh0"
        "zh0" "sh-zh0"
        "sh1" "sh-zh1"
        "zh1" "sh-zh1"
    )

    typeset -g -A renameList=(
        "p0" "0.p0"
        "b0" "1.b0"
        "p1" "0.p1"
        "b1" "1.b1"
        "pj0" "0.pj0"
        "bj0" "1.bj0"
        "pj1" "0.pj1"
        "bj1" "1.bj1"
        "t0" "0.t0"
        "d0" "1.d0"
        "t1" "0.t1"
        "d1" "1.d1"
        "k0" "0.k0"
        "g0" "1.g0"
        "k1" "0.k1"
        "g1" "1.g1"
        "kj0" "0.kj0"
        "gj0" "1.gj0"
        "kj1" "0.kj1"
        "gj1" "1.gj1"
        "tsh0" "0.tsh0"
        "dzh0" "1.dzh0"
        "tsh1" "0.tsh1"
        "dzh1" "1.dzh1"
        "s0" "0.s0"
        "z0" "1.z0"
        "s1" "0.s1"
        "z1" "1.z1"
        "sh0" "0.sh0"
        "zh0" "1.zh0"
        "sh1" "0.sh1"
        "zh1" "1.zh1"
    )

    cd $inputDir
    echo -e "${GREEN}kurabe:${TAB}kurabe1:${TAB}started${NORMAL}"
    for speechType in ${speechTypes[@]}; do
        echo -e "kurabe:${TAB}kurabe1:${TAB}type=${TAB}$speechType"
        for subjectNum in ${subjectNums[@]}; do
            echo -e "kurabe:${TAB}kurabe1:${TAB}subject num=${TAB}$subjectNum"
            mkdir -p "syll-pairs/$speechType/$subjectNum"

            for pair in ${pairs[@]}; do
                mkdir "syll-pairs/$speechType/$subjectNum/$pair"
            done

            local overTonesDir="overtones-json/$speechType/$subjectNum"
            local cutSoundFilesDir="cut-sound-files/$speechType/$subjectNum"
            local syllPairsDir="syll-pairs/$speechType/$subjectNum"

            cd $inputDir
            # VSCode raises a warning `parameter expansion requires a literal` at
            # `${(k)kurabePairs}` but there is no problem at runtime. The warning
            # can be removed by using the expression `${!kurabePairs[@]}` instead
            # of `${(k)kurabePairs}` but Zsh will raise an error `bad substitution`
            # with this expression at runtime and doesn't work.
            for kurabePair in ${(k)kurabePairs}; do
                kurabe1 \
                    "$overTonesDir" \
                    "$cutSoundFilesDir" \
                    "$kurabePair" \
                    "$syllPairsDir/${kurabePairs[$kurabePair]}" &
            done
            wait
        done
    done
    echo -e "${GREEN}kurabe:${TAB}kurabe1:${TAB}done${NORMAL}"

    cd $inputDir
    echo -e "${GREEN}kurabe:${TAB}kurabe2:${TAB}started${NORMAL}"
    for speechType in ${speechTypes[@]}; do
        echo -e "kurabe:${TAB}kurabe2:${TAB}type=${TAB}$speechType"
        for subjectNum in ${subjectNums[@]}; do
            echo -e "kurabe:${TAB}kurabe2:${TAB}subject num=${TAB}$subjectNum"
            local syllPairsDir="syll-pairs/$speechType/$subjectNum"
            for pair in ${pairs[@]}; do
                python3 \
                    "$systemDir/py/kurabe/run-kurabe.py" \
                    "$inputDir" \
                    "$inputDir/$syllPairsDir/$pair" \
                    "$speechType" \
                    "$subjectNum" \
                    "$pair" \
                    "$inputDir/result1-fig/$speechType/$subjectNum/$pair.jpg" &
            done
            wait
        done
    done
    echo -e "${GREEN}kurabe:${TAB}kurabe2:${TAB}done${NORMAL}"
}

function kurabe1() {
    local overTonesDir=$1
    local cutSoundFilesDir=$2
    local kurabePair=$3
    local syllPairPath=$4

    echo -e "kurabe:${TAB}kurabe1:${TAB}pair=${TAB}$kurabePairs[$kurabePair]" &&
        cp \
            "$overTonesDir/$syllables[$kurabePair].json" \
            $syllPairPath &&
        mv \
            "$syllPairPath/$(basename $syllables[$kurabePair]).json" \
            "$syllPairPath/$renameList[$kurabePair].json" &&
        cp \
            "$cutSoundFilesDir/$syllables[$kurabePair].wav" \
            $syllPairPath &&
        mv \
            "$syllPairPath/$(basename $syllables[$kurabePair]).wav" \
            "$syllPairPath/$renameList[$kurabePair].wav"
}

function finale() {
    pairs=(
        "p-b0"
        "p-b1"
        "pj-bj0"
        "pj-bj1"
        "t-d0"
        "t-d1"
        "k-g0"
        "k-g1"
        "kj-gj0"
        "kj-gj1"
        "tsh-dzh0"
        "tsh-dzh1"
        "s-z0"
        "s-z1"
        "sh-zh0"
        "sh-zh1"
    )

    cd $inputDir
    for speechType in ${speechTypes[@]}; do
        for pair in ${pairs[@]}; do
            mkdir "result2-json/$speechType/$pair" &&
                mkdir "result2-fig/$speechType/$pair" &
        done
        wait
    done

    for speechType in ${speechTypes[@]}; do
        for subjectNum in ${subjectNums[@]}; do
            for pair in ${pairs[@]}; do
                cp \
                    "result1-json/$speechType/$subjectNum/$pair.json" \
                    "result2-json/$speechType/$pair" &&
                mv \
                    "result2-json/$speechType/$pair/$pair.json" \
                    "result2-json/$speechType/$pair/$subjectNum.json" &
            done
            wait
        done
    done

    echo -e "${GREEN}finale:${TAB}started${NORMAL}"
    for speechType in ${speechTypes[@]}; do
        echo -e "finale:${TAB}type=${TAB}$speechType"
        for pair in ${pairs[@]}; do
            # `${#subjectNums}` == (size of `$subjectNums`)
            python3 \
                "$systemDir/py/finale/run-finale.py" \
                "$inputDir" \
                "$speechType" \
                "$pair" \
                "${#subjectNums}" \
                "$inputDir/result2-fig/$speechType/$pair/result.jpg" &
        done
        wait
    done
    echo -e "${GREEN}finale:${TAB}done${NORMAL}"
}

function term() {
    pairs=(
        "p-b0"
        "p-b1"
        "pj-bj0"
        "pj-bj1"
        "t-d0"
        "t-d1"
        "k-g0"
        "k-g1"
        "kj-gj0"
        "kj-gj1"
        "tsh-dzh0"
        "tsh-dzh1"
        "s-z0"
        "s-z1"
        "sh-zh0"
        "sh-zh1"
    )

    cd $inputDir
    for speechType in ${speechTypes[@]}; do
        for pair in ${pairs[@]}; do
            cp \
                "result2-fig/$speechType/$pair/result.jpg" \
                "final-output-fig/$speechType" &&
            mv \
                "final-output-fig/$speechType/result.jpg" \
                "final-output-fig/$speechType/$pair.jpg" &&
            cp \
                "result2-json/$speechType/$pair/result.json" \
                "final-output-json/$speechType" &&
            mv \
                "final-output-json/$speechType/result.json" \
                "final-output-json/$speechType/$pair.json"
        done
    done
}
