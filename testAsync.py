# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 11:43:57 2023

@author: loveaoe33
"""

import asyncio


async def async_op():
    print("開始非同步")
    await asyncio.sleep(2)
    print("完成")
    
async def main():
    print("主程式開始")
    await asyncio.sleep(3)
    print("主程式結束")

async def test():
    await asyncio.sleep(2)
    print("不等待")

def MainLoop():  
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.create_task(test())


MainLoop()