from nonebot import on_command
from nonebot.rule import Rule
from nonebot.adapters.onebot.v11.adapter import Message, MessageSegment
from nonebot.adapters.onebot.v11 import Message, MessageSegment, Bot, MessageEvent
from nonebot.matcher import Matcher
from nonebot.params import CommandArg

from pathlib import Path
import random
import os

fabing = on_command("fabing", rule=Rule(), aliases={'发病', '发病文学'}, priority=5)
PACKAGE_PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = str(Path(PACKAGE_PATH) / "templates.txt")
fabing_tmpl = []
random_index = 0


def load_fabing_tmpl():
    global fabing_tmpl
    global random_index

    fabing_tmpl = []
    with open(TEMPLATE_PATH, encoding='utf-8') as fp:
        contents = fp.readlines()
        for line in contents:
            fabing_tmpl.append(line.strip().replace('\\n', '\n\n'))

    random.shuffle(fabing_tmpl)
    random_index = 0

load_fabing_tmpl()

@fabing.handle()
async def handle_fabing(matcher: Matcher, event: MessageEvent, arg: Message = CommandArg()):
    global random_index
    
    if len(arg) == 0:
        await matcher.finish('缺少必要的参数：必须指定一个对象')
        
    args = arg.extract_plain_text().rsplit()
    if args[0] == '重载' or args[0] == 'reload':
        load_fabing_tmpl()
        await matcher.finish('重载成功')
    
    target = args[0]
    if random_index >= len(fabing_tmpl):
        random_index = 0
    tmpl = fabing_tmpl[random_index]
    random_index += 1
    await matcher.finish(tmpl.format(target))
