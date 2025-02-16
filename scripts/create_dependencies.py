FILEPATH_DEPENDENCY_H = project_path + '/include/memory.h'

contents = '''/**
 * @file memory.h
 * @author your name (you@domain.com)
 * @brief 
 * @version 0.1
 * @date 2025-02-08
 * 
 * @copyright Copyright (c) 2025
 * 
 */

// #define rapidPlugin_memory_override_main_loop
// #define rapidPlugin_memory_override_interface

#ifndef memory_h
#define memory_h

#include "errors.h"

#include "EEPROManager.h"

/**
 * @brief Device Memory stored to non-volatile memory and automatically managed by
 * the rapidPlugin_memory rapidRTOS task.
 * 
 */
struct Memory_t
{
  uint8_t DEBUG_LEVEL = 0;
} Memory;

EEPROManager<Memory_t> manageMemory(&Memory, 0x0001);

#include "rapidPlugin_memory.h"

#ifdef rapidPlugin_memory_override_main_loop
/**
 * @brief main loop task
 * 
 * @param pModule pointer to the calling object
 */
void rapidPlugin_memory::main_loop(void* pModule)
{
  rapidPlugin_memory* plugin = (rapidPlugin_memory*)pModule;
  for ( ;; )
  {
    if (plugin->_count = manageMemory.update()) { rapidRTOS.printDebug(1, rapidDebug::INFO, "memory_update(%d)", plugin->_count); }
    vTaskDelay(1000 / portTICK_PERIOD_MS);
  }
}
#endif

#ifdef rapidPlugin_memory_override_interface
/**
 * @brief Interface handler extended functions.
 * This function is to be used for creating custom states 
 * that are called when rapidFunction commands are received
 * 
 * @param incoming message broken into 2 strings: function and parameters
 * @param messageBuffer buffer to store return message
 * @return uint8_t return 0 if the function was handled, 1 if not
 */
uint8_t rapidPlugin_memory::interface(rapidFunction incoming, char messageBuffer[])
{
  do
  {
    if (!strcmp(incoming.function, "force"))
    {
      manageMemory.force();
      sprintf(messageBuffer, "memory_force()");
      continue;
    }
    if (!strcmp(incoming.function, "reset"))
    {
      manageMemory.reset();
      sprintf(messageBuffer, "memory_reset()");
      continue;
    }
    if (!strcmp(incoming.function, "wipe"))
    {
      manageMemory.wipe();
      sprintf(messageBuffer, "memory_wipe()");
      continue;
    }
    rapidPlugin::interface(incoming, messageBuffer);
    return 0;
  } while (false);
  return 1;
}
#endif

#endif // memory_h

'''

try:
  open(FILEPATH_DEPENDENCY_H, "r+")
  print(info + '\'memory.h\' already present')
except:
  print(warning + '\'memory.h\' not present, generating default...')
  try:
    with open(FILEPATH_DEPENDENCY_H, 'x') as f:
      f.write(contents)
  except:
    print(error + '\'memory.h\' could not be written to')