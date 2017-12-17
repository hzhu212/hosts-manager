# -*- coding: utf-8 -*-

import os
import sys
import json
import shutil
from cmd import Cmd

from util import parameter as p
from util.updator import HostsUpdator

help_message = '''
Usage:
  <command> [<parameters>]

Commands:
  h:      \tShow this help message.
  add:    \tAdd a new source.
  help:   \tShow help message for a specified command.
  list:   \tList all the sources available. Source in use starts with "*".
  ls:     \tAlias of `list`.
  pull:   \tPull and store hosts from remote.
  rename: \tRename a source.
  ren:    \tAlias of `rename`.
  remove: \tRemove existing source(s).
  rm:     \tAlias of `remove`.
  reorder:\tReorder a source.
  use:    \tUse specified source as system hosts.
'''


class HostsManager(Cmd):
    """Hosts Manager CLI."""
    prompt = '(hman)> '
    intro = 'Welcome to hosts-manager CLI. Type "h" to get general help. Type "help <command>" to get command help.\n'

    def __init__(self):
        Cmd.__init__(self)
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


    def get_all_names(self):
        return [src['name'] for src in self.sources]


    def do_h(self, line):
        """Get help message.\n"""
        print(help_message)


    def do_rewrite_config(self, line):
        """Rewrite config.py manually.
        Generally, hman will rewrite it automaticly after config changed.\n"""
        self._rewrite_config()


    def complete_name(self, text, line, begidx, endidx):
        # print('\ntext, line, begidx, endidx: %s\n' %([text, line, begidx, endidx]))
        all_names = self.get_all_names()
        return [n for n in all_names if n.startswith(text)]


    def complete_name_once(self, text, line, begidx, endidx):
        if len((line + '_').split()) > 2:
            return []
        all_names = self.get_all_names()
        return [n for n in all_names if n.startswith(text)]


    @p.parameter(name='extra', validator=p.Choice(['-a','--all']))
    @p.parameter_over()
    def do_list(self, is_detail):
        """List all the hosts sources. Symbol "*" indicates the one in use.
        Usage: `list` or `ls`.
        Use extra parameter `-a` or `--all` to list detail information.\n"""
        for index, src in enumerate(self.sources):
            lead = '*' if src['name'] == self.current else ' '
            if is_detail:
                print('{lead} [{index}]\tname: {name}\n\turl: {url}\n\tnote: {note}'.format(
                    lead=lead, index=index, name=src['name'], url=src['url'], note=src['note']))
            else:
                print('{lead} {name}:\t{url}'.format(lead=lead, name=src['name'], url=src['url']))
        print('')


    @p.parameter(name='name', required=True)
    @p.parameter(name='url', required=True)
    @p.parameter(name='note')
    @p.parameter_over()
    def do_add(self, name, url, note):
        """Add a new source.
        Usage: `add name url [note]`.\n"""
        all_names = self.get_all_names()
        rewrite = False
        if name in all_names:
            prompt = 'Warning: source "%s" already exists, do you want to overwrite?[Y/n]' %name
            try:
                answer = raw_input(prompt)
            except NameError:
                answer = input(prompt)
            if answer not in ('', 'y', 'Y'):
                print('Operation was canceled by user.\n')
                return
            rewrite = True
        to_add = { 'name': name, 'url': url, 'note': note }
        if rewrite:
            self.sources[all_names.index(name)].update(to_add)
            print('Updated source: %s - %s\n' %(name, url))
            return
        self.sources.append(to_add)
        print('Added new source: %s - %s\n' %(name, url))


    @p.parameter_vary(name='name', validator=(p.Choice, p.FromObj(get_all_names)))
    def do_remove(self, names):
        """Remove source(s).
        Usage: `remove name1 [name2 [name3]]...` or `rm name1 [name2 [name3]]...`\n"""
        self.sources = [src for src in self.sources if src['name'] not in names]
        data_dirs = [os.path.join(self.app_root, 'data', name) for name in names]
        for d in data_dirs:
            self.rmdir(d)


    @p.parameter(name='old_name', required=True, validator=(p.Choice, p.FromObj(get_all_names)))
    @p.parameter(name='new_name', required=True)
    @p.parameter_over()
    def do_rename(self, old_name, new_name):
        """Rename a source.
        Usage: `rename old_name new_name`.\n"""
        all_names = self.get_all_names()
        self.sources[all_names.index(old_name)]['name'] = new_name
        if old_name == self.current:
            self.current = new_name
        old_data_dir = os.path.join(self.app_root, 'data', old_name)
        new_data_dir = os.path.join(self.app_root, 'data', new_name)
        if os.path.isdir(old_data_dir):
            os.rename(old_data_dir, new_data_dir)
        # print('Renamed "%s" to "%s"\n' %(old_name, new_name))


    @p.parameter(name='name', required=True, validator=(p.Choice, p.FromObj(get_all_names)))
    @p.parameter(name='order', required=True, validator=p.Regex(r'[+-]?\d+'))
    @p.parameter_over()
    def do_reorder(self, name, order):
        """Reorder a source.
        Usage: `reorder name order`.
            Both absolute and relative order are supported:
            absolute order is a number: 1 means the first position, 2 means the seconde, and so on.
            relative order is a number with leading "+" or "-": "+" means moving backward and "-" means forward.
        Example: `reorder src1 5` moves src1 to the 5th position.
            `reorder src1 +2` moves src1 backward by 2 positions.\n"""
        all_names = self.get_all_names()
        current_order = all_names.index(name)
        new_order = int(order)-1 if order.isdigit() else eval(str(current_order)+order)
        new_order = min(max(0, new_order), len(all_names)-1)
        to_reorder = self.sources[current_order]
        self.sources.remove(to_reorder)
        self.sources.insert(new_order, to_reorder)
        # print('Reordered "%s" to the %dth position\n' %(name, new_order+1))


    @p.parameter_vary(name='name', validator=(p.Choice, p.FromObj(get_all_names)))
    def do_pull(self, names):
        """Pull source(s) from remote.
        Usage: `pull [name1 [name2 [name3]]]...`
        If `name1` not specified, then pull current source.
        `pull *` will pull all sources.\n"""
        if not names:
            names = [self.current]
        elif '*' in names:
            names = self.get_all_names()
        for name in names:
            to_pull = self._get_source_by_name(name)
            updator = HostsUpdator(to_pull['name'], to_pull['url'], self.app_root)
            updator.pull()


    @p.parameter(name='name', required=True, validator=(p.Choice, p.FromObj(get_all_names)))
    @p.parameter(name='extra', validator=p.Choice(['-p', '--pull']))
    @p.parameter_over()
    def do_use(self, name, extra):
        """Switch to specified source.
        Usage: `use name [-p]` or `use name [--pull]`.
            `name`: source name to switch to.
            `-p` or `--pull`: pull from the source before switch.\n"""
        is_pull = bool(extra)
        if not is_pull:
            data_dir = os.path.join(self.app_root, 'data', name)
            if not os.path.isdir(data_dir):
                is_pull = True
        to_use = self._get_source_by_name(name)
        updator = HostsUpdator(to_use['name'], to_use['url'], self.app_root)
        if is_pull:
            updator.pull()
        updator.use()
        self.current = name
        # print('%ssed hosts from source %s\n' %('Pulled and u' if is_pull else 'U', name))


    def do_exit(self, line):
        """Exit hosts-manager.\n"""
        self._rewrite_config()
        sys.exit(0)


    do_ls = do_list
    do_rm = do_remove
    do_ren = do_rename

    complete_remove = complete_rm = complete_name
    complete_pull = complete_name
    complete_rename = complete_ren = complete_name_once
    complete_reorder = complete_name_once
    complete_use = complete_name_once


if __name__ == '__main__':
    from util import admin
    if os.name == 'nt':
        if not admin.is_admin_nt():
            print('\n*** Need administrator privileges!\nInstead of Requesting UAC elevation from within the script?, we recommand runing as admin from the very begining.\n')
            admin.run_as_admin()
            exit(0)
    elif os.name == 'posix':
        if not admin.is_admin_posix():
            print('\n*** Need root privileges!\nUse `sudo python hman.py` to run the script as root.\n')
            exit(0)
    else:
        raise RuntimeError('Unsupported operating system: %s' %(os.name,))

    hman = HostsManager()
    try:
        hman.cmdloop()
    except Exception as e:
        hman._rewrite_config()
        raise
