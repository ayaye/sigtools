#!/usr/bin/env python
# sigtools - Collection of Python modules for manipulating function signatures
# Copyright (c) 2013-2015 Yann Kaiser
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


from sigtools.signatures import embed, IncompatibleSignatures
from sigtools.support import s
from sigtools.tests.util import Fixtures


class EmbedTests(Fixtures):
    def _test(self, result, exp_src, signatures,
              use_varargs=True, use_varkwargs=True):
        assert len(signatures) >= 2
        sigs = [s(sig_str, name='_' + str(i))
                for i, sig_str in enumerate(signatures, 1)]

        sig = embed(*sigs, use_varargs=use_varargs, use_varkwargs=use_varkwargs)
        exp_sig = s(result)
        self.assertSigsEqual(sig, exp_sig)
        self.assertSourcesEqual(sig.sources, exp_src)

        sigs = [self.downgrade_sig(sig) for sig in sigs]
        self.assertSigsEqual(
            embed(*sigs, use_varargs=use_varargs, use_varkwargs=use_varkwargs),
            exp_sig)

    passthrough_pos = '<a>', {2: 'a'}, ['*args, **kwargs', '<a>']
    passthrough_pok = 'a', {2: 'a'}, ['*args, **kwargs', 'a']
    passthrough_kwo = '*, a', {2: 'a'}, ['*args, **kwargs', '*, a']

    add_pos_pos = '<a>, <b>', {1: 'a', 2: 'b'}, ['<a>, *args, **kwargs', '<b>']
    add_pos_pok = '<a>, b', {1: 'a', 2: 'b'}, ['<a>, *args, **kwargs', 'b']
    add_pos_kwo = '<a>, *, b', {1: 'a', 2: 'b'}, ['<a>, *args, **kwargs', '*, b']

    add_pok_pos = '<a>, <b>', {1: 'a', 2: 'b'}, ['a, *args, **kwargs', '<b>']
    add_pok_pok = 'a, b', {1: 'a', 2: 'b'}, ['a, *args, **kwargs', 'b']
    add_pok_kwo = 'a, *, b', {1: 'a', 2: 'b'}, ['a, *args, **kwargs', '*, b']

    add_kwo_pos = '<b>, *, a', {1: 'a', 2: 'b'}, ['*args, a, **kwargs', '<b>']
    add_kwo_pok = 'b, *, a', {1: 'a', 2: 'b'}, ['*args, a, **kwargs', 'b']
    add_kwo_kwo = '*, a, b', {1: 'a', 2: 'b'}, ['*args, a, **kwargs', '*, b']

    conv_pok_pos = '<a>', {2: 'a'}, ['*args', 'a']
    conv_pok_kwo = '*, a', {2: 'a'}, ['**kwargs', 'a']

    three = (
        'a, b, c', {1: 'a', 2: 'b', 3: 'c'},
        ['a, *args, **kwargs', 'b, *args, **kwargs', 'c'])

    dont_use_varargs = (
        'a, *p, b', {1: 'ap', 2: 'b'}, ['a, *p, **k', 'b'], False)
    dont_use_varkwargs = (
        'a, b, /, **k', {1: 'ak', 2: 'b'}, ['a, *p, **k', 'b'], True, False)
    dont_use_either_empty = (
        'a, *p, **k', {1: 'apk'}, ['a, *p, **k', ''], False, False)



class EmbedRaisesTests(Fixtures):
    def _test(self, signatures, use_varargs=True, use_varkwargs=True):
        assert len(signatures) >= 2
        sigs = [s(sig) for sig in signatures]
        with self.assertRaises(IncompatibleSignatures):
            embed(*sigs, use_varargs=use_varargs, use_varkwargs=use_varkwargs)

    no_placeholders_pos = ['', '<a>'],
    no_placeholders_pok = ['', 'a'],
    no_placeholders_kwo = ['', '*, a'],

    no_args_pos = ['**kwargs', '<a>'],

    dup_pos_pos = ['<a>, *args, **kwargs', '<a>'],

    dont_use_either = ['a, *p, **k', 'b'], False, False
