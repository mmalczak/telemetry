KERNEL_PATH?=../linux-5.3.1
all:
	gcc tlm.c -I $(KERNEL_PATH)/drivers/cpufreq/ -o tlm

clean:
	rm -f tlm
