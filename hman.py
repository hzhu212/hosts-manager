# -*- coding: utf-8 -*-

# hosts-manager CLI

import os
import sys
import platform
import json
from cmd import Cmd

help_message = '''
Usage:
  hman <command> [<parameters>]

Commands:
  help:   \tShow this help message. Equivalent to "-h", "/?", "--help".
  list:   \tList all the sources available. Source in use starts with "*".
  pull:   \t<[source_name]>. Pull and store hosts from specified source or current source, but not use!
  use:    \t<source_name>. Use specified source to replace system hosts.
  update: \t<[source_name]>. Pull and use hosts from specified source or current source. Same as pull && use.
  add:    \t<source_name source_url>. Add new source.
  remove: \t<source_name>. Remove an existing source.
  rename: \t<old_name new_name>. Rename source.
  ls:     \tSame as list.
  rm:     \tSame as remove.
'''

class HostsManager(Cmd):
    def __init__(self):
        Cmd.__init__(self)
        self.prompt = '(hman)>> '
        try:
            import config
        except ImportError:
            config = __import__('config-default')
        self.sources = config.sources
        self.current = config.current

    def _rewrite_config(self):
        config_dict = { "current": self.current, "sources": self.sources }
        app_root = os.path.dirname(os.path.abspath(sys.modules[self.__module__].__file__))
        config_file = os.path.join(app_root, 'config.py')
        with open(config_file, 'w') as f:
            f.write('# -*- coding: utf-8 -*-\n')
            for k, v in sorted(config_dict.items()):
                s = '\n{name} = {value}\n'.format(name=k, value=json.dumps(v, indent=4, sort_keys=True))
                f.write(s)

    def default(self, line):
        Cmd.default(self, line)
        print(help_message)

    def do_rewrite_config(self, line):
        """Rewrite config.py manually.
        Generally, hman will rewrite it automaticly after config changed.\n"""
        self._rewrite_config()

    def do_list(self, line):
        """List all the hosts sources. Symbol "*" indicates the one in use.
        Use "-a" or "--all" to list detail information.\n"""
        for index, src in enumerate(self.sources):
            lead = '*' if src['name'] == self.current else ' '
            if line in ('-a', '--all'):
                print('{lead} [{index}]\tname: {name}\n\turl: {url}\n\tnote: {note}'.format(
                    lead=lead, index=index, name=src['name'], url=src['url'], note=src['note']))
            else:
                print('{lead} {name}:\t{url}'.format(lead=lead, name=src['name'], url=src['url']))
        print()

    do_ls = do_list

    def do_add(self, line):
        """Add a new source.
        Usage: add name url [note].\n"""
        params = line.split()
        if len(params) < 2:
            print('*** Error: require "name" and "url" of the source to add.\n')
            return
        name, url = params[:2]
        note = params[2] if len(params)>2 else ''
        self.sources.append({ 'name': name, 'url': url, 'note': note })
        print('Added new source: %s - %s\n' %(name, url))

    def do_remove(self, line):
        """Remove source(s).
        Usage: remove name [name2 [name3]]...
        Use alias "rm" for simplicity.\n"""
        names = line.split()
        if not names:
            print('*** Error: require at least one source name.\n')
            return
        all_names = [src['name'] for src in self.sources]
        for name in names:
            if name not in all_names:
                print('*** Error: unknown source name "%s".\n' %name)
                return
        self.sources = [src for src in self.sources if src['name'] not in names]
        print('Removed source(s): %s\n' %(' '.join(names)))

    do_rm = do_remove

    def do_rename(self, line):
        """Rename a source.
        Usage: rename old_name new_name.\n"""
        params = line.split()
        if len(params) < 2:
            print('*** Error: require old_name and new_name.\n')
            return
        old_name, new_name = params[:2]
        all_names = [src['name'] for src in self.sources]
        if old_name not in all_names:
            print('*** Error: unknown source name "%s".\n' %old_name)
            return
        self.sources[all_names.index(old_name)]['name'] = new_name
        print('Renamed "%s" to "%s"\n' %(old_name, new_name))

    def do_reorder(self, line):
        pass

    def do_pull(self, line):
        pass

    def do_use(self, line):
        pass

    def do_update(self, line):
        pass

    def do_exit(self, line):
        """Exit hosts-manager.\n"""
        self._rewrite_config()
        sys.exit(0)


"""if __name__ == '__main__':
    command = sys.argv[1] if len(sys.argv) > 1 else None

    if command == 'pull':
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
        print(help_message)"""

if __name__ == '__main__':
    hman = HostsManager()
    hman.cmdloop()
