# -*- coding: utf-8 -*-

import os
import sys
import json
import shutil
from cmd import Cmd

from updator import HostsUpdator

help_message = '''
Usage:
  hman <command> [<parameters>]

Commands:
  add:    \tAdd a new source.
  help:   \tShow help message for a specified command.
  list:   \tList all the sources available. Source in use starts with "*".
  ls:     \tSame as list.
  pull:   \tPull and store hosts from specified source.
  rename: \tRename a source.
  remove: \tRemove (an) existing source(s).
  rm:     \tSame as remove.
  reorder:\tReorder a source.
  use:    \tUse specified source as system hosts.
  others: \tShow this help message.
'''

# def log(method):
#     def wrapper(self, line):
#         print('call %s():' % method.__name__)
#         return method(self, line)
#     return wrapper


class HostsManager(Cmd):
    """Hosts Manager CLI."""
    def __init__(self):
        Cmd.__init__(self)
        self.prompt = '(hman)>> '
        try:
            import config
        except ImportError:
            config = __import__('config-default')
        self.sources = config.sources
        self.current = config.current
        self.app_root = os.path.dirname(os.path.abspath(sys.modules[self.__module__].__file__))


    def _rewrite_config(self):
        config_dict = { "current": self.current, "sources": self.sources }
        config_file = os.path.join(self.app_root, 'config.py')
        with open(config_file, 'w') as f:
            f.write('# -*- coding: utf-8 -*-\n')
            for k, v in sorted(config_dict.items()):
                s = '\n{name} = {value}\n'.format(name=k, value=json.dumps(v, indent=4, sort_keys=True))
                f.write(s)


    def _get_source_by_name(self, name):
        for src in self.sources:
            if src['name'] == name:
                return src


    @staticmethod
    def rmdir(dirname):
        if os.path.isdir(dirname):
            shutil.rmtree(dirname)


    def default(self, line):
        Cmd.default(self, line)
        print(help_message)


    def do_rewrite_config(self, line):
        """Rewrite config.py manually.
        Generally, hman will rewrite it automaticly after config changed.\n"""
        self._rewrite_config()

    # @log
    def do_list(self, line):
        """List all the hosts sources. Symbol "*" indicates the one in use.
        Usage: `list` or `ls`.
            Use addational parameter `-a` or `--all` to list detail information.\n"""
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
        Usage: `add name url [note]`.\n"""
        params = line.split()
        if len(params) < 2:
            print('*** Parameter Error: require "name" and "url" of the source to add.\n')
            return
        name, url = params[:2]
        all_names = [src['name'] for src in self.sources]
        if name in all_names:
            prompt = 'Warning: source "%s" already exists, do you want to overwrite?[Y/n]' %name
            try:
                answer = raw_input(prompt)
            except NameError:
                answer = input(prompt)
            if answer not in ('', 'y', 'Y'):
                print('Operation was canceled by user.\n')
                return
        note = params[2] if len(params)>2 else ''
        self.sources.append({ 'name': name, 'url': url, 'note': note })
        print('Added new source: %s - %s\n' %(name, url))


    def do_remove(self, line):
        """Remove source(s).
        Usage: `remove name1 [name2 [name3]]...` or `rm name1 [name2 [name3]]...`\n"""
        names = line.split()
        if not names:
            print('*** Parameter Error: require at least one source name.\n')
            return
        all_names = [src['name'] for src in self.sources]
        for name in names:
            if name not in all_names:
                print('*** Parameter Error: unknown source name "%s".\n' %name)
                return
        self.sources = [src for src in self.sources if src['name'] not in names]
        data_dirs = [os.path.join(self.app_root, 'data', name) for name in names]
        for d in data_dirs:
            self.rmdir(d)
        print('Removed source(s): %s\n' %(' '.join(names)))


    do_rm = do_remove


    def do_rename(self, line):
        """Rename a source.
        Usage: `rename old_name new_name`.\n"""
        params = line.split()
        if len(params) < 2:
            print('*** Parameter Error: require old_name and new_name.\n')
            return
        old_name, new_name = params[:2]
        all_names = [src['name'] for src in self.sources]
        if old_name not in all_names:
            print('*** Parameter Error: unknown source name "%s".\n' %old_name)
            return
        self.sources[all_names.index(old_name)]['name'] = new_name
        old_data_dir = os.path.join(self.app_root, 'data', old_name)
        new_data_dir = os.path.join(self.app_root, 'data', new_name)
        if os.path.isdir(old_data_dir):
            os.rename(old_data_dir, new_data_dir)
        print('Renamed "%s" to "%s"\n' %(old_name, new_name))


    def do_reorder(self, line):
        """Reorder a source.
        Usage: `reorder name order`.
            Both absolute and relative order are supported:
            absolute order is a number: 1 means the first position, 2 means the seconde, and so on.
            relative order is a number with leading "+" or "-": "+" means moving backward and "-" means forward.
        Example: `reorder src1 5` moves src1 to the 5th position.
            `reorder src1 +2` moves src1 backward by 2 positions.\n"""
        params = line.split()
        if len(params) < 2:
            print('*** Parameter Error: require source_name and order.\n')
            return
        name, order = params[:2]
        all_names = [src['name'] for src in self.sources]
        if name not in all_names:
            print('*** Parameter Error: unknown source name "%s".\n' %name)
            return
        if not (order.isdigit() or (order[0] in '+-' and order[1:].isdigit())):
            print('*** Parameter Error: unknown syntax for "order".\nOrder should be absolute(eg: 5) or relative(eg: +2).\n')
            return
        current_order = all_names.index(name)
        new_order = int(order)-1 if order.isdigit() else eval(str(current_order)+order)
        new_order = min(max(0, new_order), len(all_names)-1)
        to_reorder = self.sources[current_order]
        self.sources.remove(to_reorder)
        self.sources.insert(new_order, to_reorder)
        print('Reordered "%s" to the %dth position\n' %(name, new_order+1))


    def do_pull(self, line):
        """Pull (specified or current) source from remote.
        Usage: `pull [name [-u]]` or `pull [name [--use]]`
            name: source name to pull from. Default as current source.
            -u or --use: use the source after pull.
        `pull name -u` is same as `use name -p`\n"""
        params = line.split()
        name = params[0] if params else self.current
        all_names = [src['name'] for src in self.sources]
        if name not in all_names:
            print('*** Parameter Error: unknown source name "%s".\n' %name)
            return
        is_use = False
        if len(params) > 1:
            if params[1] not in ('-u', '--use'):
                print('*** Unknown syntax: %s\n' %params[1])
                return
            is_use = True
        to_pull = self._get_source_by_name(name)
        updator = HostsUpdator(to_pull['name'], to_pull['url'])
        updator.pull()
        if is_use:
            updator.use()
            self.current = name
        print('Pulled%s hosts from source %s\n' %(' and used' if is_use else '', name))


    def do_use(self, line):
        """Switch to specified source.
        Usage: `use name [-p]` or `use name [--pull]`.
            name: source name to switch to.
            -p or --pull: pull from the source before switch.
        `use name -p` is same as `pull name -u`.\n"""
        params = line.split()
        if not params:
            print('*** Parameter Error: need a source name.\n')
            return
        name = params[0]
        all_names = [src['name'] for src in self.sources]
        if name not in all_names:
            print('*** Parameter Error: unknown source name "%s".\n' %name)
            return
        is_pull = False
        if len(params) > 1:
            if params[1] not in ('-p', '--pull'):
                print('*** Unknown syntax: %s\n' %params[1])
                return
            is_pull = True
        if not is_pull:
            data_dir = os.path.join(self.app_root, 'data', name)
            if not os.path.isdir(data_dir):
                is_pull = True
        to_use = self._get_source_by_name(name)
        updator = HostsUpdator(to_use['name'], to_use['url'])
        if is_pull:
            updator.pull()
        updator.use()
        self.current = name
        print('%ssed hosts from source %s\n' %('Pulled and u' if is_pull else 'U', name))


    def preloop(self):
        print(help_message)


    def do_exit(self, line):
        """Exit hosts-manager.\n"""
        self._rewrite_config()
        sys.exit(0)


if __name__ == '__main__':
    hman = HostsManager()
    try:
        hman.cmdloop()
    except Exception as e:
        hman._rewrite_config()
        raise e

