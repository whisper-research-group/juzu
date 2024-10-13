#!/usr/bin/zsh

# ----------  CONST SETTINGS  ---------> #

dir=/path/to/discussion-dir # set the directory location of the `discussion-dir`

# JUZU DIR
juzu=juzu/zsh/juzu/juzu.sh

# SYSTEM & INPUT DIRS
systemDir=juzu
inputDir=data-dir

# UZUME
# audible frequency
minAudibleFreq=20
maxAudibleFreq=20000

# uzume consts
minFreqDif=60
minContDifStr="8.0 * 10 ** -4"
OutFormantNum=30

# kazune consts
kazuneFormantNum=6
kazuneThreshold=50
kazuneErrorRange=10
kazuneAccuracy=3

# <---------  CONST SETTINGS  ---------- #

main() {
    source $juzu
    juzu \
        $systemDir \
        $inputDir \
        \
        $minAudibleFreq \
        $maxAudibleFreq \
        \
        $minFreqDif \
        $minContDif \
        $OutFormantNum \
        $minContDifStr \
        \
        $kazuneFormantNum \
        $kazuneThreshold \
        $kazuneErrorRange \
        $kazuneAccuracy

}

# ----------  (JUZU CONSTS STRUCT)  ---------> #
#
# juzu () {
#     systemDir=$1
#     inputDir=$2
#
#     minAudibleFreq=$3
#     maxAudibleFreq=$4
#
#     minFreqDif=$5
#     minContDif=$6
#     OutFormantNum=$7
# }
#
# <---------  (JUZU CONSTS STRUCT)  ---------- #

juzu=$dir/$juzu
systemDir=$dir/$systemDir
inputDir=$dir/$inputDir
minContDif=$((minContDifStr))

# ==========  EXEC MAIN  ========== #

main
