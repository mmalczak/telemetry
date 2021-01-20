KERNEL_PATH?=../linux-[0-9].[0-9].[0-9]
all:
	gcc tlm.c -I $(KERNEL_PATH)/drivers/cpufreq/ -o tlm

clean:
	rm -f tlm
