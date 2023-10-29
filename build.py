###########################################################################
# BUILD                                                                   #
# This script is ran to initialise the plugin and generate any dependent  #
# files necessary for operation and any other pre-build actions           #
###########################################################################

try:
  Import("env") # type: ignore
  current_env = env["PIOENV"] # type: ignore
  project_path = env["PROJECT_DIR"] #type: ignore
  error = '\033[0;31m'
  warning = '\033[0;33m'
  report = '\033[0;32m'
  info = '\033[0;30m'
except:
  error = '[error] '
  warning = '[warning] '
  report = ''
  info = '[info] '

print(report + '\'rapidPlugin_memory\' running \'build.py\'...')

FILEPATH_DEPENDENCY_H = project_path + '/include/memory.h'

header_contents = '''/**
 * @file memory.h
 * @author your name (you@domain.com)
 * @brief 
 * @version 0.1
 * @date 2023-10-29
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "EEPROManager.h"

/**
 * @brief Device Memory stored to non-volatile memory and automatically managed by
 * the rapidPlugin_memory rapidRTOS task.
 * 
 */
struct Memory_t
{
  uint32_t baudRate = 115200;
  uint8_t debugLevel = 1;
} Memory;

EEPROManager<Memory_t> manageMemory(&Memory, 0x0001);'''

try:
  open(FILEPATH_DEPENDENCY_H, "r+")
  print(info + '\'memory.h\' already present')
except:
  print(warning + '\'memory.h\' not present, generating default...')
  try:
    with open(FILEPATH_DEPENDENCY_H, 'x') as f:
      f.write(header_contents)
      print(report + 'dependencies generated')
  except:
    print(error + '\'memory.h\' could not be written to')