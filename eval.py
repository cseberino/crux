# Copyright 2020 Christian Seberino
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import types

def is_int(exp):
        """
        Identifies.
        """

        return isinstance(exp, int) and not isinstance(exp, bool)

def is_var(exp):
        """
        Identifies.
        """

        return isinstance(exp, tuple) and (len(exp) == 1) and                  \
                                                       isinstance(exp[0], str)

def is_atom(exp):
        """
        Identifies.
        """

        return isinstance(exp, (bool, int, str, types.FunctionType)) or        \
                                                                   is_var(exp)

def is_list(exp):
        """
        Identifies.
        """

        return isinstance(exp, list) and                                       \
                                    all(is_atom(e) or is_list(e) for e in exp)

def regular(n_args, any_len = False):
        """
        Decorates.
        """

        def decor(func):
                def func_(args, env):
                        result = None
                        if any_len or (len(args) == n_args):
                                args_ = [eval(e, env) for e in args]
                                if None not in args_:
                                        result = func(args_, env)

                        return result

                return func_

        return decor

def eval_ne(args, env):
        """
        Helps.
        """

        result = None
        if len(args) == 1:
                result = args[0]

        return result

def eval_if(args, env):
        """
        Helps.
        """

        result = None
        if len(args) == 3:
                cond = eval(args[0], env)
                if cond is not None:
                        if cond:
                                result = eval(args[1], env)
                        else:
                                result = eval(args[2], env)

        return result

def eval_def(args, env):
        """
        Helps.
        """

        result = None
        if (len(args) == 2) and is_var(args[0]):
                result = env[args[0]] = eval(args[1], env)

        return result

def eval_func(args, env):
        """
        Helps.
        """

        result = None
        if (len(args) >= 2) and (is_var(args[0]) or                            \
                      (is_list(args[0]) and all(is_var(e) for e in args[0]))):
                @regular(len(args[0]), is_var(args[0]))
                def func(args_, env_):
                        result = None
                        params = args[0]
                        if is_var(params):
                                params, args_ = [params], [args_]
                        env__  = {**env, **dict(zip(params, args_))}
                        for e in args[1:]:
                                result = eval(e, env__)

                        return result

                result = func

        return result

def eval_macro(args, env):
        """
        Helps.
        """

        result = None
        if (len(args) >= 3) and is_var(args[0]) and (is_var(args[1]) or        \
                      (is_list(args[1]) and all(is_var(e) for e in args[1]))):
                def macro(args_, env_):
                        result = None
                        params = args[1]
                        if is_var(params) or (len(params) == len(args_)):
                                if is_var(params):
                                        params, args_ = [params], [args_]
                                env__ = {**env, **dict(zip(params, args_))}
                                for e in args[2:]:
                                        code   = eval(e,    env__)
                                        result = eval(code, env_)

                        return result

                result = env[args[0]] = macro

        return result

@regular(1)
def eval_atom(args, env):
        """
        Helps.
        """

        return is_atom(args[0])

@regular(2)
def eval_equal(args, env):
        """
        Helps.
        """

        return args[0] == args[1]

@regular(1)
def eval_first(args, env):
        """
        Helps.
        """

        result = None
        if is_list(args[0]):
                result = args[0][0] if args[0] else []

        return result

@regular(1)
def eval_rest(args, env):
        """
        Helps.
        """

        result = None
        if is_list(args[0]):
                result = args[0][1:]

        return result

@regular(2)
def eval_append(args, env):
        """
        Helps.
        """

        result = None
        if is_list(args[0]):
                result = args[0] + [args[1]]

        return result

@regular(2)
def eval_add(args, env):
        """
        Helps.
        """

        result = None
        if is_int(args[0]) and is_int(args[1]):
                result = args[0] + args[1]

        return result

@regular(1)
def eval_negate(args, env):
        """
        Helps.
        """

        result = None
        if is_int(args[0]):
                result = -args[0]

        return result

@regular(2)
def eval_gt(args, env):
        """
        Helps.
        """

        result = None
        if is_int(args[0]) and is_int(args[1]):
                result = args[0] > args[1]

        return result

def eval(exp, env):
        """
        Evaluates.
        """

        result = None
        if   is_atom(exp):
                if is_var(exp):
                        if   exp in env:
                                if is_atom(env[exp]) or is_list(env[exp]):
                                        result = env[exp]
                        elif ("eval_" + exp[0]) in globals():
                                result = globals()["eval_" + exp[0]]
                else:
                        result = exp
        elif is_list(exp):
                if exp:
                        func = eval(exp[0], env)
                        if isinstance(func, types.FunctionType):
                                result = func(exp[1:], env)
                else:
                        result = []

        return result
