/**
 * @file rapidPlugin_memory.h
 * @author Larry Colvin (PCLabTools@github)
 * @brief 
 * @version 0.1
 * @date 2023-10-22
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#ifndef rapidPlugin_memory_h
#define rapidPlugin_memory_h

#include "rapidRTOS.h"
#include "memory.h"

/**
 * @brief rapidPlugin top level description
 * 
 */
class rapidPlugin_memory : public rapidPlugin
{
  public:
    rapidPlugin_memory(const char* identity);
    BaseType_t run();
    BaseType_t runCore(BaseType_t core);

  private:
    static void main_loop(void*);
    uint32_t _count = 0;
};

/**
 * @brief Construct a new rapidPlugin template::rapidPlugin template object
 * 
 * @param identity string literal containing task name
 */
rapidPlugin_memory::rapidPlugin_memory(const char* identity)
{
  _pID = identity;
}

/**
 * @brief Runs the main loop task.
 * rapidRTOS registers the task with the manager and creates the interface handlers
 * 
 * @return BaseType_t 1 = task run successful | 0 = task failed to start
 */
BaseType_t rapidPlugin_memory::run()
{
  manageMemory.synchronise();
  return rapidPlugin::run(&main_loop);
}

/**
 * @brief Runs the main loop task on the specified core.
 * rapidRTOS registers the task with the manager and creates the interface handlers
 * using the same core as the main loop
 * 
 * @param core core ID
 * @return BaseType_t 1 = task run successful | 0 = task failed to start
 */
BaseType_t rapidPlugin_memory::runCore(BaseType_t core)
{
  manageMemory.synchronise();
  return rapidPlugin::runCore(core, &main_loop);
}

/**
 * @brief Main loop task responsible for monitoring memory and updating EEPROM if changed
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