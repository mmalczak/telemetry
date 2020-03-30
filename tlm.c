/*
 *  tlm.c
 *
 *  User-space application reading data from tlm LKM.
 *
 *  Copyright (C)  2017 Michał Getka
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation.
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <libgen.h>
#include "tlmt.h"

// accepted data formats
enum fmt_t {CSV, HR};

#define max(a,b) \
  ({ __typeof__ (a) _a = (a); \
      __typeof__ (b) _b = (b); \
    _a > _b ? _a : _b; })

#define min(a,b) \
  ({ __typeof__ (a) _a = (a); \
      __typeof__ (b) _b = (b); \
    _a < _b ? _a : _b; })

int help(char *appName)
{
  printf(  "Kernel telemetry reader."                     \
    "  Copyright (C)  2017 Michał Getka\n\n"              \
    "\tProvides tlm LKM buffer to stdout with "           \
    "specified formatting.\n\n");                         \
  printf("\tThis tlm application is appropriate to read"  \
    "\n\tdata from tlmsrv of type %s.\n\n", DEVICE_NAME); \
  printf(  "usage:\t%s [-option <arguments>]\n"           \
    "\t-h\t\tPrint out this message\n"                    \
    "\t-p\t\tPrint model parameters to a file\n"          \
    "\t-d DEVICE\tRead data from tlm server DEVICE.\n"    \
    "\t\t\tif not set, DEVICE defaults to \\dev\\%s\n"    \
    "\t-r\t\treset tlm srerver buffer.\n"                 \
    "\t-l\t\tinclude labels of timeseries signals\n"      \
    "\t-f FORMAT\tSets output format type\n"              \
    "\tArguments:\n"                                      \
    "\t hr - human readable (default)\n"                  \
    "\t csv - comma separated values\n"                   \
    "\nExit status:\n"                                    \
      "-lost_frames\tif OK,\n"                            \
      ">0\t\tif problems,\n"                              \
    "\n\tReport bugs to michal.getka[at]gmail.com\n", appName, DEVICE_NAME, DEVICE_NAME);

  exit(0);

}

int main(int argc, char *argv[])
{

  unsigned int i, numel;
  int fd, ret, rc   = 0;
  char *program     = strdup(argv[0]), *appName=basename(program);
  char *devname     = "/dev/" DEVICE_NAME;
  int labels        = 0;
  enum fmt_t format = HR;
  int show_output   = 1;
  char option;
  int model_params = 0;

  int next_arg = 1;

  // parameters handling
  while (next_arg < argc && argv[next_arg][0] == '-') {

    option = argv[next_arg][1];

    switch (option) {
      case 'h':
        help(appName);
        // this is actually unnecessary. help function terminates application.
        next_arg += 1;
        break;
      case 'p':
        model_params = 1;
        show_output = 0;
        next_arg++;
        break;
      case 'd':
        if (next_arg + 1 < argc) {
          devname = argv[ next_arg + 1 ];
        } else {
          printf("Invalid device name...\n");
          rc = -EINVAL;
          goto invalid_argument;
        }
        next_arg += 2;
        break;
      case 'r':
        show_output = 0;
        next_arg += 1;
        break;
      case 'f':
        if (next_arg + 1 < argc) {
          if (strcmp(argv[ next_arg + 1 ], "csv") == 0)
            format = CSV;
          else if (strcmp(argv[ next_arg + 1 ], "hr") == 0)
            format = HR;
          else {
            printf("Invalid format name...\n");
            rc = -EINVAL;
            goto invalid_argument;
          }
        } else {
          printf("Invalid format name...\n");
          rc = -EINVAL;
          goto invalid_argument;
        }
        next_arg += 2;
        break;
      case 'l':
        labels = 1;
        next_arg += 1;
        break;
    }

  };

  // if device name is set ...
  if (devname) {
    FILE * fp;
    fp = fopen("params.txt", "w");
    fd = open(devname, O_RDONLY);

    if (fd < 0) {
      perror("Failed to open the device...");
      return errno;
    }

    ret = read(fd, &tlm, sizeof(struct tlm_private));

    if (ret < 0) {
      perror("Failed to communicate with the device...");
      close(fd);
      return errno;
    }

    if(model_params)
    {
        numel = min(tlm.data_count, TLM_BUFFER_SIZE);

        for (i = 0; i<numel; i++){
          fprintf(fp, "%ld, %ld\n", tlm.data[i].theta[0], tlm.data[i].theta[1]);
        }

    }
    if (show_output) {

      // For the case when some trash data are loaded instead of valid tlm,
      // eg ./tlm -d /dev/sda1
      numel = min(tlm.data_count, TLM_BUFFER_SIZE);

      switch (format) {
        case HR:

          printf("Retrieved samples:\t%d\n", tlm.data_count);
          printf("Missed samples:\t\t%d\n\n", tlm.data_lost);

          printf("%s\t\t","ts_sec");
          printf("%s\t","ts_usec");
          for (i = 0; labelsDef[i]; i++)
            printf("%s\t", labelsDef[i]);
          printf("\n");

          for (i = 0; i<numel; i++) {
            printf("%d\t%d\t", tlm.data[i].ts_sec, tlm.data[i].ts_usec);
            print_sample(tlm.data + i, "\t");
            printf("\n");
          }

          break;
        case CSV:

          if (labels) {
            printf("%s,","ts_sec");
            printf("%s","ts_usec");
            for (i = 0; labelsDef[i]; i++)
              printf(",%s", labelsDef[i]);
            printf("\n");
          }

          for (i = 0; i<numel; i++){
            printf("%d;%d;", tlm.data[i].ts_sec, tlm.data[i].ts_usec);
            print_sample(tlm.data + i, ";");
            printf("\n");
          }

          break;
      }


      rc = -tlm.data_lost;

    }

    close(fd);
    fclose(fp);
  }

invalid_argument:
  free(program);
  return rc;
}
