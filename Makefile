KERNEL_PATH?=../linux-5.6.4
all:
	gcc tlm.c -I $(KERNEL_PATH)/drivers/cpufreq/ -o tlm

clean:
	rm tlm
