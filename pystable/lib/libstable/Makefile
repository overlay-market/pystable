# Libstable main Makefile
# 
# This file compiles the whole Libstable package:
#    - Shared and static versions of the library and MATLAB interface.
#    - Example and test programs
#
# When publising results obtained with this software, please cite:
#  [1] Libstable: Fast, Parallel and High-Precision Computation of \alpha-stable
#      Distributions in C/C++, R and MATLAB. Javier Royuela del Val, Federico
#      Simmross Wattenberg and Carlos Alberola López, Journal of Statistical
#      Software (under review), 2015.
#
# Copyright (C) 2013. Javier Royuela del Val
#                    Federico Simmross Wattenberg
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; ; version 3 of the license.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; If not, see <http://www.gnu.org/licenses/>.
#
#  Javier Royuela del Val.
#  E.T.S.I. Telecomunicación
#  Universidad de Valladolid
#  Paseo de Belén 15, 47002 Valladolid, Spain.
#  jroyval@lpi.tel.uva.es    
#

# Compiling and linking options
CC      = gcc
CFLAGS  = -fPIC -O3 -march=native -ffast-math -DHAVE_INLINE
LDFLAGS = 
LIBS    = -lgsl -lgslcblas -lm -pthread

OBJ = src
SRC = src
BIN = bin

# Library files
STABLE_DIR = ./stable
s_HDR = stable.h stable_integration.h methods.h mcculloch.h
s_SRC = stable_dist.c stable_pdf.c stable_cdf.c stable_rnd.c stable_q.c  \
        stable_integration.c methods.c stable_common.c                   \
        mcculloch.c stable_fit.c stable_koutrouvelis.c

STABLE_HDR = $(patsubst %,$(STABLE_DIR)/$(SRC)/%,$(s_HDR))
STABLE_SRC = $(patsubst %,$(STABLE_DIR)/$(SRC)/%,$(s_SRC))
STABLE_OBJ = $(patsubst %.c,$(STABLE_DIR)/$(OBJ)/%.o,$(s_SRC))

# Test programs files
TESTS_DIR = ./tests
t_HDR = 
t_SRC = stable_test.c stable_array.c fittest.c

TESTS_HDR = $(patsubst %,$(TESTS_DIR)/$(SRC)/%,$(t_HDR))
TESTS_SRC = $(patsubst %,$(TESTS_DIR)/$(SRC)/%,$(t_SRC))
TESTS_OBJ = $(patsubst %.c,$(TESTS_DIR)/$(OBJ)/%.o,$(t_SRC))

# Targets
.PHONY: all libstable tests clean

all: libstable tests clean

clean:
	rm -rf $(STABLE_OBJ)
	rm -rf $(TESTS_OBJ)
	rm -rf $(REPLM_OBJ)
	                  	
# Stable library. Shared and static versions.
#libstable:
libstable: $(STABLE_OBJ) $(STABLE_HDR)
	@echo -ne '\n$@:\n\t'
	$(CC) -shared $(STABLE_OBJ) $(LDFLAGS) -o $(STABLE_DIR)/libs/$@.so $(LIBS)
	ar -rv $(STABLE_DIR)/libs/$@.a $(STABLE_OBJ)
	@echo Copy libstable.so and stable.h to matlab front-end folder
	cp ./stable/src/stable.h ./matlab
	cp ./stable/libs/libstable.so ./matlab

# Test programs.
tests: $(TESTS_OBJ) $(TESTS_HDR)
	@echo -ne '\n$@:\n\t'
	$(CC) $(TESTS_DIR)/$(OBJ)/stable_test.o $(STABLE_DIR)/libs/libstable.a -I$(STABLE_DIR)/$(SRC) \
	                 -o $(TESTS_DIR)/$(BIN)/stable_test $(LIBS) $(LDFLAGS)
	$(CC) $(TESTS_DIR)/$(OBJ)/stable_array.o $(STABLE_DIR)/libs/libstable.a -I$(STABLE_DIR)/$(SRC) \
	                 -o $(TESTS_DIR)/$(BIN)/stable_array $(LIBS) $(LDFLAGS)
	$(CC) $(TESTS_DIR)/$(OBJ)/fittest.o $(STABLE_DIR)/libs/libstable.a -I$(STABLE_DIR)/$(SRC) \
	                 -o $(TESTS_DIR)/$(BIN)/fittest $(LIBS) $(LDFLAGS)
	@echo
	
# General compilation target.
$(STABLE_DIR)/$(OBJ)/%.o: $(STABLE_DIR)/$(SRC)/%.c
	@echo -ne '$@:  '
	$(CC) -c -I $(STABLE_DIR)/$(SRC) -o $@ $< $(CFLAGS)
$(TESTS_DIR)/$(OBJ)/%.o: $(TESTS_DIR)/$(SRC)/%.c
	@echo -ne '$@:  '
	$(CC) -c -I $(STABLE_DIR)/$(SRC) -o $@ $< $(CFLAGS)