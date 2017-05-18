TARGET = sudoku sudoku_fc sudoku_fc_h

GPP = g++
GPP_FLAGS = -std=c++11

.PHONY : all clean

all :	$(TARGET)

clean :
	rm -f $(TARGET)

sudoku : sudoku.cpp
	 $(GPP) $(GPP_FLAGS) -o $@ $<

sudoku_fc : sudoku_fc.cpp
	 $(GPP) $(GPP_FLAGS) -o $@ $<

sudoku_fc_h : sudoku_fc_h.cpp
	 $(GPP) $(GPP_FLAGS) -o $@ $<

