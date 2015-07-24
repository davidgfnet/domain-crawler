/* Copyright 1998 by the Massachusetts Institute of Technology.
 *
 *
 * Permission to use, copy, modify, and distribute this
 * software and its documentation for any purpose and without
 * fee is hereby granted, provided that the above copyright
 * notice appear in all copies and that both that copyright
 * notice and this permission notice appear in supporting
 * documentation, and that the name of M.I.T. not be used in
 * advertising or publicity pertaining to distribution of the
 * software without specific, written prior permission.
 * M.I.T. makes no representations about the suitability of
 * this software for any purpose.  It is provided "as is"
 * without express or implied warranty.
 */

#define MAX_INFLIGHT 300

#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string.h>

#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>

#include <ares.h>

const char * dns_servers[10] = { "209.244.0.3", "209.244.0.4", "8.8.8.8", "8.8.4.4", "4.2.2.1", "4.2.2.2", "4.2.2.3", "4.2.2.4", "208.67.222.222", "208.67.220.220" };
struct in_addr dns_servers_addr[10];

int inflight = 0;

static void callback(void *arg, int status, int timeouts, struct hostent *host);

int main(int argc, char **argv) {
  ares_channel channel;
  int status, addr_family = AF_INET;
  fd_set read_fds, write_fds;
  struct timeval *tvp, tv;
  
  status = ares_library_init(ARES_LIB_INIT_ALL);
  if (status != ARES_SUCCESS)
    {
      fprintf(stderr, "ares_library_init: %s\n", ares_strerror(status));
      return 1;
    }

  addr_family = AF_INET;

  struct ares_options a_opt;
  memset(&a_opt,0,sizeof(a_opt));
  a_opt.tries = 1;
  a_opt.nservers = sizeof(dns_servers)/sizeof(dns_servers[0]);
  a_opt.servers = &dns_servers_addr[0];

  int i;
  for (i = 0; i < a_opt.nservers; i++)
    inet_aton(dns_servers[i], &dns_servers_addr[i]);

  status = ares_init_options(&channel, &a_opt, ARES_OPT_TRIES | ARES_OPT_SERVERS | ARES_OPT_ROTATE);
  if (status != ARES_SUCCESS)
    {
      fprintf(stderr, "ares_init: %s\n", ares_strerror(status));
      return 1;
    }

  int nfds = 0;
  std::string domain;
  while (true) {
    /* Initiate the queries, one per command-line argument. */
    bool input_end = !(std::cin >> domain);
    while (!input_end)
    {
      ares_gethostbyname(channel, domain.c_str(), addr_family, callback, (void*)domain.c_str());
      inflight++;
      if (inflight >= MAX_INFLIGHT)
        break;
      
      input_end = !(std::cin >> domain);
    } 

    /* Wait for queries to complete. */
    do
    {
      FD_ZERO(&read_fds);
      FD_ZERO(&write_fds);
      nfds = ares_fds(channel, &read_fds, &write_fds);
      tvp = ares_timeout(channel, NULL, &tv);
      select(nfds, &read_fds, &write_fds, NULL, tvp);
      ares_process(channel, &read_fds, &write_fds);
    } while(inflight >= MAX_INFLIGHT);
    
    if (input_end && inflight == 0)
      break;
  }

  ares_destroy(channel);

  ares_library_cleanup();

  return 0;
}

static void callback(void *arg, int status, int timeouts, struct hostent *host)
{
  inflight--;
  if (status == ARES_SUCCESS) {
    std::cout << host->h_name << std::endl;
/*    struct in_addr  ** pptr = (struct in_addr **)host->h_addr_list;

    while( *pptr != NULL ){
		printf("%d\n", sizeof(long));
        printf("ip address: %s\n", inet_ntoa(**(pptr++)));
    }*/
  }
}



