#include <enkf_types.h>
#include <enkf_node.h>
#include <stdio.h>
#include <util.h>
#include <plain_driver_common.h>

/**
   This file implements small functions which are common to to 
   all the plain_driver_xxxx drivers. 
*/

void plain_driver_common_load_node(const char * filename ,  int report_step , state_enum state , enkf_node_type * node ) {
  FILE * stream   = util_fopen(filename , "r");
  enkf_node_fread(node , stream , report_step , state);
  fclose(stream);
}


void plain_driver_common_save_node(const char * filename ,  int report_step , state_enum state , enkf_node_type * node ) {
  FILE * stream = util_fopen(filename , "w");
  bool data_written = enkf_node_fwrite(node , stream , report_step , state);
  fclose(stream);
  if (!data_written)
      unlink(filename);
}
