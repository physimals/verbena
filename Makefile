#include ${FSLCONFDIR}/default.mk

PROJNAME = verbena

SCRIPTS = verbena

# Pass Git revision details
GIT_SHA1:=$(shell git describe --dirty)
GIT_DATE:=$(shell git log -1 --format=%ad --date=local)
CXXFLAGS += -DGIT_SHA1=\"${GIT_SHA1}\" -DGIT_DATE="\"${GIT_DATE}\""

all: ${SCRIPTS}

# Always rebuild scripts
.PHONY: FORCE
FORCE:

$(SCRIPTS): %: %.in FORCE
	sed -e "s/\$${GIT_SHA1}/${GIT_SHA1}/" -e "s/\$${GIT_DATE}/${GIT_DATE}/" $< >$@

clean:
	rm ${SCRIPTS}

