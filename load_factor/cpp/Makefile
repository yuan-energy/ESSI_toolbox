# /usr/lib/x86_64-linux-gnu/hdf5/serial/libhdf5_cpp.a
# /usr/lib/x86_64-linux-gnu/hdf5/serial/libhdf5_cpp.a
compile: main.cpp
	g++ main.cpp -o main -I/usr/include/hdf5/serial -L/usr/lib/x86_64-linux-gnu/hdf5/serial/ -lhdf5 -lhdf5_cpp -std=c++11 -Wall


run:
	./main

clean:
	rm -f case_cpp_combine.h5.feioutput
	rm -f main
