# -*- coding: utf-8 -*-

# hosts-manager CLI

import os
import sys
import platform
import json

help_message = '''
Usage:
  hman <command> [<parameters>]

Commands:
  help:   \tShow this help message. Equivalent to "-h", "/?", "--help".
  run:    \tUpdate hosts using current source.
  list:   \tList all the sources available. Source in use starts with "*".
  add:    \tAdd a new source. Usage: hman add source_name source_url.
  remove: \tRemove an existing source. Usage: hman remove source_name.
  use:    \tChange current source. Usage: hman use source_name.
  rename: \tRename a source. Usage: hman rename old_name new_name.
  ls:     \tSame as list.
  rm:     \tSame as remove.
'''

def update_config(update_dict):
    import config
    keys = [k for k in dir(config) if not k.startswith('__')]
    values = [config.__dict__.get(k, None) for k in keys]
    config_dict = dict(zip(keys, values))
    config_dict.update(update_dict)
    config_file = os.path.join(os.path.dirname(__file__), 'config.py')
    with open(config_file, 'w') as f:
        f.write('# -*- coding: utf-8 -*-\n')
        for k, v in sorted(config_dict.items()):
            s = '\n{name} = {value}\n'.format(name=k, value=json.dumps(v, indent=4, sort_keys=True))
            f.write(s)


if __name__ == '__main__':
    command = sys.argv[1] if len(sys.argv) > 1 else None

    if command == 'run':
        script = os.path.join(os.path.dirname(__file__), 'updator.py')
        system = platform.system()

        # 以管理员权限运行更新脚本
        if system == 'Windows':
            import win32com.shell.shell as shell
            shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=script, nShow=5)
        else:
            os.system('sudo %s' %script)

    elif command in ('list', 'ls'):
        import config
        slist = []
        for name, url in sorted(config.sources.items()):
            symbol = '*' if name == config.current else ''
            slist.append('%2s%s\t%s' %(symbol, name, url))
        print('\n'.join(slist))

    elif command == 'add':
        if len(sys.argv) < 4:
            print('Error: source name and url required!')
            sys.exit(1)
        import config
        sources = config.sources
        new_name, new_url = sys.argv[2:4]
        sources[new_name] = new_url
        update_config({ 'sources': sources })
        print('Added new source: %s - %s' %(new_name, new_url))

    elif command in ('remove', 'rm'):
        import config
        sources = config.sources
        if len(sys.argv) < 3:
            print('Error: source name required!')
            sys.exit(1)
        try:
            name = sys.argv[2]
            sources.pop(name)
        except Exception as e:
            print('Error: invalid hosts source name: %s' %name)
            sys.exit(1)
        update_config({ 'sources': sources })
        print('Deleted source: %s' %(name))

    elif command == 'use':
        if len(sys.argv) < 3:
            print('Error: source name required!')
            sys.exit(1)
        to_use = sys.argv[2]
        update_config({ 'current': to_use })
        print('switched current source to "%s"' %to_use)

    elif command == 'rename':
        if len(sys.argv) < 4:
            print('Error: Old name and new name required!')
            sys.exit(1)
        old_name, new_name = sys.argv[2:4]
        import config
        sources = config.sources
        current = config.current
        if old_name in sources:
            sources[new_name] = sources[old_name]
            sources.pop(old_name)
            if old_name == current:
                current = new_name
        update_config({ 'sources': sources, 'current': current })
        print('renamed "%s" to "%s"' %(old_name, new_name))

    elif command in ('help', '-h', '/?', '--help', None):
        print(help_message)
    else:
        print('Unknown command: "%s"\n' %(' '.join(sys.argv)))
        print(help_message)
