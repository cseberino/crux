"""
evaluator
"""

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

def handle_args(n_args, any_len = False):
        """
        Decorates.
        """

        def decor(func):
                def func_(args, extra):
                        result = None
                        if any_len or (len(args) == n_args):
                                args_ = [evaluate(e, extra) for e in args]
                                if None not in args_:
                                        result = func(args_, extra)

                        return result

                return func_

        return decor

def core_noeval(args, extra):
        """
        Helps.
        """

        result = None
        if len(args) == 1:
                result = args[0]

        return result

def core_if(args, extra):
        """
        Helps.
        """

        result = None
        if len(args) == 3:
                if evaluate(args[0], extra) not in [False, "", 0, []]:
                        result = evaluate(args[1], extra)
                else:
                        result = evaluate(args[2], extra)

        return result

def core_def(args, extra):
        """
        Helps.
        """

        result = None
        if (len(args) == 2) and is_var(args[0]):
                extra[args[0]] = evaluate(args[1], extra)
                result = True

        return result

def core_func(args, extra):
        """
        Helps.
        """

        result = None
        if (len(args) >= 2) and (is_var(args[0]) or (is_list(args[0]) and      \
                                            all(is_var(e) for e in args[0]))):
                @handle_args(len(args[0]), is_var(args[0]))
                def func(args_, extra_):
                        result  = None
                        params  = args[0]
                        if is_var(params):
                                params, args_ = [params], [args_]
                        extra__ = {**extra, **dict(zip(params, args_))}
                        for e in args[1:]:
                                result = evaluate(e, extra__)

                        return result

                result = func

        return result

def core_macro(args, extra):
        """
        Helps.
        """

        result = None
        if (len(args) >= 3) and is_var(args[0]) and (is_var(args[1]) or        \
                      (is_list(args[1]) and all(is_var(e) for e in args[1]))):
                def macro(args_, extra_):
                        result = None
                        params = args[1]
                        if is_var(params) or (len(params) == len(args_)):
                                if is_var(params):
                                        params, args_ = [params], [args_]
                                extra__ = {**extra, **dict(zip(params, args_))}
                                for e in args[2:]:
                                        code   = evaluate(e,    extra__)
                                        result = evaluate(code, extra_)

                        return result

                extra[args[0]] = macro
                result         = True

        return result

@handle_args(1)
def core_atom(args, extra):
        """
        Helps.
        """

        return is_atom(args[0])

@handle_args(2)
def core_equal(args, extra):
        """
        Helps.
        """

        return args[0] == args[1]

@handle_args(1)
def core_first(args, extra):
        """
        Helps.
        """

        result = None
        if is_list(args[0]):
                if args[0]:
                        result = args[0][0]
                else:
                        result = []

        return result

@handle_args(1)
def core_rest(args, extra):
        """
        Helps.
        """

        result = None
        if is_list(args[0]):
                result = args[0][1:]

        return result

@handle_args(2)
def core_append(args, extra):
        """
        Helps.
        """

        result = None
        if is_list(args[0]):
                result = args[0] + [args[1]]

        return result

@handle_args(2)
def core_add(args, extra):
        """
        Helps.
        """

        result = None
        if is_int(args[0]) and is_int(args[1]):
                result = args[0] + args[1]

        return result

@handle_args(1)
def core_negate(args, extra):
        """
        Helps.
        """

        result = None
        if is_int(args[0]):
                result = -args[0]

        return result

@handle_args(2)
def core_gt(args, extra):
        """
        Helps.
        """

        result = None
        if is_int(args[0]) and is_int(args[1]):
                result = args[0] > args[1]

        return result

def evaluate(exp, extra):
        """
        Evaluates.
        """

        result = None
        if   is_atom(exp):
                if is_var(exp):
                        if   exp in extra:
                                if is_atom(extra[exp]) or is_list(extra[exp]):
                                        result = extra[exp]
                        elif ("core_" + exp[0]) in globals():
                                result = globals()["core_" + exp[0]]
                else:
                        result = exp
        elif is_list(exp):
                if exp:
                        func = evaluate(exp[0], extra)
                        if isinstance(func, types.FunctionType):
                                result = func(exp[1:], extra)
                else:
                        result = []

        return result
