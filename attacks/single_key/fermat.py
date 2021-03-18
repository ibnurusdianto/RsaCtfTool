#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from attacks.abstract_attack import AbstractAttack
import math
from lib.timeout import timeout
from lib.keys_wrapper import PrivateKey
from lib.exceptions import FactorizationError
from lib.utils import timeout, TimeoutError


class Attack(AbstractAttack):
    def __init__(self, attack_rsa_obj, timeout=60):
        super().__init__(attack_rsa_obj, timeout)
        self.speed = AbstractAttack.speed_enum["medium"]

    # Source - http://stackoverflow.com/a/20465181
    def isqrt(self, n):
        """Is n a square ?"""
        x = n
        y = (x + n // x) // 2
        while y < x:
            x = y
            y = (x + n // x) // 2
        return x

    def fermat(self, n):
        """Fermat attack"""
        a = self.isqrt(n)
        b2 = a * a - n
        b = self.isqrt(n)
        count = 0
        while b * b != b2:
            a = a + 1
            b2 = a * a - n
            b = self.isqrt(b2)
            count += 1
        p = a + b
        q = a - b
        assert n == p * q
        return p, q

    def attack(self, publickey, cipher=[]):
        """Run fermat attack with a timeout"""
        try:
            with timeout(seconds=attack_rsa_obj.args.timeout):
                try:
                    publickey.p, publickey.q = self.fermat(publickey.n)
                except TimeoutError:
                    return (None, None)

        except FactorizationError:
            return (None, None)

        if publickey.p is not None and publickey.q is not None:
            try:
                priv_key = PrivateKey(
                    int(publickey.p), int(publickey.q), int(publickey.e)
                )
                return (priv_key, None)
            except ValueError:
                return (None, None)

        return (None, None)


if __name__ == "__main__":
    attack = Attack()
    attack.test()